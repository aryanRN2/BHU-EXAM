import os
import re

def parse_geo_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comment lines
    content = re.sub(r'(?m)^%.*$', '', content)
    
    # Extract Question 1 sub-questions from parts
    parts_questions = []
    
    # Look for the parts block
    parts_match = re.search(r'\\begin\{parts\}(.*?)\\end\{parts\}', content, re.DOTALL)
    if parts_match:
        parts_content = parts_match.group(1)
        # Split by \item
        items = re.split(r'\\item', parts_content)
        for item in items[1:]:  # Skip the first element which is empty/prefix
            cleaned = clean_text(item)
            if len(cleaned) > 10:
                parts_questions.append(cleaned)
                
    # Extract Questions 2 to 9
    main_questions = []
    # Match pattern: \textbf{Question X.} Question text \pts{...}
    # Or variations
    matches = re.findall(r'\\textbf\{\s*Question\s*([2-9])\.\}\s*(.*?)(?=\\pts|\\hfill|\\medskip|\\noindent|\\vfill|\\begin\{center\}|\Z)', content, re.DOTALL)
    for q_num, q_text in matches:
        cleaned = clean_text(q_text)
        if len(cleaned) > 10:
            main_questions.append(cleaned)
            
    return parts_questions + main_questions

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
    # Replace LaTeX bracket math with $ delimiters
    text = text.replace(r'\[', '$')
    text = text.replace(r'\]', '$')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Test on one BA and one BSc file
file1 = "aaa/geography/GRA-101_PhysicalBasisOfGeography_SemI_2022-23_BA.tex"
file2 = "aaa/geography/GRB-403A_BasicsOfRemoteSensing_SemIV_2023-24_BSc.tex"

for fpath in [file1, file2]:
    print(f"--- Parsing {fpath} ---")
    qs = parse_geo_file(fpath)
    print(f"Found {len(qs)} questions:")
    for idx, q in enumerate(qs):
        print(f" {idx+1}: {q}")
