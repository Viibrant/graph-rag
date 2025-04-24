from .core import health_check
from .index import PaperIndex
from .vector import VectorStore, get_vector_store

__all__ = ["get_vector_store", "VectorStore", "health_check", "PaperIndex"]

_paper_index = None


def get_paper_index() -> PaperIndex:
    global _paper_index
    if _paper_index is None:
        _paper_index = PaperIndex()
    return _paper_index
