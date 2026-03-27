# 知识卡片 · KnowledgeCard

将抖音短视频链接转化为结构化知识卡片。

## 功能

- 提交抖音视频链接，自动提取文案
- AI 分析文案亮点（钩子设计、节奏、结尾）
- 生成可复用文案结构模板
- 知识卡片管理（收藏、标签、搜索）

## 技术栈

| 层级 | 技术 |
|---|---|
| 后端 | Python · FastAPI |
| 数据库 | SQLite · SQLAlchemy |
| 文案提取 | 扣子 Bot API |
| AI 分析 | Kimi / Claude API |
| 前端 | Next.js · Tailwind CSS |

## 快速开始

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 填写 API Keys
uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
Ben1/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # API 路由
│   │   ├── core/           # 配置、数据库连接
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic 数据结构
│   │   └── services/       # 业务逻辑（扣子、AI分析）
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── src/
│       ├── components/     # 通用组件
│       ├── pages/          # 页面
│       ├── hooks/          # 自定义 Hook
│       └── utils/          # 工具函数
└── docs/                   # 文档
```
