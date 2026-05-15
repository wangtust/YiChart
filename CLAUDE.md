# 大模型算命网站 (YiChart)

结合大模型（OpenAI GPT）的中国传统算命网站，前后端分离架构。

## 技术栈

- **前端**: Vue 3 + Vite + TypeScript + Pinia + Vue Router + Element Plus
- **后端**: Python 3.11+ + FastAPI + SQLAlchemy 2.0 + Alemic
- **数据库**: MySQL
- **大模型**: OpenAI GPT API (gpt-4o / gpt-4o-mini)

## 项目结构

```
/root/YiChart/
├── frontend/          # Vue 3 前端
├── backend/           # FastAPI 后端
├── CLAUDE.md          # 本文件
└── README.md
```

## 开发命令

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端
```bash
cd frontend
npm install
npm run dev
```

## API 端点

### 认证
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录 (返回 JWT)
- `GET /api/auth/me` - 当前用户信息

### 八字算命
- `POST /api/bazi/calculate` - 排盘计算
- `POST /api/bazi/analyze` - 大模型解读 (SSE 流式)
- `GET /api/bazi/history` - 历史记录
- `GET /api/bazi/{id}` - 记录详情

## 开发阶段

### Phase 1 - MVP
1. 八字排盘 (天干地支、五行)
2. 大模型解读 (OpenAI GPT)
3. 用户系统 (注册/登录/历史)
4. 命盘可视化

### Phase 2 - 扩展
5. 紫微斗数
6. 每日运势
7. 合婚分析
8. 分享功能

### Phase 3 - 商业化
9. 付费高级解读
10. 历史记录管理

## 配置

后端环境变量 (`.env`):
```
DATABASE_URL=mysql+pymysql://user:password@host:3306/yichart?charset=utf8mb4
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o-mini
```

前端环境变量 (`.env`):
```
VITE_API_BASE_URL=/api
```
