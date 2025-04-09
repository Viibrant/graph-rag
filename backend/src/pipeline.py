from typing import Generator
from src.models import IngestEvent
from src.arxiv import fetch_papers
from src.embedder import embed_papers
from src.vector_store import index_papers, search_faiss
from src.graph_store import update_graph, get_related_papers


def run_pipeline(query: str) -> Generator[IngestEvent, None, None]:
    """
    Runs the entire pipeline for processing papers.
    This function orchestrates the fetching of papers from ArXiv,
    embedding them, indexing in FAISS, updating the graph,
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
    papers = fetch_papers(query)

    # Embed papers
    yield IngestEvent(type="step", step="embedding", message="Embedding papers")
    embeddings = embed_papers(papers)

    # Index papers in FAISS
    yield IngestEvent(type="step", step="vector_index", message="Indexing in FAISS")
    index_papers(papers, embeddings)

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
