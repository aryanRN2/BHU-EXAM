import os
import re
import json

def camel_case_split(identifier):
    # First insert spaces before lowercase conjunctions/prepositions run-on, e.g. "StructureandBonding"
    for word in ['and', 'in', 'of', 'to', 'with', 'is', 'for', 'from', 'on', 'by', 'at']:
        identifier = re.sub(r'([a-zA-Z])' + word + r'([A-Z])', r'\1 ' + word + r' \2', identifier)
        
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    words = [m.group(0) for m in matches]
    result = []
    for word in words:
        # Split Roman numerals from words if they got stuck
        sub_matches = re.split(r'(?i)\b(I|II|III|IV|V|VI)\b', word)
        for part in sub_matches:
            if part:
                result.append(part.strip())
    # Join with space and clean
    text = " ".join(result)
    # Re-align words and clean up double spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_semester(sem_str):
    # SemI -> 1, SemII -> 2, SemIII -> 3, SemIV -> 4, SemV -> 5, SemVI -> 6
    sem_str = sem_str.lower()
    if 'semv' in sem_str:
        if 'semvi' in sem_str:
            return 6
        return 5
    elif 'semiv' in sem_str:
        return 4
    elif 'semiii' in sem_str:
        return 3
    elif 'semii' in sem_str:
        return 2
    elif 'semi' in sem_str:
        return 1
    return 1

def get_code_mapping(code, filename, dept):
    code_upper = code.upper()
    filename_upper = filename.upper()
    
    if dept == "Chemistry":
        if "CHB-02A" in code_upper:
            return "CHEMD11", "CHB-02A"
        elif "CHB-04A" in code_upper:
            return "CHEMD21", "CHB-04A"
        elif "CHB-101" in code_upper:
            return "CHEMJ11 / CHEMN11", "CHB-101"
        elif "CHB-201" in code_upper:
            return "CHEMJ21 / CHEMN21", "CHB-201"
        elif "CHB-301" in code_upper or "CHB-361" in code_upper:
            return "CHEMJ32 / CHEMJ33", "CHB-301 / CHB-361"
        elif "CHB-401" in code_upper:
            return "CHEMJ41 / CHEMJ42", "CHB-401"
        elif "CHB-501" in code_upper:
            return "CHEMJ51", "CHB-501"
        elif "CHB-502" in code_upper:
            return "CHEMJ52", "CHB-502"
        elif "CHB-503" in code_upper:
            return "CHEMJ53", "CHB-503"
        elif "CHB-504" in code_upper:
            return "CHEMJ54", "CHB-504"
        elif "CHB-505" in code_upper:
            return "CHEMD31", "CHB-505"
        elif "CHB-601" in code_upper:
            return "CHEMJ61", "CHB-601"
        elif "CHB-602" in code_upper:
            return "CHEMJ62", "CHB-602"
        elif "CHB-603" in code_upper:
            return "CHEMJ63", "CHB-603"
        elif "CHB-604" in code_upper:
            return "CHEMJ64", "CHB-604"
        elif "CHB-605" in code_upper or "CHB-608" in code_upper:
            return "CHEMJ85 / CHEMJ8R5", "CHB-605 / CHB-608"
        return "N/A", code
        
    elif dept == "Physics":
        if "BPT-101" in code_upper:
            return "PHYMJ11 / PHYMN11", "BPT-101"
        elif "BSCU7A" in code_upper:
            return "PHYMN11", "BSCU7A"
        elif "BP-ANC-I" in code_upper:
            return "PHYMN21", "BP-Anc-I"
        elif "BPT-201" in code_upper:
            return "PHYMJ21 / PHYMN21", "BPT-201"
        elif "BPT-301" in code_upper:
            return "PHYMJ31", "BPT-301"
        elif "BPT-401" in code_upper:
            if "ELECTROMAGNETIC" in filename_upper:
                return "PHYMJ41 / PHYMN41", "BPT-401"
            elif "ELECTRONICS" in filename_upper:
                return "PHYMJ61", "BPT-401"
            return "PHYMJ41 / PHYMJ61", "BPT-401"
        elif "BPT-501" in code_upper:
            return "PHYMJ42", "BPT-501"
        elif "BPT-502" in code_upper:
            return "PHYMJ52", "BPT-502"
        elif "BPT-503" in code_upper:
            return "PHYMJ51", "BPT-503"
        elif "BPT-504" in code_upper:
            return "PHYMJ32", "BPT-504"
        elif "BPT-505" in code_upper:
            return "PHYMJ41 / PHYMN41", "BPT-505"
        elif "BPT-601" in code_upper:
            return "PHYMJ53", "BPT-601"
        elif "BPT-602" in code_upper:
            return "PHYMJ62", "BPT-602"
        elif "BPT-603" in code_upper:
            return "PHYMJ64", "BPT-603"
        elif "BPT-604" in code_upper:
            return "PHYMJ63", "BPT-604"
        elif "BPE-601" in code_upper:
            return "PHYMJ63", "BPE-601"
        elif "BPE-602" in code_upper:
            return "PHYMJ75", "BPE-602"
        elif "BSC-07A" in code_upper or "PHYSICS" in code_upper:
            return "PHYMN41", "BSC-07A"
        return "N/A", code
        
    return "N/A", code

def scan_tex_files():
    data = []
    
    # 1. Chemistry tex files
    chem_dir = "aaa/chemistry/tex_files"
    if os.path.exists(chem_dir):
        for f in os.listdir(chem_dir):
            if f.endswith(".tex") and not f.startswith("test_") and f != "test_clean.tex":
                filepath = os.path.join(chem_dir, f)
                # Parse name
                name_without_ext = f[:-4]
                parts = name_without_ext.split("_")
                if len(parts) >= 4:
                    code = parts[0]
                    subject_raw = parts[1]
                    sem_raw = parts[2]
                    year = parts[3]
                    
                    subject = camel_case_split(subject_raw)
                    semester = parse_semester(sem_raw)
                    nep_code, old_code = get_code_mapping(code, f, "Chemistry")
                    
                    data.append({
                        "code": code,
                        "subject": subject,
                        "semester": semester,
                        "year": year,
                        "department": "Chemistry",
                        "filePath": filepath,
                        "fileName": f,
                        "nepCode": nep_code,
                        "oldCode": old_code
                    })
                else:
                    print(f"Skipping Chemistry file due to pattern mismatch: {f}")
                    
    # 2. Physics tex files
    phys_dir = "aaa/PHYSICS OUT"
    if os.path.exists(phys_dir):
        for f in os.listdir(phys_dir):
            if f.endswith(".tex") and not f.startswith("test_"):
                filepath = os.path.join(phys_dir, f)
                name_without_ext = f[:-4]
                parts = name_without_ext.split("_")
                if len(parts) >= 4:
                    code = parts[0]
                    subject_raw = parts[1]
                    sem_raw = parts[2]
                    year = parts[3]
                    
                    subject = camel_case_split(subject_raw)
                    semester = parse_semester(sem_raw)
                    nep_code, old_code = get_code_mapping(code, f, "Physics")
                    
                    data.append({
                        "code": code,
                        "subject": subject,
                        "semester": semester,
                        "year": year,
                        "department": "Physics",
                        "filePath": filepath,
                        "fileName": f,
                        "nepCode": nep_code,
                        "oldCode": old_code
                    })
                else:
                    # Let's handle some alternative patterns if any
                    print(f"Skipping Physics file due to pattern mismatch: {f}")
                    
    # Sort data: department, semester, subject, year
    data.sort(key=lambda x: (x["department"], x["semester"], x["subject"], x["year"]))
    return data

def main():
    papers = scan_tex_files()
    print(f"Found {len(papers)} LaTeX paper files.")
    
    js_content = f"// Automatically generated NEP Curriculum LaTeX PYQ data\n"
    js_content += f"export const NEP_LATEX_PYQ_DATA = {json.dumps(papers, indent=2)};\n"
    
    out_dir = "js"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "nep-data.js")
    with open(out_path, "w", encoding="utf-8") as out_f:
        out_f.write(js_content)
        
    print(f"Successfully wrote data to {out_path}")

if __name__ == "__main__":
    main()
