# main.py
# AutoContentGen - Initial version of an AI-driven content generation tool
# AutoContentGen - AI驱动内容生成工具的初始版本
# This is the first release; developers are invited to improve or extend it via GitHub!
# 这是首个版本，欢迎开发者通过 GitHub 改进或扩展！

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.config.config import Config
from src.core.pipeline import ContentPipeline
from src.routers import content, auth
from src.utils.logger import setup_logger
import asyncio
from contextlib import asynccontextmanager

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化
    try:
        Config.init_directories()
        logger.info("系统初始化完成")
        yield
    except Exception as e:
        logger.error(f"系统初始化失败: {e}")
        raise
    finally:
        # 清理资源
        logger.info("系统关闭，清理资源")

app = FastAPI(
    title="AutoContentGen API",
    description="AI驱动的内容生成服务 API",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP错误: {exc.detail}")
    return {"error": exc.detail}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"系统错误: {str(exc)}")
    return {"error": "系统内部错误"}

# 注册路由
app.include_router(auth.router)
app.include_router(content.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        workers=4
    )
