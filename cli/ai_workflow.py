from __future__ import annotations
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from ai import AI
from tools.web_tool import search_scrape_tool
from tools.nvd_tool import nvd_keyword_search_minimal_120d

from models.llm_models import (
    ALLOWED_SUBCATEGORIES,
    ALLOWED_CATEGORIES,
    AssessmentSummary,
    VendorIntel,
    CVESection,
    ComplianceSection,
    IncidentSection,
    DocFeatures,
    ResearchReport,
    AppCategoryResult,
    FullAssesment,
    Alternatives,
    ArchitectureSummary,
    CVECounts,
    IncidentCounts,
    AssessmentMetadata,
)

from helpers.build_metadata import build_metadata
from helpers.build_cve_counts_from_section import build_cve_counts_from_section
from helpers.build_incident_counts import build_incident_counts

# ---- Shared state ----
class State(TypedDict, total=False):
    query: str
    vendor: VendorIntel
    cve: CVESection
    compliance: ComplianceSection
    incidents: IncidentSection
    docs: DocFeatures
    category: AppCategoryResult
    alternatives: Alternatives
    summary: AssessmentSummary
    architecture: ArchitectureSummary
    report: ResearchReport
    full_assessment: FullAssesment
    

ai = AI(model="gemini-2.5-flash-lite", temperature=0.2)


# ---- Agent node helpers ----
def _tools():
    return [search_scrape_tool]


def _cve_tools():
    return [nvd_keyword_search_minimal_120d]


def vendor_node(state: State) -> State:
    prompt = (
        "Act as a Vendor Intelligence agent. Use web search to gather official background.\n"
        "Return a structured VendorIntel with: name, legal_name, country, size, notable_customers (up to 8), "
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
        "- First choose a high-level *category* from this list:\n"
        f"{', '.join(ALLOWED_CATEGORIES)}\n\n"
        "- Then choose a more specific *subcategory* from this list:\n"
        f"{', '.join(ALLOWED_SUBCATEGORIES)}\n\n"
        "Return an AppCategoryResult with category, subcategory, confidence, reasoning."
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
        "Focus on major frameworks like SOC2, ISO27001, GDPR, HIPAA, FedRAMP, etc."
        "GDPR status should always be included."
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

def alternatives_node(state: State) -> State:
    prompt = (
        "You are an alternatives & comparison analyst.\n"
        "Given a vendor/product from the user query, find 2–5 comparable tools in the same category.\n"
        "Return an Alternatives object with items having: name, url, and an optional trust_score (0–100) "
        "representing rough relative security/compliance strength compared to the original tool.\n"
        "Prefer well-known vendors and SaaS tools where applicable."
    )
    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=state["query"],
        tools=_tools(),
        output_model=Alternatives,
        max_steps=6,
    )
    return {"alternatives": result}

def architecture_node(state: State) -> State:
    """
    Use the structured outputs from vendor/docs/cve/compliance/incidents
    to infer a concise ArchitectureSummary via the LLM.
    """

    vendor = state.get("vendor")
    docs = state.get("docs")
    cve = state.get("cve")
    compliance = state.get("compliance")
    incidents = state.get("incidents")
    category = state.get("category")

    # Build a textual context the model can read
    context_parts = [f"User query: {state.get('query', '')}"]

    if vendor is not None:
        context_parts.append("Vendor intel (JSON):\n" + vendor.model_dump_json(indent=2))
    if category is not None:
        context_parts.append("App category (JSON):\n" + category.model_dump_json(indent=2))
    if docs is not None:
        context_parts.append("Documentation features (JSON):\n" + docs.model_dump_json(indent=2))
    if cve is not None:
        context_parts.append("CVE section (JSON):\n" + cve.model_dump_json(indent=2))
    if compliance is not None:
        context_parts.append("Compliance section (JSON):\n" + compliance.model_dump_json(indent=2))
    if incidents is not None:
        context_parts.append("Incident section (JSON):\n" + incidents.model_dump_json(indent=2))

    context = "\n\n".join(context_parts)

    prompt = (
        "You are a security architecture summarization agent.\n\n"
        "You will be given structured JSON about a vendor/product:\n"
        "- VendorIntel (vendor background)\n"
        "- AppCategoryResult (product category)\n"
        "- DocFeatures (security-related documentation extracts)\n"
        "- CVESection (vulnerability history)\n"
        "- ComplianceSection (certifications and frameworks)\n"
        "- IncidentSection (past incidents)\n\n"
        "From this context, infer a concise ArchitectureSummary with the following fields:\n"
        "- encryption: main encryption scheme(s) in use (e.g., 'AES-256-GCM, TLS 1.2+')\n"
        "- key_derivation: key derivation / password hashing (e.g., 'PBKDF2-HMAC-SHA256, Argon2')\n"
        "- zero_knowledge: true if the design clearly follows a zero-knowledge model; false if clearly not; null if unclear.\n"
        "- open_source: true if core components are clearly open source; false if clearly closed; null if unclear.\n"
        "- authentication: short phrase summarizing auth methods (e.g., 'MFA, SSO (SAML/OIDC), biometric').\n"
        "- deployment: short phrase for main deployment models (e.g., 'SaaS only', 'SaaS + self-hosted', 'On-prem').\n\n"
        "Important rules:\n"
        "- ONLY fill fields when there is evidence or very strong hints in the provided JSON.\n"
        "- If a field is not supported by the context, leave it as null.\n"
        "- Do not invent cryptographic details or deployment options that are not clearly implied.\n\n"
        "Return a valid ArchitectureSummary Pydantic object."
    )

    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=context,
        tools=[],  # no extra web search; use only the provided JSON context
        output_model=ArchitectureSummary,
        max_steps=1,
    )
    return {"architecture": result}

def summary_node(state: State) -> State:
    """
    Use all previously collected sections to generate qualitative strengths/risks.
    trust_score stays None here and is filled later by the trust-score engine.
    """

    parts = [f"User query: {state.get('query', '')}"]

    vendor = state.get("vendor")
    if vendor is not None:
        parts.append("VendorIntel:\n" + vendor.model_dump_json(indent=2))

    category = state.get("category")
    if category is not None:
        parts.append("AppCategoryResult:\n" + category.model_dump_json(indent=2))

    docs = state.get("docs")
    if docs is not None:
        parts.append("DocFeatures:\n" + docs.model_dump_json(indent=2))

    cve = state.get("cve")
    if cve is not None:
        parts.append("CVESection:\n" + cve.model_dump_json(indent=2))

    compliance = state.get("compliance")
    if compliance is not None:
        parts.append("ComplianceSection:\n" + compliance.model_dump_json(indent=2))

    incidents = state.get("incidents")
    if incidents is not None:
        parts.append("IncidentSection:\n" + incidents.model_dump_json(indent=2))
    
    incident = state.get("incident")
    if incident is not None:
        parts.append("IncidentSection:\n" + incident.model_dump_json(indent=2))

    architecture = state.get("architecture")
    if architecture is not None:
        parts.append("ArchitectureSummary:\n" + architecture.model_dump_json(indent=2))

    alternatives = state.get("alternatives")
    if alternatives is not None:
        parts.append("Alternatives:\n" + alternatives.model_dump_json(indent=2))

    context = "\n\n".join(parts)

    prompt = (
        "You are a security posture summarization agent.\n\n"
        "You are given structured JSON describing a vendor/product:\n"
        "- VendorIntel (background)\n"
        "- AppCategoryResult (what kind of product it is)\n"
        "- DocFeatures (security features from docs)\n"
        "- CVESection (vulnerability history)\n"
        "- ComplianceSection (certifications & frameworks)\n"
        "- IncidentSection (past incidents)\n"
        "- ArchitectureSummary (high-level architecture)\n"
        "- Alternatives (peer tools)\n\n"
        "Your task is to produce an AssessmentSummary with:\n"
        "- key_strengths: 3–7 short bullet points highlighting the strongest security, "
        "  privacy, or compliance attributes.\n"
        "- key_risks: 3–7 short bullet points capturing the most important risks, gaps, "
        "  uncertainties, or tradeoffs.\n\n"
        "Rules:\n"
        "- Base your bullets ONLY on the information in the provided JSON; do not invent facts.\n"
        "- Focus on what matters for an enterprise security review: architecture robustness, "
        "  encryption, auth & access controls, incident history, CVE posture, and compliance.\n"
        "- Do NOT fill in the numeric trust_score field; it will be computed by a separate "
        "  scoring engine later. Leave trust_score as null / None.\n\n"
        "Return a valid AssessmentSummary Pydantic object."
    )

    result = ai.generate_structured_with_tools(
        prompt=prompt,
        input_text=context,
        tools=[],  # no extra web tools; use only the provided context
        output_model=AssessmentSummary,
        max_steps=1,
    )
    return {"summary": result}

def finalize_node(state: State) -> State:
    required = (
        "vendor",
        "cve",
        "compliance",
        "incidents",
        "docs",
        "category",
        "alternatives",
        "architecture",
        "summary",        # <-- now required
    )
    missing = [k for k in required if k not in state]
    if missing:
        print(f"[finalize_node] Missing sections: {missing}")
        return {}

    vendor = state["vendor"]
    cve = state["cve"]
    compliance = state["compliance"]
    incidents = state["incidents"]
    docs = state["docs"]
    category = state["category"]
    alternatives = state["alternatives"]
    architecture = state["architecture"]
    summary = state["summary"]

    # 1) ResearchReport for trust-score engine
    report = ResearchReport(
        vendor=vendor,
        category=category,
        cve=cve,
        compliance=compliance,
        incidents=incidents,
        docs=docs,
    )

    # 2) FullAssesment skeleton (summary has strengths/risks, but trust_score None)
    metadata = build_metadata()
    cve_counts: CVECounts = build_cve_counts_from_section(cve)
    incident_counts: IncidentCounts = build_incident_counts(incidents)

    full = FullAssesment(
        id=None,
        metadata=metadata,
        vendor=vendor,
        cve=cve,
        cves=cve_counts,
        incidents=incident_counts,
        incident=incidents,
        architecture=architecture,
        compliance=compliance,
        application=category,
        alternatives=alternatives,
        summary=summary,
    )

    return {"report": report, "full_assessment": full}

def build_app():
    g = StateGraph(State)

    g.add_node("vendor", vendor_node)
    g.add_node("category", category_node)
    g.add_node("cve", cve_node)
    g.add_node("compliance", compliance_node)
    g.add_node("incidents", incidents_node)
    g.add_node("docs", docs_node)
    g.add_node("alternatives", alternatives_node)
    g.add_node("architecture", architecture_node)
    g.add_node("summary", summary_node)          # <--- new
    g.add_node("finalize", finalize_node)

    # First wave
    g.add_edge(START, "vendor")
    g.add_edge(START, "category")
    g.add_edge(START, "cve")
    g.add_edge(START, "compliance")
    g.add_edge(START, "incidents")
    g.add_edge(START, "docs")
    g.add_edge(START, "alternatives")

    # Architecture after core signals
    g.add_edge("vendor", "architecture")
    g.add_edge("category", "architecture")
    g.add_edge("cve", "architecture")
    g.add_edge("compliance", "architecture")
    g.add_edge("incidents", "architecture")
    g.add_edge("docs", "architecture")

    # Summary after architecture (and thus after everything else)
    g.add_edge("architecture", "summary")

    # Finalize after summary
    g.add_edge("summary", "finalize")
    g.add_edge("finalize", END)

    memory = MemorySaver()
    return g.compile(checkpointer=memory)

app = build_app()
