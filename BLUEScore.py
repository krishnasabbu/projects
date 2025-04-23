import streamlit as st
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from docx import Document

def compute_bleu(source_text, destination_text):
    reference = [source_text.split()]
    candidate = destination_text.split()
    smoothie = SmoothingFunction().method4
    return sentence_bleu(reference, candidate, smoothing_function=smoothie)

def read_docx_file(file):
    try:
        doc = Document(file)
        full_text = '\n'.join([para.text for para in doc.paragraphs])
        return full_text.strip()
    except Exception as e:
        return ""

st.title("Compare Word Documents - BLEU Score")

st.header("Upload Source Word Files (.docx)")
source_files = st.file_uploader("Upload source Word files", type=['docx'], accept_multiple_files=True)

st.header("Upload Destination Word Files (.docx)")
destination_files = st.file_uploader("Upload destination Word files", type=['docx'], accept_multiple_files=True)

if source_files and destination_files and st.button("Compare"):
    # Sort files by name
    source_files_sorted = sorted(source_files, key=lambda f: f.name)
    destination_files_sorted = sorted(destination_files, key=lambda f: f.name)

    min_len = min(len(source_files_sorted), len(destination_files_sorted))
    results = []

    for i in range(min_len):
        src_file = source_files_sorted[i]
        dst_file = destination_files_sorted[i]

        src_text = read_docx_file(src_file)
        dst_text = read_docx_file(dst_file)

        bleu = compute_bleu(src_text, dst_text)
        results.append([src_file.name, dst_file.name, bleu])

    df = pd.DataFrame(results, columns=["source", "destination", "BLEU score"])
    st.dataframe(df)
