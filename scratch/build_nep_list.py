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
        
    elif dept == "Computer Science":
        if code_upper in ["CS-101", "BSC-044"] or "CS-101" in code_upper:
            return "CSMJ11 / CSMN11", "CS-101"
        elif "CS-102" in code_upper:
            if "DIGITAL" in filename_upper:
                return "CSMJ21 / CSMN21", "CS-102"
            elif "OBJECT" in filename_upper or "OOP" in filename_upper:
                return "CSMJ22 / CSMN22", "CS-102"
            return "CSMJ21 / CSMN21", "CS-102"
        elif "BCS-201" in code_upper:
            return "CSMJ21 / CSMN21", "BCS-201"
        elif "BCS-203" in code_upper:
            return "CSMD11", "BCS-203"
        elif "CS-103" in code_upper or "BCS-301" in code_upper or "CSB-401" in code_upper:
            return "CSMJ31 / CSMN31", "CS-103"
        elif "CS-104" in code_upper or "BCS-401" in code_upper:
            return "CSMJ41 / CSMN41", "CS-104"
        elif "CS-105" in code_upper:
            if "DISCRETE" in filename_upper:
                return "CSMJ42 / CSMN42", "CS-105"
            elif "COMPUTER" in filename_upper:
                return "CSMJ41 / CSMN41", "CS-105"
            return "CSMJ42 / CSMN42", "CS-105"
        elif "BCS-403" in code_upper:
            return "CSMD11", "BCS-403"
        elif "CS-106" in code_upper or "BCS-502" in code_upper or "CSB-504" in code_upper:
            return "CSMJ51", "CS-106"
        elif "CS-107" in code_upper or "CSB-601" in code_upper:
            return "CSMJ52", "CS-107"
        elif "CS-108" in code_upper or "CSB-602" in code_upper:
            return "CSMJ53", "CS-108"
        elif "CS-109" in code_upper or "BCS-501" in code_upper or "CSB-502" in code_upper:
            return "CSMJ61", "CS-109"
        elif "BCS-503" in code_upper or "CSB-503" in code_upper:
            return "CSMJ42 / CSMN42", "BCS-503"
        elif "BCS-504A" in code_upper or "CSB-603A" in code_upper:
            return "CSMJ54", "BCS-504A"
        elif "CSB-501" in code_upper:
            return "CSMJ22 / CSMN22", "CSB-501"
        elif "CSB-604C" in code_upper:
            return "CSMJ64", "CSB-604C"
        elif "CS-403" in code_upper:
            return "CSMD11", "CS-403"
        elif code_upper.startswith("BVCA-"):
            digits = re.findall(r'\d+', code_upper)
            if digits:
                num = digits[0]
                sem = num[0]
                paper = num[-1]
                return f"BVCA{sem}{paper}", code
            return "BVCA11", code
        elif code_upper.startswith("GEN-"):
            digits = re.findall(r'\d+', code_upper)
            if digits:
                num = digits[0]
                sem = num[0]
                paper = num[-1]
                return f"GEN{sem}{paper}", code
            return "GEN11", code
        return "N/A", code
        
    return "N/A", code

def get_math_code_mapping(code):
    code_upper = code.upper()
    if "MTB-101" in code_upper:
        return "MATHJ11", "MTB-101"
    elif "MTB-102" in code_upper:
        return "MATHJ12", "MTB-102"
    elif "MTB-201" in code_upper:
        return "MATHJ21", "MTB-201"
    elif "MTB-202" in code_upper:
        return "MATHJ22", "MTB-202"
    elif "MTB-203" in code_upper or "MTB-AM-203" in code_upper:
        return "MATHD11", "MTB-203A / MTB-AM-203"
    elif "MTB-301" in code_upper:
        return "MATHJ31 / MATHJ32", "MTB-301"
    elif "MTB-302" in code_upper:
        return "MATHJ33 / MATHJ34", "MTB-302"
    elif "MTB-401" in code_upper:
        return "MATHJ41", "MTB-401"
    elif "MTB-402" in code_upper:
        return "MATHJ42", "MTB-402"
    elif "MTB-AM-403" in code_upper:
        return "MATHD21", "MTB-AM-403"
    elif "MTB-502" in code_upper:
        return "MATHJ52", "MTB-502"
    elif "MTB-601" in code_upper:
        return "MATHJ61", "MTB-601"
    elif "MTB-602" in code_upper:
        return "MATHJ62", "MTB-602"
    elif "MTB-603" in code_upper:
        return "MATHJ63", "MTB-603"
    elif "MTB-611" in code_upper:
        return "MATHJ64", "MTB-611"
    
    # Generic fallback pattern
    match = re.search(r'MTB-(?:AM-)?(\d+)', code_upper)
    if match:
        num = match.group(1)
        sem = num[0]
        if len(num) >= 3:
            return f"MATHJ{sem}1", code
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
                    
    # 3. Mathematics tex files
    math_dir = "aaa/latest corrected maths pdf/final maths export latex"
    if os.path.exists(math_dir):
        for f in os.listdir(math_dir):
            if f.endswith(".tex") and not f.startswith("test_"):
                filepath = os.path.join(math_dir, f)
                # Parse the file content to extract metadata
                with open(filepath, 'r', encoding='utf-8') as file_obj:
                    content = file_obj.read()
                
                # Extract code and subject
                code = "MTB-Unknown"
                subject = ""
                
                # Check for comment pattern: % Paper: MTB-101 : Calculus-I
                comment_match = re.search(r'%\s*Paper:\s*(MTB-[A-Z0-9-]+)\s*:\s*([^\n]+)', content, re.IGNORECASE)
                if comment_match:
                    code = comment_match.group(1).strip()
                    subject = comment_match.group(2).strip()
                else:
                    # Check for pdftitle: pdftitle={MTB-502: Abstract Algebra -- BHU PYQ}
                    pdf_match = re.search(r'pdftitle\s*=\s*\{\s*(MTB-[A-Z0-9-]+)\s*:\s*([^}-]+)', content, re.IGNORECASE)
                    if pdf_match:
                        code = pdf_match.group(1).strip()
                        subject = pdf_match.group(2).strip()
                    else:
                        # Check for fancyhead[R]: \fancyhead[R]{\small\textit{MTB-502: Abstract Algebra}}
                        fancy_match = re.search(r'\\fancyhead\[R\]\s*\{\s*\\small\\textit\s*\{\s*(MTB-[A-Z0-9-]+)\s*:\s*([^}]+)', content, re.IGNORECASE)
                        if fancy_match:
                            code = fancy_match.group(1).strip()
                            subject = fancy_match.group(2).strip()
                        else:
                            # Check for Paper No.: Paper No. MTB-502: Abstract Algebra
                            paper_match = re.search(r'Paper\s*(?:No\.)?\s*(MTB-[A-Z0-9-]+)\s*:\s*([^}\n\\]+)', content, re.IGNORECASE)
                            if paper_match:
                                code = paper_match.group(1).strip()
                                subject = paper_match.group(2).strip()
                
                # If subject is empty, try to parse from filename
                if not subject:
                    name_without_ext = f[:-4]
                    parts = name_without_ext.split('_')
                    if parts[0].startswith('MTB-'):
                        code = parts[0]
                        subject = camel_case_split(parts[1])
                    else:
                        subject = camel_case_split(parts[0])
                        # Search for MTB code in file
                        code_match = re.search(r'MTB-[A-Z0-9-]+', content)
                        if code_match:
                            code = code_match.group(0)
                
                # Parse Year
                year = ""
                # Try from filename first: e.g. MTB-101_Calculus-I_BSc-SemI_2023-24.tex or AbstractAlgebra_SemV_2022-23.tex
                year_match = re.search(r'(\d{4}-\d{2}|\d{4}-\d{4})', f)
                if year_match:
                    year = year_match.group(1)
                else:
                    # Try from content: e.g. "Examination, 2023-24"
                    exam_match = re.search(r'Examination,\s*(\d{4}-\d{2}|\d{4}-\d{4})', content)
                    if exam_match:
                        year = exam_match.group(1)
                    else:
                        year = "2023-24" # Default
                
                # Parse Semester
                semester = 1
                # Try from filename first
                sem_match = re.search(r'Sem\s*([I|V]+)', f, re.IGNORECASE)
                if sem_match:
                    semester = parse_semester("Sem" + sem_match.group(1))
                else:
                    # Try from content
                    sem_content_match = re.search(r'Semester\s*([I|V]+)', content, re.IGNORECASE)
                    if sem_content_match:
                        semester = parse_semester("Sem" + sem_content_match.group(1))
                
                # Clean subject
                subject = subject.replace('--', '').replace('BHU PYQ', '').replace('BHU', '').strip()
                
                # Map codes
                nep_code, old_code = get_math_code_mapping(code)
                
                data.append({
                    "code": code,
                    "subject": subject,
                    "semester": semester,
                    "year": year,
                    "department": "Mathematics",
                    "filePath": filepath,
                    "fileName": f,
                    "nepCode": nep_code,
                    "oldCode": old_code
                })

    # 4. Computer Science tex files
    cs_dir = "aaa/cs"
    if os.path.exists(cs_dir):
        for f in os.listdir(cs_dir):
            if f.endswith(".tex") and not f.startswith("test_"):
                filepath = os.path.join(cs_dir, f)
                name_without_ext = f[:-4]
                parts = name_without_ext.split("_")
                if len(parts) >= 4 or f.startswith("CS-101_BCS-101"):
                    if f.startswith("CS-101_BCS-101"):
                        code = "CS-101"
                        subject_raw = "ProblemSolvingC"
                        sem_raw = "SemI"
                        year = "2016-17"
                    else:
                        code = parts[0]
                        subject_raw = parts[1]
                        sem_raw = parts[2]
                        year = parts[3]
                    
                    subject = camel_case_split(subject_raw)
                    semester = parse_semester(sem_raw)
                    nep_code, old_code = get_code_mapping(code, f, "Computer Science")
                    
                    data.append({
                        "code": code,
                        "subject": subject,
                        "semester": semester,
                        "year": year,
                        "department": "Computer Science",
                        "filePath": filepath,
                        "fileName": f,
                        "nepCode": nep_code,
                        "oldCode": old_code
                    })
                else:
                    print(f"Skipping Computer Science file due to pattern mismatch: {f}")

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
