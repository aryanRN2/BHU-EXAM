import json
import re

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    content = f.read()

json_start = content.find("{")
json_end = content.rfind("}")
EXAMS = json.loads(content[json_start:json_end+1])

print("Subject | Title | Question Count | Dirty Question Count")
print("---|---|---|---")
total_dirty = 0
total_questions = 0

for k, exam in EXAMS.items():
    questions = exam.get("questions", [])
    if not questions:
        continue
    
    dirty_count = 0
    for q in questions:
        q_text = q.get("question", "")
        # Check conditions
        is_dirty = False
        if "Page" in q_text:
            is_dirty = True
        elif "contributor" in q_text or "website" in q_text:
            is_dirty = True
        elif "Banaras" in q_text or "BANARAS" in q_text:
            is_dirty = True
        elif re.search(r"\[\d+(\.\d+)?\]", q_text):
            is_dirty = True
        elif re.search(r"\bOR\b\s*$", q_text):
            is_dirty = True
        elif "\\" in q_text and "$" not in q_text:
            is_dirty = True
        
        # Check for unicode symbols
        unicode_symbols = ["\u03c8", "\u03c0", "\u221a", "\u2212", "\u03b8", "\u03bb", "\u03b1", "\u03b2", "\u221e", "\u2202"]
        for sym in unicode_symbols:
            if sym in q_text:
                is_dirty = True
                break
                
        if is_dirty:
            dirty_count += 1
            
    print(f"{k} | {exam.get('title')} | {len(questions)} | {dirty_count}")
    total_dirty += dirty_count
    total_questions += len(questions)

print(f"\nTotal questions: {total_questions}, Total dirty questions: {total_dirty}")
