from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.card import KnowledgeCard
from app.schemas.card import CardCreate, CardUpdate, CardOut, CardList
from app.services.coze import extract_transcript
from app.services.analyzer import analyze_transcript

router = APIRouter()


async def process_card(card_id: int, url: str, db: Session):
    card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
    if not card:
        return
    try:
        coze_result = await extract_transcript(url)
        transcript = coze_result.get("raw_response", "")

        analysis = await analyze_transcript(transcript)

        card.transcript = transcript
        card.title = analysis.get("suggested_title", "未命名卡片")
        card.core_value = analysis.get("core_value")
        card.why_it_works = analysis.get("why_it_works")
        card.writing_techniques = analysis.get("writing_techniques")
        card.reusable_structure = analysis.get("reusable_structure")
        card.tags = analysis.get("tags")
        card.status = "done"
    except Exception as e:
        card.status = "failed"
    finally:
        db.commit()


@router.post("", response_model=CardOut, status_code=202)
async def create_card(
    body: CardCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    card = KnowledgeCard(
        title="处理中...",
        source_url=body.url,
        status="processing",
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    background_tasks.add_task(process_card, card.id, body.url, db)
    return card


@router.get("", response_model=CardList)
def list_cards(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    tag: str = Query(None),
    favorite: bool = Query(None),
    q: str = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(KnowledgeCard)
    if favorite is not None:
        query = query.filter(KnowledgeCard.is_favorite == favorite)
    if q:
        query = query.filter(
            KnowledgeCard.title.contains(q) | KnowledgeCard.transcript.contains(q)
        )
    total = query.count()
    items = query.order_by(KnowledgeCard.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return CardList(total=total, items=items)


@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    return card


@router.put("/{card_id}", response_model=CardOut)
def update_card(card_id: int, body: CardUpdate, db: Session = Depends(get_db)):
    card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(card, field, value)
    db.commit()
    db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=204)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    db.delete(card)
    db.commit()


@router.post("/{card_id}/favorite", response_model=CardOut)
def toggle_favorite(card_id: int, db: Session = Depends(get_db)):
    card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    card.is_favorite = not card.is_favorite
    db.commit()
    db.refresh(card)
    return card
