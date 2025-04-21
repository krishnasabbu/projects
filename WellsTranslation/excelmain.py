import streamlit as st
import pandas as pd
from langdetect import detect, DetectorFactory, LangDetectException
from llm_utils import LLMTranslator
from st_aggrid import AgGrid, GridOptionsBuilder

# Streamlit page setup
st.set_page_config(page_title="Excel Language Translator", layout="wide")
st.title("📊 Excel Language Translator with LLM")

DetectorFactory.seed = 0

API_KEY = "b69ffe06f2699f9bce616ac15a6c009585ebb822f58c5107f8549053609ef539"
LANGUAGE_MAP = {
    "en": "English", "de": "German", "es": "Spanish", "fr": "French",
    "zh-cn": "Chinese (Simplified)", "hi": "Hindi", "ja": "Japanese"
}
REVERSE_LANGUAGE_MAP = {v: k for k, v in LANGUAGE_MAP.items()}

@st.cache_resource
def get_translator():
    return LLMTranslator(api_key=API_KEY)

translator = get_translator()

@st.cache_data
def detect_language_cache(text):
    try:
        lang_code = detect(text)
        return lang_code, LANGUAGE_MAP.get(lang_code, f"Unknown ({lang_code})")
    except LangDetectException:
        return "unknown", "Could not detect"

def translate_dataframe(df, target_lang_code):
    translated_rows = []
    for index, row in df.iterrows():
        translated_row = [
            translator.translate_text(str(cell), target_lang_code) if pd.notnull(cell) else ""
            for cell in row
        ]
        translated_rows.append(translated_row)
    return pd.DataFrame(translated_rows, columns=df.columns)

def show_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=False)
    grid_options = gb.build()
    AgGrid(df, gridOptions=grid_options, height=400, theme="streamlit")

uploaded_file = st.file_uploader("📤 Upload your Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    text_sample = " ".join(df.astype(str).fillna("").values.flatten().tolist()[:20])
    lang_code, lang_name = detect_language_cache(text_sample)

    st.session_state.setdefault("translated_df", None)
    st.session_state.setdefault("reversed_df", None)
    st.session_state.setdefault("summary", "")
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("show_col3", False)
    st.session_state.setdefault("show_col5", False)

    target_options = [name for name in REVERSE_LANGUAGE_MAP if REVERSE_LANGUAGE_MAP[name] != lang_code]

    st.write("#### 🗣️ Language Detection & Selection")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Detected Source Language: **{lang_name}**")
    with col2:
        target_lang = st.radio("Choose Target Language:", target_options, horizontal=True)
        target_lang_code = REVERSE_LANGUAGE_MAP[target_lang]

    col1, col2, col3, col4, col5 = st.columns([3, 1, 3, 1, 3])

    with col1:
        st.markdown("##### 📊 Original Data")
        view_mode = st.radio("View Mode", ["Table", "AgGrid"], key="original_view")
        if view_mode == "Table":
            st.dataframe(df)
        else:
            show_aggrid(df)

    with col2:
        if st.button("➡️ Translate", key="to_col3"):
            st.session_state.translated_df = translate_dataframe(df, target_lang_code)
            st.session_state.show_col3 = True

    if st.session_state.show_col3:
        with col3:
            st.markdown("##### 🌐 Translated Data")
            view_mode = st.radio("View Mode", ["Table", "AgGrid"], key="translated_view")
            if view_mode == "Table":
                st.dataframe(st.session_state.translated_df)
            else:
                show_aggrid(st.session_state.translated_df)

    with col4:
        if st.button("➡️ Reverse Translate", key="to_col5"):
            if st.session_state.translated_df is not None:
                st.session_state.reversed_df = translate_dataframe(
                    st.session_state.translated_df, lang_code)
                st.session_state.show_col5 = True

    if st.session_state.show_col5:
        with col5:
            st.markdown("##### 🔁 Reversed Translation")
            view_mode = st.radio("View Mode", ["Table", "AgGrid"], key="reversed_view")
            if view_mode == "Table":
                st.dataframe(st.session_state.reversed_df)
            else:
                show_aggrid(st.session_state.reversed_df)

    st.markdown("---")

    # --- Summary Section ---
    st.markdown("### 📋 Summary")
    if st.button("📝 Generate Summary"):
        summary_text = "\n".join(df.astype(str).fillna("").values.flatten().tolist()[:100])
        st.session_state.summary = translator.summarize_text(summary_text)

    if st.session_state.summary:
        st.text_area("Summary", st.session_state.summary, height=200)

    st.markdown("---")

    # --- Chat Section ---
    st.markdown("### 💬 Ask About the Data")
    user_question = st.text_input("Ask a question:")
    if st.button("Ask"):
        if user_question.strip():
            full_text = "\n".join(df.astype(str).fillna("").values.flatten().tolist()[:200])
            response = translator.chat_with_pdf(full_text, user_question)
            st.session_state.chat_history.append(("🧑‍💻 You", user_question))
            st.session_state.chat_history.append(("🤖 LLM", response))

    for sender, msg in st.session_state.chat_history:
        st.markdown(f"**{sender}:** {msg}")
