import requests
from api_keys import OPENAI_API_KEY

def select_best_result(options, criteria, num_to_select=1):
    selected = []
    try:
        url = "https://api.openai.com/v1/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        payload = {
            "model": "text-davinci-003",
            "prompt": f"From the following options: {options}, select the top {num_to_select} based on: {criteria}. Return only the selected items as a list.",
            "max_tokens": 100
        }
        response = requests.post(url, json=payload, headers=headers)
        selected = eval(response.json()["choices"][0]["text"].strip())
    except Exception as e:
        print(f"AI 决策失败: {e}")
        selected = options[:num_to_select]  # 失败时默认选择前几个
    return selected