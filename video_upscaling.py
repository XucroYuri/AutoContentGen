import os
from utils.apiClient import ApiClient
from config.api_config import API_CONFIG
from utils.logger import logger

class VideoUpscaler:
    def __init__(self, api="topaz"):
        self.api = api
        self.config = API_CONFIG[api]
        self.client = ApiClient(self.config['baseUrl'])

    def upscale_video(self, video_path, output_dir):
        try:
            result = self.client.post(
                self.config['endpoints']['upscale'],
                {"video_url": video_path}
            )
            
            upscaled_path = os.path.join(
                output_dir, 
                f"{os.path.basename(video_path)}_{self.api}.mp4"
            )
            
            self.save_video(result['upscaled_url'], upscaled_path)
            return upscaled_path
            
        except Exception as e:
            logger.error(f"Video upscaling failed: {str(e)}", exc_info=True)
            raise

    def save_video(self, url, path):
        video_data = self.client.get(url)
        with open(path, "wb") as f:
            f.write(video_data)