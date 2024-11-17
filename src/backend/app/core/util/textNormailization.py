import re
import unicodedata
from typing import Dict

class TextNormalizationService:
    def __init__(self):
        self.patterns = {
            'trim': r'^\s+|\s+$',  # 앞뒤 공백 제거
            'duplicate_spaces': r'\s+',  # 중복 공백 제거
            'newline': r'\n',  # 줄바꿈 문자 제거
            'numbers': r'\d+',  # 숫자 제거
            'html_tags': r'<.*?>',  # HTML 태그 제거
            'urls': r'http[s]?://\S+',  # URL 제거
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # 이메일 주소 제거
            'punctuation': r'[^\w\s]',  # 문장 부호 제거
        }

    def normalize_text(self, text: str, options: Dict[str, bool]) -> str:
        if options.get('trim', False):
            text = re.sub(self.patterns['trim'], '', text)
        
        if options.get('duplicate_spaces', False):
            text = re.sub(self.patterns['duplicate_spaces'], ' ', text)
        
        if options.get('newline', False):
            text = re.sub(self.patterns['newline'], ' ', text)
        
        if options.get('numbers', False):
            text = re.sub(self.patterns['numbers'], '', text)
        
        if options.get('html_tags', False):
            text = re.sub(self.patterns['html_tags'], '', text)
        
        if options.get('urls', False):
            text = re.sub(self.patterns['urls'], '', text)
        
        if options.get('emails', False):
            text = re.sub(self.patterns['emails'], '', text)
        
        if options.get('punctuation', False):
            text = re.sub(self.patterns['punctuation'], '', text)
        
        if options.get('lowercase', False):
            text = text.lower()
        
        if options.get('uppercase', False):
            text = text.upper()
        
        if options.get('normalize_special_chars', False):
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        
        return text