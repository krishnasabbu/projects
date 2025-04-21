from bs4 import BeautifulSoup


def fit_html_to_one_page(input_html: str, page_height=1120, top_margin=100, bottom_margin=80, min_font_size=8):
    soup = BeautifulSoup(input_html, 'html.parser')

    # Constants
    available_height = page_height - top_margin - bottom_margin
    line_divs = soup.find_all('div', class_='line')

    # Step 1: Extract original positions and font size
    original_lines = []
    default_font_size = 16  # fallback
    for div in line_divs:
        style = div.get('style', '')
        top_str = next((s.split(':')[1].strip().replace('px', '') for s in style.split(';') if 'top' in s), None)
        font_str = next((s.split(':')[1].strip().replace('px', '') for s in style.split(';') if 'font-size' in s), None)

        if top_str is None:
            continue

        top = float(top_str)
        font_size = float(font_str) if font_str else default_font_size

        original_lines.append({
            'div': div,
            'text': div.text,
            'original_top': top,
            'font_size': font_size,
        })

    if not original_lines:
        raise ValueError("No lines found in the input HTML.")

    # Step 2: Compute total height based on current spacing
    tops = [line['original_top'] for line in original_lines]
    tops.sort()
    original_total_height = tops[-1] + default_font_size - tops[0]  # last line's bottom

    # Step 3: Scale if needed
    scale_factor = 1.0
    if original_total_height > available_height:
        scale_factor = available_height / original_total_height

    # Prevent font going too small
    scaled_font_size = max(min_font_size, original_lines[0]['font_size'] * scale_factor)
    font_scale = scaled_font_size / original_lines[0]['font_size']

    # Step 4: Adjust all `top` positions and font sizes
    for line in original_lines:
        new_top = top_margin + (line['original_top'] - tops[0]) * font_scale
        style = line['div'].get('style', '')

        # Update style with new top and font-size
        style_parts = style.split(';')
        new_style_parts = []
        for part in style_parts:
            if 'top' in part:
                new_style_parts.append(f'top: {new_top:.2f}px')
            elif 'font-size' in part:
                new_style_parts.append(f'font-size: {scaled_font_size:.2f}px')
            else:
                new_style_parts.append(part.strip())
        line['div']['style'] = '; '.join(filter(None, new_style_parts))

    # Step 5: Return updated HTML
    return str(soup)


# ======================
# Example usage:
# ======================
if __name__ == "__main__":
    with open("input.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    adjusted_html = fit_html_to_one_page(html_content)

    with open("output_fit.html", "w", encoding="utf-8") as f:
        f.write(adjusted_html)

    print("✅ HTML adjusted and written to output_fit.html")
