from __future__ import annotations
from typing import List, Optional, Tuple
import os
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
from readability import Document  # provided by readability-lxml
from pydantic import BaseModel, Field
from langchain.tools import tool

# ---------- Pydantic input schema ----------
class SearchScrapeInput(BaseModel):
    query: str = Field(..., description="Search query to find relevant pages.")
    top_k: int = Field(3, ge=1, le=10, description="How many pages to scrape from search results.")
    min_chars: int = Field(200, ge=0, description="Ignore pages whose extracted text is shorter than this.")
    max_page_chars: int = Field(3000, ge=500, le=20000, description="Hard cap per page after cleaning; excess truncated.")
    max_total_chars: int = Field(8000, ge=1000, le=50000, description="Maximum total characters in combined_corpus.")
    include_domains: Optional[List[str]] = Field(
        default=None,
        description="If set, only accept pages whose hostname contains any of these substrings."
    )
    exclude_domains: Optional[List[str]] = Field(
        default=["twitter.com", "x.com", "facebook.com", "linkedin.com",
                 "youtube.com", "play.google.com", "apps.apple.com",
                 "github.com", "medium.com", "reddit.com", "producthunt.com",
                 "g2.com", "capterra.com", "getapp.com", "wikipedia.org"],
        description="Reject pages whose hostname contains any of these substrings."
    )

# ---------- Helpers ----------
def _hostname(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).hostname or ""
    except Exception:
        return ""

def serpapi_search(query: str, num: int = 10) -> List[dict]:
    """
    Returns a list of organic results with keys: link, title, snippet (when available).
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY not set in environment variables.")
    # Import here so the module is optional at import time
    from serpapi import GoogleSearch  # provided by 'google-search-results'
    data = GoogleSearch({
        "engine": "google",
        "q": query,
        "num": min(max(num, 1), 10),
        "hl": "en",
        "api_key": api_key,
    }).get_dict()
    return list(data.get("organic_results") or [])

def fetch_text(url: str, *, timeout: int = 12) -> Tuple[str, str]:
    """
    Fetch URL and return (title, readable_text).
    Uses Readability; falls back to raw BeautifulSoup extraction.
    """
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
    except Exception:
        return "", ""

    html = r.text or ""
    if not html.strip():
        return "", ""

    # Try Readability to get article-like main content
    title = ""
    try:
        doc = Document(html)
        title = (doc.short_title() or doc.title() or "").strip()
        summary_html = doc.summary(html_partial=True)
        soup = BeautifulSoup(summary_html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "lxml")

    # Remove junk
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    for sel in ["nav", "footer", "header", ".navbar", ".site-footer",
                ".cookie", "#cookie", ".banner", ".subscribe"]:
        for t in soup.select(sel):
            t.decompose()

    # Extract text cleanly
    raw = " ".join(s.strip() for s in soup.get_text("\n").splitlines() if s.strip())
    raw = re.sub(r"\s+", " ", raw).strip()
    # Remove common boilerplate phrases (heuristic)
    boilerplate_patterns = [
        r"cookie preferences", r"all rights reserved", r"privacy policy", r"terms of (use|service)",
        r"subscribe", r"sign up", r"newsletter", r"follow us", r"contact us"
    ]
    lowered = raw.lower()
    for pat in boilerplate_patterns:
        lowered = re.sub(pat, "", lowered)
    cleaned = re.sub(r"\s+", " ", lowered).strip()
    return title, cleaned

def _domain_allowed(url: str, include: Optional[List[str]], exclude: Optional[List[str]]) -> bool:
    host = _hostname(url).lower()
    if not host:
        return False
    if exclude:
        for bad in exclude:
            if bad.lower() in host:
                return False
    if include:
        return any(good.lower() in host for good in include)
    return True

# ---------- The tool ----------
@tool(args_schema=SearchScrapeInput)
def search_scrape_tool(
    query: str,
    top_k: int = 3,
    min_chars: int = 200,
    max_page_chars: int = 4000,
    max_total_chars: int = 10000,
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
) -> dict:
    """
    Search the web (SerpAPI) and scrape the top matching pages.
    Returns a dict with 'pages': [{url, title, content}], and 'combined_corpus'.
    """
    results = serpapi_search(query, num=max(top_k * 3, 10))  # overfetch, then filter
    pages = []
    seen_paths = set()

    for item in results:
        if len(pages) >= top_k:
            break

        url = item.get("link") or ""
        if not url:
            continue
        if not _domain_allowed(url, include_domains, exclude_domains):
            continue

        # de-dup (host + path)
        key = (_hostname(url), urllib.parse.urlparse(url).path)
        if key in seen_paths:
            continue
        seen_paths.add(key)

        title, text = fetch_text(url)
        if not text:
            continue
        if min_chars and len(text) < min_chars:
            continue
        # Truncate page content hard cap
        if len(text) > max_page_chars:
            text = text[:max_page_chars]
            last_period = text.rfind('.')
            if last_period > max_page_chars * 0.6:
                text = text[:last_period+1]

        # Prefer SERP title if Readability didn't produce one
        title = title or (item.get("title") or "")
        pages.append({"url": url, "title": title, "content": text})
    # Build combined corpus with total cap
    combined_parts = []
    total_chars = 0
    for p in pages:
        segment = p["content"]
        if total_chars + len(segment) > max_total_chars:
            remaining = max_total_chars - total_chars
            if remaining <= 0:
                break
            segment = segment[:remaining]
            last_period = segment.rfind('.')
            if last_period > remaining * 0.5:
                segment = segment[:last_period+1]
        combined_parts.append(segment)
        total_chars += len(segment)
        if total_chars >= max_total_chars:
            break
    combined = "\n\n---\n\n".join(combined_parts)
    return {"query": query, "pages": pages, "combined_corpus": combined}
