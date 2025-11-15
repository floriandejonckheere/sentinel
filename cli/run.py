import os
from ai_workflow import app

REPORT_PATH = "research_report.json"

def main():
    # If a cached report exists, reuse it instead of invoking the model.
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            cached = f.read()
        print("Loaded cached report. Delete research_report.json to regenerate.\n")
        print(cached)
        return

    state = app.invoke({"query": "1Password"}, config={"configurable": {"thread_id": "run-1"}})
    report = state.get("report")
    if report:
        full_report = report.model_dump_json(indent=2)
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write(full_report)
        print(full_report)
    else:
        # If sections were missing, you can inspect partial outputs:
        print("No report built. Partial state keys:", list(state.keys()))

if __name__ == "__main__":
    main()