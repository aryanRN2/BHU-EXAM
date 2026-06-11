import json

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

for key, exam in sorted(EXAMS.items()):
    if not key.startswith("che") or exam.get("comingSoon"):
        continue
    questions = exam.get("questions", [])
    placeholders = [q for q in questions if "Discuss the theoretical foundations" in q.get("question", "")]
    if placeholders:
        print(f"Exam: {key} ({exam['title']}) has {len(placeholders)} placeholder questions.")
