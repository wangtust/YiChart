# YiChart 优化记录

日期：2026-05-15

## 优化内容

- 前端标签页图标改用项目 logo，并将 `frontend/public/logo.png` 从 1254x1254 压缩为 64x64，体积从约 1.4 MB 降到约 7 KB。
- 移除前端对 Element Plus 的全量 JS 注册，保留按需组件自动导入，并在根组件通过 `el-config-provider` 设置中文 locale。
- 为 Vite 构建增加 Vue/Pinia 分包，生产构建不再出现大 chunk 警告。
- 抽出 `formatAnalysisHtml`，统一 AI 分析内容渲染，并先转义 HTML 再处理 Markdown 样式，降低 `v-html` 注入风险。
- 统一前端 SSE 流式解析，支持跨 chunk 缓冲、HTTP 错误透传和后端 SSE error 事件透传。
- 紫微、六爻页面改用统一 API 客户端，减少重复手写 `fetch`。
- 修复六爻“展示卦象”和“AI 解卦/保存记录”二次随机不一致：AI 分析使用第一次摇出的六爻数值作为 `manual_yao`。
- 补齐前端 API 类型，减少 `any`，覆盖登录、历史记录、八字、紫微、六爻核心响应。
- 补齐 Alembic 初始迁移建表逻辑，避免新数据库只有 `alembic_version` 而没有业务表。
- 后端输入 schema 收窄为明确枚举，避免非法性别或起卦方式进入业务逻辑。
- `.gitignore` 增加 `.venv/`、`venv/` 和根目录临时 `logo.png`，避免虚拟环境和重复大图被提交。

## 验证结果

- `npm run build`：通过。
- `python -m compileall app alembic`：通过。
- `DATABASE_URL=sqlite:////tmp/yichart_migration_test.db alembic upgrade head`：通过，生成 `users`、`bazi_records`、`ziwei_records`、`liuyao_records`。

## 注意事项

- 当前远程 MySQL 可连接，但 MariaDB 在 Alembic 反射 `alembic_version` 时仍可能返回 1021 临时空间不足。后端启动已保留兜底：当版本表确认处于当前 head 时继续启动。
- 本机没有安装 `gh` CLI，因此本次只能执行 Git commit/push，不能用 GitHub CLI 自动创建 PR。
