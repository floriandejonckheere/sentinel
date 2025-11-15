"""
TrustScoreEngine
----------------
Self-contained class to convert LLM vendor output into
category scores, overall trust score, and confidence.
"""

from typing import Dict, Tuple

class TrustScoreEngine:
    """
    TrustScoreEngine:
    - Converts LLM output into normalized category scores.
    - Computes overall trust score and confidence.
    """
    
    def __init__(self, weights: Dict[str,float] = None):
        """
        Initialize the engine with optional category weights.
        Default: equal weights for 8 categories.
        """
        if weights is None:
            weights = {
                "architecture": 0.125,
                "data_protection": 0.125,
                "identity_access": 0.125,
                "devsecops": 0.125,
                "historical_security": 0.125,
                "compliance": 0.125,
                "platform_security": 0.125,
                "risks_exposure": 0.125
            }
        self.weights = weights

    # -------------------------
    # Public method
    # -------------------------
    def evaluate_llm_output(self, llm_output: Dict) -> Tuple[Dict[str,float], float, str]:
        """
        Takes LLM JSON output and returns:
        - category_scores: dict of 8 categories
        - trust_score: weighted 0-100
        - confidence: "low"/"medium"/"high"
        """
        category_scores = self._extract_category_scores(llm_output)
        trust_score, confidence = self._compute_trust(category_scores)
        return category_scores, trust_score, confidence

    # -------------------------
    # Internal helper: extract category scores
    # -------------------------
    def _extract_category_scores(self, llm_output: Dict) -> Dict[str,float]:
        """
        Extracts normalized category scores from LLM output.
        """
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
        
        docs = llm_output.get("docs", {})
        compliance = llm_output.get("compliance", {})
        
        # 1. Architecture
        if any("AES-256" in enc for enc in docs.get("encryption", [])) and "zero-knowledge" in docs.get("summary","").lower():
            scores["architecture"] = 94
        if any("bug bounty" in cert.get("framework","").lower() for cert in compliance.get("certs",[])):
            scores["architecture"] += 2
        scores["architecture"] = min(100, scores["architecture"])
        
        # 2. Data Protection
        if len(docs.get("data_handling",[])) > 0:
            scores["data_protection"] = 93
        
        # 3. Identity & Access
        if len(docs.get("authentication",[])) > 0 and "RBAC" in docs.get("admin_controls", []):
            scores["identity_access"] = 92
        
        # 4. DevSecOps
        cve_list = llm_output.get("cve", {}).get("critical", [])
        num_critical = sum(1 for x in cve_list if x.get("severity")=="High")
        num_medium = sum(1 for x in cve_list if x.get("severity")=="Medium")
        scores["devsecops"] = max(0, 100 - num_critical*10 - num_medium*5)
        
        # 5. Historical Security
        trend = llm_output.get("cve", {}).get("trend","").lower()
        if trend in ["stable","improving"]:
            scores["historical_security"] = 85
        
        # 6. Compliance
        certs = compliance.get("certs", [])
        comp_score = 0
        for cert in certs:
            if cert.get("status","").lower() in ["certified","claimed"]:
                comp_score += 15
        scores["compliance"] = min(100, comp_score)
        
        # 7. Platform & Operational Security
        deployment = docs.get("deployment_model", [])
        if "SaaS" in deployment:
            scores["platform_security"] = 90
        
        # 8. Risks & Residual Exposure
        incidents = llm_output.get("incidents", {}).get("items", [])
        risks_score = 78 - min(len(incidents)*5, 20)
        scores["risks_exposure"] = max(0, risks_score)
        
        # Round scores
        for k in scores:
            scores[k] = round(scores[k], 2)
        
        return scores

    # -------------------------
    # Internal helper: compute trust
    # -------------------------
    def _compute_trust(self, category_scores: Dict[str,float]) -> Tuple[float, str]:
        """
        Compute weighted trust score and confidence.
        """
        trust_score = sum(category_scores.get(cat,0)*weight for cat, weight in self.weights.items())
        
        # Confidence based on missing categories
        missing = sum(1 for cat in self.weights if cat not in category_scores)
        if missing == 0:
            confidence = "high"
        elif missing <= 2:
            confidence = "medium"
        else:
            confidence = "low"
        
        return round(trust_score,2), confidence