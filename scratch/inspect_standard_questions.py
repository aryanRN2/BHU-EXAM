import re
import ast

with open("scratch/populate_chemistry.py", "r", encoding="utf-8") as f:
    content = f.read()

# Locate CHEMISTRY_SYLLABI = { ... }
start_match = re.search(r'CHEMISTRY_SYLLABI\s*=\s*\{', content)
if start_match:
    start_pos = start_match.start()
    # Find matching brace
    brace_count = 0
    end_pos = -1
    for i in range(start_pos + len("CHEMISTRY_SYLLABI ="), len(content)):
        char = content[i]
        if char == '{':
            brace_count += 1
        elif char == '}':
            if brace_count == 0:
                end_pos = i
                break
            else:
                brace_count -= 1
    
    if end_pos != -1:
        dict_str = content[start_pos:end_pos+1]
        # Parse it safely using python ast or regex
        # Let's extract each key and its standard questions title and count
        # For simplicity, print keys and questions directly by evaluating the dict definition
        # Since it is safe python code, we can evaluate it in a namespace
        local_ns = {}
        try:
            exec(dict_str, {}, local_ns)
            syllabi = local_ns.get("CHEMISTRY_SYLLABI", {})
            for key, info in syllabi.items():
                print(f"Key: {key} | Title: {info.get('title')}")
                print(f"  Standard Questions Count: {len(info.get('standard_questions', []))}")
                if info.get('standard_questions'):
                    print("  First 2 standard questions:")
                    for q, u in info['standard_questions'][:2]:
                        print(f"    - [Unit {u}] {q}")
        except Exception as e:
            print("Error parsing dictionary:", e)
else:
    print("Could not find CHEMISTRY_SYLLABI in populate_chemistry.py")
