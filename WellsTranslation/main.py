import streamlit as st
import fitz  # PyMuPDF
from llm_utils import LLMTranslator
from streamlit_quill import st_quill  # WYSIWYG Editor

API_KEY = "b69ffe06f2699f9bce616ac15a6c009585ebb822f58c5107f8549053609ef539"
translator = LLMTranslator(api_key=API_KEY)

st.set_page_config(page_title="PDF Language Translator", layout="wide")
st.title("📄 PDF Language Translator with LLM")

# CSS to force fixed height editors (the keys are used to target the wrappers)
st.markdown("""
    <style>
    /* Force height and scrolling for all Quill editors */
    .ql-container {
        height: 400px !important;
        overflow-y: auto;
    }

    /* Specifically make summary shorter */
    .stMarkdown + div .ql-container {
        height: 200px !important;
    }
    </style>
""", unsafe_allow_html=True)

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


if uploaded_file:
    content = extract_text_from_pdf(uploaded_file)

    # Initialize session state variables and flags
    st.session_state.setdefault("translated", "")
    st.session_state.setdefault("reversed", "")
    st.session_state.setdefault("summary", "")
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("show_translated", False)
    st.session_state.setdefault("show_reversed", False)
    st.session_state.setdefault("show_summary", False)

    col1, col2, col3 = st.columns([1, 1, 1])

    ### Column 1: Original Content Editor
    with col1:
        st.subheader("📄 Original")
        # Display the original PDF content in a WYSIWYG HTML editor
        original_html = st_quill(
            placeholder=content,
            html=True,
            readonly=True,
        )
        st.write(original_html)
        st.download_button("⬇️ Download Edited Original", data=original_html, file_name="edited_original.html")

    ### Column 2: Translated Content Editor
    with col2:
        header_col, button_col = st.columns([4, 1])
        with header_col:
            st.subheader("🌐 Translated")
        with button_col:
            if st.button("Translate", key="translate_btn"):
                st.session_state.translated = translator.translate_text(content, lang_map[target_lang])
                st.session_state.show_translated = True

        if st.session_state.get("show_translated", False):
            translated_html = st_quill(
                placeholder=st.session_state.translated,
                html=True,
                readonly=True,
            )
            st.write(translated_html)
            if st.session_state.translated:
                st.download_button("⬇️ Download Translated", data=translated_html, file_name="translated.html")

    ### Column 3: Reverse Translated Editor
    with col3:
        header_col, button_col = st.columns([3, 2])
        with header_col:
            st.subheader("🔁 Reverse Translated")
        with button_col:
            if st.button("Convert Back", key="reverse_btn"):
                if st.session_state.translated:
                    st.session_state.reversed = translator.reverse_translate_text(st.session_state.translated,
                                                                                  "English")
                    st.session_state.show_reversed = True

        if st.session_state.get("show_reversed", False):
            reversed_html = st_quill(
                placeholder=st.session_state.reversed,
                html=True,
                readonly=True,
            )
            st.write(reversed_html)
            if st.session_state.reversed:
                st.download_button("⬇️ Download Reversed", data=reversed_html, file_name="reversed.html")

    ### Summary Section
    st.markdown("---")
    if st.button("📋 Show Summary"):
        st.session_state.summary = translator.summarize_text(content)
        st.session_state.show_summary = True

    if st.session_state.get("show_summary", False):
        st.subheader("📝 Summary of Uploaded PDF")
        summary_html = st_quill(
            placeholder=st.session_state.summary,
            html=True,
            readonly=True,
        )
        st.write(summary_html)

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
