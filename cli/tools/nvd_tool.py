from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, List, Dict, Any
import requests

from langchain.tools import tool

NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000"


def get_120_day_range(end: Optional[datetime] = None) -> Tuple[str, str]:
    """
    Return (pubStartDate, pubEndDate) for a 120-day window in ISO-8601.

    - end: end of the window (UTC). If None, uses current UTC time.
    """
    if end is None:
        end = datetime.now(timezone.utc)

    start = end - timedelta(days=120)

    pub_start = start.strftime(DATE_FORMAT)
    pub_end = end.strftime(DATE_FORMAT)
    return pub_start, pub_end



def _extract_description(cve_obj: Dict[str, Any]) -> str:
    """
    Get a short English description if available, otherwise fallback.
    """
    descriptions = cve_obj.get("descriptions") or []
    # Prefer English description
    for d in descriptions:
        if d.get("lang") == "en" and d.get("value"):
            return d["value"]

    # Fallback to first non-empty description
    for d in descriptions:
        if d.get("value"):
            return d["value"]

    return ""


def _extract_severity(cve_obj: Dict[str, Any]) -> Optional[str]:
    """
    Extract severity as one of Critical/High/Medium/Low if possible.

    NVD 2.0 metrics usually look like:
    - metrics.cvssMetricV31[0].cvssData.baseSeverity
    - metrics.cvssMetricV30[0].cvssData.baseSeverity
    - metrics.cvssMetricV2[0].baseSeverity or .severity
    """
    metrics = cve_obj.get("metrics") or {}

    candidates = [
        "cvssMetricV31",
        "cvssMetricV30",
        "cvssMetricV2",
    ]

    for key in candidates:
        metric_list = metrics.get(key)
        if not metric_list:
            continue

        m0 = metric_list[0] or {}

        # v3.x
        cvss_data = m0.get("cvssData") or {}
        sev = (
            cvss_data.get("baseSeverity")
            or cvss_data.get("severity")
            or m0.get("baseSeverity")
            or m0.get("severity")
        )
        if not sev:
            continue

        sev_norm = sev.strip().upper()
        mapping = {
            "CRITICAL": "Critical",
            "HIGH": "High",
            "MEDIUM": "Medium",
            "LOW": "Low",
        }
        if sev_norm in mapping:
            return mapping[sev_norm]

    return None


def _extract_year(cve_obj: Dict[str, Any]) -> Optional[int]:
    """
    Use published date (preferred) or lastModified to derive year.
    """
    published = cve_obj.get("published")
    if not published:
        published = cve_obj.get("lastModified")

    if not published or len(published) < 4:
        return None

    try:
        return int(published[:4])
    except ValueError:
        return None


def _extract_sources(cve_obj: Dict[str, Any]) -> List[str]:
    """
    Collect URLs from references. NVD 2.0 typically has:
    - references: [ { "url": "...", ... }, ... ]
    but we also support older v1-style shapes.
    """
    urls: List[str] = []

    refs = cve_obj.get("references") or []
    if isinstance(refs, list):
        for r in refs:
            if isinstance(r, dict):
                url = r.get("url")
                if url:
                    urls.append(url)
    elif isinstance(refs, dict):
        # v1-style compatibility: { "reference_data": [ { "url": ... }, ... ] }
        ref_data = refs.get("reference_data") or []
        for r in ref_data:
            if isinstance(r, dict):
                url = r.get("url")
                if url:
                    urls.append(url)

    # Deduplicate preserving order
    seen = set()
    unique_urls = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)
    return unique_urls



@tool
def nvd_keyword_search_minimal_120d(
    keyword: str,
    results_per_page: int = 50,
    start_index: int = 0,
) -> Dict[str, Any]:
    """
    Search NVD CVE API by keyword over the last 120 days and return
    only the fields needed to build CVEItem / CVESection.

    Returns:
        {
          "cves": [
            {
              "cve_id": str,
              "severity": Optional[str],
              "description": str,
              "year": Optional[int],
              "sources": List[str]
            },
            ...
          ]
        }
    """
    pub_start, pub_end = get_120_day_range()

    params = {
        "keywordSearch": keyword,
        "pubStartDate": pub_start,
        "pubEndDate": pub_end,
        "resultsPerPage": results_per_page,
        "startIndex": start_index,
    }

    response = requests.get(NVD_BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    vulns = data.get("vulnerabilities") or []
    minimal_cves: List[Dict[str, Any]] = []

    for v in vulns:
        cve_obj = v.get("cve") or {}

        cve_id = cve_obj.get("id")
        if not cve_id:
            continue  

        description = _extract_description(cve_obj)
        severity = _extract_severity(cve_obj)
        year = _extract_year(cve_obj)
        sources = _extract_sources(cve_obj)

        minimal_cves.append(
            {
                "cve_id": cve_id,
                "severity": severity,        # "Critical" | "High" | "Medium" | "Low" | None
                "description": description,
                "year": year,
                "sources": sources,
            }
        )

    return {"cves": minimal_cves}
