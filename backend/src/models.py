from pydantic import BaseModel, Field
from typing import Any
from enum import Enum


class IngestEventType(str, Enum):
    STEP = "step"
    PROGRESS = "progress"
    WARNING = "warning"
    ERROR = "error"
    RESULT = "result"


class IngestEvent(BaseModel):
    """
    Represents an event in the ingestion pipeline.

    Attributes:
        type (IngestEventType): The type of the event (e.g., step, progress, warning, error, result).
        step (str): The name of the step in the pipeline.
        message (str): A message describing the event.
        progress (float): A float representing the progress percentage (0.0 to 1.0).
        paper_id (str): The ID of the paper being processed.
        data (Any): Additional data related to the event.
    """

    type: IngestEventType | None = Field(
        default=None,
        description="Type of the event (e.g., step, progress, warning, error, result)",
    )
    step: str | None = Field(
        default=None,
        description="Name of the step in the pipeline",
    )
    message: str | None = Field(
        default=None,
        description="Message describing the event",
    )
    progress: float | None = Field(
        default=None,
        description="Progress percentage (0.0 to 1.0)",
    )
    paper_id: str | None = Field(
        default=None,
        description="ID of the paper being processed",
    )
    data: Any = Field(
        default=None,
        description="Additional data related to the event",
    )


class Paper(BaseModel):
    id: str
    title: str
    abstract: str
    authors: list[str]


class SearchResult(BaseModel):
    id: str
    title: str
    authors: list[str]
    score: float | None = Field(
        default=None,
        description="Score of the search result",
    )
    related_ids: list[str] | None = Field(
        default=None,
        description="List of related paper IDs",
    )
