from pathlib import Path

from loguru import logger

PAPER_INDEX_PATH = Path("~/.cache/graph-rag/paper_index.db").expanduser()
if not PAPER_INDEX_PATH.exists():
    logger.warning(f"Paper index path {PAPER_INDEX_PATH} does not exist. Creating a new one.")
    PAPER_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
