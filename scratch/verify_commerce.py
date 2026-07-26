import json
import os
import re

project_dir = '/Users/aryanmaurya/exam portal'
nep_data_path = os.path.join(project_dir, 'js/nep-data.js')

def verify():
    # 1. Read nep-data.js and parse JSON array
    with open(nep_data_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    array_match = re.search(r'export const NEP_LATEX_PYQ_DATA = (\[[\s\S]*?\]);', content)
    if not array_match:
        print("FAIL: Could not locate NEP_LATEX_PYQ_DATA array in js/nep-data.js")
        return
        
    data = json.loads(array_match.group(1))
    print(f"Total entries in nep-data.js: {len(data)}")
    
    commerce_entries = [e for e in data if e.get('department') == 'Commerce']
    print(f"Total Commerce entries: {len(commerce_entries)}")
    
    if len(commerce_entries) != 226:
        print(f"FAIL: Expected 226 Commerce entries, but found {len(commerce_entries)}")
        return
        
    errors = 0
    checked_files = set()
    
    # 2. Check each entry
    for entry in commerce_entries:
        file_path = entry.get('filePath')
        file_name = entry.get('fileName')
        nep_code = entry.get('nepCode')
        old_code = entry.get('code')
        
        # Verify file path exists
        full_path = os.path.join(project_dir, file_path)
        if not os.path.exists(full_path):
            print(f"FAIL: File does not exist: {file_path}")
            errors += 1
            
        # Verify name consistency
        if os.path.basename(full_path) != file_name:
            print(f"FAIL: fileName mismatch: {file_name} vs actual {os.path.basename(full_path)}")
            errors += 1
            
        # Verify nepCode and oldCode presence
        if not nep_code:
            print(f"FAIL: Missing nepCode for old code {old_code}")
            errors += 1
            
        if not old_code:
            print(f"FAIL: Missing old code for file {file_name}")
            errors += 1
            
        checked_files.add(file_path)
        
    print(f"Checked {len(checked_files)} unique files.")
    
    # 3. Check for any duplicate records in database
    all_filenames = [e.get('fileName') for e in data]
    duplicates = len(all_filenames) - len(set(all_filenames))
    if duplicates > 0:
        print(f"FAIL: Found {duplicates} duplicate filenames in the array!")
        errors += 1
        
    if errors == 0:
        print("SUCCESS: All Commerce integrations in js/nep-data.js are verified successfully!")
    else:
        print(f"FAIL: Encountered {errors} validation errors.")

if __name__ == '__main__':
    verify()
