from typing import Generator
from src.models import IngestEvent, Paper
from src.arxiv import fetch_papers
from src.embedder import embed_papers
from src.store import get_vector_store, VectorStore


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
    # Search ArXiv for papers
    yield IngestEvent(
        type="step", step="fetching_arxiv", message=f"Searching ArXiv for '{query}'"
    )
    papers: list[Paper] = fetch_papers(query)

    # Embed papers
    yield IngestEvent(type="step", step="embedding", message="Embedding papers")
    embeddings = embed_papers(papers)

    # Upsert to Qdrant
    yield IngestEvent(type="step", step="vector_index", message="Upserting to Qdrant")
    vector_store: VectorStore = get_vector_store()
    vector_store.index(papers=papers, vectors=embeddings)

    # Update graph
    yield IngestEvent(type="step", step="graph_index", message="Updating graph")
    update_graph(papers)

    # Perform semantic search
    yield IngestEvent(
        type="step", step="semantic_search", message="Running semantic search"
    )
    top = search_faiss(query)

    # Update graph with neighbours
    yield IngestEvent(
        type="step", step="graph_search", message="Retrieving graph neighbours"
    )
    enriched = get_related_papers(top)

    # Return enriched papers
    yield IngestEvent(type="result", data=enriched)
