import os
import requests
from api_keys import RUNWAYML_API_KEY, BAIDU_API_KEY

def generate_video(image_path, output_dir, api="runwayml"):
    video_path = None
    try:
        if api == "runwayml":
            url = "https://api.runwayml.com/v1/video"
            payload = {
                "api_key": RUNWAYML_API_KEY,
                "image_url": image_path
            }
            response = requests.post(url, json=payload)
            video_url = response.json()["video_url"]
            video_data = requests.get(video_url).content
            video_path = os.path.join(output_dir, f"{os.path.basename(image_path)}_runway.mp4")
            with open(video_path, "wb") as f:
                f.write(video_data)
        elif api == "baidu":
            # 模拟 Baidu API 调用（需替换为实际接口）
            video_path = os.path.join(output_dir, f"{os.path.basename(image_path)}_baidu.mp4")
            with open(video_path, "wb") as f:
                f.write(b"模拟视频数据")
    except Exception as e:
        print(f"API {api} 调用失败: {e}")
    return video_path