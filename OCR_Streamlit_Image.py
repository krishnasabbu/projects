import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import json
import io
import re
import warnings
from pdf2image import convert_from_bytes
import pytesseract

warnings.filterwarnings('ignore')

st.set_page_config(page_title="PDF Reading!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Sample Doc Reading")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


def clean_text(text):
    # Find the index of the '\n' character
    newline_index = text.find('\n')

    # Keep only the part before the '\n' character
    cleaned_text = text[:newline_index] if newline_index != -1 else text

    return cleaned_text


# Function to extract information from text
def extract_information(text):
    # Regular expressions to extract fields
    received_date_pattern = r'Received Date\s*([\d/]+)'
    priority_date_pattern = r'Priority Date\s*([\d/]+)'
    notice_date_pattern = r'Notice Date\s*([\d/]+)'
    notice_type_pattern = r'SEX:\s*([\w\s]+)'
    class_pattern = r'Class:\s*([\w\d]+)'
    valid_from_to_pattern = r'Valid from\s*([\d/]+)\s*to\s*([\d/]+)'

    # Extracting fields using regular expressions
    received_date_match = re.search(received_date_pattern, text)
    priority_date_match = re.search(priority_date_pattern, text)
    notice_date_match = re.search(notice_date_pattern, text)
    notice_type_match = re.search(notice_type_pattern, text)
    class_match = re.search(class_pattern, text)
    valid_from_to_match = re.search(valid_from_to_pattern, text)

    # Storing extracted values
    extracted_fields = {}
    if received_date_match:
        extracted_fields['Received Date'] = clean_text(received_date_match.group(1))
    if priority_date_match:
        extracted_fields['Priority Date'] = clean_text(priority_date_match.group(1))
    if notice_date_match:
        extracted_fields['Notice Date'] = clean_text(notice_date_match.group(1))
    if notice_type_match:
        extracted_fields['Notice Type'] = clean_text(notice_type_match.group(1).strip())
    if class_match:
        extracted_fields['Class'] = clean_text(class_match.group(1))
    if valid_from_to_match:
        extracted_fields['Valid from'] = clean_text(valid_from_to_match.group(1))
        extracted_fields['Valid to'] = clean_text(valid_from_to_match.group(2))

    return extracted_fields


# Function to perform OCR on an image
def ocr_image(image):
    return pytesseract.image_to_string(image)


# Main Streamlit app
def main():
    st.title("PDF Document Text Extraction")

    # File uploader for PDF documents
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    text = ''

    if uploaded_file is not None:
        pages = convert_from_bytes(uploaded_file.read())

        for i, page in enumerate(pages):
            text += pytesseract.image_to_string(page)

        st.write(text)


if __name__ == "__main__":
    main()
