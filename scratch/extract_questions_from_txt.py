import re

with open("scratch/all_physics_pyqs_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split by file header
files_data = text.split("=========================================\nFILE: ")
subjects_questions = {}

for section in files_data:
    section = section.strip()
    if not section:
        continue
    
    # The first line of each section is now the filename
    lines = section.split("\n")
    file_name = lines[0].strip()
    
    # Identify code
    code = file_name.split("_")[0]
    
    # We map the code to one of our 14 unique subject keys
    key = None
    if code.startswith("BPT-101") or code.startswith("BSCU7A"):
        key = "phymj11" # Mechanics
    elif code.startswith("BPT-201") or code.startswith("BP-Anc-I"):
        key = "phymj21" # Thermal
    elif code.startswith("BPT-301"):
        key = "phymj31" # Optics
    elif code.startswith("BPT-401") and "Electromagnetic" in file_name:
        key = "phymj41" # Electromagnetic Theory
    elif code.startswith("BPT-401") and "Electronics" in file_name:
        key = "phymj61" # Electronic Circuits
    elif code.startswith("BPT-501"):
        key = "phymj42" # Mathematical Physics
    elif code.startswith("BPT-502"):
        key = "phymj52" # Classical Mechanics
    elif code.startswith("BPT-503"):
        key = "phymj51" # Quantum Mechanics
    elif code.startswith("BPT-504"):
        key = "phymj32" # Semiconductor Devices
    elif code.startswith("BPT-505"):
        key = "phymj41" # Electromagnetic Theory
    elif code.startswith("BPT-601"):
        key = "phymj53" # Statistical Mechanics
    elif code.startswith("BPT-602"):
        key = "phymj62" # Solid State Physics
    elif code.startswith("BPT-603"):
        key = "phymj64" # Nuclear Physics
    elif code.startswith("BPT-604") or code.startswith("BPE-601"):
        key = "phymj63" # Atomic/Modern Physics
    elif code.startswith("BPE-602"):
        key = "phymj75" # Nanoscience
    elif code.startswith("BSC-07A") or code == "PHYSICS":
        key = "phymj41" # Ancillary physics is mostly electromagnetism/waves
        
    if not key:
        continue
        
    if key not in subjects_questions:
        subjects_questions[key] = []
        
    # Extract questions based on common numbering patterns:
    # e.g., "Question 1", "(a)", "(b)", etc.
    lines = section.split("\n")
    current_q = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Match starting with Question/Q. or subquestions (a), (b), (c), (d), (i), (ii)
        # or starting with numbers followed by period/parenthesis
        is_new_q = False
        if re.match(r"^(Question\s*\d+|Q\d+|Answer\s*any|Answer\s*all)", line, re.IGNORECASE):
            is_new_q = True
        elif re.match(r"^(\([a-z]\)|\d+\.|[a-z]\))", line):
            is_new_q = True
            
        if is_new_q:
            if current_q:
                clean_q = re.sub(r"\s+", " ", current_q).strip()
                if len(clean_q) > 20: # ignore short headings
                    subjects_questions[key].append(clean_q)
            current_q = line
        else:
            if current_q:
                current_q += " " + line
                
    if current_q:
        clean_q = re.sub(r"\s+", " ", current_q).strip()
        if len(clean_q) > 20:
            subjects_questions[key].append(clean_q)

print("=== EXTRACTED QUESTIONS COUNT ===")
for k, qs in subjects_questions.items():
    print(f"Key: {k}, Count: {len(qs)}")
    # Print first 2 questions as sample
    for q in qs[:2]:
        print(f"  - {q}")
