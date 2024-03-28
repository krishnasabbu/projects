import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import json
import io
import re
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="PDF Reading!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Sample Doc Reading")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# Function to extract information from text
def extract_information(text):
    # Regular expressions to extract fields
    received_date_pattern = r'Received Date\s*([\d/]+)'
    priority_date_pattern = r'Priority Date\s*([\d/]+)'
    notice_date_pattern = r'Notice Date\s*([\d/]+)'
    notice_type_pattern = r'Notice Type:\s*([\w\s]+)'
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
        extracted_fields['Received Date'] = received_date_match.group(1)
    if priority_date_match:
        extracted_fields['Priority Date'] = priority_date_match.group(1)
    if notice_date_match:
        extracted_fields['Notice Date'] = notice_date_match.group(1)
    if notice_type_match:
        extracted_fields['Notice Type'] = notice_type_match.group(1).strip()
    if class_match:
        extracted_fields['Class'] = class_match.group(1)
    if valid_from_to_match:
        extracted_fields['Valid from'] = valid_from_to_match.group(1)
        extracted_fields['Valid to'] = valid_from_to_match.group(2)

    return extracted_fields


# Function to perform OCR on an image
def ocr_image(image):
    return pytesseract.image_to_string(image)


# Main Streamlit app
def main():
    st.title("PDF Document Text Extraction")

    # File uploader for PDF documents
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    if uploaded_file is not None:
        pdf_document = fitz.open(stream=io.BytesIO(uploaded_file.read()))

        # Iterate through each page of the PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)

            # Iterate through each image on the page
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]

                # Perform OCR on the extracted image
                extracted_text = ocr_image(Image.open(io.BytesIO(image_bytes)))

                # Extract information from the provided text
                total_information = extract_information(extracted_text)

                # Display Excel Sheet and Filtered DataFrame
                col1, col2 = st.columns(2)
                with col1:
                    # Display extracted information
                    st.subheader("Extracted Information:")
                    st.json(total_information)
                with col2:
                    st.subheader("Original Text:")
                    st.text(extracted_text)

        # Close the PDF document
        pdf_document.close()


if __name__ == "__main__":
    main()
