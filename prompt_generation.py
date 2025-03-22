import requests
from api_keys import OPENAI_API_KEY, BAIDU_API_KEY

def generate_prompts(subtopic, api="openai", num_prompts=5):
    prompts = []
    try:
        if api == "openai":
            url = "https://api.openai.com/v1/completions"
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
            payload = {
                "model": "text-davinci-003",
                "prompt": f"Generate {num_prompts} creative prompts for '{subtopic}'.",
                "max_tokens": 200
            }
            response = requests.post(url, json=payload, headers=headers)
            prompts = response.json()["choices"][0]["text"].strip().split("\n")
        elif api == "baidu":
            # 模拟 Baidu API 调用（需替换为实际接口）
            prompts = [f"{subtopic} 示例提示 {i}" for i in range(num_prompts)]
    except Exception as e:
        print(f"API {api} 调用失败: {e}")
    return prompts