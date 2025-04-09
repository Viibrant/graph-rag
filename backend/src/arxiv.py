from src.models import Paper


def fetch_papers(query: str) -> list[Paper]:
    return [
        Paper(
            id="arxiv:1234", title="Fake Paper", abstract="...", authors=["Jane Doe"]
        ),
        Paper(
            id="arxiv:5678",
            title="Another Paper",
            abstract="...",
            authors=["John Smith"],
        ),
    ]
