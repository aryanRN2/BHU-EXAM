import os
import re

math_dir = "aaa/latest corrected maths pdf/final maths export latex"
files = [f for f in os.listdir(math_dir) if f.endswith(".tex")]

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
    text = text.replace(r'\[', '$').replace(r'\]', '$')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(r'\end{{parts}}', r'\end{parts}')
    content = content.replace(r'\begin{{parts}}', r'\begin{parts}')
    content = re.sub(r'(?m)^%.*$', '', content)
    
    doc_start = content.find(r'\begin{document}')
    idx = doc_start + len(r'\begin{document}') if doc_start != -1 else 0
    subcontent = content[idx:]
    
    tokens = re.split(r'(\\begin\{parts\}|\\end\{parts\}|\\item)', subcontent)
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

# Active keys mapping
def get_course_keys(file_name, content):
    name_upper = file_name.upper()
    
    # Try to parse code from content or name
    code = "Unknown"
    comment_match = re.search(r'%\s*Paper:\s*(MTB-[A-Z0-9-]+)', content, re.IGNORECASE)
    if comment_match:
        code = comment_match.group(1).strip().upper()
    else:
        pdf_match = re.search(r'pdftitle\s*=\s*\{\s*(MTB-[A-Z0-9-]+)', content, re.IGNORECASE)
        if pdf_match:
            code = pdf_match.group(1).strip().upper()
        else:
            code_match = re.search(r'MTB-[A-Z0-9-]+', content)
            if code_match:
                code = code_match.group(0).upper()
            else:
                code_match = re.search(r'MTB-[A-Z0-9-]+', name_upper)
                if code_match:
                    code = code_match.group(0).upper()
    
    if "MTB-101" in code:
        return ["matmj11", "matmn11"]
    elif "MTB-102" in code:
        return ["matmj53"]
    elif "MTB-201" in code:
        if "CALCULUS-III" in name_upper or "CALCULUS-II" in name_upper or "CALCULUS II" in name_upper:
            return ["matmj41"]
        return ["matmj11"]
    elif "MTB-202" in code or "STATICS" in name_upper or "MECHANICS" in name_upper:
        return ["matmj44"]
    elif "MTB-301" in code or "ALGEBRA" in name_upper:
        if "ABSTRACT" in name_upper:
            return ["matmj51"]
        return ["matmj21"]
    elif "MTB-302" in code or "DIFF" in name_upper:
        if "PDE" in name_upper:
            return ["matmj43", "matmn41"]
        return ["matmj43", "matmn41"]
    elif "MTB-401" in code or "PDE" in name_upper:
        return ["matmj43", "matmn41"]
    elif "MTB-402" in code or "METHODS" in name_upper:
        return ["matmj43", "matmn41"]
    elif "MTB-501" in code or "ANALYSIS" in name_upper:
        if "COMPLEX" in name_upper:
            return ["matmj62"]
        return ["matmj32"]
    elif "MTB-502" in code:
        return ["matmj51"]
    elif "MTB-503" in code or "PROGRAMMING" in name_upper:
        return ["matmv31"]
    elif "MTB-504" in code or "DIFFGEOMETRY" in name_upper:
        return ["matmj63"]
    elif "MTB-505" in code:
        return ["matmj44"]
    elif "MTB-506" in code or "MTB-605" in code or "OPERATIONS" in name_upper:
        return ["matmj65"]
    elif "MTB-509" in code or "MTB-609" in code or "RELATIVITY" in name_upper:
        return ["matmj66"]
    elif "MTB-601" in code:
        return ["matmj52"]
    elif "MTB-602" in code or "LINEARALGEBRA" in name_upper:
        return ["matmj31"]
    elif "MTB-603" in code or "NUMERICAL" in name_upper:
        return ["matmj54"]
    elif "MTB-604" in code or "DISCRETE" in name_upper:
        return ["matmj68"]
    elif "MTB-606" in code or "COMPLEX" in name_upper:
        return ["matmj62"]
    elif "MTB-608" in code:
        return ["matmj63"]
    elif "MTB-611" in code or "DYNAMICAL" in name_upper:
        return ["matmj610"]
    elif "VECTOR" in name_upper or "TENSOR" in name_upper:
        return ["matmj42"]
        
    return []

counts = {}
for f in files:
    filepath = os.path.join(math_dir, f)
    with open(filepath, 'r', encoding='utf-8') as file_obj:
        content = file_obj.read()
    
    keys = get_course_keys(f, content)
    qs = parse_tex_file(filepath)
    for k in keys:
        counts[k] = counts.get(k, 0) + len(qs)

print("Parsed question counts per active course key:")
for k in sorted(counts.keys()):
    print(f"- {k}: {counts[k]} questions parsed")
