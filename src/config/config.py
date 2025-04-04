import os
from pathlib import Path

class Config:
    # 项目根目录
    ROOT_DIR = Path(__file__).parent.parent.parent
    
    # 域名和主题配置
    DOMAIN = "Artificial Intelligence"
    SUBTOPICS = ["Machine Learning", "Natural Language Processing", "Robotics"]
    
    # 阈值配置
    TREND_THRESHOLD = 50
    NUM_PROMPTS = 5
    NUM_TO_SELECT = 2
    
    # 发布平台
    PUBLISH_PLATFORM = "Social Media"
    
    # 数据目录配置
    DATA_DIR = ROOT_DIR / 'data'
    PROMPTS_DIR = DATA_DIR / 'prompts'
    IMAGES_DIR = DATA_DIR / 'images'
    VIDEOS_DIR = DATA_DIR / 'videos'
    UPSCALED_DIR = DATA_DIR / 'upscaled_videos'
    LOGS_DIR = DATA_DIR / 'logs'
    
    # API重试配置
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds

    @classmethod
    def init_directories(cls):
        """初始化所有必要的目录"""
        for dir_path in [cls.DATA_DIR, cls.PROMPTS_DIR, cls.IMAGES_DIR, 
                        cls.VIDEOS_DIR, cls.UPSCALED_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
