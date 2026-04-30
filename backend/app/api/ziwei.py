import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user_id, get_optional_user_id
from app.models.ziwei_record import ZiweiRecord
from app.schemas.ziwei import ZiweiInput, ZiweiRecordResponse
from app.services.ziwei_calculator import calculate_ziwei
from app.services.llm_service import stream_chat_completion
from app.prompts.ziwei_prompt import format_ziwei_prompt

router = APIRouter(prefix="/api/ziwei", tags=["紫微斗数"])


@router.post("/calculate")
def ziwei_calculate(data: ZiweiInput):
    """紫微排盘计算"""
    try:
        result = calculate_ziwei(data.birth_date, data.birth_time, data.gender)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"计算错误: {str(e)}")


@router.post("/analyze")
async def ziwei_analyze(
    data: ZiweiInput,
    db: Session = Depends(get_db),
    user_id: int | None = Depends(get_optional_user_id),
):
    """紫微 AI 解读 (SSE 流式)"""
    try:
        result = calculate_ziwei(data.birth_date, data.birth_time, data.gender)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"排盘错误: {str(e)}")

    prompt = format_ziwei_prompt(result, data.gender)

    record = ZiweiRecord(
        user_id=user_id,
        birth_date=data.birth_date,
        birth_time=data.birth_time,
        gender=data.gender,
        palaces=result["palaces"],
        sihua=result["sihua"],
        ming_gong=result["ming_gong"],
        shen_gong=result["shen_gong"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    collected_text = []

    async def stream_and_save():
        async for chunk in stream_chat_completion(prompt):
            yield chunk
            if chunk.startswith("data: ") and "[DONE]" not in chunk:
                try:
                    d = json.loads(chunk[6:])
                    if "content" in d:
                        collected_text.append(d["content"])
                except json.JSONDecodeError:
                    pass

        full_text = "".join(collected_text)
        if full_text:
            record.ai_analysis = full_text
            db.commit()

    return StreamingResponse(
        stream_and_save(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/history", response_model=list[ZiweiRecordResponse])
def get_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    records = (
        db.query(ZiweiRecord)
        .filter(ZiweiRecord.user_id == user_id)
        .order_by(ZiweiRecord.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return records


@router.get("/{record_id}", response_model=ZiweiRecordResponse)
def get_record(record_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    record = db.query(ZiweiRecord).filter(ZiweiRecord.id == record_id, ZiweiRecord.user_id == user_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record
