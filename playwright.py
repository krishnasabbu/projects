from playwright.sync_api import sync_playwright
import os

# Step 1: Simulated input HTML
original_html = """
<p><b>Original Title</b></p>
<p>This is the first paragraph<br>This is line 2</p>
"""

# Step 2: Simulated LLM call that "translates" the content
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

# Step 3: Optional – Save HTML to file
def save_html_to_file(html_content, html_path="translated_output.html"):
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return html_path

# Step 4: Convert HTML to PDF using Playwright (supports direct HTML or file path)
def html_to_pdf_playwright(html_content: str, pdf_output_path: str, use_file: bool = False, chrome_path: str = None):
    with sync_playwright() as p:
        launch_args = {
            "headless": True,
            "args": ["--no-sandbox"]
        }

        if chrome_path:
            launch_args["executable_path"] = chrome_path

        browser = p.chromium.launch(**launch_args)
        page = browser.new_page()

        if use_file:
            abs_path = os.path.abspath(save_html_to_file(html_content))
            page.goto(f"file://{abs_path}")
        else:
            page.set_content(html_content, wait_until="load")

        page.pdf(
            path=pdf_output_path,
            format="A4",
            margin={"top": "40px", "left": "40px", "right": "40px", "bottom": "40px"},
            print_background=True
        )

        browser.close()


# === Run the flow ===

translated_html = call_custom_llm(original_html)

# Optional: If you want to test using saved file instead of direct HTML
use_file_rendering = False

# Optional: Set your custom Chrome path here if needed (e.g., company machine)
custom_chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # or None

# Generate PDF
html_to_pdf_playwright(
    html_content=translated_html,
    pdf_output_path="translated_output.pdf",
    use_file=use_file_rendering,
    chrome_path=custom_chrome_path
)

print("✅ PDF generated using Playwright!")
