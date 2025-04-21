import fitz  # PyMuPDF

def extract_full_styled_html_with_divs(pdf_path, page_num=0):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    data = page.get_text("dict")

    # Detect underlines based on horizontal lines
    underline_y_coords = set()
    for block in data["blocks"]:
        if block["type"] == 4:  # Drawing
            for line in block.get("lines", []):
                if abs(line["p1"][1] - line["p2"][1]) < 1:  # horizontal
                    underline_y_coords.add(round(line["p1"][1]))

    html = '<div style="position:relative;">\n'

    for block in data["blocks"]:
        if block["type"] != 0:
            continue

        for line in block["lines"]:
            is_bullet = False
            bullet_text = ""
            for span in line["spans"]:
                text = span["text"].strip()
                if not text:
                    continue

                top = round(span["origin"][1], 2)
                left = round(span["origin"][0], 2)

                font = span.get("font", "").lower()
                size = round(span.get("size", 12), 2)
                color = "#{:06x}".format(span.get("color", 0))

                # Detect bullet
                if text in ("•", "-", "▪") or left < 50:
                    is_bullet = True
                    bullet_text += text + " "
                    continue

                style = f"position:absolute; top:{top}px; left:{left}px;"
                style += f" font-size:{size}px; color:{color};"
                if "bold" in font:
                    style += " font-weight:bold;"
                if "italic" in font:
                    style += " font-style:italic;"
                if round(top) in underline_y_coords:
                    style += " text-decoration:underline;"

                html += f"<div style='{style}'>{text}</div>\n"

            # If bullet detected, output bullet line
            if is_bullet:
                style = f"position:absolute; top:{top}px; left:{left}px;"
                html += f"<div style='{style}'><li>{bullet_text.strip()}</li></div>\n"

    html += "</div>"
    return html
