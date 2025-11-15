from __future__ import annotations
from typing import List, Optional, Tuple, Literal
import os
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
from readability import Document  # readability-lxml
from pydantic import BaseModel, Field
from langchain.tools import tool

# your AI helper
from ..ai import AI

# ---------------------------
# SerpAPI search helpers
# ---------------------------

SERP_EXCLUDE_DOMAINS = {
    "twitter.com", "x.com", "facebook.com", "linkedin.com",
    "youtube.com", "play.google.com", "apps.apple.com",
    "github.com", "medium.com", "reddit.com", "producthunt.com",
    "g2.com", "capterra.com", "getapp.com", "wikipedia.org",
}

ABOUT_HINTS = {"about", "about-us", "aboutus", "company", "team", "our-story"}

def _hostname(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).hostname or ""
    except Exception:
        return ""

def _looks_official(url: str, app_name: str) -> bool:
    host = _hostname(url).lower()
    name = re.sub(r"[^a-z0-9]", "", app_name.lower())
    host_flat = re.sub(r"[^a-z0-9]", "", host)
    return name and name in host_flat and not any(bad in host for bad in SERP_EXCLUDE_DOMAINS)

def _is_aboutish(url: str) -> bool:
    path = urllib.parse.urlparse(url).path.lower().strip("/")
    return any(hint in path for hint in ABOUT_HINTS)

def serpapi_find_about_pages(product: str, *, num: int = 10) -> List[str]:
    """
    Use SerpAPI (Google) to find 'About' pages for a given product/site.
    Prioritizes official domains and urls whose path suggests an About page.
    """
    from serpapi import GoogleSearch  # lazy import to keep optional

    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return []

    # A couple of queries to improve recall
    queries = [
        f"{product} about",
        f"{product} company about",
        f"{product} official site about",
        f"{product} team",
    ]

    candidates: List[Tuple[str, float]] = []  # (url, score)

    for q in queries:
        data = GoogleSearch({
            "engine": "google",
            "q": q,
            "num": num,
            "hl": "en",
            "api_key": api_key,
        }).get_dict()

        for item in (data.get("organic_results") or []):
            url = item.get("link") or ""
            if not url:
                continue
            host = _hostname(url).lower()
            if not host or any(ex in host for ex in SERP_EXCLUDE_DOMAINS):
                continue

            score = 0.0
            if _looks_official(url, product):
                score += 2.0
            if _is_aboutish(url):
                score += 2.0

            # small boost if title/snippet mention “about”
            title = (item.get("title") or "").lower()
            snippet = (item.get("snippet") or "").lower()
            if "about" in title:
                score += 1.0
            if "about" in snippet:
                score += 0.5

            # de-dup by url
            if not any(u == url for u, _ in candidates):
                candidates.append((url, score))

        # Also check knowledge graph/website when present
        kg = data.get("knowledge_graph") or {}
        official_site = kg.get("website")
        if official_site and official_site not in [u for u, _ in candidates]:
            # Seed the root home; we'll try /about on it later
            candidates.append((official_site, 1.0))

    # Expand root sites to /about style guesses
    expanded: List[Tuple[str, float]] = []
    for url, base_score in candidates:
        parsed = urllib.parse.urlparse(url)
        if parsed.path in ("", "/"):
            for guess in ("about", "about-us", "company", "team", "our-story"):
                expanded.append((
                    urllib.parse.urljoin(url if url.endswith("/") else url + "/", guess),
                    base_score + 1.0
                ))
    candidates.extend(expanded)

    # Sort by score desc, keep unique by (hostname, path)
    seen = set()
    ranked: List[str] = []
    for url, _score in sorted(candidates, key=lambda x: x[1], reverse=True):
        key = ( _hostname(url), urllib.parse.urlparse(url).path )
        if key in seen:
            continue
        seen.add(key)
        ranked.append(url)

    # Keep a reasonable top-k
    return ranked[:8]


# ---------------------------
# Content extraction
# ---------------------------

def fetch_text(url: str, *, timeout: int = 12) -> str:
    """
    Fetch URL and return readable text. 
    Prefers Readability; falls back to simple BeautifulSoup extraction.
    """
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
    except Exception:
        return ""

    html = r.text or ""
    if not html.strip():
        return ""

    try:
        # Readability tends to extract the main content area
        doc = Document(html)
        summary_html = doc.summary(html_partial=True)
        soup = BeautifulSoup(summary_html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "lxml")

    # Remove scripts/styles/nav/footer as best-effort
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Heuristic: drop obvious chrome if present
    for sel in ["nav", "footer", "header", ".navbar", ".site-footer", ".cookie", "#cookie", ".banner", ".subscribe"]:
        for t in soup.select(sel):
            t.decompose()

    text = " ".join(s.strip() for s in soup.get_text("\n").splitlines() if s.strip())
    # Trim excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def gather_about_corpus(product: str) -> Tuple[str, List[str]]:
    """
    Returns (combined_text, urls_used).
    """
    urls = serpapi_find_about_pages(product)
    texts: List[str] = []
    used: List[str] = []

    for url in urls:
        t = fetch_text(url)
        if t and len(t) > 200:  # ignore tiny/empty extractions
            texts.append(t)
            used.append(url)
        if len(texts) >= 3:  # cap to 3 pages to keep prompt sizes reasonable
            break

    combined = "\n\n---\n\n".join(texts)
    return combined, used


ALLOWED_CATEGORIES = [
    "Productivity", "Communication", "Developer Tools", "Design", "Marketing", "Finance",
    "Data & Analytics", "Security", "HR & People", "Education", "Healthcare", "Sales",
    "Customer Support", "Media", "Operations", "Legal", "Creative", "AI & ML",
]

class CategoryResponse(BaseModel):
    category: Literal[tuple(ALLOWED_CATEGORIES)]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str

class TaxonomyInput(BaseModel):
    application_name: str
    about: str = "about"

LLM_SYSTEM = (
    "You are an expert product taxonomist. "
    "Classify apps into exactly one category from a closed set."
)

@tool
def taxonomy_tool(input: TaxonomyInput) -> str:
    """
    Classify the application using:
    1) SerpAPI to discover About pages
    2) Fetch & extract text from those pages
    3) Feed the corpus to Gemini (via AI helper) for closed-set classification
    Returns only the category string (to maintain your original signature).
    """
    # 1–2) Build an 'about corpus' from live web pages
    about_corpus, urls_used = gather_about_corpus(input.application_name)

    # Fallback to provided 'about' if the web is empty (or append it for extra signal)
    if not about_corpus:
        about_corpus = (input.about or "").strip()
    else:
        extra = (input.about or "").strip()
        if extra and extra.lower() != "about":
            about_corpus = about_corpus + "\n\n---\n\n" + extra

    # 3) Ask Gemini for the classification
    ai = AI(model="gemini-2.5-pro", temperature=0.2)

    prompt = (
        "Choose exactly one category from this closed set:\n"
        f"{', '.join(ALLOWED_CATEGORIES)}\n\n"
        "Instructions:\n"
        "- Base your decision on the provided About-page corpus.\n"
        "- If unsure, pick the single best fit.\n"
        "- Return only the structured object.\n\n"
        f"Application: {input.application_name}\n"
        f"Sources (for your reference only):\n" +
        "\n".join(f"- {u}" for u in urls_used)
    )

    result: CategoryResponse = ai.generate(
        prompt=prompt,
        input_text=about_corpus,
        output_model=CategoryResponse,
        system=LLM_SYSTEM,
    )

    # Return just the category to match your tool's return type
    return result

response = taxonomy_tool.invoke(
    {"input": TaxonomyInput(application_name="1Password")}
)

print(f"Predicted category: {response}")