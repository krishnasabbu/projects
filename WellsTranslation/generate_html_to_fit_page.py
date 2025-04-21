def generate_html_fit_to_page(lines):
    # A4 Page setup
    PAGE_WIDTH = 800
    PAGE_HEIGHT = 1120
    MARGIN_LEFT = 96
    MARGIN_RIGHT = 96
    MARGIN_TOP = 100
    MARGIN_BOTTOM = 80
    CHAR_WIDTH = 8  # For monospace font
    AVAILABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    AVAILABLE_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

    DEFAULT_FONT_SIZE = 16
    LINE_HEIGHT_FACTOR = 1.2  # Line height relative to font size

    # Estimate height needed with default font size
    total_height = 0
    line_heights = []
    for line in lines:
        num_chars = len(line)
        est_lines = max(1, (num_chars * CHAR_WIDTH) // AVAILABLE_WIDTH)
        line_height = DEFAULT_FONT_SIZE * LINE_HEIGHT_FACTOR * est_lines
        line_heights.append(line_height)
        total_height += line_height

    # Adjust font size if total height exceeds page
    if total_height > AVAILABLE_HEIGHT:
        scale_factor = AVAILABLE_HEIGHT / total_height
        font_size = DEFAULT_FONT_SIZE * scale_factor
    else:
        font_size = DEFAULT_FONT_SIZE

    # Recalculate line heights with new font size
    top = MARGIN_TOP
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
            white-space: pre-wrap;
            width: {AVAILABLE_WIDTH}px;
            font-size: {font_size}px;
            line-height: {LINE_HEIGHT_FACTOR};
        }}
    </style>
</head>
<body>
"""

    for i, line in enumerate(lines):
        num_chars = len(line)
        est_lines = max(1, (num_chars * CHAR_WIDTH) // AVAILABLE_WIDTH)
        line_block_height = font_size * LINE_HEIGHT_FACTOR * est_lines

        html += f'<div class="line" style="top: {top}px; left: {MARGIN_LEFT}px;">{line}</div>\n'
        top += line_block_height

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

html_output = generate_html_fit_to_page(actual_lines)

with open("output.html", "w") as f:
    f.write(html_output)