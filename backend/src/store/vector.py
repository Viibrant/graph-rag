import os
from typing import Callable, Protocol

from loguru import logger
import numpy as np
from dotenv import load_dotenv
from numpy.typing import NDArray
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, ScoredPoint, VectorParams

from src.models import Paper, SearchResult

load_dotenv()

COLLECTION_NAME = "papers"
VECTOR_DIM = 384

host = os.getenv("QDRANT_HOST", "localhost")
port = int(os.getenv("QDRANT_PORT", 6333))


class VectorStore(Protocol):
    def index(self, papers: list[Paper], vectors: NDArray[np.float32]) -> None: ...

    def search(self, query_vector: NDArray[np.float32], top_k: int = 5) -> list[SearchResult]: ...

    def is_healthy(self) -> bool: ...


class QdrantVectorStore(VectorStore):
    def __init__(self, host: str = host, port: int = port):
        self.client = QdrantClient(host=host, port=port)
        self.is_healthy()

    def ensure_collection(self) -> None:
        """
        Ensure the collection exists. If it doesn't, create it.
        """
        existing_collections: list[str] = [
            collection.name for collection in self.client.get_collections().collections
        ]
        logger.info(
            f"Existing Qdrant collections: {[c.name for c in self.client.get_collections().collections]}"
        )
        if COLLECTION_NAME not in existing_collections:
            logger.info(f"Collection '{COLLECTION_NAME}' not found. Creating new collection...")
            self.client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
            )
            logger.success(f"Collection '{COLLECTION_NAME}' created successfully.")
        else:
            logger.debug(f"Collection '{COLLECTION_NAME}' already exists.")

    def index(self, papers: list[Paper], vectors: NDArray[np.float32]) -> None:
        """
        Index the papers and their corresponding vectors into Qdrant.
        """
        # Ensure the collection exists
        self.ensure_collection()

        points: list[PointStruct] = []
        for _, (paper, vector) in enumerate(zip(papers, vectors)):
            points.append(
                PointStruct(
                    id=paper.id,
                    vector=vector.flatten().tolist(),
                    payload={
                        "title": paper.title,
                        "authors": paper.authors,
                    },
                )
            )
        logger.info(f"Indexing {len(papers)} papers into Qdrant...")
        self.client.upsert(collection_name=COLLECTION_NAME, points=points)
        logger.success(f"Successfully upserted {len(points)} points into '{COLLECTION_NAME}'")
        count = self.client.count(COLLECTION_NAME, exact=True).count
        logger.debug(f"Collection now contains {count} vectors")

    def search(self, query_vector: NDArray[np.float32], top_k: int = 5) -> list[SearchResult]:
        results: list[ScoredPoint] = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector[0].tolist(),
            limit=top_k,
        )
        logger.info(f"Searching Qdrant for top {top_k} matches...")
        return [
            SearchResult(
                id=str(point.id),
                title=(point.payload or {}).get("title", ""),
                authors=(point.payload or {}).get("authors", []),
                score=point.score,
                related_ids=(point.payload or {}).get("related_ids", []),
            )
            for point in results
        ]

    def is_healthy(self) -> bool:
        """
        Check if the Qdrant instance is healthy.
        """
        try:
            self.client.get_collections()
            logger.info("Qdrant is healthy.")
            return True
        except Exception as e:
            logger.error(f"Qdrant is not healthy: {e}")
            return False


VECTOR_STORE: dict[str, Callable[[], VectorStore]] = {
    "qdrant": QdrantVectorStore,
}


def get_vector_store(backend: str = "qdrant") -> VectorStore:
    """
    Get the vector store instance based on the backend specified.
    """
    if backend not in VECTOR_STORE:
        raise ValueError(f"Unsupported vector store backend: {backend}")
    return VECTOR_STORE[backend]()
