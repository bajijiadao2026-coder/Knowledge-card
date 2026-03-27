import httpx
from app.core.config import settings


async def extract_transcript(video_url: str) -> dict:
    """
    调用扣子 Bot API，传入抖音链接，返回视频文案和元信息。
    返回格式: {"title": str, "author": str, "transcript": str}
    """
    headers = {
        "Authorization": f"Bearer {settings.coze_api_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "bot_id": settings.coze_bot_id,
        "user": "knowledge_card_app",
        "query": video_url,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{settings.coze_api_base}/open_api/v2/chat",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()

    # 扣子返回的消息在 messages 列表里，取 type=answer 的那条
    answer = ""
    for msg in data.get("messages", []):
        if msg.get("type") == "answer":
            answer = msg.get("content", "")
            break

    return {"raw_response": answer}
