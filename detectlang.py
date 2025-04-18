DetectorFactory.seed = 0

# Language code to full name mapping
LANGUAGE_MAP = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "hi": "Hindi",
    "de": "German",
    "it": "Italian",
    "zh-cn": "Chinese (Simplified)",
    "ja": "Japanese",
    "ru": "Russian",
    "ar": "Arabic",
    "pt": "Portuguese",
    "bn": "Bengali",
    "ko": "Korean",
    # Add more as needed
}

def detect_language(text):
    try:
        lang_code = detect(text)
        lang_name = LANGUAGE_MAP.get(lang_code, f"Unknown ({lang_code})")
        return f"Detected language: {lang_name}"
    except LangDetectException:
        return "Could not detect language. Please enter more text."
