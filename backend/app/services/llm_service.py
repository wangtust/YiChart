"""
大模型服务封装
支持 OpenAI API 流式输出
"""

import json
from openai import AsyncOpenAI
from app.core.config import get_settings


async def stream_chat_completion(prompt: str):
    """
    流式调用大模型 API, 使用 SSE 格式返回

    Yields:
        SSE 格式的文本片段
    """
    settings = get_settings()
    client = AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )

    try:
        stream = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一位精通中国传统命理学的大师，擅长八字、紫微斗数、风水等。请用温暖专业的语气进行分析。",
                },
                {"role": "user", "content": prompt},
            ],
            stream=True,
            temperature=0.8,
            max_tokens=2000,
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"


async def get_completion(prompt: str) -> str:
    """
    非流式调用大模型 API, 返回完整结果
    """
    settings = get_settings()
    client = AsyncOpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一位精通中国传统命理学的大师，擅长八字、紫微斗数、风水等。请用温暖专业的语气进行分析。",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=2000,
    )

    return response.choices[0].message.content
