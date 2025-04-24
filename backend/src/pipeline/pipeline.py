from typing import Generator

from src.models import IngestEvent, IngestEventType, Paper
from src.pipeline.discovery import discover_papers
from src.queuing import enqueue_missing
from src.store.redis import get_redis_conn


def run_pipeline(query: str) -> Generator[IngestEvent, None, None]:
    """
    Runs the entire pipeline for processing papers.
    This function orchestrates the fetching of papers from ArXiv,
    embedding them, upserting to Qdrant, updating the graph,
    and performing semantic search.

    Args:
        query (str): The search query to use for fetching papers.

    Yields:
        IngestEvent: Events that represent the steps in the pipeline.
            Each event contains information about the step being executed
            and any relevant data.
    """
    # Search for papers
    papers: list[Paper] = discover_papers(query)
    yield IngestEvent(
        type=IngestEventType.STEP,
        step="discovery",
        message="Papers discovered",
        data=papers,
    )
    # Enqueue missing papers
    enqueue_missing(papers, redis_conn=get_redis_conn())
