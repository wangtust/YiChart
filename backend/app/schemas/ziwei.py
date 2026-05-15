from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class ZiweiInput(BaseModel):
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    gender: Literal["male", "female"]


class ZiweiRecordResponse(BaseModel):
    id: int
    birth_date: str
    birth_time: str
    gender: str
    palaces: Optional[dict] = None
    sihua: Optional[dict] = None
    ming_gong: Optional[str] = None
    shen_gong: Optional[str] = None
    ai_analysis: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
