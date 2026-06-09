import os
import re

math_dir = "aaa/latest corrected maths pdf/final maths export latex"
files = [f for f in os.listdir(math_dir) if f.endswith(".tex")]
files.sort()

print(f"Scanning {len(files)} latex files:")
for f in files:
    filepath = os.path.join(math_dir, f)
    with open(filepath, "r", encoding="utf-8") as file_obj:
        content = file_obj.read()
    
    # Try to extract paper code and title from comments or content
    code = "Unknown"
    title = "Unknown"
    
    comment_match = re.search(r'%\s*Paper:\s*(MTB-[A-Z0-9-]+)\s*:\s*([^\n]+)', content, re.IGNORECASE)
    if comment_match:
        code = comment_match.group(1).strip()
        title = comment_match.group(2).strip()
    else:
        pdf_match = re.search(r'pdftitle\s*=\s*\{\s*(MTB-[A-Z0-9-]+)\s*:\s*([^}-]+)', content, re.IGNORECASE)
        if pdf_match:
            code = pdf_match.group(1).strip()
            title = pdf_match.group(2).strip()
        else:
            paper_match = re.search(r'Paper\s*(?:No\.)?\s*(MTB-[A-Z0-9-]+)\s*:\s*([^}\n\\]+)', content, re.IGNORECASE)
            if paper_match:
                code = paper_match.group(1).strip()
                title = paper_match.group(2).strip()
    
    print(f"- File: {f}\n  Code: {code} | Title: {title}")
