from PIL import Image, ImageDraw, ImageFont
from xhtml2pdf import pisa
import base64
from io import BytesIO
import re

# Step 1: Convert HTML to plain formatted image
def html_to_image(html: str, image_file="html_render.png"):
    # Very basic tag parsing: supports <p>, <br>, <b>
    html = html.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    paragraphs = re.findall(r"<p>(.*?)</p>", html, re.DOTALL)

    # Font setup (use built-in fonts)
    font = ImageFont.load_default()
    width, height = 800, 1000
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)

    y = 20
    for para in paragraphs:
        # Bold handling
        bold_parts = re.split(r"(<b>.*?</b>)", para)
        for part in bold_parts:
            if part.startswith("<b>") and part.endswith("</b>"):
                text = part[3:-4]
                draw.text((20, y), text, fill="black", font=font)  # optionally load bold font
            else:
                draw.text((20, y), part, fill="black", font=font)
            y += 20

        y += 10  # space between paragraphs

    image.save(image_file)
    return image_file

# Step 2: Convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return encoded

# Step 3: Simulated LLM response
def call_custom_llm(image_b64):
    translated_html = """
    <p><b>Título traducido</b></p>
    <p>Este es un párrafo traducido<br>con otra línea.</p>
    """
    return translated_html

# Step 4: HTML to PDF
def html_to_pdf(html_content, output_file="output_translated.pdf"):
    with open(output_file, "wb") as result_file:
        pisa.CreatePDF(html_content, dest=result_file)

# === Run it all ===

html_content = """
<p><b>Original Title</b></p>
<p>This is the first paragraph<br>This is line 2</p>
"""

image_path = html_to_image(html_content)
b64_img = image_to_base64(image_path)

translated_html = call_custom_llm(b64_img)

html_to_pdf(translated_html)
print("✅ PDF created with translated content.")
