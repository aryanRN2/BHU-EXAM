import os
import re

def count_all_tex_in_aaa():
    total_files = 0
    total_lines = 0
    total_questions = 0
    
    for root, dirs, files in os.walk('aaa'):
        for file in files:
            if file.endswith('.tex'):
                total_files += 1
                full_path = os.path.join(root, file)
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    
                    content = "".join(lines)
                    content = re.sub(r'(?m)^%.*$', '', content)
                    items = content.count(r'\item')
                    total_questions += items
                    
    print(f"Total .tex files in aaa/: {total_files}")
    print(f"Total lines of LaTeX: {total_lines}")
    print(f"Total questions: {total_questions}")

if __name__ == "__main__":
    count_all_tex_in_aaa()
