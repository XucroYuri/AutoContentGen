
import re

def clean_text(text):
    """清理文本中的多余空白字符"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def format_output(text):
    """格式化输出文本"""
    return text.capitalize()