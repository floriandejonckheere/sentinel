"""
Self-Contained Trust Score Evaluation
-------------------------------------
Maps LLM output of vendor security data into category scores,
calculates overall trust score and confidence.
"""

from typing import Dict, Tuple

# -------------------------
# TrustScoreEngine
# -------------------------
class TrustScoreEngine:
    """
    Simple Trust Score Engine
    - Calculates trust score based on weighted category scores.
    - Assigns confidence level based on coverage.
    """
    def __init__(self, weights: Dict[str,float] = None):
        # Default equal weighting if none provided
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

    def evaluate(self, category_scores: Dict[str,float]) -> Tuple[float,str]:
        """
        Compute weighted trust score and confidence.
        Confidence is based on completeness and coverage of categories.
        """
        # Weighted sum
        trust_score = sum(category_scores.get(cat,0)*weight for cat, weight in self.weights.items())
        
        # Determine confidence
        missing = sum(1 for cat in self.weights if cat not in category_scores)
        if missing == 0:
            confidence = "high"
        elif missing <= 2:
            confidence = "medium"
        else:
            confidence = "low"

        return round(trust_score,2), confidence

# -------------------------
# LLM Output Normalization
# -------------------------
def extract_category_scores(llm_output: dict) -> dict:
    """
    Extracts normalized category scores from a vendor LLM output JSON.
    
    Categories:
        1. Architecture & Security Model
        2. Data Protection Controls
        3. Identity, Access & Authentication
        4. Secure Development & Vulnerability Management (DevSecOps)
        5. Historical Security Performance
        6. Compliance, Governance & Third-Party Validation
        7. Platform & Operational Security Controls
        8. Risks, Weaknesses & Residual Exposure
    
    Returns:
        dict: category -> score (0-100)
    """
    
    # Initialize scores with default values
    scores = {
        "architecture": 75,
        "data_protection": 80,
        "identity_access": 75,
        "devsecops": 70,
        "historical_security": 70,
        "compliance": 60,
        "platform_security": 80,
        "risks_exposure": 70
    }
    
    # 1. Architecture & Security Model
    docs = llm_output.get("docs", {})
    compliance = llm_output.get("compliance", {})
    vendor = llm_output.get("vendor", {})
    
    if any("AES-256" in enc for enc in docs.get("encryption", [])) and "zero-knowledge" in docs.get("summary","").lower():
        scores["architecture"] = 94
    if any("bug bounty" in cert.get("framework","").lower() for cert in compliance.get("certs",[])):
        scores["architecture"] += 2
    scores["architecture"] = min(100, scores["architecture"])
    
    # 2. Data Protection Controls
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
    
    # 5. Historical Security Performance
    trend = llm_output.get("cve", {}).get("trend","").lower()
    if trend in ["stable","improving"]:
        scores["historical_security"] = 85
    
    # 6. Compliance, Governance & Third-Party Validation
    certs = compliance.get("certs", [])
    comp_score = 0
    for cert in certs:
        if cert.get("status","").lower() in ["certified","claimed"]:
            comp_score += 15
    scores["compliance"] = min(100, comp_score)
    
    # 7. Platform & Operational Security Controls
    deployment = docs.get("deployment_model", [])
    if "SaaS" in deployment:
        scores["platform_security"] = 90
    
    # 8. Risks, Weaknesses & Residual Exposure
    incidents = llm_output.get("incidents", {}).get("items", [])
    risks_score = 78 - min(len(incidents)*5, 20)
    scores["risks_exposure"] = max(0, risks_score)
    
    # Round scores for neatness
    for k in scores:
        scores[k] = round(scores[k], 2)
    
    return scores

# -------------------------
# Main Function
# -------------------------
if __name__ == "__main__":
    import json

    # Load LLM output from JSON file
    with open("llm_output.json","r") as f:
        llm_output = json.load(f)

    # Extract category scores
    category_scores = extract_category_scores(llm_output)

    # Evaluate trust score
    engine = TrustScoreEngine()
    trust_score, confidence = engine.evaluate(category_scores)

    # Display results
    print("Category Scores:")
    for cat, score in category_scores.items():
        print(f"{cat}: {score}")
    print(f"\nOverall Trust Score: {trust_score}, Confidence: {confidence}")
