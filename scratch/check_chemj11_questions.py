import json

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

chemj11 = EXAMS.get("chemj11", {})
print(f"Title: {chemj11.get('title')}")
print("Questions:")
for idx, q in enumerate(chemj11.get("questions", [])):
    print(f"  {idx + 1}. [Unit {q.get('unit')}] {q.get('question')[:100]}")
