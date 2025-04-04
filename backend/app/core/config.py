from pydantic import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "AutoContentGen"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./content.db"
    
    # API密钥配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    STABLE_DIFFUSION_API_KEY: str = os.getenv("STABLE_DIFFUSION_API_KEY", "")
    BAIDU_API_KEY: str = os.getenv("BAIDU_API_KEY", "")
    
    # 文件存储路径
    STORAGE_DIR: Path = Path("data/storage")
    IMAGES_DIR: Path = STORAGE_DIR / "images"
    VIDEOS_DIR: Path = STORAGE_DIR / "videos"
    
    class Config:
        case_sensitive = True

settings = Settings()
