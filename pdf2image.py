import asyncio
import os
from pyppeteer import launch

# Step 1: Simulated input HTML
original_html = """
<p><b>Original Title</b></p>
<p>This is the first paragraph<br>This is line 2</p>
"""

# Step 2: Simulated LLM "translation"
def call_custom_llm(html_b64_or_text):
    return """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }
            p {
                font-size: 14pt;
            }
            b {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <p><b>Page 1 Title</b></p>
        <p>This is content for page 1.</p>

        <div style="page-break-after: always;"></div>

        <p><b>Page 2 Title</b></p>
        <p>This is content for page 2.</p>

        <div style="page-break-after: always;"></div>

        <p><b>Page 3 Title</b></p>
        <p>This is content for page 3.</p>
    </body>
    </html>
    """

# Step 3: Save HTML to a file (optional)
def save_html_to_file(html_content, html_path="translated_output.html"):
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return html_path

# Step 4: Convert HTML to PDF using pyppeteer
async def html_to_pdf_pyppeteer(html_content: str, pdf_output_path: str, use_file: bool = False, chrome_path: str = None):
    launch_args = {"headless": True, "args": ["--no-sandbox"]}
    if chrome_path:
        launch_args["executablePath"] = chrome_path

    browser = await launch(**launch_args)
    page = await browser.newPage()

    if use_file:
        html_path = save_html_to_file(html_content)
        abs_path = os.path.abspath(html_path)
        await page.goto(f"file:///{abs_path}")
    else:
        await page.setContent(html_content)

    await page.pdf({
        'path': pdf_output_path,
        'format': 'A4',
        'margin': {'top': '40px', 'right': '40px', 'bottom': '40px', 'left': '40px'},
        'printBackground': True
    })

    await browser.close()

# === Run the full flow ===
translated_html = call_custom_llm(original_html)

use_file_rendering = False  # Change to True if you want to render from saved file
custom_chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Replace or set to None

asyncio.get_event_loop().run_until_complete(
    html_to_pdf_pyppeteer(translated_html, "translated_output.pdf", use_file_rendering, custom_chrome_path)
)

print("✅ PDF generated using pyppeteer!")

import re

def fix_top_styles(html):
    # Match inline style attributes
    def replacer(match):
        style_content = match.group(1)
        if "top" in style_content and "position:absolute" not in style_content:
            # Insert position:absolute before top:NNpx
            updated = re.sub(r'\btop\s*:', r'position:absolute;top:', style_content)
            return f'style="{updated}"'
        return match.group(0)

    return re.sub(r'style="(.*?)"', replacer, html, flags=re.IGNORECASE | re.DOTALL)

