import re

def clean_text(doc):
    lines = doc.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if re.search(r'Page\s*\d+', line, re.IGNORECASE):
            continue
        if re.search(r'\.{2,}\s*\d+$', line):
            continue
        if re.search(r'^\.*\s*\d+\s*$', line):
            continue
        cleaned_lines.append(line)

    doc = "\n".join(cleaned_lines)
    doc = re.sub(r'\n+', '\n', doc)
    doc = re.sub(r'[ \t]+', ' ', doc)
    return doc.strip()