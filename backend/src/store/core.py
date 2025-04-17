from src.embedder import embed_query
from src.models import SearchResult
from src.store.graph import get_graph_store
from src.store.vector import get_vector_store


def search(query: str, expand_hops: int = 1) -> list[SearchResult]:
    vector = get_vector_store()
    graph = get_graph_store()

    embedding = embed_query(query)
    top_results = vector.search(embedding)

    all_ids = {r.id for r in top_results}
    for r in top_results:
        related = graph.get_related_ids(r.id)
        all_ids.update(related)

    enriched = graph.get_papers_by_ids(list(all_ids))
    return enriched


def health_check() -> bool:
    """
    Check the health of the vector store and graph store.
    """
    vector_store = get_vector_store()
    graph_store = get_graph_store()

    # Check if the vector store is healthy
    vector_healthy = vector_store.is_healthy()

    # Check if the graph store is healthy
    graph_healthy = graph_store.is_healthy()

    return vector_healthy and graph_healthy
