from fastapi import APIRouter

from src.models import IngestEvent
from src.pipeline import run_pipeline

router = APIRouter()


@router.get("/pipeline", response_model=list[IngestEvent])
def pipeline(query: str) -> list[IngestEvent]:
    """
    Run the pipeline with the given query and return a list of IngestEvent objects.
    """
    return list(run_pipeline(query))
