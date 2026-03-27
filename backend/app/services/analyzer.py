import json
import httpx
from app.core.config import settings

ANALYSIS_PROMPT = """你是一个短视频文案分析专家。请分析以下抖音短视频文案，并严格以JSON格式返回，不要有任何多余文字或markdown标记：

{{
  "suggested_title": "建议的知识卡片标题（简洁有力，15字内）",
  "core_value": "这条视频传递的核心价值或观点（50字内）",
  "why_it_works": [
    "亮点1：说明开头如何设计钩子抓住注意力",
    "亮点2：说明中间如何用节奏和内容维持兴趣",
    "亮点3：说明结尾如何引发转发或关注行为"
  ],
  "writing_techniques": ["文案技巧标签1", "文案技巧标签2", "文案技巧标签3"],
  "reusable_structure": "可复用的文案结构模板，如：[痛点问题] + [N个解法] + [行动号召]",
  "tags": ["内容标签1", "内容标签2", "内容标签3"]
}}

视频文案：
{transcript}"""

_MOCK_ANALYSIS = {
    "suggested_title": "3个技巧让文案秒变爆款",
    "core_value": "好文案要站在用户视角，用具体数字+行动指令，而非自说自话",
    "why_it_works": [
        "亮点1·钩子设计：开头用反问'你有没有发现'制造代入感，直击写作者痛点",
        "亮点2·节奏控制：3个技巧用'第一/第二/第三'排列，节奏清晰，便于记忆和传播",
        "亮点3·结尾设计：最后一句先给出价值观总结，再给出明确的关注理由，引导行动",
    ],
    "writing_techniques": ["反问钩子", "数字冲击", "排比结构", "行动指令"],
    "reusable_structure": "[反问痛点] + [3个具体解法（每个含对比示例）] + [价值观金句] + [关注理由]",
    "tags": ["文案技巧", "爆款方法论", "内容创作"],
}


async def analyze_transcript(transcript: str) -> dict:
    """
    调用 Kimi API 对文案进行结构化分析。
    未配置 KIMI_API_KEY 时返回 mock 分析结果。
    """
    if not settings.kimi_api_key:
        return _MOCK_ANALYSIS

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

    raw = data["choices"][0]["message"]["content"].strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"suggested_title": "分析结果", "raw_analysis": raw}
