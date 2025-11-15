"""TrustScoreEngine
---------------------
Converts raw LLM JSON output into a structured `TrustScoreBreakdown` Pydantic model.
"""

from typing import Dict, Any
from cli.models.llm_models import TrustScoreBreakdown, TrustConfidence, TrustTrend


class TrustScoreEngine:
    """Compute category scores and aggregate trust score into `TrustScoreBreakdown`."""

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "architecture": 0.125,
        "data_protection": 0.125,
        "identity_access": 0.125,
        "devsecops": 0.125,
        "historical_security": 0.125,
        "compliance": 0.125,
        "platform_security": 0.125,
        "risks_exposure": 0.125,
    }

    def __init__(self, weights: Dict[str, float] | None = None) -> None:
        self.weights = weights or self.DEFAULT_WEIGHTS

    def evaluate_llm_output(self, llm_output: Dict[str, Any]) -> TrustScoreBreakdown:
        """Return a populated `TrustScoreBreakdown` model from LLM output JSON."""
        category_scores = self._extract_category_scores(llm_output)
        trust_score, confidence = self._compute_trust(category_scores)
        trend = self._derive_trend(llm_output)
        # Cast floats to int for the model fields expecting int
        breakdown = TrustScoreBreakdown(
            score=int(round(trust_score)),
            confidence=TrustConfidence(confidence),
            trend=trend,
            architecture=int(round(category_scores["architecture"])),
            data_protection=int(round(category_scores["data_protection"])),
            identity_access=int(round(category_scores["identity_access"])),
            devsecops=int(round(category_scores["devsecops"])),
            historical_security=int(round(category_scores["historical_security"])),
            compliance=int(round(category_scores["compliance"])),
            platform_security=int(round(category_scores["platform_security"])),
            risks_exposure=int(round(category_scores["risks_exposure"])),
        )
        return breakdown

    # # ------------------------- Internal helpers -------------------------
    # def _extract_category_scores(self, llm_output: Dict[str, Any]) -> Dict[str, float]:
    #     """Derive per-category scores from the LLM output JSON structure."""
    #     scores: Dict[str, float] = {
    #         "architecture": 75,
    #         "data_protection": 80,
    #         "identity_access": 75,
    #         "devsecops": 70,
    #         "historical_security": 70,
    #         "compliance": 60,
    #         "platform_security": 80,
    #         "risks_exposure": 70,
    #     }

    #     docs = llm_output.get("docs", {})
    #     compliance = llm_output.get("compliance", {})

    #     # Architecture
    #     if any("AES-256" in enc for enc in docs.get("encryption", [])) and "zero-knowledge" in docs.get("summary", "").lower():
    #         scores["architecture"] = 94
    #     if any("bug bounty" in cert.get("framework", "").lower() for cert in compliance.get("certs", [])):
    #         scores["architecture"] = min(100, scores["architecture"] + 2)

    #     # Data Protection
    #     if docs.get("data_handling"):
    #         scores["data_protection"] = 93

    #     # Identity & Access
    #     if docs.get("authentication") and "RBAC" in docs.get("admin_controls", []):
    #         scores["identity_access"] = 92

    #     # DevSecOps (penalize for vulnerabilities)
    #     cve_list = llm_output.get("cve", {}).get("critical", [])
    #     num_critical = sum(1 for x in cve_list if x.get("severity") == "High")
    #     num_medium = sum(1 for x in cve_list if x.get("severity") == "Medium")
    #     scores["devsecops"] = max(0, 100 - num_critical * 10 - num_medium * 5)

    #     # Historical Security influenced by CVE trend
    #     cve_trend = llm_output.get("cve", {}).get("trend", "").lower()
    #     if cve_trend in {"stable", "improving"}:
    #         scores["historical_security"] = 85

    #     # Compliance: accumulate cert status
    #     certs = compliance.get("certs", [])
    #     comp_score = 0
    #     for cert in certs:
    #         if cert.get("status", "").lower() in {"certified", "claimed"}:
    #             comp_score += 15
    #     scores["compliance"] = min(100, comp_score)

    #     # Platform Security
    #     if "SaaS" in docs.get("deployment_model", []):
    #         scores["platform_security"] = 90

    #     # Risks / Exposure (incident penalty)
    #     incidents = llm_output.get("incidents", {}).get("items", [])
    #     risks_score = 78 - min(len(incidents) * 5, 20)
    #     scores["risks_exposure"] = max(0, risks_score)

    #     # Round floats for consistency prior to casting
    #     for key, val in scores.items():
    #         scores[key] = round(val, 2)
    #     return scores
    def _extract_category_scores(self, data):
        """Robust, multi-signal scoring across all 8 trust model categories."""

        scores = {
            "architecture": 0,
            "data_protection": 0,
            "identity_access": 0,
            "devsecops": 0,
            "historical_security": 0,
            "compliance": 0,
            "platform_security": 0,
            "risks_exposure": 0
        }

        # --- 1. ARCHITECTURE ---
        arch = data.get("docs", {})
        security_model = " ".join(arch.get("encryption", [])) + " ".join(arch.get("summary", []))

        if "end-to-end" in security_model.lower() or "zero-knowledge" in security_model.lower():
            scores["architecture"] += 25

        if any(enc in security_model for enc in ["AES-256", "GCM", "PBKDF2", "Argon2", "SRP"]):
            scores["architecture"] += 25

        if "threat" in security_model.lower() or "modeling" in security_model.lower():
            scores["architecture"] += 15

        if "aws" in security_model.lower():
            scores["architecture"] += 15

        # --- 2. DATA PROTECTION ---
        dh = data.get("docs", {}).get("data_handling", [])

        if any(x for x in dh if "residency" in x.lower()):
            scores["data_protection"] += 30

        if any(x for x in dh if "retention" in x.lower() or "backup" in x.lower()):
            scores["data_protection"] += 20

        if "encryption" in " ".join(arch.get("encryption", [])).lower():
            scores["data_protection"] += 25

        # --- 3. IDENTITY & ACCESS ---
        auth = data.get("docs", {}).get("authentication", [])

        if any(x for x in auth if "mfa" in x.lower()):
            scores["identity_access"] += 25

        if any(x for x in auth if "sso" in x.lower() or "scim" in x.lower()):
            scores["identity_access"] += 35

        # --- 4. DEVSECOPS / VULN MGMT ---
        if "bug bounty" in json.dumps(data.get("compliance", {}), default=str).lower():
            scores["devsecops"] += 25

        if "penetration" in json.dumps(data.get("compliance", {}), default=str).lower():
            scores["devsecops"] += 25

        cve = data.get("cve", {})
        if "trend" in cve and cve["trend"].lower() == "stable":
            scores["devsecops"] += 15

        # --- 5. HISTORICAL SECURITY PERFORMANCE ---
        critical_cves = [c for c in cve.get("critical", []) if c.get("severity") in ("High", "Critical")]
        num_critical = len(critical_cves)

        if num_critical == 0:
            scores["historical_security"] += 35
        elif num_critical == 1:
            scores["historical_security"] += 25
        elif num_critical == 2:
            scores["historical_security"] += 10
        # else → 0

        if "summary" in data.get("incidents", {}):
            scores["historical_security"] += 15

        # --- 6. COMPLIANCE ---
        certs = data.get("compliance", {}).get("certs", [])

        iso_count = sum(1 for c in certs if "ISO" in c.get("framework", ""))
        soc2 = any("SOC 2" in c.get("framework", "") for c in certs)

        scores["compliance"] += min(iso_count * 10, 40)
        if soc2:
            scores["compliance"] += 30

        # --- 7. PLATFORM SECURITY ---
        admin = data.get("docs", {}).get("admin_controls", [])
        monitoring = data.get("docs", {}).get("summary", "")

        if "audit" in " ".join(admin).lower():
            scores["platform_security"] += 20

        if "rbac" in " ".join(admin).lower():
            scores["platform_security"] += 25

        if "monitor" in monitoring.lower():
            scores["platform_security"] += 25

        # --- 8. RISKS & RESIDUAL EXPOSURE ---
        risks = 0

        if any("reserved" in c.get("description", "").lower() for c in cve.get("critical", [])):
            risks += 10

        if "no self-hosted" in json.dumps(data, default=str).lower():
            risks += 10

        if "third-party" in json.dumps(data, default=str).lower():
            risks += 10

        scores["risks_exposure"] = max(0, 100 - risks)

        return scores
    def _compute_trust(self, category_scores: Dict[str, float]) -> tuple[float, str]:
        trust_score = sum(category_scores.get(cat, 0) * w for cat, w in self.weights.items())
        missing = sum(1 for cat in self.weights if cat not in category_scores)
        if missing == 0:
            confidence = "high"
        elif missing <= 2:
            confidence = "medium"
        else:
            confidence = "low"
        return round(trust_score, 2), confidence

    def _derive_trend(self, llm_output: Dict[str, Any]) -> TrustTrend:
        raw = llm_output.get("cve", {}).get("trend", "stable").lower()
        if raw not in {"improving", "degrading", "stable"}:
            raw = "stable"
        return TrustTrend(raw)
