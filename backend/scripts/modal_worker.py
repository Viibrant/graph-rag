"""
This script is used to run the GraphRAG worker on Modal.

It fetches batches of papers from Redis, processes them by embedding,
and updates the vector store and paper index.
"""

import modal

from src.worker import run_worker_once

stub = modal.Stub("graph-rag-worker")

image = modal.Image.debian_slim().pip_install(
    "upstash-redis", "loguru", "numpy", "qdrant-client", "sentence-transformers"
)


@stub.function(
    image=image,
    schedule=modal.Period(weeks=1),  # Run once a week
    secret=modal.Secret.from_name("graph-rag-secrets"),
)
def worker():
    run_worker_once()
