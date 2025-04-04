import os
import requests
from api_keys import STABLE_DIFFUSION_API_KEY, BAIDU_API_KEY
from concurrent.futures import ThreadPoolExecutor
import asyncio
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
    async def generate_image_async(self, prompt: str, output_dir: str, api: str = "stable_diffusion") -> str:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if api == "stable_diffusion":
                return await self._generate_stable_diffusion(prompt, output_dir)
            elif api == "baidu":
                return await self._generate_baidu(prompt, output_dir)
            else:
                raise ValueError(f"不支持的 API: {api}")
                
        except Exception as e:
            logger.error(f"生成图像失败: {e}")
            raise

    async def _generate_stable_diffusion(self, prompt: str, output_dir: Path) -> str:
        url = "https://api.stablediffusionapi.com/v1/generation"
        payload = {
            "key": STABLE_DIFFUSION_API_KEY,
            "prompt": prompt,
            "width": 512,
            "height": 512
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        image_url = response.json()["output"][0]
        
        loop = asyncio.get_event_loop()
        image_path = await loop.run_in_executor(
            self.executor,
            self._download_and_save,
            image_url,
            output_dir / f"{prompt[:10]}_sd.png"
        )
        return str(image_path)

    async def _generate_baidu(self, prompt: str, output_dir: Path) -> str:
        image_path = output_dir / f"{prompt[:10]}_baidu.png"
        with open(image_path, "wb") as f:
            f.write(b"模拟图像数据")
        return str(image_path)

    def _download_and_save(self, url: str, filepath: Path) -> Path:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filepath