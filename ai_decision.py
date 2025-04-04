import requests
from api_keys import OPENAI_API_KEY
from typing import List, Any
import json
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class AIDecisionMaker:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def select_best_result(self, options: List[Any], criteria: str, num_to_select: int = 1) -> List[Any]:
        if not options:
            raise ValueError("选项列表不能为空")
        if num_to_select < 1:
            raise ValueError("选择数量必须大于0")
        if num_to_select > len(options):
            logger.warning(f"请求选择数量({num_to_select})大于可用选项数量({len(options)})")
            num_to_select = len(options)

        try:
            url = "https://api.openai.com/v1/completions"
            payload = {
                "model": "text-davinci-003",
                "prompt": self._construct_prompt(options, criteria, num_to_select),
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            selected = self._parse_response(response.json(), options, num_to_select)
            return selected
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API 请求失败: {e}")
            raise
        except Exception as e:
            logger.error(f"选择过程发生错误: {e}")
            return options[:num_to_select]  # 降级处理

    def _construct_prompt(self, options: List[Any], criteria: str, num_to_select: int) -> str:
        return f"""基于以下标准: {criteria}
从这些选项中选择前 {num_to_select} 个最佳选项: {json.dumps(options, ensure_ascii=False)}
仅返回选中项的编号(从0开始),格式如: [0, 1, 2]"""

    def _parse_response(self, response: dict, options: List[Any], num_to_select: int) -> List[Any]:
        try:
            indices = json.loads(response["choices"][0]["text"].strip())
            return [options[i] for i in indices if 0 <= i < len(options)]
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.error(f"解析响应失败: {e}")
            return options[:num_to_select]