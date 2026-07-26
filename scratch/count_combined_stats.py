import os
import re

def count_nep_papers():
    # Count entries in js/nep-data.js
    with open('js/nep-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Each entry has a "filePath"
    matches = re.findall(r'"filePath":\s*"([^"]+)"', content)
    return len(set(matches)), matches

def count_legacy_papers():
    if not os.path.exists('js/legacy-data.js'):
        return 0, []
    with open('js/legacy-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.findall(r'"filePath":\s*"([^"]+)"', content)
    return len(set(matches)), matches

def count_all_tex_stats():
    _, nep_files = count_nep_papers()
    _, legacy_files = count_legacy_papers()
    
    all_files = set(nep_files + legacy_files)
    
    total_lines = 0
    total_questions = 0
    missing = 0
    
    for rel_path in all_files:
        full_path = os.path.join(os.getcwd(), rel_path)
        if not os.path.exists(full_path):
            missing += 1
            continue
            
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            total_lines += len(lines)
            
            content = "".join(lines)
            content = re.sub(r'(?m)^%.*$', '', content)
            items = content.count(r'\item')
            total_questions += items
            
    print(f"Total Unique Transcribed PYQs: {len(all_files)}")
    print(f"Total Lines of LaTeX: {total_lines}")
    print(f"Total Questions: {total_questions}")
    print(f"Missing: {missing}")

if __name__ == "__main__":
    count_all_tex_stats()
