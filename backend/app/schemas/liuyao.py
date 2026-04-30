from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LiuYaoInput(BaseModel):
    question: str  # 占卜问题
    method: str = "random"  # 起卦方式: random(自动) / manual(手动输入六爻)
    manual_yao: Optional[list[int]] = None  # 手动输入六爻 (7=少阳, 8=少阴, 9=老阳, 6=老阴)


class LiuYaoRecordResponse(BaseModel):
    id: int
    question: str
    yao_lines: Optional[list] = None
    ben_gua: Optional[dict] = None
    bian_gua: Optional[dict] = None
    gua_name: Optional[str] = None
    bian_gua_name: Optional[str] = None
    shi_yao: Optional[int] = None
    ying_yao: Optional[int] = None
    liu_qin: Optional[list] = None
    ai_analysis: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
