import os
import re

# Simple TeX parser to extract items
def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace common transcribed double curly brace typos
    content = content.replace(r'\end{{parts}}', r'\end{parts}')
    content = content.replace(r'\begin{{parts}}', r'\begin{parts}')
    
    # Remove comments
    content = re.sub(r'(?m)^%.*$', '', content)
    
    doc_start = content.find(r'\begin{document}')
    idx = 0
    if doc_start != -1:
        idx = doc_start + len(r'\begin{document}')
    
    subcontent = content[idx:]
    pattern = r'(\\begin\{parts\}|\\end\{parts\}|\\item)'
    tokens = re.split(pattern, subcontent)
    
    stack = []
    current_items = []
    all_questions = []
    
    def clean_text(text):
        text = text.replace(r'\"{o}', 'ö')
        text = text.replace(r'\'e', 'é')
        text = text.replace(r'\"{a}', 'ä')
        text = text.replace(r'\"o', 'ö')
        
        # Remove \pts{...}
        text = re.sub(r'\\pts\{[^\}]*\}', '', text)
        # Remove \hfill, \smallskip, \mediumskip, etc.
        text = re.sub(r'\\hfill', '', text)
        text = re.sub(r'\\s*\\(small|me|big)skip', '', text)
        text = re.sub(r'\\noindent', '', text)
        text = re.sub(r'\\rule\{[^\}]*\}\{[^\}]*\}', '', text)
        text = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\textit\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\emph\{([^\}]*)\}', r'\1', text)
        text = text.replace('~', ' ')
        text = re.sub(r'\\\\(?:\[[^\]]*\])?', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

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

# Scan and count
files = [f for f in os.listdir('aaa/chemistry/tex_files') if f.endswith('.tex')]
files.sort()

grouped = {}
for f in files:
    if f.startswith('test_'):
        continue
    prefix = f.split('_')[0]
    filepath = os.path.join('aaa/chemistry/tex_files', f)
    qs = parse_tex_file(filepath)
    if prefix not in grouped:
        grouped[prefix] = []
    grouped[prefix].extend(qs)
    print(f"File: {f} -> Extracted {len(qs)} questions")

print("\n=== SUMMARY BY PREFIX ===")
for prefix, qs in sorted(grouped.items()):
    # unique questions
    seen = set()
    uniq_qs = []
    for q in qs:
        norm = q.lower().strip()
        if norm not in seen:
            seen.add(norm)
            uniq_qs.append(q)
    print(f"Prefix: {prefix} | Total: {len(qs)} | Unique: {len(uniq_qs)}")
