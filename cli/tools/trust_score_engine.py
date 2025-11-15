"""TrustScoreEngine
---------------------
Converts raw LLM JSON output into a structured `TrustScoreBreakdown` Pydantic model.
"""
import json
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
        """
        Robust scoring engine with:
        - Baseline 50 per category
        - Additive scoring for strong indicators
        - Soft penalty only for proven risks
        - Normalization to 0-100
        """

        # Start with 50 baseline for every category
        scores = {
            "architecture": 50,
            "data_protection": 50,
            "identity_access": 50,
            "devsecops": 50,
            "historical_security": 50,
            "compliance": 50,
            "platform_security": 50,
            "risks_exposure": 50
        }

        # Helper to normalize to 0–100
        def clamp(x): return max(0, min(100, x))

        # ----------------------------
        # 1. ARCHITECTURE
        # ----------------------------
        encryption_text = " ".join(data.get("docs", {}).get("encryption", []))
        summary_text = data.get("docs", {}).get("summary", "")

        if any(k in encryption_text.lower() for k in ["zero-knowledge", "end-to-end"]):
            scores["architecture"] += 25

        if "aes" in encryption_text.lower() or "gcm" in encryption_text.lower():
            scores["architecture"] += 10

        if "pbkdf2" in encryption_text.lower() or "argon2" in encryption_text.lower():
            scores["architecture"] += 10

        if "aws" in summary_text.lower():
            scores["architecture"] += 5

        # ----------------------------
        # 2. DATA PROTECTION
        # ----------------------------
        dh = data.get("docs", {}).get("data_handling", [])

        if any("residency" in x.lower() for x in dh):
            scores["data_protection"] += 15

        if any("retention" in x.lower() for x in dh):
            scores["data_protection"] += 10

        if "backup" in " ".join(dh).lower():
            scores["data_protection"] += 10

        # ----------------------------
        # 3. IDENTITY / ACCESS
        # ----------------------------
        auth = data.get("docs", {}).get("authentication", [])

        if any("mfa" in x.lower() for x in auth):
            scores["identity_access"] += 15

        if any("sso" in x.lower() for x in auth):
            scores["identity_access"] += 15

        if any("scim" in x.lower() for x in auth):
            scores["identity_access"] += 15

        # ----------------------------
        # 4. DEVSECOPS
        # ----------------------------
        comp = json.dumps(data.get("compliance", {})).lower()

        if "bug bounty" in comp:
            scores["devsecops"] += 15

        if "penetration" in comp:
            scores["devsecops"] += 15

        cve = data.get("cve", {})
        if cve.get("trend", "").lower() == "stable":
            scores["devsecops"] += 10

        # ----------------------------
        # 5. HISTORICAL SECURITY
        # ----------------------------
        critical = [c for c in cve.get("critical", []) if c.get("severity") in ("High", "Critical")]

        if len(critical) == 0:
            scores["historical_security"] += 20
        elif len(critical) <= 2:
            scores["historical_security"] += 10
        else:
            scores["historical_security"] -= 10  # soft penalty

        if "incidents" in data and not data["incidents"].get("items", []):
            scores["historical_security"] += 10

        # ----------------------------
        # 6. COMPLIANCE
        # ----------------------------
        certs = data.get("compliance", {}).get("certs", [])

        if any("SOC 2" in c.get("framework", "") for c in certs):
            scores["compliance"] += 20

        iso_count = sum(1 for c in certs if "ISO" in c.get("framework", ""))
        scores["compliance"] += min(iso_count * 5, 25)

        # ----------------------------
        # 7. PLATFORM SECURITY
        # ----------------------------
        admin = data.get("docs", {}).get("admin_controls", [])

        if any("audit" in x.lower() for x in admin):
            scores["platform_security"] += 15

        if any("rbac" in x.lower() for x in admin):
            scores["platform_security"] += 15

        if "monitor" in summary_text.lower():
            scores["platform_security"] += 10

        # ----------------------------
        # 8. RISKS / RESIDUAL EXPOSURE
        # ----------------------------
        risks = 50

        # Only real risks reduce score
        reserved_cves = [c for c in cve.get("critical", []) if "reserved" in c.get("description", "").lower()]
        if reserved_cves:
            risks -= 10

        if "third-party" in summary_text.lower():
            risks -= 5

        scores["risks_exposure"] = clamp(risks)

        # Normalize all
        return {k: clamp(v) for k, v in scores.items()}
       
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
