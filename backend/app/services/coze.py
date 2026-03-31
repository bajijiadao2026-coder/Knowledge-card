import json
import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

COZE_WORKFLOW_URL = "https://api.coze.cn/v1/workflow/stream_run"

_MOCK_TRANSCRIPT = """这是一条模拟的视频文案（Coze 工作流未配置时使用）

你有没有发现，很多人写文案，写了很久，就是没有人看？

原因很简单：你写的是你想说的，不是用户想听的。

今天分享3个让文案秒变爆款的核心技巧：

第一，用"你"代替"我"。把"我们产品很好用"改成"你终于可以..."，用户立刻感觉被看见。

第二，具体数字比形容词有力。"效率提升很多"不如"节省3小时"，让人一秒相信。

第三，结尾给行动指令。"点个关注，每天学一个文案技巧"比"谢谢大家"传播率高10倍。

记住：好文案不是你写得有多好，是用户读完有多想转发。

关注我，下期教你开头3秒如何钩住所有人。"""


async def extract_transcript(video_url: str) -> dict:
    """
    调用扣子工作流提取视频文案（直接 HTTP / SSE，完全可控）。
    未配置凭据时返回 mock 数据。
    """
    if not settings.coze_api_token or not settings.coze_workflow_id:
        logger.warning("⚠️  COZE_API_TOKEN 或 COZE_WORKFLOW_ID 未配置，使用 mock 文案数据")
        return {"raw_response": _MOCK_TRANSCRIPT, "mock": True}

    logger.info(f"🚀 [扣子] 开始调用工作流，视频链接: {video_url}")
    logger.info(f"   Workflow ID : {settings.coze_workflow_id}")

    headers = {
        "Authorization": f"Bearer {settings.coze_api_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "workflow_id": settings.coze_workflow_id,
        "parameters": {"input": video_url},
    }

    parts: list[str] = []

    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream(
            "POST",
            COZE_WORKFLOW_URL,
            headers=headers,
            json=payload,
        ) as resp:
            logger.info(f"   HTTP 状态码: {resp.status_code}")
            resp.raise_for_status()

            async for raw_line in resp.aiter_lines():
                line = raw_line.strip()
                if not line or not line.startswith("data:"):
                    continue

                data_str = line[len("data:"):].strip()
                if data_str in ("[DONE]", ""):
                    continue

                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                content = data.get("content") or data.get("output") or ""
                if content:
                    parts.append(str(content))
                    logger.info(f"   📦 收到数据片段（{len(str(content))} 字）")

    transcript = "\n".join(parts).strip()

    if transcript:
        logger.info(f"✅ [扣子] 工作流调用成功，提取文案 {len(transcript)} 字")
    else:
        logger.warning("⚠️  [扣子] 工作流返回为空，请检查工作流输出节点")

    return {"raw_response": transcript, "mock": False}
