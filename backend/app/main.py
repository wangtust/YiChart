from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.core.database import engine, Base
from app.api import auth, bazi, ziwei, liuyao

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

    base_dir = os.path.dirname(os.path.dirname(__file__))
    alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    # 应用已有迁移
    command.upgrade(alembic_cfg, "head")
    print("数据库迁移检查完成")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield

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
