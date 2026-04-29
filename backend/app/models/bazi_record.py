from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, func
from app.core.database import Base


class BaziRecord(Base):
    __tablename__ = "bazi_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    birth_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    birth_time = Column(String(5), nullable=False)  # HH:MM
    gender = Column(String(10), nullable=False)
    is_lunar = Column(Integer, default=0)

    # 八字结果
    bazi_result = Column(JSON)  # 四柱天干地支
    wuxing_result = Column(JSON)  # 五行统计
    shengxiao = Column(String(5))  # 生肖
    nayin = Column(String(10))  # 纳音

    # 大模型解读
    ai_analysis = Column(Text)  # AI 分析结果

    created_at = Column(DateTime, server_default=func.now())
