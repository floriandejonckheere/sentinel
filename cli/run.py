import os
import json
from ai_workflow import app
from tools import trust_score_engine
from models.llm_models import FullAssesment  # and other models if needed

REPORT_PATH = "research_report.json"
FULL_PATH = "full_assessment.json"


def print_trust_report(breakdown):
    """Pretty-print category scores and overall trust based on TrustScoreBreakdown."""
    print("\n===== Trust Score Report =====\n")
    print("Category Scores:")
    category_scores = {
        "architecture": breakdown.architecture,
        "data_protection": breakdown.data_protection,
        "identity_access": breakdown.identity_access,
        "devsecops": breakdown.devsecops,
        "historical_security": breakdown.historical_security,
        "compliance": breakdown.compliance,
        "platform_security": breakdown.platform_security,
        "risks_exposure": breakdown.risks_exposure,
    }
    for cat, score in category_scores.items():
        print(f"  {cat}: {score}")

    print(f"\nOverall Trust Score: {breakdown.score}")
    print(f"Confidence Level: {breakdown.confidence.value}")
    print(f"Trend: {breakdown.trend.value}")
    print("\n===============================\n")


def main():
    engine = trust_score_engine.TrustScoreEngine()

    # 1) If cached outputs exist, reuse them
    if os.path.exists(REPORT_PATH) and os.path.exists(FULL_PATH):
        print("Loaded cached report & full assessment. Delete JSON files to regenerate.\n")

        # Load ResearchReport JSON
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            llm_output = json.load(f)

        # Compute trust breakdown from ResearchReport
        breakdown = engine.evaluate_llm_output(llm_output)
        print_trust_report(breakdown)

        # Load FullAssesment and inject trust_score into summary
        with open(FULL_PATH, "r", encoding="utf-8") as f:
            full_json = json.load(f)

        full = FullAssesment.model_validate(full_json)

        if full.summary is None:
            # Shouldn't happen if summary_node ran, but be defensive.
            from models.llm_models import AssessmentSummary
            full.summary = AssessmentSummary(key_strengths=[], key_risks=[])

        full.summary.trust_score = breakdown

        # Save updated FullAssesment
        with open(FULL_PATH, "w", encoding="utf-8") as f:
            json.dump(full.model_dump(), f, indent=2)

        return

    # 2) Otherwise, run the graph to produce fresh report + full_assessment
    state = app.invoke({"query": "1Password"}, config={"configurable": {"thread_id": "run-1"}})

    report = state.get("report")
    full = state.get("full_assessment")

    if not report or not full:
        print("No report or full_assessment built. Partial state keys:", list(state.keys()))
        return

    # 3) Save ResearchReport JSON (this is what the engine reads)
    report_json = report.model_dump()
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)

    # 4) Run trust-score engine
    breakdown = engine.evaluate_llm_output(report_json)
    print_trust_report(breakdown)

    # 5) Inject trust_score into FullAssesment.summary
    if full.summary is None:
        from models.llm_models import AssessmentSummary
        full.summary = AssessmentSummary(key_strengths=[], key_risks=[])

    full.summary.trust_score = breakdown

    # 6) Save FullAssesment JSON
    with open(FULL_PATH, "w", encoding="utf-8") as f:
        json.dump(full.model_dump(), f, indent=2)

    # Optional: print full assessment
    print("Full assessment:")
    print(json.dumps(full.model_dump(), indent=2))


if __name__ == "__main__":
    main()
