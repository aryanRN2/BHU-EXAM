import os
import json
import re

project_dir = '/Users/aryanmaurya/exam portal'

def get_all_tex_files():
    target_dirs = [os.path.join(project_dir, 'aaa'), os.path.join(project_dir, 'COMMERCE_LATEX')]
    all_files = []
    
    for d in target_dirs:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.tex'):
                    all_files.append({
                        'name': file[:-4],
                        'path': os.path.join(root, file)
                    })
    return all_files

def resolve_paper(filename, all_files):
    # 1. Exact match
    matched = next((f for f in all_files if f['name'] == filename), None)
    if matched:
        return matched['path']
        
    # 2. Normalized match
    norm_target = re.sub(r'[^a-z0-9]', '', filename.lower())
    if not matched:
        matched = next((f for f in all_files if re.sub(r'[^a-z0-9]', '', f['name'].lower()) == norm_target), None)
        
    # 3. Code-year regex match
    if not matched:
        code_match = re.match(r'([A-Z]{3})[-_](\d{3})', filename, re.IGNORECASE)
        year_match = re.search(r'(\d{4}[-_]\d{2})', filename)
        if code_match and year_match:
            code = code_match.group(1).upper() + '-' + code_match.group(2)
            year = year_match.group(1).replace('_', '-')
            
            def match_code_year(f):
                name_upper = f['name'].upper()
                has_code = code in name_upper or code.replace('-', '_') in name_upper
                has_year = year in name_upper
                return has_code and has_year
                
            matched = next((f for f in all_files if match_code_year(f)), None)
            
    # 4. Fuzzy match
    if not matched:
        matched = next((f for f in all_files if norm_target in re.sub(r'[^a-z0-9]', '', f['name'].lower()) or re.sub(r'[^a-z0-9]', '', f['name'].lower()) in norm_target), None)
        
    if matched:
        return matched['path']
    return None

def run_test():
    all_files = get_all_tex_files()
    print(f"Total .tex files scanned: {len(all_files)}")
    
    with open(os.path.join(project_dir, 'js/nep-data.js'), 'r') as f:
        content = f.read()
        
    array_match = re.search(r'export const NEP_LATEX_PYQ_DATA = (\[[\s\S]*?\]);', content)
    data = json.loads(array_match.group(1))
    
    commerce_entries = [e for e in data if e.get('department') == 'Commerce']
    print(f"Verifying {len(commerce_entries)} commerce entries...")
    
    unresolved = []
    mismatch = []
    
    for entry in commerce_entries:
        file_name = entry['fileName']
        filename_without_ext = file_name.replace('.tex', '')
        expected_path = os.path.join(project_dir, entry['filePath'])
        
        resolved_path = resolve_paper(filename_without_ext, all_files)
        
        if not resolved_path:
            unresolved.append(file_name)
        elif os.path.realpath(resolved_path) != os.path.realpath(expected_path):
            mismatch.append({
                'file': file_name,
                'expected': expected_path,
                'actual': resolved_path
            })
            
    if unresolved:
        print(f"FAIL: {len(unresolved)} papers could not be resolved by the API matching logic:")
        for u in unresolved[:5]:
            print(f"  - {u}")
    else:
        print("PASS: All papers are successfully resolved by the matching logic!")
        
    if mismatch:
        print(f"FAIL: {len(mismatch)} papers resolved to a different path than expected:")
        for m in mismatch[:5]:
            print(f"  - {m['file']}\n    Expected: {m['expected']}\n    Actual: {m['actual']}")
    else:
        print("PASS: All resolved paths match their expected database filePaths exactly!")
        
    if not unresolved and not mismatch:
        print("ALL TESTS PASSED!")
    else:
        exit(1)

if __name__ == '__main__':
    run_test()
