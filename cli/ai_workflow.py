# research_graph.py
from __future__ import annotations
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver  # optional
from ai import AI
from tools.web_tool import search_scrape_tool  # your BaseTool
from tools.nvd_tool import nvd_keyword_search_minimal_120d
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

ai = AI(model="gemini-2.5-flash", temperature=0.2)

# ---- Agent node helpers ----
def _tools(): 
    return [search_scrape_tool]

def _cve_tools():
    return [nvd_keyword_search_minimal_120d]

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
        "You have access to the `search_nvd_cves` tool which queries the official "
        "NVD CVE 2.0 API using a keyword. It returns JSON shaped as:\n"
        "  { \"cves\": [\n"
        "      {\n"
        "        \"cve_id\": str,\n"
        "        \"severity\": Optional[str],     # One of: Critical, High, Medium, Low, or null\n"
        "        \"description\": str,            # Short English description\n"
        "        \"year\": Optional[int],         # Year published\n"
        "        \"sources\": List[str]           # URLs (NVD detail + advisories if available)\n"
        "      },\n"
        "      ...\n"
        "  ] }\n\n"
        "Your job is to take the user query, fetch relevant CVEs with the tool, "
        "and return a structured CVESection.\n\n"
        "Instructions:\n"
        "1. From the user query, infer an appropriate keyword (vendor, product, or technology).\n"
        "2. Call `search_nvd_cves` ONCE using that keyword. The tool already handles the 120-day date range.\n"
        "3. Use the returned list of CVEs to build `by_year_counts`:\n"
        "   - Group CVEs by their `year` field (ignore entries without a year).\n"
        "   - Keys in by_year_counts must be strings like \"2023\", \"2024\".\n"
        "4. Select 3–8 **representative or notable** CVEs (not just severity=Critical):\n"
        "   - If there are fewer than 3 CVEs total, include all of them.\n"
        "   - Otherwise, choose those with highest severity first "
        "     (Critical > High > Medium > Low > null), and prefer recent years.\n"
        "5. For each selected CVE, build a CVEItem and put it into CVESection.critical:\n"
        "   - cve_id from c.cve_id.\n"
        "   - severity from c.severity (map to Critical/High/Medium/Low if not null; otherwise leave as null).\n"
        "   - description from c.description.\n"
        "   - year from c.year.\n"
        "   - sources from c.sources. If the NVD detail URL is missing, add:\n"
        "       https://nvd.nist.gov/vuln/detail/{cve_id}\n"
        "   - The CVESection.critical list must contain these 3–8 CVEItem objects.\n"
        "6. Determine trend (Improving, Degrading, or Stable):\n"
        "   - Look at by_year_counts over time. More recent years having fewer CVEs suggests 'Improving';\n"
        "     more suggests 'Degrading'; roughly flat suggests 'Stable'.\n"
        "7. Set CVESection.sources as a deduplicated list of all URLs from all CVEItem.sources.\n"
        "8. Write a concise 3–5 sentence summary for CVESection.summary describing:\n"
        "   - Overall vulnerability exposure for the vendor/product.\n"
        "   - Any notable spikes, drops, or patterns by year.\n"
        "   - The impact and nature of the most serious vulnerabilities.\n"
        "9. If **no CVEs** are returned from the tool:\n"
        "   - Use an empty by_year_counts and critical list.\n"
        "   - Set trend to 'Stable'.\n"
        "   - Write a summary explaining that no recent CVEs were found in the last 120 days.\n"
        "   - Set sources to an empty list.\n"
        "10. IMPORTANT: If at least one CVE is returned, CVESection.critical MUST NOT be empty. "
        "    Always include the selected 3–8 representative CVEs.\n\n"
        "Always return a valid CVESection Pydantic object."
    )

    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"],
        tools=_cve_tools(),   
        output_model=CVESection,
        max_steps=4,          
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
