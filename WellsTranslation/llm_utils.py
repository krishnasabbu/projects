from openai import OpenAI


class LLMTranslator:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.together.xyz/v1"
        )
        self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

    def _call_llm(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()

    def translate_text(self, text, target_language):
        print(text)
        prompt = f"Translate the following text to {target_language}:\n\n{text}"
        return self._call_llm(prompt)

    def reverse_translate_text(self, text, original_language="English"):
        prompt = f"Translate the following text back to {original_language}:\n\n{text}"
        return self._call_llm(prompt)

    def summarize_text(self, text):
        prompt = f"Summarize the following text:\n\n{text}"
        return self._call_llm(prompt)

    def chat_with_pdf(self, pdf_text, question):
        prompt = f"Given the following PDF content:\n\n{pdf_text}\n\nAnswer the user's question: {question}"
        return self._call_llm(prompt)
