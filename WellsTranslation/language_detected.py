from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Fix randomness
DetectorFactory.seed = 0

def detect_language(text):
    try:
        # Split the text into sentences (or chunks)
        import re
        sentences = re.split(r'[.!?]\s*', text)  # Split by punctuation marks
        sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty strings

        # Count the occurrences of each detected language
        language_counts = {}
        for sentence in sentences:
            try:
                lang = detect(sentence)
                language_counts[lang] = language_counts.get(lang, 0) + 1
            except LangDetectException:
                continue  # Skip sentences that cannot be detected

        # Determine the most frequent language
        if not language_counts:
            return "Could not detect language. Please enter more text."

        most_common_lang = max(language_counts, key=language_counts.get)
        return f"Detected language: {most_common_lang}"
    except Exception as e:
        return f"Error during language detection: {str(e)}"

# Example usage
sample_texts = [
    "Hello, how are you? Bonjour, comment ça va? Ça va bien, merci.",
    "Bonjour, comment ça va? Je suis très heureux aujourd'hui.",
    "Hola, ¿cómo estás? Estoy bien, gracias.",
    "नमस्ते, आप कैसे हैं? मैं ठीक हूँ।"
]

for text in sample_texts:
    print(f"Text: {text}")
    print(detect_language(text))
    print("-" * 50)
