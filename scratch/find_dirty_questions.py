import json
import re

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    content = f.read()

json_start = content.find("{")
json_end = content.rfind("}")
EXAMS = json.loads(content[json_start:json_end+1])

physics_keys = [
    "phymj11", "phymj21", "phymj31", "phymj32", "phymj41", "phymj42",
    "phymj51", "phymj52", "phymj53", "phymj61", "phymj62", "phymj63",
    "phymj64", "phymj75"
]

print("=== INSPECTING PHYSICS QUESTIONS FOR ISSUES ===")
for k in physics_keys:
    exam = EXAMS.get(k)
    if not exam or "questions" not in exam:
        continue
    
    print(f"\nSubject: {k} ({exam['title']})")
    dirty_count = 0
    for q in exam["questions"]:
        q_text = q["question"]
        # Look for run-together words (e.g. lowercase letter followed by uppercase, or numbers without space, or LaTeX code not inside $)
        has_issues = False
        if re_match := any(w in q_text for w in ["1sstate", "whereais", "whereis", "firststate", "restmass", "wavefunction"]):
            has_issues = True
        elif "\\" in q_text and "$" not in q_text:
            has_issues = True
        elif re.search(r"[a-zA-Z]{3,}\d+[a-zA-Z]{3,}", q_text): # e.g. a3e
            has_issues = True
        import re
        if re.search(r"\b[a-z]+[A-Z][a-z]+\b", q_text): # camelcase in single word
            has_issues = True
            
        if has_issues and dirty_count < 4:
            print(f"  Q{q['id']}: {q_text}")
            dirty_count += 1
