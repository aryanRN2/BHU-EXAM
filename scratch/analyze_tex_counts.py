import os
import re

def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
subjects_questions = {}
tex_files = [f for f in os.listdir('aaa/PHYSICS OUT') if f.endswith('.tex')]

for file_name in tex_files:
    code = file_name.split("_")[0]
    
    key = None
    if code.startswith("BPT-101") or code.startswith("BSCU7A"):
        key = "phymj11"
    elif code.startswith("BPT-201") or code.startswith("BP-Anc-I"):
        key = "phymj21"
    elif code.startswith("BPT-301"):
        key = "phymj31"
    elif code.startswith("BPT-401") and "Electromagnetic" in file_name:
        key = "phymj41"
    elif code.startswith("BPT-401") and "Electronics" in file_name:
        key = "phymj61"
    elif code.startswith("BPT-501"):
        key = "phymj42"
    elif code.startswith("BPT-502"):
        key = "phymj52"
    elif code.startswith("BPT-503"):
        key = "phymj51"
    elif code.startswith("BPT-504"):
        key = "phymj32"
    elif code.startswith("BPT-505"):
        key = "phymj41"
    elif code.startswith("BPT-601"):
        key = "phymj53"
    elif code.startswith("BPT-602"):
        key = "phymj62"
    elif code.startswith("BPT-603"):
        key = "phymj64"
    elif code.startswith("BPT-604") or code.startswith("BPE-601"):
        key = "phymj63"
    elif code.startswith("BPE-602"):
        key = "phymj75"
    elif code.startswith("BSC-07A") or code == "PHYSICS":
        key = "phymj41"
        
    if not key:
        continue
        
    if key not in subjects_questions:
        subjects_questions[key] = []
        
    qs = parse_tex_file(os.path.join('aaa/PHYSICS OUT', file_name))
    subjects_questions[key].extend(qs)

for k, qs in sorted(subjects_questions.items()):
    # Remove duplicates
    unique_qs = list(dict.fromkeys(qs))
    print(f"{k}: {len(unique_qs)} unique questions (out of {len(qs)} total)")
