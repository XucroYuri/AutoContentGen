import requests
from api_keys import OPENAI_API_KEY, BAIDU_API_KEY

def get_trend_scores(subtopics, api="openai"):
    scores = {}
    try:
        if api == "openai":
            url = "https://api.openai.com/v1/completions"
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
            for subtopic in subtopics:
                payload = {
                    "model": "text-davinci-003",
                    "prompt": f"Evaluate the trend score (0-100) of '{subtopic}' in current AI research.",
                    "max_tokens": 50
                }
                response = requests.post(url, json=payload, headers=headers)
                scores[subtopic] = int(response.json()["choices"][0]["text"].strip())
        elif api == "baidu":
            # 模拟 Baidu API 调用（需替换为实际接口）
            for subtopic in subtopics:
                scores[subtopic] = 60  # 示例值
    except Exception as e:
        print(f"API {api} 调用失败: {e}")
    return scores