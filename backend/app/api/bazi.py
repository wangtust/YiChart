import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user_id, get_optional_user_id
from app.models.bazi_record import BaziRecord
from app.schemas.bazi import BaziInput, BaziResult, BaziRecordResponse
from app.services.bazi_calculator import calculate_bazi
from app.services.llm_service import stream_chat_completion
from app.prompts.bazi_prompt import format_bazi_prompt

router = APIRouter(prefix="/api/bazi", tags=["八字算命"])


@router.post("/calculate")
def bazi_calculate(data: BaziInput):
    """排盘计算 - 返回八字、五行等基础信息"""
    try:
        result = calculate_bazi(data.birth_date, data.birth_time, data.gender)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"计算错误: {str(e)}")


@router.post("/analyze")
async def bazi_analyze(
    data: BaziInput,
    db: Session = Depends(get_db),
    user_id: int | None = Depends(get_optional_user_id),
):
    """
    大模型解读 - 流式返回分析结果 (SSE)

    前端使用 EventSource 或 fetch + ReadableStream 接收
    """
    try:
        bazi_result = calculate_bazi(data.birth_date, data.birth_time, data.gender)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"排盘计算错误: {str(e)}")

    prompt = format_bazi_prompt(bazi_result, data.gender)

    # 先保存一条记录 (AI 分析后续更新)
    record = BaziRecord(
        user_id=user_id,
        birth_date=data.birth_date,
        birth_time=data.birth_time,
        gender=data.gender,
        is_lunar=1 if data.is_lunar else 0,
        bazi_result={
            "year_pillar": bazi_result["year_pillar"],
            "month_pillar": bazi_result["month_pillar"],
            "day_pillar": bazi_result["day_pillar"],
            "hour_pillar": bazi_result["hour_pillar"],
        },
        wuxing_result=bazi_result["wuxing"],
        shengxiao=bazi_result["shengxiao"],
        nayin=bazi_result["nayin"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    # 流式返回, 同时收集完整文本
    collected_text = []

    async def stream_and_save():
        async for chunk in stream_chat_completion(prompt):
            yield chunk
            # 收集内容用于保存
            if chunk.startswith("data: ") and "[DONE]" not in chunk:
                try:
                    data = json.loads(chunk[6:])
                    if "content" in data:
                        collected_text.append(data["content"])
                except json.JSONDecodeError:
                    pass

        # 流结束后更新记录
        full_text = "".join(collected_text)
        if full_text:
            record.ai_analysis = full_text
            db.commit()

    return StreamingResponse(
        stream_and_save(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Record-Id": str(record.id),
        },
    )


@router.get("/history", response_model=list[BaziRecordResponse])
def get_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    user_id: int | None = Depends(get_optional_user_id),
):
    """获取历史记录 - 登录用户只看自己的，未登录看全部"""
    query = db.query(BaziRecord)
    if user_id:
        query = query.filter(BaziRecord.user_id == user_id)
    records = query.order_by(BaziRecord.created_at.desc()).offset(skip).limit(limit).all()
    return records


@router.get("/{record_id}", response_model=BaziRecordResponse)
def get_record(record_id: int, db: Session = Depends(get_db)):
    """获取单条记录详情"""
    record = db.query(BaziRecord).filter(BaziRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record
