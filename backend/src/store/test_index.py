import os
import uuid
from datetime import datetime

import pytest

from src.models import PaperState, PaperStatus
from src.store.index import PaperIndex


@pytest.fixture(params=["sqlite", "supabase"])
def paper_index(request, tmp_path):
    if request.param == "sqlite":
        db_path = tmp_path / "test_papers.db"
        return PaperIndex(db_path=db_path)
    elif request.param == "supabase":
        db_url = os.getenv("SUPABASE_DB_URL")
        if not db_url:
            pytest.skip("SUPABASE_DB_URL not set")
        return PaperIndex(db_url=db_url)


def test_set_and_get_single_paper(paper_index):
    paper_id = str(uuid.uuid4())
    state = PaperState(
        id=paper_id,
        status=PaperStatus.QUEUED,
        in_graph=False,
        last_seen=datetime.now(),
    )

    paper_index.set(state)
    retrieved = paper_index.get(paper_id)

    assert retrieved is not None
    assert retrieved.id == state.id
    assert retrieved.status == PaperStatus.QUEUED
    assert retrieved.in_graph is False


def test_set_many_papers(paper_index):
    paper_ids = [str(uuid.uuid4()) for _ in range(3)]
    states = [
        PaperState(id=pid, status=PaperStatus.EMBEDDED, in_graph=False, last_seen=datetime.now())
        for pid in paper_ids
    ]

    paper_index.set_many(states)

    for pid in paper_ids:
        retrieved: PaperState = paper_index.get(pid)
        assert retrieved is not None
        assert retrieved.status == PaperStatus.EMBEDDED
        assert retrieved.in_graph is False


def test_update_existing_paper(paper_index):
    paper_id = str(uuid.uuid4())
    initial_state = PaperState(
        id=paper_id, status=PaperStatus.QUEUED, in_graph=False, last_seen=datetime.now()
    )
    paper_index.set(initial_state)

    updated_state = PaperState(
        id=paper_id, status=PaperStatus.EMBEDDED, in_graph=True, last_seen=datetime.now()
    )
    paper_index.set(updated_state)

    retrieved = paper_index.get(paper_id)

    assert retrieved is not None
    assert retrieved.status == PaperStatus.EMBEDDED
    assert retrieved.in_graph is True
