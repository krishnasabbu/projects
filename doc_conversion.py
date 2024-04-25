import fitz
import cv2
import numpy as np


# Function to convert pixmap to grayscale
def convert_to_grayscale(pixmap):
    # Convert the pixmap to numpy array
    np_image = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape((pixmap.height, pixmap.width, pixmap.n))

    # Convert to grayscale using OpenCV
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)

    return gray_image


# Open the PDF file
pdf_file = 'D:\\python\\docReading\\passport.pdf'
doc = fitz.open(pdf_file)

# Iterate through each page
for page_num in range(len(doc)):
    # Get the page
    page = doc.load_page(page_num)

    # Get pixmap of the page
    pixmap = page.get_pixmap()

    # Convert pixmap to grayscale
    gray_image = convert_to_grayscale(pixmap)

    # Save the grayscale image
    image_path = f'page_{page_num + 1}_grayscale.png'
    cv2.imwrite(image_path, gray_image)

    print(f"Screenshot of page {page_num + 1} converted to grayscale saved as {image_path}")

# Close the document
doc.close()
