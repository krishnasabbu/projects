def generate_html_from_lines(lines):
    # Constants
    PAGE_WIDTH = 800
    PAGE_HEIGHT = 1120  # ~A4 size in pixels
    MARGIN_LEFT = 96
    MARGIN_RIGHT = 96
    MARGIN_TOP = 100
    LINE_HEIGHT = 20
    CHAR_WIDTH = 8  # Monospace

    AVAILABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    AVAILABLE_HEIGHT = PAGE_HEIGHT - MARGIN_TOP
    MAX_LINES = AVAILABLE_HEIGHT // LINE_HEIGHT

    # Clip lines if they exceed page height
    if len(lines) > MAX_LINES:
        print(f"⚠️ Warning: Too many lines for one page. Only first {MAX_LINES} will be rendered.")
        lines = lines[:MAX_LINES]

    # Start HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            width: {PAGE_WIDTH}px;
            height: {PAGE_HEIGHT}px;
            margin: 0;
            font-family: monospace;
            position: relative;
        }}
        .line {{
            position: absolute;
            white-space: pre;
        }}
    </style>
</head>
<body>
"""

    for idx, line in enumerate(lines):
        text_width = len(line) * CHAR_WIDTH
        left = MARGIN_LEFT + (AVAILABLE_WIDTH - text_width) / 2 if text_width < AVAILABLE_WIDTH else MARGIN_LEFT
        top = MARGIN_TOP + idx * LINE_HEIGHT
        html += f'    <div class="line" style="top: {top}px; left: {left}px;">{line}</div>\n'

    html += """
</body>
</html>
"""
    return html



actual_lines = [
    "Centered Title",
    "Another line",
    "This is a full-width line meant to test left alignment in the HTML layout.",
    "Short again",
    *["Line " + str(i) for i in range(50)]  # Test multiple lines
]

html_output = generate_html_from_lines(actual_lines)

with open("output.html", "w") as f:
    f.write(html_output)
