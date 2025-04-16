import streamlit as st
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Translation Confidence Checker", layout="wide")
st.title("🧠 Translation Confidence Score")


# st.set_page_config(page_title="Excel Visualize!!!", page_icon=":bar_chart:", layout="wide")
#
# st.title(" :bar_chart: Sample Excel Store")
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

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
