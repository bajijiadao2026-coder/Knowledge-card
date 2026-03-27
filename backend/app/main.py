from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.api.routes import cards, tags

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="知识卡片 API",
    description="将抖音短视频链接转化为结构化知识卡片",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cards.router, prefix="/api/cards", tags=["cards"])
app.include_router(tags.router, prefix="/api/tags", tags=["tags"])


@app.get("/")
def health_check():
    return {"status": "ok", "message": "知识卡片 API 运行中"}
