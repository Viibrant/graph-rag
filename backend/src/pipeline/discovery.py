from src.arxiv import fetch_papers as fetch_arxiv_papers
from src.models import Paper, PaperState, PaperStatus
from src.store import get_paper_index


def discover_papers(query: str, num_papers: int = 5) -> list[Paper]:
    """
    Discover papers based on a query using the arXiv API.

    Args:
        query (str): The search query.
        num_papers (int): The number of papers to fetch.

    Returns:
        list[Paper]: A list of discovered papers.
    """
    papers: list[Paper] = fetch_arxiv_papers(query, num_papers)

    # Update index
    paper_index = get_paper_index()
    paper_index.set_many(
        [
            PaperState(
                id=paper.id,
                status=PaperStatus.SEEN,
                in_graph=False,
                last_seen=None,
            )
            for paper in papers
        ]
    )

    return papers
