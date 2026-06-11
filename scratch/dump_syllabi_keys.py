import re

with open("scratch/populate_chemistry.py", "r", encoding="utf-8") as f:
    content = f.read()

# Extract CHEMISTRY_SYLLABI keys and titles
matches = re.findall(r'\s*"([^"]+)":\s*\{\s*"title":\s*"([^"]+)"', content)
print("CHEMISTRY_SYLLABI Keys and Titles:")
for key, title in matches:
    print(f"  Key: {key} -> Title: {title}")
