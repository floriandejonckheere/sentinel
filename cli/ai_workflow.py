# research_graph.py
from __future__ import annotations
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver  # optional
from ai import AI
from tools.web_tool import search_scrape_tool  # your BaseTool
from tools.nvd_tool import search_nvd_cves_tool
from models.llm_models import (
    ALLOWED_SUBCATEGORIES,ALLOWED_CATEGORIES, VendorIntel, CVESection, ComplianceSection, IncidentSection, DocFeatures, ResearchReport,AppCategoryResult
)

# ---- Shared state ----
class State(TypedDict, total=False):
    query: str
    vendor: VendorIntel
    cve: CVESection
    compliance: ComplianceSection
    incidents: IncidentSection
    docs: DocFeatures
    category: AppCategoryResult
    report: ResearchReport

ai = AI(model="gemini-2.5-flash-lite", temperature=0.2)

# ---- Agent node helpers ----
def _tools():  # keep tools centralized; easy to add more later
    return [search_scrape_tool]

def _cve_tools():
    return [search_nvd_cves_tool]

def vendor_node(state: State) -> State:
    prompt = (
        "Act as a Vendor Intelligence agent. Use web search to gather official background.\n"
        "Return a structured VendorIntel with: name, country, size, notable_customers (up to 8), "
        "security_team (if any), and sources (URLs you used). Prefer official pages."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"],
        tools=_tools(),
        output_model=VendorIntel,
        max_steps=6,
    )
    return {"vendor": result}

def category_node(state: State) -> State:
    prompt = (
        "You are a product categorization agent.\n\n"
        "Task:\n"
        "- Read the user's research query about a vendor or product.\n"
        "- First choose a high-level *category* from this list of column headers:\n"
        f"{', '.join(ALLOWED_CATEGORIES)}\n\n"
        "- Then choose a more specific *subcategory* from this list of allowed subcategories:\n"
        f"{', '.join(ALLOWED_SUBCATEGORIES)}\n\n"
        "  * category: the single best top-level category.\n"
        "  * subcategory: a specific type from the allowed subcategories.\n"
        "  * confidence: float between 0.0 and 1.0 reflecting your certainty.\n"
        "  * reasoning: short explanation justifying both choices."
    )

    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"],
        tools=_tools(),
        output_model=AppCategoryResult,
        max_steps=2,
    )
    return {"category": result}



def cve_node(state: State) -> State:
    prompt = (
        "You are a CVE & Vulnerability analyst.\n\n"
        "Use the `search_nvd_cves` tool to query the official NVD CVE 2.0 API. "
        "The tool returns a list of CVEs as JSON objects containing fields like "
        "`id`, `published`, `english_description`, `best_cvss`, and `affected_cpes`.\n\n"
        "Your job is to transform the raw CVE list into a structured CVESection.\n\n"
        "Steps:\n"
        "1. Call search_nvd_cves with the vendor or product from the query.\n"
        "2. Group all CVEs by publication year to populate by_year_counts.\n"
        "3. Select 3–8 representative or critical CVEs (use highest severity or broad impact).\n"
        "4. For each, build a CVEItem:\n"
        "   - cve_id from c.id\n"
        "   - severity from c.best_cvss['severity'] if available\n"
        "   - description from c.english_description\n"
        "   - year extracted from c.published\n"
        "   - sources: include NVD detail link (https://nvd.nist.gov/vuln/detail/[cve_id])\n"
        "5. Determine trend: Improving, Degrading, or Stable based on changes over years.\n"
        "6. Write a concise 3–5 sentence summary.\n\n"
        "Return a CVESection Pydantic object."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"],
        tools=_cve_tools(),
        output_model=CVESection,
        max_steps=8,
    )
    return {"cve": result}

def compliance_node(state: State) -> State:
    prompt = (
        "You are a Compliance & Certification analyst. Find third-party validations and claims. "
        "Return a list of structured ComplianceCert objects—one per certification found—"
        "and an overall_summary across frameworks."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"] + " trust center security compliance certifications",
        tools=_tools(),
        output_model=ComplianceSection,
        max_steps=8,
    )
    return {"compliance": result}

def incidents_node(state: State) -> State:
    prompt = (
        "You are an Incident & Breach analyst. Search news/blogs for confirmed security incidents, controversies, or public advisories. "
        "Return IncidentSection with 3–10 items, each with title, date (if available), severity (Low/Med/High if inferred), "
        "a 1–2 sentence description, and sources. If none found, include summary explaining search coverage."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"] + " breach incident security news",
        tools=_tools(),
        output_model=IncidentSection,
        max_steps=8,
    )
    return {"incidents": result}

def docs_node(state: State) -> State:
    prompt = (
        "You are a Documentation Scraper for security features. Use web search to find docs/FAQs/whitepapers. "
        "Extract lists for: encryption (at rest/in transit, key mgmt), authentication (SSO, MFA, SCIM), "
        "data handling (data residency, retention, backups), admin controls (RBAC, audit logs), "
        "deployment model (SaaS/self-hosted/regions). Provide a concise summary and sources."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"] + " security documentation site:docs.* OR site:support.*",
        tools=_tools(),
        output_model=DocFeatures,
        max_steps=8,
    )
    return {"docs": result}

def finalize_node(state: State) -> State:
    # Ensure all sections exist; you could add retries/defaults if any are missing
    missing = [k for k in ("vendor","cve","compliance","incidents","docs","category") if k not in state]
    if missing:
        # You can choose to raise, or inject empty shells. Here we just no-op.
        # raise ValueError(f"Missing sections: {missing}")
        pass

    # Construct the report only if sections are present
    if all(k in state for k in ("vendor","cve","compliance","incidents","docs","category")):
        report = ResearchReport(
            vendor=state["vendor"],
            category=state["category"],
            cve=state["cve"],
            compliance=state["compliance"],
            incidents=state["incidents"],
            docs=state["docs"],
        )
        return {"report": report}

    return {}

def build_app():
    g = StateGraph(State)

    g.add_node("vendor", vendor_node)
    g.add_node("category", category_node)
    g.add_node("cve", cve_node)
    g.add_node("compliance", compliance_node)
    g.add_node("incidents", incidents_node)
    g.add_node("docs", docs_node)
    g.add_node("finalize", finalize_node)

    # Fan out from START to all agents (they run in parallel and merge state)
    g.add_edge(START, "vendor")
    g.add_edge(START, "category")
    g.add_edge(START, "cve")
    g.add_edge(START, "compliance")
    g.add_edge(START, "incidents")
    g.add_edge(START, "docs")

    # All agents converge to finalize
    g.add_edge("vendor", "finalize")
    g.add_edge("category", "finalize")
    g.add_edge("cve", "finalize")
    g.add_edge("compliance", "finalize")
    g.add_edge("incidents", "finalize")
    g.add_edge("docs", "finalize")
    g.add_edge("finalize", END)

    # Optional: enable checkpointing so you can resume/rerun nodes
    memory = MemorySaver()
    return g.compile(checkpointer=memory)

app = build_app()
