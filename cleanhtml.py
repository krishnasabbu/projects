import re

# Collapse multiple spaces
html_cleaned = re.sub(r'\s{2,}', ' ', html_output)

# Remove spaces between HTML tags (e.g., <b> text </b>)
html_cleaned = re.sub(r'>\s+<', '><', html_cleaned)

# Optional: Remove leading/trailing spaces inside tags
html_cleaned = re.sub(r'>([^<]+)<', lambda m: f'>{m.group(1).strip()}<', html_cleaned)

print(html_cleaned)