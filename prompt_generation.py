import requests
from api_keys import OPENAI_API_KEY, BAIDU_API_KEY
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_input(subtopic: str, num_prompts: int) -> bool:
    if not isinstance(subtopic, str) or not subtopic.strip():
        raise ValueError("主题不能为空")
    if not isinstance(num_prompts, int) or num_prompts < 1:
        raise ValueError("提示数量必须为正整数")
    return True

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_prompts(subtopic: str, api: str = "openai", num_prompts: int = 5) -> list:
    validate_input(subtopic, num_prompts)
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
            response.raise_for_status()  # 检查 HTTP 响应状态
            prompts = response.json()["choices"][0]["text"].strip().split("\n")
        elif api == "baidu":
            # 模拟 Baidu API 调用（需替换为实际接口）
            prompts = [f"{subtopic} 示例提示 {i}" for i in range(num_prompts)]
        else:
            raise ValueError(f"不支持的 API 类型: {api}")
            
        return [p.strip() for p in prompts if p.strip()]  # 过滤空提示
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API 请求失败: {e}")
        raise
    except Exception as e:
        logger.error(f"生成提示时发生错误: {e}")
        raise