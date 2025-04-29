from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import sessionmaker

from src.config import PAPER_INDEX_PATH
from src.models import PaperState
from src.store.models import Base, Paper, PaperHistory


class PaperIndex:
    def __init__(self, db_url: str | None = None, db_path: Path = PAPER_INDEX_PATH):
        if db_url is not None:
            self.engine = create_engine(
                db_url,
                future=True,
                pool_pre_ping=True,
                pool_recycle=1800,  # recycle stale connections every 30 min
            )

        else:
            self.engine = create_engine(f"sqlite:///{db_path}", future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)

    def get(self, paper_id: str) -> PaperState | None:
        """Get the state of a paper by its ID."""
        with self.Session() as session:
            paper = session.get(Paper, paper_id)
            if paper is None:
                return None
            return PaperState.model_validate(paper)

    def set(self, paper_state: PaperState) -> None:
        """Set the state of a paper."""
        now = paper_state.last_seen or datetime.now()
        with self.Session() as session:
            obj = session.get(Paper, paper_state.id)
            if obj is None:
                obj = Paper(
                    id=paper_state.id,
                    status=paper_state.status,
                    in_graph=paper_state.in_graph,
                    last_seen=now,
                )
                session.add(obj)
            else:
                obj.status = paper_state.status  # type: ignore
                obj.in_graph = paper_state.in_graph  # type: ignore
                obj.last_seen = now  # type: ignore

            # Use an upsert for PaperHistory to avoid UNIQUE constraint violations
            stmt = (
                insert(PaperHistory)
                .values(
                    id=paper_state.id,
                    state=paper_state.status,
                )
                .on_conflict_do_nothing(index_elements=["id"])
            )
            session.execute(stmt)
            session.commit()

    def set_many(self, states: list[PaperState]) -> None:
        """Set the state of multiple papers."""
        ids = [s.id for s in states]
        now = datetime.now()
        with self.Session() as session:
            existing_papers = session.query(Paper).filter(Paper.id.in_(ids)).all()
            existing_map = {p.id: p for p in existing_papers}

            for s in states:
                obj = existing_map.get(s.id)
                if obj is None:
                    obj = Paper(
                        id=s.id,
                        status=s.status,
                        in_graph=s.in_graph,
                        last_seen=now,
                    )
                    session.add(obj)
                else:
                    obj.status = s.status  # type: ignore
                    obj.in_graph = s.in_graph  # type: ignore
                    obj.last_seen = now  # type: ignore

                session.add(PaperHistory(id=s.id, state=s.status))

            session.commit()
