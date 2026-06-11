import json
import re

# Load chemistry_syllabus.json
with open('aaa/chemistry/chemistry_syllabus.json', 'r', encoding='utf-8') as f:
    syllabus_data = json.load(f)

# Collect all syllabus courses
syllabus_papers = {}
for sem in syllabus_data.get("semesters", []):
    for paper in sem.get("papers", []):
        code = paper["code"].lower()
        syllabus_papers[code] = paper

print(f"Loaded {len(syllabus_papers)} papers from syllabus JSON.")

# Load exams-data.js
with open('js/exams-data.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract EXAMS JSON block
json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

# Filter chemistry exams that are in syllabus
chem_exams = {}
for key, exam in EXAMS.items():
    if key.startswith("che") and exam.get("comingSoon") == False:
        chem_exams[key] = exam

print(f"Found {len(chem_exams)} live chemistry exams in database.")

# Write out questions for papers in syllabus to a JSON file for analysis
review_data = {}
for key, exam in chem_exams.items():
    # Find matching syllabus paper code
    matched_code = None
    for s_code in syllabus_papers:
        if s_code == key:
            matched_code = s_code
            break
    
    if matched_code:
        review_data[key] = {
            "title": exam["title"],
            "module": exam["module"],
            "syllabus": syllabus_papers[matched_code]["syllabus"],
            "questions": exam["questions"]
        }
    else:
        print(f"Live exam key '{key}' has no matching paper in chemistry_syllabus.json")

with open('scratch/chemistry_review_data.json', 'w', encoding='utf-8') as f:
    json.dump(review_data, f, indent=2)

print("Saved review data to scratch/chemistry_review_data.json.")
