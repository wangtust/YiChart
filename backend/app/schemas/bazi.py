from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class BaziInput(BaseModel):
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    gender: Literal["male", "female"]
    is_lunar: bool = False  # 是否农历


class Pillar(BaseModel):
    heavenly_stem: str  # 天干
    earthly_branch: str  # 地支
    hidden_stems: list[str] = Field(default_factory=list)  # 藏干
    wuxing: str  # 五行


class BaziResult(BaseModel):
    year_pillar: Pillar
    month_pillar: Pillar
    day_pillar: Pillar
    hour_pillar: Pillar
    wuxing: dict[str, int]  # 五行统计
    shengxiao: str  # 生肖
    nayin: str  # 纳音
    day_master: str  # 日主
    day_master_wuxing: str  # 日主五行
    shishen: dict[str, str]  # 十神


class BaziRecordResponse(BaseModel):
    id: int
    birth_date: str
    birth_time: str
    gender: str
    bazi_result: Optional[dict] = None
    wuxing_result: Optional[dict] = None
    shengxiao: Optional[str] = None
    nayin: Optional[str] = None
    ai_analysis: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
