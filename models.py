from sqlalchemy import (create_engine, Column, Integer, Text, String,
                        DateTime, ForeignKey, UniqueConstraint, Index)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os

DB_URL = os.getenv("DB_URL", "sqlite:///app.db")
engine = create_engine(DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)
Base = declarative_base()

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    src_text = Column(Text, nullable=False)
    tgt_text = Column(Text, nullable=False)
    lang_src = Column(String(8), default="zh")
    lang_tgt = Column(String(8), default="en")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    url  = Column(String(1024))

class EntrySource(Base):
    __tablename__ = "entry_sources"
    entry_id  = Column(Integer, ForeignKey("entries.id"), primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"), primary_key=True)

Index("idx_entries_text", Entry.src_text, Entry.tgt_text)

def init_db():
    Base.metadata.create_all(engine)
