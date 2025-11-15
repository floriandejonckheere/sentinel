import os
from ai_workflow import app
from tools import trust_score_engine
import json

REPORT_PATH = "research_report.json"

def main():
    # If a cached report exists, reuse it instead of invoking the model.
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            cached = f.read()
        print("Loaded cached report. Delete research_report.json to regenerate.\n")
        print(cached)
        return

    state = app.invoke({"query": "Facebook"}, config={"configurable": {"thread_id": "run-1"}})
    report = state.get("report")
    if report:
        full_report = report.model_dump_json(indent=2)
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write(full_report)
        print(full_report)
    else:
        # If sections were missing, you can inspect partial outputs:
        print("No report built. Partial state keys:", list(state.keys()))

    # Calculate trust score & confidence based on output assesmet
    try:
        with open("research_report.json", "r") as f:
            llm_output = json.load(f)
    except FileNotFoundError:
        print("Error: 'research_report.json' not found.")
        return
    except json.JSONDecodeError:
        print("Error: JSON file is not valid.")
        return
    
    engine = trust_score_engine.TrustScoreEngine()
    category_scores, trust_score, confidence = engine.evaluate_llm_output(llm_output)
    # Print results
    print("\n===== Trust Score Report =====\n")
    print("Category Scores:")
    for cat, score in category_scores.items():
        print(f"  {cat}: {score}")

    print(f"\nOverall Trust Score: {trust_score}")
    print(f"Confidence Level: {confidence}")
    print("\n===============================\n")

if __name__ == "__main__":
    main()