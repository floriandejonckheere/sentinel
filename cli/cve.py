"""NVD CVE search and models (Pydantic v2 compatible)."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, field_validator
import requests
import time


# =========================
# Models
# =========================
class CvssV2Data(BaseModel):
    version: str
    vectorString: str
    baseScore: float
    accessVector: Optional[str] = None
    accessComplexity: Optional[str] = None
    authentication: Optional[str] = None
    confidentialityImpact: Optional[str] = None
    integrityImpact: Optional[str] = None
    availabilityImpact: Optional[str] = None


class CvssV2Metric(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    cvssData: CvssV2Data
    baseSeverity: Optional[str] = None
    exploitabilityScore: Optional[float] = None
    impactScore: Optional[float] = None
    acInsufInfo: Optional[bool] = None
    obtainAllPrivilege: Optional[bool] = None
    obtainUserPrivilege: Optional[bool] = None
    obtainOtherPrivilege: Optional[bool] = None
    userInteractionRequired: Optional[bool] = None


class CvssV3Data(BaseModel):
    version: str
    vectorString: str
    baseScore: float
    baseSeverity: str
    attackVector: Optional[str] = None
    attackComplexity: Optional[str] = None
    privilegesRequired: Optional[str] = None
    userInteraction: Optional[str] = None
    scope: Optional[str] = None
    confidentialityImpact: Optional[str] = None
    integrityImpact: Optional[str] = None
    availabilityImpact: Optional[str] = None


class CvssV3Metric(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    cvssData: CvssV3Data
    exploitabilityScore: Optional[float] = None
    impactScore: Optional[float] = None


class Metrics(BaseModel):
    cvssMetricV2: Optional[List[CvssV2Metric]] = None
    cvssMetricV30: Optional[List[CvssV3Metric]] = None
    cvssMetricV31: Optional[List[CvssV3Metric]] = None


class LangString(BaseModel):
    lang: str
    value: str


class WeaknessDesc(BaseModel):
    lang: str
    value: str


class Weakness(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    description: List[WeaknessDesc]


class CpeMatch(BaseModel):
    vulnerable: Optional[bool] = None
    criteria: str
    matchCriteriaId: Optional[str] = None


class ConfigNode(BaseModel):
    operator: Optional[str] = None  # "OR"/"AND"
    negate: Optional[bool] = None
    cpeMatch: Optional[List[CpeMatch]] = None
    nodes: Optional[List["ConfigNode"]] = None


ConfigNode.model_rebuild()


class Configuration(BaseModel):
    nodes: List[ConfigNode]


class Reference(BaseModel):
    url: str
    source: Optional[str] = None
    tags: Optional[List[str]] = None


class Cve(BaseModel):
    id: str
    sourceIdentifier: Optional[str] = None
    published: Optional[str] = None
    lastModified: Optional[str] = None
    vulnStatus: Optional[str] = None
    cveTags: Optional[List[str]] = None  # normalized list of tag strings
    descriptions: List[LangString]
    metrics: Optional[Metrics] = None
    weaknesses: Optional[List[Weakness]] = None
    configurations: Optional[List[Configuration]] = None
    references: Optional[List[Reference]] = None

    model_config = ConfigDict(extra="ignore")

    @field_validator("cveTags", mode="before")
    def _normalize_cve_tags(cls, v):  # type: ignore[override]
        if v is None:
            return v
        out: List[str] = []
        for item in v:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):  # shape: {"sourceIdentifier":..., "tags":[...]}
                tags = item.get("tags")
                if isinstance(tags, list):
                    for t in tags:
                        if isinstance(t, str):
                            out.append(t)
        return out or None

    def english_description(self) -> Optional[str]:
        return next((d.value for d in self.descriptions if d.lang.lower() == "en"), None)

    def best_cvss(self) -> Optional[dict]:
        if not self.metrics:
            return None

        def pick_v3(lst: Optional[List[CvssV3Metric]]):
            if lst:
                m = lst[0].cvssData
                return {
                    "version": m.version,
                    "score": m.baseScore,
                    "severity": m.baseSeverity,
                    "vector": m.vectorString,
                }
            return None

        for candidate in (self.metrics.cvssMetricV31, self.metrics.cvssMetricV30):
            b = pick_v3(candidate)
            if b:
                return b
        if self.metrics.cvssMetricV2:
            m = self.metrics.cvssMetricV2[0].cvssData
            sev = getattr(self.metrics.cvssMetricV2[0], "baseSeverity", None)
            return {
                "version": m.version,
                "score": m.baseScore,
                "severity": sev,
                "vector": m.vectorString,
            }
        return None

    def affected_cpes(self) -> List[str]:
        out: List[str] = []

        def walk(node: ConfigNode):
            if node.cpeMatch:
                for cm in node.cpeMatch:
                    if cm.vulnerable:
                        out.append(cm.criteria)
            if node.nodes:
                for ch in node.nodes:
                    walk(ch)

        if self.configurations:
            for cfg in self.configurations:
                for n in cfg.nodes:
                    walk(n)
        return out


class Vulnerability(BaseModel):
    cve: Cve


class NvdResponse(BaseModel):
    resultsPerPage: int
    startIndex: int
    totalResults: int
    format: str
    version: str
    timestamp: str
    vulnerabilities: List[Vulnerability]

    model_config = ConfigDict(extra="ignore")


BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def _request(url: str, params: Dict[str, Any], api_key: Optional[str], session: Optional[requests.Session], attempt: int) -> dict:
    headers = {}
    if api_key:
        headers["apiKey"] = api_key
    s = session or requests
    resp = s.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code == 429:
        sleep = min(2 ** attempt, 16)
        time.sleep(sleep)
        return _request(url, params, api_key, session, attempt + 1)
    resp.raise_for_status()
    return resp.json()


def search_cves_keyword(
    keyword: str,
    *,
    results_per_page: int = 200,
    max_pages: int = 1,
    pub_start: Optional[str] = None,
    pub_end: Optional[str] = None,
    cvss_v3_severity: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[Cve]:
    """Search CVEs by keyword. Handles pagination and basic retry/backoff."""
    start_index = 0
    all_cves: List[Cve] = []

    params_base: Dict[str, Any] = {
        "keywordSearch": keyword,
        "resultsPerPage": min(max(results_per_page, 1), 2000),
    }
    if pub_start:
        params_base["pubStartDate"] = pub_start
    if pub_end:
        params_base["pubEndDate"] = pub_end
    if cvss_v3_severity:
        params_base["cvssV3Severity"] = cvss_v3_severity

    with requests.Session() as session:
        for _ in range(max_pages):
            params = dict(params_base)
            params["startIndex"] = start_index
            data = _request(BASE, params, api_key, session, attempt=0)
            parsed = NvdResponse(**data)
            page_cves = [v.cve for v in parsed.vulnerabilities]
            all_cves.extend(page_cves)
            start_index += parsed.resultsPerPage
            if start_index >= parsed.totalResults or parsed.resultsPerPage == 0:
                break
            time.sleep(0.5)

    return all_cves

