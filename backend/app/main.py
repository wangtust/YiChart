import asyncio
import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.core.database import engine, Base
from app.api import auth, bazi, ziwei, liuyao

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("yichart")

settings = get_settings()

# 导入所有 model，确保 create_all 和 alembic 能识别
from app.models.user import User
from app.models.bazi_record import BaziRecord
from app.models.ziwei_record import ZiweiRecord
from app.models.liuyao_record import LiuYaoRecord


def run_migrations():
    """自动执行 alembic 迁移"""
    import os
    from alembic.config import Config
    from alembic import command
    from alembic.script import ScriptDirectory
    from sqlalchemy import text
    from sqlalchemy.exc import OperationalError

    base_dir = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    # 应用已有迁移
    try:
        command.upgrade(alembic_cfg, "head")
    except OperationalError as exc:
        error_code = getattr(getattr(exc, "orig", None), "args", [None])[0]
        if error_code != 1021:
            raise

        script = ScriptDirectory.from_config(alembic_cfg)
        head = script.get_current_head()
        with engine.connect() as connection:
            versions = {
                row[0]
                for row in connection.execute(text("SELECT version_num FROM alembic_version"))
            }

        if head not in versions:
            raise

        logger.warning(
            "Alembic 检查遇到 MySQL 临时空间不足，但数据库已在当前版本 %s，继续启动",
            head,
        )
    logger.info("数据库迁移检查完成")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("正在启动 YiChart API ...")
    logger.info("数据库: %s", settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else settings.DATABASE_URL)
    await asyncio.to_thread(run_migrations)
    logger.info("YiChart API 启动完成")
    yield
    logger.info("YiChart API 正在关闭")

app = FastAPI(
    title=settings.APP_NAME,
    description="大模型算命网站 API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info("%s %s %d (%.0fms)", request.method, request.url.path, response.status_code, duration * 1000)
    return response


# 注册路由
app.include_router(auth.router)
app.include_router(bazi.router)
app.include_router(ziwei.router)
app.include_router(liuyao.router)


@app.get("/")
def root():
    return {"message": "YiChart API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
