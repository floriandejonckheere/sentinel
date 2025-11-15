# tools/nvd_cve_tool.py
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from cli.cve import search_cves_keyword, Cve


class NvdCveSearchArgs(BaseModel):
    """
    Arguments for the NVD CVE search tool.
    """

    keyword: str = Field(
        ...,
        description=(
            "Keyword to search for in NVD CVE records. Typically this is the "
            "vendor or product name (e.g. 'Okta', 'Microsoft Exchange')."
        ),
    )
    results_per_page: int = Field(
        20,
        ge=1,
        le=100,
        description=(
            "Number of CVEs to fetch per request. The tool will handle pagination "
            "up to 'max_pages'."
        ),
    )
    
    max_results: int = Field(
        20,
        ge=1,
        le=100,
        description=(
            "Maximum number of CVEs to return. "
            "The tool will fetch pages until this limit is reached."
        ),
    )
    
    max_pages: int = Field(
        1,
        ge=1,
        description=(
            "Maximum number of pages to fetch from the NVD API. Each page "
            "contains up to 'results_per_page' CVEs."
        ),
    )
    pub_start: Optional[str] = Field(
        None,
        description=(
            "Optional publication start date in ISO 8601 format "
            "(e.g. '2020-01-01T00:00:00.000'). If provided, only CVEs published "
            "on or after this date are returned."
        ),
    )
    pub_end: Optional[str] = Field(
        None,
        description=(
            "Optional publication end date in ISO 8601 format. If provided, only "
            "CVEs published on or before this date are returned."
        ),
    )
    cvss_v3_severity: Optional[str] = Field(
        None,
        description=(
            "Optional filter for CVSS v3 severity (e.g. 'CRITICAL', 'HIGH', "
            "'MEDIUM', 'LOW'). If set, only CVEs with matching severity are returned."
        ),
    )


def _search_nvd_cves(args: NvdCveSearchArgs) -> List[Dict[str, Any]]:
    """
    Internal function used by the LangChain tool.

    Returns a JSON-serializable list of CVEs with some helpful derived fields
    (english_description, best_cvss, affected_cpes) to make it easier for the LLM
    to summarize. The result list is capped at `max_results`.
    """
    # api_key = os.getenv("NVD_API_KEY")

    # Make sure we don't request more per page than the overall max we care about
    results_per_page = min(args.results_per_page, args.max_results)

    cves: List[Cve] = search_cves_keyword(
        keyword=args.keyword,
        results_per_page=results_per_page,
        max_pages=args.max_pages,
        pub_start=args.pub_start,
        pub_end=args.pub_end,
        cvss_v3_severity=args.cvss_v3_severity,
        # api_key=api_key,
    )

    # Hard cap the total CVEs handed to the LLM
    cves = cves[: args.max_results]

    out: List[Dict[str, Any]] = []
    for c in cves:
        data = c.model_dump()  # full raw CVE data
        # Convenience fields for the LLM:
        data["english_description"] = c.english_description()
        data["best_cvss"] = c.best_cvss()
        data["affected_cpes"] = c.affected_cpes()
        out.append(data)

    return out



search_nvd_cves_tool = StructuredTool.from_function(
    name="search_nvd_cves",
    description=(
        "Searches the NVD (National Vulnerability Database) CVE 2.0 API for "
        "vulnerabilities matching a given keyword (usually a vendor or product). "
        "Returns a list of CVE records as JSON objects, including convenience "
        "fields for english_description, best_cvss, and affected_cpes."
    ),
    args_schema=NvdCveSearchArgs,
    func=_search_nvd_cves,
)
