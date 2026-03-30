import json
import httpx
from app.core.config import settings

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
        return {"raw_response": _MOCK_TRANSCRIPT, "mock": True}

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

                # 工作流输出节点的内容
                content = data.get("content") or data.get("output") or ""
                if content:
                    parts.append(str(content))

    transcript = "\n".join(parts).strip()
    return {"raw_response": transcript, "mock": False}
