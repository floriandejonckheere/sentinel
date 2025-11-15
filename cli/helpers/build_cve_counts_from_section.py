from models.llm_models import CVECounts, CVESection, TrustTrend, SeverityLevel


def build_cve_counts_from_section(cve_section: CVESection) -> CVECounts:
    """Aggregate simple CVE severity counts from a CVESection.

    Previous version expected a list of dict trend entries; the current LLM output
    provides a CVESection with:
      - by_year_counts: Dict[str, int]
      - critical: List[CVEItem] (representative CVEs of mixed severities)

    We derive totals by summing by_year_counts (fallback to len(critical) if empty)
    and count severities from the CVEItem list.
    """

    # Total CVEs in window: prefer explicit yearly counts, else representative list length
    total = sum(cve_section.by_year_counts.values()) if cve_section.by_year_counts else len(cve_section.critical)

    critical = high = medium = low = 0
    for item in cve_section.critical:
        if item.severity is None:
            continue
        if item.severity == SeverityLevel.critical:
            critical += 1
        elif item.severity == SeverityLevel.high:
            high += 1
        elif item.severity == SeverityLevel.medium:
            medium += 1
        elif item.severity == SeverityLevel.low:
            low += 1

    # Map textual trend to enum
    mapping = {
        "improving": TrustTrend.improving,
        "degrading": TrustTrend.degrading,
        "worsening": TrustTrend.degrading,
        "stable": TrustTrend.stable,
    }
    trend = mapping.get(cve_section.trend.strip().lower(), TrustTrend.stable)

    return CVECounts(
        total=total,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        trend=trend,
    )
