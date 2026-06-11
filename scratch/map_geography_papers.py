import os
import re
import json

geography_dir = "aaa/geography"
files = [f for f in os.listdir(geography_dir) if f.endswith(".tex")]
files.sort()

# Load geography keys from exams-data.js
with open("js/exams-data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

ggr_keys = {k: v for k, v in EXAMS.items() if k.startswith("ggr")}

# Let's map each tex file to potential GGR keys
mapping = {}
for f in files:
    filepath = os.path.join(geography_dir, f)
    with open(filepath, "r", encoding="utf-8") as file_obj:
        content = file_obj.read()
    
    # Try to extract paper code and title
    title = ""
    code = ""
    comment_paper_match = re.search(r'%\s*Paper:\s*([^\n]+)', content, re.IGNORECASE)
    if comment_paper_match:
        val = comment_paper_match.group(1).strip()
        parts = val.split(":", 1)
        if len(parts) == 2:
            code = parts[0].strip()
            title = parts[1].strip()
        else:
            code = val

    # Standardize title for matching
    title_clean = re.sub(r'\(.*?\)', '', title).replace("of", "").replace("and", "").replace("-", "").strip().lower()
    title_words = set(title_clean.split())

    matches = []
    for gkey, gval in ggr_keys.items():
        gtitle = gval.get("title", "")
        gtitle_clean = re.sub(r'\(.*?\)', '', gtitle).replace("of", "").replace("and", "").replace("-", "").strip().lower()
        gtitle_words = set(gtitle_clean.split())
        
        # Check intersection
        intersection = title_words.intersection(gtitle_words)
        if len(intersection) > 0:
            score = len(intersection) / max(len(title_words), len(gtitle_words))
            matches.append((gkey, gtitle, score))
    
    matches.sort(key=lambda x: x[2], reverse=True)
    mapping[f] = {
        "extracted_code": code,
        "extracted_title": title,
        "matches": matches[:3]
    }

print(json.dumps(mapping, indent=2))
