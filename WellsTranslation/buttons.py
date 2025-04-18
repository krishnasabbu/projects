import streamlit as st
import fitz  # PyMuPDF
from langdetect import detect, DetectorFactory, LangDetectException
from llm_utils import LLMTranslator
import base64
import asyncio
from pyppeteer import launch
import subprocess

# Fix randomness for consistent detection
DetectorFactory.seed = 0

API_KEY = "b69ffe06f2699f9bce616ac15a6c009585ebb822f58c5107f8549053609ef539"
translator = LLMTranslator(api_key=API_KEY)

st.set_page_config(page_title="PDF Language Translator", layout="wide")
st.title("📄 PDF Language Translator with LLM")

# Language code to full name map
LANGUAGE_MAP = {
    "en": "English",
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "zh-cn": "Chinese (Simplified)",
    "hi": "Hindi",
    "ja": "Japanese"
}

REVERSE_LANGUAGE_MAP = {v: k for k, v in LANGUAGE_MAP.items()}


def detect_language(text):
    try:
        lang_code = detect(text)
        lang_name = LANGUAGE_MAP.get(lang_code, f"Unknown ({lang_code})")
        return lang_code, lang_name
    except LangDetectException:
        return "unknown", "Could not detect"


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
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>',
        unsafe_allow_html=True)


def display_bytes(value):
    base64_pdf = base64.b64encode(value).decode("utf-8")
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>',
        unsafe_allow_html=True)


async def html_to_pdf(html_content, output_path):
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.setContent(f"<html><body>{html_content}</body></html>", waitUntil='networkidle0')
    await page.pdf({'path': output_path, 'format': 'A4'})
    await browser.close()


uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    content = extract_text_from_pdf(uploaded_file)
    lang_code, lang_name = detect_language(content)

    st.session_state.setdefault("translated", "")
    st.session_state.setdefault("reversed", "")
    st.session_state.setdefault("summary", "")
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("show_translated", False)
    st.session_state.setdefault("show_reversed", False)
    st.session_state.setdefault("show_summary", False)

    available_languages = [name for name in REVERSE_LANGUAGE_MAP if REVERSE_LANGUAGE_MAP[name] != lang_code]

    with st.container():
        st.write("---")
        st.write("#### 🗣️ Language Detection & Selection")

        col_src, col_tgt = st.columns([2, 4])

        # Source Language Selection (Disabled)
        with col_src:
            st.write(f"**Detected Source Language:** {lang_name}")

        # Target Language Selection
        with col_tgt:
            target_lang = st.radio("Choose target Language:", available_languages, horizontal=True)

    import streamlit as st

    # Inject custom CSS for styling
    st.markdown("""
        <style>
        .arrow-button {
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center;     /* Center vertically */
            height: 100%;            /* Full height of the column */
            width: 100%;             /* Full width of the column */
            font-size: 24px;         /* Larger arrow size */
            cursor: pointer;         /* Pointer cursor for clickable buttons */
            position: relative;      /* Enable positioning context */
            margin-top: 300px;                /* Move the arrow to 50% of the container's height */
            margin-left: 100px;               /* Move the arrow to 50% of the container's width */
        }
        
        .pdf-column {
            display: flex;
            justify-content: center; /* Center content horizontally */
            align-items: center;     /* Center content vertically */
            height: 100%;            /* Full height of the column */
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables
    if "show_third_column" not in st.session_state:
        st.session_state.show_third_column = False
    if "show_fifth_column" not in st.session_state:
        st.session_state.show_fifth_column = False

    # Create five columns
    col1, col2, col3, col4, col5 = st.columns([3,1,3,1,3])

    # --- Column 1: Display PDF ---
    with col1:
        with st.container():
            st.markdown('<div class="pdf-column">', unsafe_allow_html=True)
            display_pdf(uploaded_file)  # Replace with your PDF display logic
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Column 2: Arrow Button (Click to Render Third Column) ---
    with col2:
        with st.container():
            st.markdown('<div class="arrow-button">', unsafe_allow_html=True)
            if st.button("→", key="arrow1", help="Click to render the next column"):
                st.session_state.show_third_column = True
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Column 3: Conditional Rendering (Third Column) ---
    with col3:
        if st.session_state.show_third_column:
            with st.container():
                st.markdown('<div class="pdf-column">', unsafe_allow_html=True)
                display_pdf(uploaded_file)  # Replace with your PDF display logic
                st.markdown('</div>', unsafe_allow_html=True)

    # --- Column 4: Arrow Button (Click to Render Fifth Column) ---
    with col4:
        with st.container():
            if st.session_state.show_third_column:  # Only show this button if the third column is rendered
                if st.button("→", key="arrow2", help="Click to render the final column"):
                    st.session_state.show_fifth_column = True

    # --- Column 5: Conditional Rendering (Fifth Column) ---
    with col5:
        if st.session_state.show_fifth_column:
            with st.container():
                st.markdown('<div class="pdf-column">', unsafe_allow_html=True)
                display_pdf(uploaded_file)  # Replace with your PDF display logic
                st.markdown('</div>', unsafe_allow_html=True)

    # --- Summary Section ---
    with st.container():
        st.markdown("---")
        st.markdown("### 📋 Summary")
        if st.button("Generate Summary"):
            st.session_state.summary = translator.summarize_text(content)
            st.session_state.show_summary = True

        if st.session_state.get("show_summary", False):
            st.text_area("Summary", st.session_state.summary, height=200)

    # --- Chat Section ---
    with st.container():
        st.markdown("---")
        st.markdown("### 💬 Ask a Question About the PDF")
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
