import os
import re
import json

def get_tex_files_from_nep_data():
    # Load JS file content and extract NEP_LATEX_PYQ_DATA array
    # Since it's a JS file, we'll parse it or just read all .tex references inside it
    js_path = 'js/nep-data.js'
    if not os.path.exists(js_path):
        print("nep-data.js not found!")
        return set()
    
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all strings matching "aaa/....tex"
    matches = re.findall(r'"filePath":\s*"([^"]+)"', content)
    return set(matches)

def analyze_stats():
    tex_files = get_tex_files_from_nep_data()
    print(f"Total unique .tex files referenced in nep-data.js: {len(tex_files)}")
    
    total_lines = 0
    total_questions = 0
    missing_files = 0
    
    for relative_path in tex_files:
        # Check if file exists
        full_path = os.path.join(os.getcwd(), relative_path)
        if not os.path.exists(full_path):
            # Try fuzzy check or ignore
            missing_files += 1
            continue
            
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            total_lines += len(lines)
            
            # Count items / questions
            file_content = "".join(lines)
            # Remove comments to avoid false matches
            file_content = re.sub(r'(?m)^%.*$', '', file_content)
            # Count \item occurrences
            items = file_content.count(r'\item')
            total_questions += items
            
    print(f"Processed files. Missing files: {missing_files}")
    print(f"Total lines of LaTeX: {total_lines}")
    print(f"Total questions (\item): {total_questions}")

if __name__ == "__main__":
    analyze_stats()
