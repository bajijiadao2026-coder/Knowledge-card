from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.card import KnowledgeCard

router = APIRouter()


@router.get("")
def list_tags(db: Session = Depends(get_db)):
    """返回所有已使用的标签及其数量"""
    cards = db.query(KnowledgeCard).filter(KnowledgeCard.tags.isnot(None)).all()
    tag_count: dict[str, int] = {}
    for card in cards:
        for tag in (card.tags or []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    return [{"name": k, "count": v} for k, v in sorted(tag_count.items(), key=lambda x: -x[1])]
