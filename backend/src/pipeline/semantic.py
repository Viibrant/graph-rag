from src.models import SearchResult
from src.store import get_vector_store


def semantic_search(query: str, top_k: int = 5) -> list[SearchResult]:
    """
    Perform a semantic search on the vector store using the provided query.

    Args:
        query (str): The search query.
        top_k (int): The number of top results to return.

    Returns:
        list[SearchResult]: Top K search results.
    """
    # TODO: Embed query
    vector_store = get_vector_store()
    raise NotImplementedError("Semantic search is not implemented yet.")
    return vector_store.search(query_vector=..., top_k=top_k)
