import json
import re

with open('js/exams-data.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Match keys starting with "che"
matches = re.findall(r'"(che[a-z0-9]+)":\s*\{', js_content)
print(f"Found {len(matches)} chemistry-related keys:")

for key in sorted(set(matches)):
    pattern = r'"' + key + r'":\s*\{(.*?)\n\s*\}'
    block_match = re.search(pattern, js_content, re.DOTALL)
    if block_match:
        block = block_match.group(1)
        title_match = re.search(r'"title":\s*"([^"]+)"', block)
        module_match = re.search(r'"module":\s*"([^"]+)"', block)
        coming_soon_match = re.search(r'"comingSoon":\s*(true|false)', block)
        
        title = title_match.group(1) if title_match else "N/A"
        module = module_match.group(1) if module_match else "N/A"
        coming_soon = coming_soon_match.group(1) if coming_soon_match else "N/A"
        
        print(f"Key: {key} | Module: {module} | Title: {title} | comingSoon: {coming_soon}")
    else:
        print(f"Key: {key} (no block match)")
