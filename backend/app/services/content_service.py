from app.core.config import settings
from app.utils.image_generator import ImageGenerator
from app.utils.prompt_generator import PromptGenerator
from app.utils.ai_decision import AIDecisionMaker
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        self.image_generator = ImageGenerator()
        self.prompt_generator = PromptGenerator()
        self.ai_decision = AIDecisionMaker()
        
    async def generate_content(self, topic: str):
        try:
            # 生成提示
            prompts = await self.prompt_generator.generate_prompts(topic)
            
            # 选择最佳提示
            selected_prompt = await self.ai_decision.select_best_result(
                prompts, 
                "创意性和可执行性"
            )
            
            # 生成图片
            image_path = await self.image_generator.generate_image_async(
                selected_prompt[0],
                str(settings.IMAGES_DIR)
            )
            
            return {
                "prompt": selected_prompt[0],
                "image_path": image_path
            }
            
        except Exception as e:
            logger.error(f"内容生成失败: {e}")
            raise
