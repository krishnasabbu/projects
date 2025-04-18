import streamlit as st
import fitz  # PyMuPDF
from llm_utils import LLMTranslator
import base64
import asyncio
from pyppeteer import launch
import subprocess
import tempfile

API_KEY = "b69ffe06f2699f9bce616ac15a6c009585ebb822f58c5107f8549053609ef539"
translator = LLMTranslator(api_key=API_KEY)

st.set_page_config(page_title="PDF Language Translator", layout="wide")
st.title("📄 PDF Language Translator with LLM")

lang_map = {
    "English": "English",
    "German": "German",
    "Spanish": "Spanish",
    "French": "French",
    "Chinese": "Chinese"
}
target_lang = st.radio("Choose a language to translate to:", list(lang_map.keys()), horizontal=True)

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])


def extract_text_from_pdf(f):
    doc = fitz.open(stream=f.read(), filetype="pdf")
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            text += block[4] + "\n"
    return text


def display_pdf(file):
    base64_pdf = base64.b64encode(file.getvalue()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_bytes(value):
    base64_pdf = base64.b64encode(value).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


async def html_to_pdf(html_content, output_path):
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.setContent(f"<html><body>{html_content}</body></html>", waitUntil='networkidle0')
    await page.pdf({'path': output_path, 'format': 'A4'})
    await browser.close()


if uploaded_file:
    content = extract_text_from_pdf(uploaded_file)

    st.session_state.setdefault("translated", "")
    st.session_state.setdefault("reversed", "")
    st.session_state.setdefault("summary", "")
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("show_translated", False)
    st.session_state.setdefault("show_reversed", False)
    st.session_state.setdefault("show_summary", False)

    col1, col2, col3 = st.columns([1, 1, 1])

    ### Column 1: Original PDF Display
    with col1:
        st.subheader("📄 Original PDF")
        display_pdf(uploaded_file)
        st.download_button("⬇️ Download Original PDF", data=uploaded_file.getvalue(), file_name="original.pdf")

    ### Column 2: Translation
    with col2:
        st.subheader("🌐 Translated Text")
        if st.button("Translate", key="translate_btn"):
            st.session_state.translated = translator.translate_text(content, lang_map[target_lang])
            st.session_state.show_translated = True

        if st.session_state.get("show_translated", False):
            with st.spinner("Generating PDF..."):
                output_path = "translated_output.pdf"
                translated_html = st.session_state.translated.replace('\n', '<br>')
                subprocess.run([
                    "python", "generate_pdf.py", translated_html, output_path
                ])

            with open(output_path, "rb") as f:
                pdf_data = f.read()
                display_bytes(pdf_data)
                st.download_button("⬇️ Download Translated", data=pdf_data, file_name="translated.pdf")

    ### Column 3: Reverse Translation
    with col3:
        st.subheader("🔁 Reverse Translated Text")
        if st.button("Convert Back", key="reverse_btn"):
            if st.session_state.translated:
                st.session_state.reversed = translator.reverse_translate_text(st.session_state.translated, "English")
                st.session_state.show_reversed = True

        if st.session_state.get("show_reversed", False):
            st.text_area("Reverse Translated Text", st.session_state.reversed, height=400)
            st.download_button("⬇️ Download Reversed", data=st.session_state.reversed, file_name="reversed.txt")

    ### Summary Section
    st.markdown("---")
    if st.button("📋 Show Summary"):
        st.session_state.summary = translator.summarize_text(content)
        st.session_state.show_summary = True

    if st.session_state.get("show_summary", False):
        st.subheader("📝 Summary")
        st.text_area("Summary", st.session_state.summary, height=200)

    ### Chat with PDF Section
    st.markdown("---")
    st.subheader("💬 Ask a question about the PDF")
    user_question = st.text_input("Ask a question:")
    if st.button("Ask"):
        if user_question.strip():
            response = translator.chat_with_pdf(content, user_question)
            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("LLM", response))

    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑‍💻 You:** {msg}")
        else:
            st.markdown(f"**🤖 LLM:** {msg}")
