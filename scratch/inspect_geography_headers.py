import os
import re
import json

geography_dir = "aaa/geography"
files = [f for f in os.listdir(geography_dir) if f.endswith(".tex")]
files.sort()

print(f"Scanning {len(files)} latex files in {geography_dir}:")
for f in files:
    filepath = os.path.join(geography_dir, f)
    with open(filepath, "r", encoding="utf-8") as file_obj:
        content = file_obj.read()
    
    # Try to extract paper code and title from comments or content
    code = "Unknown"
    title = "Unknown"
    exam = "Unknown"
    
    comment_paper_match = re.search(r'%\s*Paper:\s*([^\n]+)', content, re.IGNORECASE)
    if comment_paper_match:
        val = comment_paper_match.group(1).strip()
        parts = val.split(":", 1)
        if len(parts) == 2:
            code = parts[0].strip()
            title = parts[1].strip()
        else:
            code = val
    
    comment_exam_match = re.search(r'%\s*Exam:\s*([^\n]+)', content, re.IGNORECASE)
    if comment_exam_match:
        exam = comment_exam_match.group(1).strip()
        
    print(f"- File: {f}\n  Code: {code}\n  Title: {title}\n  Exam: {exam}\n")
