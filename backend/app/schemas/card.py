from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class CardCreate(BaseModel):
    url: str


class CardUpdate(BaseModel):
    title: Optional[str] = None
    tags: Optional[list[str]] = None
    is_favorite: Optional[bool] = None


class CardOut(BaseModel):
    id: int
    title: str
    source_url: str
    platform: str
    author: Optional[str]
    cover_url: Optional[str]
    transcript: Optional[str]
    core_value: Optional[str]
    why_it_works: Optional[list[str]]
    writing_techniques: Optional[list[str]]
    reusable_structure: Optional[str]
    tags: Optional[list[str]]
    is_favorite: bool
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CardList(BaseModel):
    total: int
    items: list[CardOut]
