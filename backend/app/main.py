from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import engine, Base
from app.api import auth, bazi, ziwei, liuyao

settings = get_settings()

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="大模型算命网站 API",
    version="1.0.0",
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
