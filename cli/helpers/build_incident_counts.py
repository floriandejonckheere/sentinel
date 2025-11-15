from typing import Optional

from models.llm_models import IncidentCounts, IncidentSection, SeverityLevel

def build_incident_counts(incidents: IncidentSection) -> IncidentCounts:
    total = len(incidents.items)
    critical = high = medium = low = 0

    for inc in incidents.items:
        sev = inc.severity
        if not sev:
            continue
        if sev == SeverityLevel.critical:
            critical += 1
        elif sev == SeverityLevel.high:
            high += 1
        elif sev == SeverityLevel.medium:
            medium += 1
        elif sev == SeverityLevel.low:
            low += 1

    return IncidentCounts(
        total=total,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        trend=incidents.trend,
    )
