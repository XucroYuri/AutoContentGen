import os
import requests
from api_keys import STABLE_DIFFUSION_API_KEY, BAIDU_API_KEY

def generate_image(prompt, output_dir, api="stable_diffusion"):
    image_path = None
    try:
        if api == "stable_diffusion":
            url = "https://api.stablediffusionapi.com/v1/generation"
            payload = {
                "key": STABLE_DIFFUSION_API_KEY,
                "prompt": prompt,
                "width": 512,
                "height": 512
            }
            response = requests.post(url, json=payload)
            image_url = response.json()["output"][0]
            image_data = requests.get(image_url).content
            image_path = os.path.join(output_dir, f"{prompt[:10]}_sd.png")
            with open(image_path, "wb") as f:
                f.write(image_data)
        elif api == "baidu":
            # 模拟 Baidu API 调用（需替换为实际接口）
            image_path = os.path.join(output_dir, f"{prompt[:10]}_baidu.png")
            with open(image_path, "wb") as f:
                f.write(b"模拟图像数据")
    except Exception as e:
        print(f"API {api} 调用失败: {e}")
    return image_path