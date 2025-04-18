async def html_to_pdf(html_content, output_path, watermark_text="CONFIDENTIAL"):
    # Add watermark to the HTML content
    watermarked_html = f"""
    <html>
        <head>
            <style>
                body {{
                    position: relative;
                }}
                .watermark {{
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) rotate(-45deg);
                    font-size: 48px;
                    color: rgba(128, 128, 128, 0.3); /* Semi-transparent gray */
                    z-index: 1000;
                    pointer-events: none; /* Ensure the watermark doesn't interfere with interactions */
                }}
            </style>
        </head>
        <body>
            <div class="watermark">{watermark_text}</div>
            {html_content}
        </body>
    </html>
    """

    # Launch the browser and generate the PDF
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.setContent(watermarked_html, waitUntil='networkidle0')
    await page.pdf({'path': output_path, 'format': 'A4'})
    await browser.close()
