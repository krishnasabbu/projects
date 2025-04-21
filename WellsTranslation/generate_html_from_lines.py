def generate_html_from_lines(lines):
    # Constants
    PAGE_WIDTH = 800
    MARGIN_LEFT = 96
    MARGIN_RIGHT = 96
    AVAILABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    CHAR_WIDTH = 8  # Assuming monospace font
    LINE_HEIGHT = 20

    # Start HTML document
    html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            width: 800px;
            height: 1120px; /* ~A4 ratio */
            margin: 0;
            font-family: monospace;
            position: relative;
        }
        .line {
            position: absolute;
            white-space: pre;
        }
    </style>
</head>
<body>
"""

    for idx, line in enumerate(lines):
        text_width = len(line) * CHAR_WIDTH
        if text_width < AVAILABLE_WIDTH:
            left = MARGIN_LEFT + (AVAILABLE_WIDTH - text_width) / 2
        else:
            left = MARGIN_LEFT
        top = idx * LINE_HEIGHT

        html += f'    <div class="line" style="top: {top}px; left: {left}px;">{line}</div>\n'

    html += """
</body>
</html>
"""
    return html
