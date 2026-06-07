import json
import re

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    content = f.read()

json_start = content.find("{")
json_end = content.rfind("}")
EXAMS = json.loads(content[json_start:json_end+1])

print("=== CHECKING ALL SUBJECT QUESTIONS FOR ISSUES ===")
for k, exam in EXAMS.items():
    questions = exam.get("questions", [])
    if not questions:
        continue
    
    dirty = []
    for q in questions:
        q_text = q.get("question", "")
        # Check conditions
        issues = []
        if "Page" in q_text:
            issues.append("Contains 'Page'")
        if "contributor" in q_text:
            issues.append("Contains 'contributor'")
        if "website" in q_text:
            issues.append("Contains 'website'")
        if "Banaras" in q_text or "BANARAS" in q_text:
            issues.append("Contains 'Banaras'")
        if re.search(r"\[\d+(\.\d+)?\]", q_text):
            issues.append("Contains marks [X]")
        if re.search(r"\bOR\b\s*$", q_text):
            issues.append("Ends with OR")
        if re.search(r"\\", q_text) and "$" not in q_text:
            issues.append("LaTeX without math delimiter")
        # Check for unicode symbols that should be LaTeX
        unicode_symbols = ["\u03c8", "\u03c0", "\u221a", "\u2212", "\u03b8", "\u03bb", "\u03b1", "\u03b2", "\u221e", "\u2202"]
        for sym in unicode_symbols:
            if sym in q_text:
                issues.append(f"Contains unicode '{sym}'")
                break
        
        if issues:
            dirty.append((q.get("id"), q_text, issues))
            
    if dirty:
        print(f"\nSubject: {k} ({exam['title']}) - Found {len(dirty)} potential issues")
        for qid, text, issues in dirty[:5]:
            print(f"  Q{qid} [{', '.join(issues)}]: {text}")
        if len(dirty) > 5:
            print(f"  ... and {len(dirty) - 5} more.")
