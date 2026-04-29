from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, func
from app.core.database import Base


class ZiweiRecord(Base):
    __tablename__ = "ziwei_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    birth_date = Column(String(10), nullable=False)
    birth_time = Column(String(5), nullable=False)
    gender = Column(String(10), nullable=False)

    # 紫微命盘结果
    palaces = Column(JSON)  # 十二宫数据
    sihua = Column(JSON)  # 四化
    ming_gong = Column(String(5))  # 命宫地支
    shen_gong = Column(String(5))  # 身宫地支

    # 大模型解读
    ai_analysis = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
