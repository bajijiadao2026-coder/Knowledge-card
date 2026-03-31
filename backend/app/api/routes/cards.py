import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.core.database import get_db, SessionLocal
from app.models.card import KnowledgeCard
from app.schemas.card import CardCreate, CardUpdate, CardOut, CardList
from app.services.coze import extract_transcript
from app.services.analyzer import analyze_transcript

logger = logging.getLogger(__name__)
router = APIRouter()


async def process_card(card_id: int, url: str):
    """后台任务：调用 Coze 提取文案 → 千问分析 → 更新数据库"""
    db = SessionLocal()
    try:
        card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
        if not card:
            return

        logger.info(f"▶️  开始处理卡片 #{card_id}")

        # Step 1: 扣子工作流提取文案
        logger.info(f"📡 Step 1 / 2：调用扣子工作流提取文案...")
        coze_result = await extract_transcript(url)
        transcript = coze_result.get("raw_response", "")
        is_mock = coze_result.get("mock", False)
        logger.info(f"   文案提取{'（mock）' if is_mock else ''}完成，共 {len(transcript)} 字")

        # Step 2: 千问分析
        logger.info(f"🤖 Step 2 / 2：调用千问分析文案...")
        analysis = await analyze_transcript(transcript)
        logger.info(f"   分析完成，建议标题：「{analysis.get('suggested_title', '?')}」")

        card.transcript = transcript
        card.title = analysis.get("suggested_title", "未命名卡片")
        card.core_value = analysis.get("core_value")
        card.why_it_works = analysis.get("why_it_works")
        card.writing_techniques = analysis.get("writing_techniques")
        card.reusable_structure = analysis.get("reusable_structure")
        card.tags = analysis.get("tags")
        card.status = "done"
        db.commit()
        logger.info(f"🎉 卡片 #{card_id}「{card.title}」处理完成并已保存")

    except Exception as e:
        logger.error(f"❌ 卡片 #{card_id} 处理失败: {e}")
        card = db.query(KnowledgeCard).filter(KnowledgeCard.id == card_id).first()
        if card:
            card.status = "failed"
            db.commit()
    finally:
        db.close()


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
    background_tasks.add_task(process_card, card.id, body.url)
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
