import re

def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
        # Remove \pts{...}
        text = re.sub(r'\\pts\{[^\}]*\}', '', text)
        # Remove \hfill, \smallskip, \mediumskip, etc.
        text = re.sub(r'\\hfill', '', text)
        text = re.sub(r'\\s*\\(small|me|big)skip', '', text)
        text = re.sub(r'\\noindent', '', text)
        text = re.sub(r'\\rule\{[^\}]*\}\{[^\}]*\}', '', text)
        # Replace LaTeX text formatting (only if NOT inside math mode to be safe,
        # but standard text replacement works if we target only \textbf, \textit outside math or be careful)
        # Let's replace text commands that are not inside math, or do a general regex that avoids math.
        # Actually, \textbf, \textit, \emph are rarely used inside math, and even if they are, MathJax supports them.
        # Let's replace them if they are in text. A simple regex:
        text = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\textit\{([^\}]*)\}', r'\1', text)
        text = re.sub(r'\\emph\{([^\}]*)\}', r'\1', text)
        # Note: We do NOT replace \text{...} anymore, preserving units!
        
        # Replace non-breaking space
        text = text.replace('~', ' ')
        # Replace double backslashes with spaces
        text = re.sub(r'\\\\(?:\[[^\]]*\])?', ' ', text)
        # Normalize whitespace
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
                    # Nested parts: merge into parent's last item
                    last_parent = parent_items[-1]
                    sub_text = " " + " ".join(f"({idx+1}) {clean_text(item)}" for idx, item in enumerate(current_items))
                    parent_items[-1] = last_parent + sub_text
                    current_items = parent_items
                else:
                    # Top-level parts: collect questions
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
                
    # Collect any leftovers
    for item in current_items:
        cleaned = clean_text(item)
        if len(cleaned) > 15:
            all_questions.append(cleaned)
            
    return all_questions

# Test on one file
qs = parse_tex_file("aaa/PHYSICS OUT/BPT-101_MechanicsandRelativity_SemI_2022-23.tex")
print(f"Extracted {len(qs)} questions:")
for i, q in enumerate(qs):
    print(f"Q{i+1}: {q}")
