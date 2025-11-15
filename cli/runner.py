import json
import os

from cli.ai_workflow import app
from cli.tools.trust_score_engine import TrustScoreEngine


class Runner():
    def __init__(self, query_id: str, assessment_id: str, name: str):
        self.query_id = query_id
        self.assessment_id = assessment_id
        self.name = name

    def run(self):
        print(f"Running assessment for {self.name}")

        # Initialize trust score engine
        engine = TrustScoreEngine()

        # Run the graph to produce fresh report + full_assessment
        state = app.invoke({"query": self.name}, config={"configurable": {"thread_id": "run-1"}})

        report = state.get("report")
        full = state.get("full_assessment")

        # Save ResearchReport JSON (this is what the engine reads)
        report_json = report.model_dump()

        # Run trust-score engine
        breakdown = engine.evaluate_llm_output(report_json)

        # Inject trust_score into FullAssessment.summary
        if full.summary is None:
            from models.llm_models import AssessmentSummary
            full.summary = AssessmentSummary(key_strengths=[], key_risks=[])

        full.summary.trust_score = breakdown

        # Save FullAssessment JSON
        query_cache_path = os.path.join("/data", f"{self.query_id}.json")
        assessments_cache_path = os.path.join("/data", f"{self.assessment_id}.json")

        # Always write the assessment (overwrite if exists)
        os.makedirs(os.path.dirname(assessments_cache_path), exist_ok=True)
        full_assessment_dict = full.model_dump()

        with open(assessments_cache_path, "w", encoding="utf-8") as f:
            json.dump(full_assessment_dict, f, indent=2)

        with open(query_cache_path, "w", encoding="utf-8") as f:
            json.dump(full_assessment_dict, f, indent=2)

        return full_assessment_dict
