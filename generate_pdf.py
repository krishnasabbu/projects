# generate_pdf.py
import asyncio
from pyppeteer import launch
import sys

html = sys.argv[1]
output_path = sys.argv[2]


async def html_to_pdf(html, output_path):
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    launch_args = {"headless": True, "args": ["--no-sandbox"], "executablePath": chrome_path}

    browser = await launch(**launch_args)
    page = await browser.newPage()
    await page.setContent(html)
    await page.pdf({'path': output_path, 'format': 'A4'})
    await browser.close()


asyncio.get_event_loop().run_until_complete(html_to_pdf(html, output_path))
