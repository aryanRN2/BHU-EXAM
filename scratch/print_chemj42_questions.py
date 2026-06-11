import json

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

chemj43 = EXAMS.get("chemj43", {})
print(f"Title: {chemj43.get('title')}")
print(f"Module: {chemj43.get('module')}")
print("Questions:")
for idx, q in enumerate(chemj43.get("questions", [])):
    print(f"  {idx + 1}. [Unit {q.get('unit')}] {q.get('question')}")
