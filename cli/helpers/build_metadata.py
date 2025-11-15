import datetime
from models.llm_models import AssessmentMetadata


def build_metadata() -> AssessmentMetadata:
    return AssessmentMetadata(
        assessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
