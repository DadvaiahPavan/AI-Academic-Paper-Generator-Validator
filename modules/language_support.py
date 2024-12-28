from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from typing import List, Tuple

# Set seed for consistent language detection
DetectorFactory.seed = 0

class MultiLanguageSupport:
    SUPPORTED_LANGUAGES = [
        "English",
        "French",
        "German",
        "Italian",
        "Portuguese",
        "Dutch",
        "Polish",
        "Russian",
        "Japanese",
        "Korean",
        "Chinese (Simplified)",
        "Spanish",
        "Arabic",
        "Turkish",
        "Hindi",
        "Swedish"
    ]

    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'nl': 'Dutch',
            'pl': 'Polish',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-CN': 'Chinese (Simplified)',
            'ar': 'Arabic',
            'tr': 'Turkish',
            'hi': 'Hindi',
            'sv': 'Swedish'
        }

    def get_supported_languages(self) -> List[str]:
        return self.SUPPORTED_LANGUAGES

    def detect_language(self, text: str) -> Tuple[str, str]:
        lang_code = detect(text)
        return lang_code, self.supported_languages.get(lang_code, 'Unknown')

    def translate_text(self, text: str, target_lang: str) -> str:
        target_code = {v: k for k, v in self.supported_languages.items()}.get(target_lang, 'en')
        return GoogleTranslator(source='auto', target=target_code).translate(text)
