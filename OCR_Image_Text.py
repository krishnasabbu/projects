from pdf2image import convert_from_path
import pytesseract

pdf_path = 'D:\\python\\docReading\\document.pdf'

pages = convert_from_path(pdf_path)

for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page)

    print(text)

