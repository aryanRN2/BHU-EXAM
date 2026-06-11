import os
import re

# Same parser as populate_chemistry.py
def clean_text(text):
    text = text.replace(r'\"{o}', 'ö')
    text = text.replace(r'\'e', 'é')
    text = text.replace(r'\"{a}', 'ä')
    text = text.replace(r'\"o', 'ö')
    text = text.replace(r'\'erot', 'érot')
    text = re.sub(r'\\pts\{[^\}]*\}', '', text)
    text = re.sub(r'\\hfill', '', text)
    text = re.sub(r'\\s*\\(small|me|big)skip', '', text)
    text = re.sub(r'\\noindent', '', text)
    text = re.sub(r'\\rule\{[^\}]*\}\{[^\}]*\}', '', text)
    text = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^\}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^\}]*)\}', r'\1', text)
    text = text.replace('~', ' ')
    text = re.sub(r'\\\\(?:\[[^\]]*\])?', ' ', text)
    text = text.replace(r'\[', '$')
    text = text.replace(r'\]', '$')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_tex_content(subcontent):
    doc_start = subcontent.find(r'\begin{document}')
    if doc_start != -1:
        subcontent = subcontent[doc_start + len(r'\begin{document}'):]
    pattern = r'(\\begin\{parts\}|\\end\{parts\}|\\item)'
    tokens = re.split(pattern, subcontent)
    stack = []
    current_items = []
    all_questions = []
    for token in tokens:
        if not token:
            continue
        token_strip = token.strip()
        if token_strip == r'\begin{parts}':
            stack.append(current_items)
            current_items = []
        elif token_strip == r'\end{parts}':
            if stack:
                parent_items = stack.pop()
                if parent_items:
                    last_parent = parent_items[-1]
                    sub_text = " " + " ".join(f"({idx+1}) {clean_text(item)}" for idx, item in enumerate(current_items))
                    parent_items[-1] = last_parent + sub_text
                    current_items = parent_items
                else:
                    for item in current_items:
                        cleaned = clean_text(item)
                        if len(cleaned) > 15:
                            all_questions.append(cleaned)
                    current_items = []
        elif token_strip == r'\item':
            current_items.append("")
        else:
            if current_items:
                current_items[-1] += " " + token
    for item in current_items:
        cleaned = clean_text(item)
        if len(cleaned) > 15:
            all_questions.append(cleaned)
    return all_questions

tex_dir = 'aaa/chemistry/tex_files'
files = [f for f in os.listdir(tex_dir) if f.endswith('.tex') and not f.startswith('test_')]
files.sort()

counts = {}
for file_name in files:
    filepath = os.path.join(tex_dir, file_name)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    code = file_name.split("_")[0]
    qs = parse_tex_content(content)
    counts[code] = counts.get(code, 0) + len(qs)

print("Parsed question counts by code prefix:")
for c, count in sorted(counts.items()):
    print(f"  {c}: {count} questions")
