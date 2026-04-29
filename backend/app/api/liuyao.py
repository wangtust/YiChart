import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_optional_user_id
from app.models.liuyao_record import LiuYaoRecord
from app.schemas.liuyao import LiuYaoInput, LiuYaoRecordResponse
from app.services.liuyao_calculator import calculate_liuyao
from app.services.llm_service import stream_chat_completion
from app.prompts.liuyao_prompt import format_liuyao_prompt

router = APIRouter(prefix="/api/liuyao", tags=["六爻占卜"])


@router.post("/calculate")
def liuyao_calculate(data: LiuYaoInput):
    """六爻起卦"""
    try:
        result = calculate_liuyao(data.question, data.method, data.manual_yao)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"起卦错误: {str(e)}")


@router.post("/analyze")
async def liuyao_analyze(
    data: LiuYaoInput,
    db: Session = Depends(get_db),
    user_id: int | None = Depends(get_optional_user_id),
):
    """六爻 AI 解读 (SSE 流式)"""
    try:
        result = calculate_liuyao(data.question, data.method, data.manual_yao)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"起卦错误: {str(e)}")

    prompt = format_liuyao_prompt(result)

    record = LiuYaoRecord(
        user_id=user_id,
        question=data.question,
        yao_lines=result["yao_lines"],
        ben_gua=result["ben_gua"],
        bian_gua=result["bian_gua"],
        gua_name=result["gua_name"],
        bian_gua_name=result["bian_gua_name"],
        shi_yao=result["shi_yao"],
        ying_yao=result["ying_yao"],
        liu_qin=result["liu_qin"],
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


@router.get("/history", response_model=list[LiuYaoRecordResponse])
def get_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    user_id: int | None = Depends(get_optional_user_id),
):
    query = db.query(LiuYaoRecord)
    if user_id:
        query = query.filter(LiuYaoRecord.user_id == user_id)
    return query.order_by(LiuYaoRecord.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{record_id}", response_model=LiuYaoRecordResponse)
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(LiuYaoRecord).filter(LiuYaoRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record
