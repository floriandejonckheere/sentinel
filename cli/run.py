from ai_workflow import app

state = app.invoke({"query": "1Password"},
                   config={"configurable": {"thread_id": "run-1"}},)
report = state.get("report")
if report:
    print(report.model_dump_json(indent=2))
else:
    # If sections were missing, you can inspect partial outputs:
    print("No report built. Partial state keys:", list(state.keys()))