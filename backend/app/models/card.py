from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON

from app.core.database import Base


class KnowledgeCard(Base):
    __tablename__ = "knowledge_cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    source_url = Column(Text, nullable=False)
    platform = Column(String(20), default="douyin")
    author = Column(String(100))
    cover_url = Column(Text)

    transcript = Column(Text)
    core_value = Column(Text)
    why_it_works = Column(JSON)          # List[str]
    writing_techniques = Column(JSON)    # List[str]
    reusable_structure = Column(Text)
    tags = Column(JSON)                  # List[str]

    is_favorite = Column(Boolean, default=False)
    status = Column(String(20), default="done")  # processing / done / failed

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
