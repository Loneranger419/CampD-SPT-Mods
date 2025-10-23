# compile_html.py
import os

# Input files
html_file = "index.html"
css_file = "style.css"
js_file = "script.js"

# Output file name
output_name = input("Enter name for compiled file (e.g. combined.html): ")

# Read the HTML, CSS, and JS
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()
with open(css_file, "r", encoding="utf-8") as f:
    css_content = f.read()
with open(js_file, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace or insert tags
# Removes any <link rel="stylesheet"> and <script src=""> lines
import re
html_content = re.sub(r'<link.*?href=".*?style\.css".*?>', '', html_content)
html_content = re.sub(r'<script.*?src=".*?script\.js".*?>\s*</script>', '', html_content)

# Insert CSS and JS directly
compiled = html_content.replace(
    "</head>", f"<style>\n{css_content}\n</style>\n</head>"
).replace(
    "</body>", f"<script>\n{js_content}\n</script>\n</body>"
)

# Write to new file
with open(output_name, "w", encoding="utf-8") as f:
    f.write(compiled)

print(f"✅ Compiled file created: {output_name}")