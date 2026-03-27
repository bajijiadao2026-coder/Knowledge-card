import json
import httpx
from app.core.config import settings

ANALYSIS_PROMPT = """
你是一个短视频文案分析专家。请分析以下抖音短视频文案，并严格以JSON格式返回，不要有多余文字：

{{
  "suggested_title": "建议的知识卡片标题（简洁有力，15字内）",
  "core_value": "这条视频传递的核心价值或观点（50字内）",
  "why_it_works": [
    "亮点1：说明开头如何设计钩子",
    "亮点2：说明中间如何维持注意力",
    "亮点3：说明结尾如何引发行动或传播"
  ],
  "writing_techniques": ["文案技巧标签1", "文案技巧标签2"],
  "reusable_structure": "可复用的文案结构模板，如：[痛点] + [解法] + [行动号召]",
  "tags": ["内容标签1", "内容标签2", "内容标签3"]
}}

视频文案：
{transcript}
"""


async def analyze_transcript(transcript: str) -> dict:
    """
    调用 Kimi API 对文案进行结构化分析。
    """
    headers = {
        "Authorization": f"Bearer {settings.kimi_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "moonshot-v1-8k",
        "messages": [
            {
                "role": "user",
                "content": ANALYSIS_PROMPT.format(transcript=transcript),
            }
        ],
        "temperature": 0.3,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.moonshot.cn/v1/chat/completions",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()

    raw = data["choices"][0]["message"]["content"]

    # 清理 markdown 代码块（模型有时会包裹 ```json ... ```）
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_analysis": raw}
