from fastapi import APIRouter
from src.pipeline import run_pipeline
from src.models import IngestEvent

router = APIRouter()


@router.get("/search", response_model=list[IngestEvent])
def search(query: str) -> list[IngestEvent]:
    events: list[IngestEvent] = list(run_pipeline(query))
    return events
