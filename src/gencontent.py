import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    md = f.read()
    f = open(template_path)
    template = f.read()
    node = markdown_to_html_node(md)
    html = node.to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", f"{title}")
    full_html = template.replace("{{ Content }}", f"{html}")
    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(full_html)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            header = line[1:].strip()
            return header
    raise ValueError("no title found")