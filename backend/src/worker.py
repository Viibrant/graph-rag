"""
Worker script for processing papers from a Redis queue.
This script continuously fetches batches of papers from a Redis queue,
embeds them using a pre-trained model, and updates the vector store and paper index.
"""

from time import sleep, time

import numpy as np
from loguru import logger
from numpy.typing import NDArray
from upstash_redis import Redis

from src.embedder import embed_papers
from src.models import Paper, PaperState, PaperStatus
from src.store import get_paper_index, get_vector_store
from src.store.redis import get_redis_conn

BATCH_SIZE = 8
SLEEP_INTERVAL = 1.0  # seconds


def get_batch(redis_conn: Redis, max_items: int) -> list[Paper]:
    """
    Fetch a batch of papers from Redis.

    Args:
        redis_conn (Redis): Redis connection object.
        max_items (int): Maximum number of items to fetch.

    Returns:
        list[Paper]: List of Paper objects.
    """
    logger.info("Fetching batch from Redis...")
    batch: list[Paper] = []

    # Fetch papers from Redis queue, validate them, and add to batch
    for _ in range(max_items):
        raw = redis_conn.lpop("paper_queue")
        if raw is None:
            break
        try:
            paper = Paper.model_validate_json(raw)
            batch.append(paper)
        except Exception as e:
            logger.warning(f"Invalid paper format: {e}")
            continue

    return batch


def process_batch(papers: list[Paper]) -> None:
    """
    Process a batch of papers by embedding them and updating the vector store and paper index.

    Args:
        papers (list[Paper]): List of Paper objects to process.
    """
    if not papers:
        return

    # Get vector store and paper index
    vector_store = get_vector_store()
    paper_index = get_paper_index()

    # Embed papers
    try:
        vectors: NDArray[np.float32] = embed_papers(papers)
    except Exception as e:
        logger.error(f"Failed to embed batch: {e}")
        return

    successes = 0

    # Index papers in vector store and update paper index
    for paper, vector in zip(papers, vectors):
        try:
            vector_store.index([paper], vector[np.newaxis, :])
            paper_index.set(
                PaperState(
                    id=paper.id,
                    status=PaperStatus.EMBEDDED,
                    in_graph=False,
                )
            )
            successes += 1
        except Exception as e:
            logger.warning(f"Failed to index paper {paper.id}: {e}")

    logger.info(f"Indexed {successes}/{len(papers)} papers")


def run_worker_loop() -> None:
    """
    Main loop for the worker process. Continuously fetches batches of papers from Redis,
    processes them, and updates the vector store and paper index.
    """
    logger.info("Starting worker loop...")
    redis_conn: Redis = get_redis_conn()

    while True:
        start_time = time()

        papers = get_batch(redis_conn, BATCH_SIZE)

        # Sleep if no papers were fetched
        if not papers:
            sleep(SLEEP_INTERVAL)
            continue

        process_batch(papers)

        duration = time() - start_time
        logger.info(f"Batch processed in {duration:.2f} seconds")


def run_worker_once() -> int:
    """
    Run a single batch of the worker. Returns number of papers processed.
    """
    redis_conn: Redis = get_redis_conn()
    papers = get_batch(redis_conn, BATCH_SIZE)
    process_batch(papers)
    return len(papers)


if __name__ == "__main__":
    processed = run_worker_once()
    if processed == 0:
        logger.info("No papers in queue — exiting.")
