from sentence_transformers import SentenceTransformer
from numpy.typing import NDArray
import numpy as np
from src.models import Paper

_model: SentenceTransformer | None = None


def embed_papers(papers: list[Paper]) -> NDArray[np.float32]:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [paper.abstract for paper in papers]
    vectors: NDArray[np.float32] = _model.encode(texts, convert_to_numpy=True)
    return vectors.astype(np.float32)


def embed_query(query: str) -> NDArray[np.float32]:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    vector: NDArray[np.float32] = _model.encode(query, convert_to_numpy=True)
    return vector.astype(np.float32)
