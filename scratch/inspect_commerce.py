import os
import json
import re

commerce_dir = '/Users/aryanmaurya/exam portal/COMMERCE_LATEX'
project_dir = '/Users/aryanmaurya/exam portal'
results = []

def walk(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.tex'):
                results.append(os.path.join(root, file))

walk(commerce_dir)
print(f"Found {len(results)} tex files.")

parsed_files = []

for file_path in results:
    relative_path = os.path.relpath(file_path, project_dir)
    file_name = os.path.basename(file_path)
    
    # Read the first 45 lines to search for titles/codes
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [f.readline() for _ in range(45)]
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        continue
        
    paper_title = ''
    paper_code = ''
    
    # Check lines for paper information
    for line in lines:
        if '% Paper:' in line:
            # e.g. % Paper: BCH-122 : Financial Accounting - II
            match = re.search(r'%\s*Paper:\s*([A-Za-z0-9\-_]+)\s*[:\-]\s*(.*)', line, re.IGNORECASE)
            if match:
                paper_code = match.group(1).strip()
                paper_title = match.group(2).strip()
                break
        elif 'Paper No.' in line:
            # e.g. {\large\bfseries Paper No. BCH-122: Financial Accounting - II}
            match = re.search(r'Paper\s+No\.\s*([A-Za-z0-9\-_]+)\s*[:\-]\s*([^\}\\]*)', line, re.IGNORECASE)
            if match:
                paper_code = match.group(1).strip()
                paper_title = match.group(2).strip()
                break
                
    # Normalize code and subject
    if paper_code:
        paper_code = paper_code.replace('-', '').strip()
        
    # Attempt to parse from filename if not found in headers
    # e.g., BCH214_CostAccounting_SemIII_2016-17.tex
    fn_match = re.match(r'^([A-Z0-9]+)_(.*?)_(Sem[IVXLC\d]+)_(\d{4}-\d{2})\.tex$', file_name, re.IGNORECASE)
    code_from_fn = ''
    subject_from_fn = ''
    sem_from_fn = ''
    year_from_fn = ''
    
    if fn_match:
        code_from_fn = fn_match.group(1)
        subject_from_fn = fn_match.group(2)
        # convert CamelCase to space separated
        subject_from_fn = re.sub(r'([A-Z])', r' \1', subject_from_fn).strip()
        sem_from_fn = fn_match.group(3)
        year_from_fn = fn_match.group(4)
    else:
        # backup match
        fn_match2 = re.match(r'^([A-Z0-9]+)_(.*?)_([A-Za-z0-9\-]+)\.tex$', file_name, re.IGNORECASE)
        if fn_match2:
            code_from_fn = fn_match2.group(1)
            subject_from_fn = fn_match2.group(2)
            subject_from_fn = re.sub(r'([A-Z])', r' \1', subject_from_fn).strip()
            
    final_code = paper_code if paper_code else code_from_fn
    final_subject = paper_title if paper_title else subject_from_fn
    
    # Normalize final_code by adding a hyphen after 3 letters, e.g. BCH121 -> BCH-121
    if final_code and len(final_code) >= 6 and not '-' in final_code:
        final_code = final_code[:3] + '-' + final_code[3:]
        
    # Semester mapping
    semester = 1
    sem_lower = (sem_from_fn if sem_from_fn else file_name).lower()
    if 'sem_i' in sem_lower or 'semi_' in sem_lower or 'sem-i' in sem_lower or 'semi' in sem_lower:
        semester = 1
    if 'sem_ii' in sem_lower or 'semii_' in sem_lower or 'sem-ii' in sem_lower or 'semii' in sem_lower:
        semester = 2
    if 'sem_iii' in sem_lower or 'semiii_' in sem_lower or 'sem-iii' in sem_lower or 'semiii' in sem_lower:
        semester = 3
    if 'sem_iv' in sem_lower or 'semiv_' in sem_lower or 'sem-iv' in sem_lower or 'semiv' in sem_lower:
        semester = 4
    if 'sem_v' in sem_lower or 'semv_' in sem_lower or 'sem-v' in sem_lower or 'semv' in sem_lower:
        semester = 5
    if 'sem_vi' in sem_lower or 'semvi_' in sem_lower or 'sem-vi' in sem_lower or 'semvi' in sem_lower:
        semester = 6

    final_year = year_from_fn if year_from_fn else ''
    if not final_year:
        year_match = re.search(r'(\d{4}-\d{2})', file_name)
        if year_match:
            final_year = year_match.group(1)

    parsed_files.append({
        'fileName': file_name,
        'filePath': relative_path,
        'code': final_code,
        'subject': final_subject,
        'semester': semester,
        'year': final_year
    })

# Sort by code and year
parsed_files.sort(key=lambda x: (x['code'], x['year']))

with open('/Users/aryanmaurya/exam portal/scratch/commerce_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_files, f, indent=2)

print(f"Written parsed files to scratch/commerce_parsed.json")
