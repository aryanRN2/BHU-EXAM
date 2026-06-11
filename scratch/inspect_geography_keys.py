import json

with open("js/exams-data.js", "r", encoding="utf-8") as f:
    js_content = f.read()

json_start = js_content.find("{")
json_end = js_content.rfind("}")
EXAMS = json.loads(js_content[json_start:json_end+1])

geography_exams = {}
for key, value in EXAMS.items():
    val_lower = json.dumps(value).lower()
    if key.startswith("ggr") or "geography" in val_lower or "remote sensing" in val_lower or "climatology" in val_lower or "oceanography" in val_lower or "geomorphology" in val_lower:
        geography_exams[key] = {
            "title": value.get("title"),
            "module": value.get("module"),
            "comingSoon": value.get("comingSoon"),
            "questions_count": len(value.get("questions", []))
        }

# Write to a file
with open("scratch/geography_keys.json", "w", encoding="utf-8") as f:
    json.dump(geography_exams, f, indent=2)

print(f"Written {len(geography_exams)} geography keys to scratch/geography_keys.json")
