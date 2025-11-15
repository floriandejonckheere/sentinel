# research_graph.py
from __future__ import annotations
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver  # optional
from ai import AI
from tools.web_tool import search_scrape_tool  # your BaseTool
from models.llm_models import (
    VendorIntel, CVESection, ComplianceSection, IncidentSection, DocFeatures, ResearchReport
)

# ---- Shared state ----
class State(TypedDict, total=False):
    query: str
    vendor: VendorIntel
    cve: CVESection
    compliance: ComplianceSection
    incidents: IncidentSection
    docs: DocFeatures
    report: ResearchReport

ai = AI(model="gemini-2.5-flash", temperature=0.2)

# ---- Agent node helpers ----
def _tools():  # keep tools centralized; easy to add more later
    return [search_scrape_tool]

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

def cve_node(state: State) -> State:
    prompt = (
        "You are a CVE & Vulnerability analyst. Research historical vulnerabilities related to the vendor/product. "
        "Use multiple searches if needed (site:nvd.nist.gov, site:mitre.org, vendor advisories, trusted blogs). "
        "Return CVESection with by_year_counts, 3–8 critical CVEItem entries, trend (improving/degrading/flat), "
        "a 3–5 sentence summary, and sources."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"],
        tools=_tools(),
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
    missing = [k for k in ("vendor","cve","compliance","incidents","docs") if k not in state]
    if missing:
        # You can choose to raise, or inject empty shells. Here we just no-op.
        # raise ValueError(f"Missing sections: {missing}")
        pass

    # Construct the report only if sections are present
    if all(k in state for k in ("vendor","cve","compliance","incidents","docs")):
        report = ResearchReport(
            vendor=state["vendor"],
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
    g.add_node("cve", cve_node)
    g.add_node("compliance", compliance_node)
    g.add_node("incidents", incidents_node)
    g.add_node("docs", docs_node)
    g.add_node("finalize", finalize_node)

    # Fan out from START to all agents (they run in parallel and merge state)
    g.add_edge(START, "vendor")
    g.add_edge(START, "cve")
    g.add_edge(START, "compliance")
    g.add_edge(START, "incidents")
    g.add_edge(START, "docs")

    # All agents converge to finalize
    g.add_edge("vendor", "finalize")
    g.add_edge("cve", "finalize")
    g.add_edge("compliance", "finalize")
    g.add_edge("incidents", "finalize")
    g.add_edge("docs", "finalize")
    g.add_edge("finalize", END)

    # Optional: enable checkpointing so you can resume/rerun nodes
    memory = MemorySaver()
    return g.compile(checkpointer=memory)

app = build_app()
