from typing import Protocol
from src.models import SearchResult


class GraphStore(Protocol):
    def get_related_ids(self, paper_id: str) -> list[str]: ...

    def get_papers_by_ids(self, ids: list[str]) -> list[SearchResult]: ...

    def is_healthy(self) -> bool: ...


class MockStore(GraphStore):
    def get_related_ids(self, paper_id: str) -> list[str]:
        return []

    def get_papers_by_ids(self, ids: list[str]) -> list[SearchResult]:
        return []

    def is_healthy(self) -> bool:
        return True


def get_graph_store() -> GraphStore:
    return MockStore()
