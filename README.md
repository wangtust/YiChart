# YiChart - 大模型算命网站

结合 OpenAI GPT 的中国传统算命网站，支持八字、紫微斗数、六爻三大术数。

## 功能

- **八字算命** - 根据生辰排盘，AI 解读命理
- **紫微斗数** - 排盘命盘，AI 分析各宫位
- **六爻占卜** - 随机/手动起卦，AI 解卦
- **用户系统** - 注册登录，历史记录管理
- **流式输出** - AI 分析结果实时流式展示

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Vue 3 + TypeScript + Element Plus |
| 后端 | Python + FastAPI + SQLAlchemy |
| 数据库 | MySQL |
| AI | OpenAI GPT (gpt-4o-mini) |
| 部署 | Docker Compose |

## 快速开始

### 环境变量

在项目根目录创建 `.env`：

```env
OPENAI_API_KEY=sk-xxx
SECRET_KEY=your-secret-key
```

### Docker 部署

```bash
docker-compose up -d
```

访问 http://localhost 即可。

### 本地开发

**后端：**

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 编辑 .env 填入配置
uvicorn app.main:app --reload --port 8000
```

**前端：**

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173。

## 项目结构

```
YiChart/
├── frontend/          # Vue 3 前端
│   └── src/
│       ├── api/       # API 接口
│       └── views/     # 页面组件
├── backend/           # FastAPI 后端
│   └── app/
│       ├── api/       # 路由
│       ├── models/    # 数据模型
│       ├── services/  # 业务逻辑
│       └── prompts/   # AI Prompt 模板
├── docker-compose.yml
└── CLAUDE.md
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 注册 |
| POST | `/api/auth/login` | 登录 |
| POST | `/api/bazi/analyze` | 八字 AI 分析 (SSE) |
| POST | `/api/ziwei/analyze` | 紫微 AI 分析 (SSE) |
| POST | `/api/liuyao/analyze` | 六爻 AI 分析 (SSE) |
| GET | `/api/bazi/history` | 八字历史记录 |

