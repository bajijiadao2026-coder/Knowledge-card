import httpx
from app.core.config import settings

# ──────────────────────────────────────────────────────────────
#  ⚠️  扣子 API 接口（唯一需要你配置的地方）
#
#  步骤：
#  1. 登录 https://www.coze.cn，进入你的 Bot
#  2. 在「发布」→「API」里获取 Bot ID
#  3. 在「个人设置」→「API Token」里生成 Token
#  4. 将两者填入 backend/.env 文件：
#       COZE_BOT_ID=xxxxxxxxxxxxxxxx
#       COZE_API_TOKEN=pat_xxxxxxxxxxxxxxxx
#
#  扣子 Bot 提示词建议（让 Bot 返回结构化文案）：
#  "你是一个短视频文案提取助手。用户发来抖音链接，请返回：
#   1. 视频标题
#   2. 视频作者
#   3. 完整文案内容（逐字稿）
#   格式：纯文字，用换行分隔三部分。"
# ──────────────────────────────────────────────────────────────

_MOCK_TRANSCRIPT = """这是一条模拟的视频文案（Coze API 未配置时使用）

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
    调用扣子 Bot API，传入抖音链接，返回视频文案。

    未配置 COZE_API_TOKEN / COZE_BOT_ID 时，自动使用 mock 数据，
    方便在没有真实 Key 的情况下开发调试。
    """
    if not settings.coze_api_token or not settings.coze_bot_id:
        return {"raw_response": _MOCK_TRANSCRIPT, "mock": True}

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

    answer = ""
    for msg in data.get("messages", []):
        if msg.get("type") == "answer":
            answer = msg.get("content", "")
            break

    return {"raw_response": answer, "mock": False}
