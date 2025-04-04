from ..config.config import Config
from ..utils.logger import setup_logger
from .services.trend_service import TrendService
from .services.prompt_service import PromptService
from .services.media_service import MediaService
from .services.ai_decision_service import AIDecisionService

class ContentPipeline:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.trend_service = TrendService()
        self.prompt_service = PromptService()
        self.media_service = MediaService()
        self.ai_decision = AIDecisionService()

    def run(self):
        try:
            self.logger.info("开始内容生成流程...")
            
            # 获取热门主题
            hot_subtopics = self._get_hot_subtopics()
            if not hot_subtopics:
                self.logger.warning("未找到热门主题")
                return False
                
            # 生成和选择提示词
            selected_prompts = self._generate_and_select_prompts(hot_subtopics[0])
            
            # 生成和选择媒体
            final_video = self._generate_and_select_media(selected_prompts)
            
            # 发布内容
            self._publish_content(final_video)
            
            return True
            
        except Exception as e:
            self.logger.error(f"内容生成失败: {str(e)}", exc_info=True)
            return False

    def _get_hot_subtopics(self):
        trend_data = self.trend_service.analyze_trends(Config.SUBTOPICS)
        return [topic for topic, score in trend_data.items() 
                if score > Config.TREND_THRESHOLD]

    def _generate_and_select_prompts(self, topic):
        prompts = self.prompt_service.generate_prompts(topic)
        return self.ai_decision.select_best(
            prompts,
            "选择最具创意和描述性的提示词",
            Config.NUM_TO_SELECT
        )

    def _generate_and_select_media(self, prompts):
        # 生成图像
        images = self.media_service.generate_images(prompts)
        selected_images = self.ai_decision.select_best(
            images,
            "选择最高质量的图像",
            Config.NUM_TO_SELECT
        )
        
        # 生成视频
        videos = self.media_service.generate_videos(selected_images)
        selected_videos = self.ai_decision.select_best(
            videos
