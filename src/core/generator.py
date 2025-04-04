
import random
from ..config.settings import TEMPLATES, KEYWORDS
from ..utils.helpers import clean_text

class ContentGenerator:
    def __init__(self):
        self.templates = TEMPLATES
        self.keywords = KEYWORDS
    
    def generate_content(self):
        template = random.choice(self.templates)
        for keyword in self.keywords:
            if keyword in template:
                replacement = random.choice(self.keywords[keyword])
                template = template.replace(keyword, replacement)
        return clean_text(template)