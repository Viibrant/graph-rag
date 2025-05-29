from fastapi import APIRouter, HTTPException, Query

from src.models import IngestEvent, PaperState
from src.pipeline import run_pipeline
from src.store import get_paper_index, health_check

router = APIRouter()


@router.get("/pipeline", response_model=list[IngestEvent])
def pipeline(query: str) -> list[IngestEvent]:
    """
    Run the pipeline with the given query and return a list of IngestEvent objects.
    """
    return list(run_pipeline(query))


@router.get("/health")
def health():
    ok: dict[str, bool] = health_check()
    if not all(ok.values()):
        raise HTTPException(status_code=503, detail="One or more components are unhealthy")
    return ok


@router.get("/status")
def status(paper_id: list[str] = Query(...)) -> list[dict[str, str | bool]]:
    """
    Return the status of one or more papers from the PaperIndex.
    """
    index = get_paper_index()
    results: list[dict[str, str | bool]] = []

    for pid in paper_id:
        state: PaperState | None = index.get(pid)
        if not state:
            results.append({"id": pid, "status": "NOT_FOUND", "in_graph": False})
        else:
            results.append(
                {
                    "id": state.id,
                    "status": state.status.value,
                    "in_graph": state.in_graph,
                }
            )

    return results
