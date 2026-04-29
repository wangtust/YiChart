from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, func
from app.core.database import Base


class LiuYaoRecord(Base):
    __tablename__ = "liuyao_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    question = Column(String(200), nullable=False)

    # 六爻结果
    yao_lines = Column(JSON)  # 六爻数据 (每爻阴阳、变爻)
    ben_gua = Column(JSON)  # 本卦
    bian_gua = Column(JSON)  # 变卦
    gua_name = Column(String(20))  # 本卦名
    bian_gua_name = Column(String(20))  # 变卦名
    shi_yao = Column(Integer)  # 世爻位置
    ying_yao = Column(Integer)  # 应爻位置
    liu_qin = Column(JSON)  # 六亲

    # 大模型解读
    ai_analysis = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
