import json
import re

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    content = f.read()

json_start = content.find("{")
json_end = content.rfind("}")
EXAMS = json.loads(content[json_start:json_end+1])

for k, exam in EXAMS.items():
    questions = exam.get("questions", [])
    if not questions:
        continue
    
    dirty = []
    for q in questions:
        q_text = q.get("question", "")
        reasons = []
        if "Page" in q_text: reasons.append("Page")
        if "contributor" in q_text or "website" in q_text: reasons.append("Links")
        if "Banaras" in q_text or "BANARAS" in q_text: reasons.append("University")
        if re.search(r"\[\d+(\.\d+)?\]", q_text): reasons.append("Marks")
        if re.search(r"\bOR\b\s*$", q_text): reasons.append("OR suffix")
        if "\\" in q_text and "$" not in q_text: reasons.append("Unwrapped LaTeX")
        
        unicode_symbols = ["\u03c8", "\u03c0", "\u221a", "\u2212", "\u03b8", "\u03bb", "\u03b1", "\u03b2", "\u221e", "\u2202"]
        for sym in unicode_symbols:
            if sym in q_text:
                reasons.append(f"Unicode {sym}")
                break
                
        if reasons:
            dirty.append((q.get("id"), q_text, reasons))
            
    if dirty:
        print(f"\n=== Subject: {k} ({exam['title']}) - {len(dirty)} issues ===")
        for qid, q_text, reasons in dirty:
            print(f"  Q{qid} [{','.join(reasons)}]: {q_text}")
