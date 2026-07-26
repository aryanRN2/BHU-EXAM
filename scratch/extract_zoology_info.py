import os
import re
import json

latex_dir = "/Users/aryanmaurya/exam portal/aaa/zoology/latex_outputs"
files = [f for f in os.listdir(latex_dir) if f.endswith('.tex')]

extracted = {}

for file_name in sorted(files):
    filepath = os.path.join(latex_dir, file_name)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paper_code = None
    paper_name = None
    
    # 1. Extract paper code from filename (e.g. ZOB-501)
    code_m = re.search(r'ZOB-\w+', file_name)
    if code_m:
        paper_code = code_m.group(0).upper()
        
    # 2. Extract from "Paper: ZOB-... --- ..."
    # We clean up optional trailing curly braces, newlines, and backslashes
    paper_line_m = re.search(r'Paper:\s*ZOB-\w+\s*\\*---+\s*(.*?)(?=\\\\|\\\[|\]|\n|\Z)', content)
    if paper_line_m:
        paper_name = paper_line_m.group(1).strip()
    
    if not paper_name:
        # Try a simpler pattern
        paper_line_m2 = re.search(r'Paper:\s*ZOB-\w+\s*\\*---*\s*(.*?)(?=\\\\|\\\[|\]|\n|\Z)', content)
        if paper_line_m2:
            paper_name = paper_line_m2.group(1).strip()
            
    if paper_name:
        # Clean up any trailing }
        paper_name = paper_name.rstrip('}').strip()
        paper_name = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', paper_name)
        paper_name = re.sub(r'\\textit\{([^\}]*)\}', r'\1', paper_name)
        paper_name = re.sub(r'\\emph\{([^\}]*)\}', r'\1', paper_name)
        paper_name = paper_name.replace(r'\&', '&')
        paper_name = paper_name.replace(r'\_', '_')
        paper_name = re.sub(r'\s+', ' ', paper_name).strip()
    
    if paper_code:
        if paper_code not in extracted or (paper_name and len(paper_name) > len(extracted[paper_code])):
            extracted[paper_code] = paper_name

print("Extracted Paper Codes and Names:")
print(json.dumps(extracted, indent=2))
