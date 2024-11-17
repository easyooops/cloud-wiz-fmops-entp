import re
from typing import Dict

class PiiMaskingService:
    def __init__(self):
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'zip': r'\b\d{5}(?:-\d{4})?\b',
            'name': r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b',  # 단순 예시로 이름 패턴
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'birthdate': r'\b\d{2}/\d{2}/\d{4}\b',
            'driver_license': r'\b[A-Z0-9]{8}\b',
            'bank_account': r'\b\d{4}-?\d{4}-?\d{4}\b',
            'social_media': r'\b@([A-Za-z0-9_]+)\b',
            'medical_records': r'\b(MEDICAL_RECORD_PATTERN)\b',  # 실제 패턴 필요
            'passport_number': r'\b[A-Z0-9]{9}\b'
        }
        self.masking_replacements = {
            'email': '[MASKED_EMAIL]',
            'phone': '[MASKED_PHONE]',
            'credit_card': '[MASKED_CREDIT_CARD]',
            'zip': '[MASKED_ZIP]',
            'name': '[MASKED_NAME]',
            'ssn': '[MASKED_SSN]',
            'birthdate': '[MASKED_BIRTHDATE]',
            'driver_license': '[MASKED_DL]',
            'bank_account': '[MASKED_ACCOUNT]',
            'social_media': '[@MASKED_ACCOUNT]',
            'medical_records': '[MASKED_MEDICAL_RECORD]',
            'passport_number': '[MASKED_PASSPORT]'
        }

    def mask_pii(self, text: str, options: Dict[str, bool]) -> str:
        for key, pattern in self.patterns.items():
            if options.get(key, False):
                replacement = self.masking_replacements.get(key, '[MASKED]')
                text = re.sub(pattern, replacement, text)
        return text