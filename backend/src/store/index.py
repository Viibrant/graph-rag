import sqlite3
from datetime import datetime
from pathlib import Path

from src.config import PAPER_INDEX_PATH
from src.models import PaperState


class PaperIndex:
    """
    A class to manage the paper index database.

    The paper index database tells us whether a paper has been seen before,
    whether it is in the graph, and its status.
    It also keeps a history of the paper states.
    """

    def __init__(self, db_path: Path = PAPER_INDEX_PATH):
        self.conn = sqlite3.connect(db_path)
        self._init_table()

    def _init_table(self) -> None:
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            status TEXT,
            in_graph BOOLEAN,
            last_seen TEXT
        );
        CREATE TABLE IF NOT EXISTS papers_history (
            id TEXT,
            state TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

    def _row_args(self, s: PaperState, now: str) -> tuple[str, str, bool, str, str, bool, str]:
        return (
            s.id,
            s.status,
            s.in_graph,
            now,
            s.status,
            s.in_graph,
            now,
        )

    def get(self, paper_id: str) -> PaperState | None:
        """Get the state of a paper by its ID."""
        row = self.conn.execute("SELECT * FROM papers WHERE ID = ?", (paper_id,)).fetchone()
        if row is None:
            return None
        return PaperState(**dict(zip(["id", "status", "in_graph", "last_seen"], row)))

    def set(self, paper_state: PaperState) -> None:
        """Set the state of a paper."""
        now = paper_state.last_seen or datetime.now().isoformat()

        self.conn.execute(
            """
            INSERT INTO papers (id, status, in_graph, last_seen)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = COALESCE(?, status),
                in_graph = COALESCE(?, in_graph),
                last_seen = ?
            """,
            self._row_args(paper_state, now),
        )

        self.conn.execute(
            "INSERT INTO papers_history (id, state) VALUES (?, ?)",
            (paper_state.id, paper_state.status),
        )

        self.conn.commit()

    def set_many(self, states: list[PaperState]) -> None:
        """Set the state of multiple papers."""
        now = datetime.now().isoformat()

        self.conn.executemany(
            """
            INSERT INTO papers (id, status, in_graph, last_seen)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status = COALESCE(?, status),
                in_graph = COALESCE(?, in_graph),
                last_seen = ?
            """,
            [self._row_args(s, now) for s in states],
        )

        self.conn.executemany(
            "INSERT INTO papers_history (id, state) VALUES (?, ?)",
            [(s.id, s.status) for s in states],
        )

        self.conn.commit()
