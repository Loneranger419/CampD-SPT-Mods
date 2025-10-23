# compile_html.py
import os, re

# Config
html_file = "index.html"
css_file = "style.css"
js_file = "script.js"
output_dir = "build"

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Ask for a name
output_name = input("Enter name for compiled file (e.g. combined.html): ")
output_path = os.path.join(output_dir, output_name)

# Read files
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()
with open(css_file, "r", encoding="utf-8") as f:
    css_content = f.read()
with open(js_file, "r", encoding="utf-8") as f:
    js_content = f.read()

# Clean up old includes
html_content = re.sub(r'<link.*?href=".*?style\.css".*?>', '', html_content)
html_content = re.sub(r'<script.*?src=".*?script\.js".*?>\s*</script>', '', html_content)

# Inject inline CSS and JS
compiled = html_content.replace(
    "</head>", f"<style>\n{css_content}\n</style>\n</head>"
).replace(
    "</body>", f"<script>\n{js_content}\n</script>\n</body>"
)

# Write to ignored build folder
with open(output_path, "w", encoding="utf-8") as f:
    f.write(compiled)

print(f"✅ Compiled file created: {output_path}")