
import re

def process_template(template, replacements):
    """处理模板并替换关键词"""
    result = template
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result

def validate_content(content):
    """验证内容是否符合要求"""
    if not content or len(content) < 10:
        return False
    return True