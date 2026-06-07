import os
import re

tex_files = [f for f in os.listdir('aaa/chemistry/tex_files') if f.endswith('.tex')]
tex_files.sort()

for f in tex_files:
    # Read the title inside the file
    filepath = os.path.join('aaa/chemistry/tex_files', f)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Try to find paper title
    title_match = re.search(r'Paper No\.\s*([^}\\]+)', content)
    paper_title = title_match.group(1).strip() if title_match else "N/A"
    
    # Print file name and the extracted paper title
    print(f"File: {f}")
    print(f"  Extracted Paper Title: {paper_title}")
