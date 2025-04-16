
import streamlit as st
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import difflib
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Translation Confidence Checker", layout="wide")
st.title("🧠 Translation Confidence Score")

# ---------- Utils ----------
def extract_html_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    html_text = ""
    for page in doc:
        html_text += page.get_text("html")
    return html_text

def extract_visible_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def compute_bleu(reference, hypothesis):
    smoothie = SmoothingFunction().method4
    return sentence_bleu([reference.split()], hypothesis.split(), smoothing_function=smoothie)

def compute_rouge(reference, hypothesis):
    rouge = Rouge()
    return rouge.get_scores(hypothesis, reference)[0]

def compute_cosine(reference, hypothesis):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([reference, hypothesis])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

def plot_scores(scores):
    labels = list(scores.keys())
    values = list(scores.values())

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color='skyblue')
    ax.set_ylim(0, 1)
    ax.set_title("Translation Confidence Metrics")
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
    return fig

def display_side_by_side_diff(manual, llm):
    manual_lines = manual.splitlines()
    llm_lines = llm.splitlines()
    max_len = max(len(manual_lines), len(llm_lines))

    rows = []
    for i in range(max_len):
        manual_line = manual_lines[i] if i < len(manual_lines) else ""
        llm_line = llm_lines[i] if i < len(llm_lines) else ""
        is_diff = manual_line.strip() != llm_line.strip()
        rows.append({
            "Manual Translation": manual_line,
            "LLM Translation": llm_line,
            "Mismatch?": "❌" if is_diff else "✅"
        })

    df = pd.DataFrame(rows)
    st.write("### 🧾 Side-by-Side Comparison")
    st.dataframe(df, use_container_width=True)

# ---------- Streamlit App ----------
col1, col2 = st.columns(2)
with col1:
    llm_pdf = st.file_uploader("Upload LLM-Translated PDF", type="pdf", key="llm")
with col2:
    manual_pdf = st.file_uploader("Upload Manually Translated PDF", type="pdf", key="manual")

if llm_pdf and manual_pdf:
    st.subheader("📄 Extracting and Comparing Translations...")

    llm_html = extract_html_from_pdf(llm_pdf)
    manual_html = extract_html_from_pdf(manual_pdf)

    llm_text = extract_visible_text(llm_html)
    manual_text = extract_visible_text(manual_html)

    # Display Side-by-Side Differences
    display_side_by_side_diff(manual_text, llm_text)

    # Compute metrics
    bleu = compute_bleu(manual_text, llm_text)
    rouge = compute_rouge(manual_text, llm_text)
    cosine = compute_cosine(manual_text, llm_text)

    scores = {
        "BLEU": bleu,
        "ROUGE-L": rouge['rouge-l']['f'],
        "Cosine": cosine
    }

    st.success("✅ Comparison Complete!")

    # Show confidence scores
    st.write("### 📊 Confidence Scores:")
    for k, v in scores.items():
        st.write(f"- **{k}**: {v:.4f}")

    # Show bar chart
    st.pyplot(plot_scores(scores))

else:
    st.info("Please upload both LLM-translated and manually-translated PDF files to begin.")
