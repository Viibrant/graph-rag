from sqlalchemy import Boolean, Column, DateTime, String, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Paper(Base):
    __tablename__ = "papers"

    id = Column(String, primary_key=True)
    status = Column(String)
    in_graph = Column(Boolean)
    last_seen = Column(DateTime)


class PaperHistory(Base):
    __tablename__ = "papers_history"

    id = Column(String, primary_key=True)
    state = Column(String)
    timestamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
