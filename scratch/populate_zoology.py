import os
import re
import json

# =============================================================================
# 1. Zoology Syllabi & Mappings
# =============================================================================
ZOOLOGY_SYLLABI = {
    "zobmj11": {
        "title": "Animal Diversity and Animal Form & Function",
        "module": "ZOOMJ11 / ZOOMN11",
        "standard_questions": [
            ("Describe the classification of animal kingdom up to phylum level with diagnostic characters.", "I"),
            ("Explain the structure of a typical animal cell with a neat labeled diagram.", "II"),
            ("Give a detailed account of the nervous system of non-chordates.", "III"),
            ("State the general properties of chordates and compare them with non-chordates.", "IV"),
            ("Describe the mechanisms of digestion and absorption in mammals.", "V")
        ]
    },
    "zobmj21": {
        "title": "Fundamentals of Cell Biology and Biochemistry",
        "module": "ZOOMJ21 / ZOOMN21",
        "standard_questions": [
            ("Describe the structure of cell membrane and explain fluid mosaic model.", "I"),
            ("Explain the structure and functions of mitochondria.", "II"),
            ("Describe the pathway of glycolysis with all intermediates and enzymes.", "III"),
            ("Explain the mechanism of oxidative phosphorylation and ATP synthesis.", "IV"),
            ("Compare mitosis and meiosis with the help of suitable diagrams.", "V")
        ]
    },
    "zobmn21": {
        "title": "Ancillary Biology (Animal Biology)",
        "module": "ZOOMN21",
        "standard_questions": [
            ("Describe the Darwinian theory of natural selection and its significance.", "I"),
            ("Explain the structure of an eukaryotic cell with a labeled diagram.", "II"),
            ("Compare the processes of mitosis and meiosis in detail.", "III"),
            ("Describe the mechanism of enzyme action and factors affecting it.", "IV"),
            ("Explain the counter current mechanism in kidney during urine formation.", "V")
        ]
    },
    "zobmj31": {
        "title": "Basic Genetics, Evolution and Developmental Biology",
        "module": "ZOOMJ31",
        "standard_questions": [
            ("State Mendel's laws of inheritance and explain them with examples.", "I"),
            ("Describe the structure of DNA and its replication mechanism.", "II"),
            ("Explain the concept of linkage and crossing over in genetics.", "III"),
            ("Describe the various stages of embryonic development in frog.", "IV"),
            ("Explain the synthetic theory of organic evolution with evidence.", "V")
        ]
    },
    "zobmj41": {
        "title": "Fundamental Endocrinology and Developmental Biology",
        "module": "ZOOMJ41 / ZOOMJ42",
        "standard_questions": [
            ("Describe the anatomy and hormones secreted by pituitary gland.", "I"),
            ("Explain the feedback mechanism of hormone action with examples.", "II"),
            ("Describe the stages of spermatogenesis and oogenesis in mammals.", "III"),
            ("Explain the process of fertilization and prevention of polyspermy.", "IV"),
            ("Describe the types of placenta in mammals based on histology.", "V")
        ]
    },
    "zobmn41": {
        "title": "Biology: Applied Zoology (Ancillary Course)",
        "module": "ZOOMN41",
        "standard_questions": [
            ("Describe the life cycle and pathogenicity of Entamoeba histolytica.", "I"),
            ("Explain the symptoms, transmission and control of malaria.", "II"),
            ("Describe the social organization and communication in honeybees.", "III"),
            ("Explain the techniques and significance of sericulture.", "IV"),
            ("Describe the culture of lac insect and economic importance of lac.", "V")
        ]
    },
    "zobmj51": {
        "title": "Functional Anatomy of Non-chordates",
        "module": "ZOOMJ51",
        "standard_questions": [
            ("Describe the different types of canal system in sponges with neat diagrams.", "I"),
            ("Explain the life history and larval stages of Fasciola hepatica.", "II"),
            ("Illustrate the structure of Euglena viridis and describe its movement.", "III"),
            ("Give a detailed account of male and female reproductive systems of Palaemon.", "IV"),
            ("Describe the water vascular system of starfish and its role in locomotion.", "V")
        ]
    },
    "zobmj52": {
        "title": "Functional Anatomy of Chordates",
        "module": "ZOOMJ52",
        "standard_questions": [
            ("Describe the anatomical structure and affinities of Balanoglossus.", "I"),
            ("Explain retrogressive metamorphosis in Herdmania with diagrams.", "II"),
            ("Give a comparative account of the brain of different vertebrates.", "III"),
            ("Describe the respiratory system and mechanism of flight in birds.", "IV"),
            ("Explain the origin, evolution and classification of mammals.", "V")
        ]
    },
    "zobmj53": {
        "title": "Biochemistry and Molecular Biology",
        "module": "ZOOMJ53",
        "standard_questions": [
            ("Describe the classification, structure and properties of proteins.", "I"),
            ("Explain the double helical structure of DNA and its replication.", "II"),
            ("Describe the process of transcription and RNA processing in eukaryotes.", "III"),
            ("Explain the mechanism of translation and genetic code features.", "IV"),
            ("Describe the regulation of gene expression in prokaryotes (lac operon).", "V")
        ]
    },
    "zobmj54": {
        "title": "Biotechniques",
        "module": "ZOOMJ54",
        "standard_questions": [
            ("Describe the principles and applications of spectrophotometry.", "I"),
            ("Explain the technique and applications of PCR (Polymerase Chain Reaction).", "II"),
            ("Describe the principles of agarose and polyacrylamide gel electrophoresis.", "III"),
            ("Explain the working and applications of chromatography techniques.", "IV"),
            ("Describe the methods and applications of recombinant DNA technology.", "V")
        ]
    },
    "zobmj55": {
        "title": "Environmental Biology and Systematics",
        "module": "ZOOMJ55",
        "standard_questions": [
            ("Define ecosystem and explain energy flow through different trophic levels.", "I"),
            ("Describe the various types of ecological adaptations in desert animals.", "II"),
            ("Explain the principles of animal taxonomy and taxonomic hierarchy.", "III"),
            ("Describe the concept of species and mechanisms of speciation.", "IV"),
            ("Explain the impacts of global warming and ozone depletion on biodiversity.", "V")
        ]
    },
    "zobmj61": {
        "title": "Mammalian Physiology",
        "module": "ZOOMJ61",
        "standard_questions": [
            ("Describe the mechanism of breathing and transport of oxygen and CO2.", "I"),
            ("Explain the cardiac cycle and regulation of heart beat in mammals.", "II"),
            ("Describe the mechanism of urine formation and counter current system.", "III"),
            ("Explain the transmission of nerve impulses along a myelinated nerve fiber.", "IV"),
            ("Describe the mechanism of muscle contraction (sliding filament theory).", "V")
        ]
    },
    "zobmj62": {
        "title": "Cell Biology, Genetics and Evolution",
        "module": "ZOOMJ62",
        "standard_questions": [
            ("Describe the structure and functions of Golgi apparatus and lysosomes.", "I"),
            ("Explain the molecular mechanism of cell cycle regulation (CDKs/cyclins).", "II"),
            ("Describe the chromosomal basis of sex determination in animals.", "III"),
            ("Explain the concepts of gene mutations and DNA repair mechanisms.", "IV"),
            ("Describe the geological time scale and evolutionary history of horse.", "V")
        ]
    },
    "zobmj63": {
        "title": "Immunology, Microbiology, Environmental Biology and Biotechniques",
        "module": "ZOOMJ63",
        "standard_questions": [
            ("Describe the structure of an antibody molecule with a labeled diagram.", "I"),
            ("Explain the differences between humoral and cell-mediated immune responses.", "II"),
            ("Describe the lytic and lysogenic cycles of bacteriophages.", "III"),
            ("Explain the role of microorganisms in nitrogen cycle and waste treatment.", "IV"),
            ("Describe the principles and applications of ELISA in disease diagnosis.", "V")
        ]
    },
    "zobmj64": {
        "title": "Evolution and Animal Behaviour",
        "module": "ZOOMJ64",
        "standard_questions": [
            ("Describe the evidence of evolution from embryology and fossil record.", "I"),
            ("Explain the concept of natural selection and industrial melanism.", "II"),
            ("Describe the various types of learning behavior in animals with examples.", "III"),
            ("Explain the social organization and communication in social insects.", "IV"),
            ("Describe biological rhythms and migration behavior in birds.", "V")
        ]
    },
    "zobmj65": {
        "title": "Immunology and Parasitology",
        "module": "ZOOMJ65",
        "standard_questions": [
            ("Describe the cells and organs of the mammalian immune system.", "I"),
            ("Explain the structure and classes of immunoglobulins.", "II"),
            ("Describe the life cycle, pathogenicity and control of Ascaris lumbricoides.", "III"),
            ("Explain the host-parasite relationships and parasitic adaptations.", "IV"),
            ("Describe the modes of transmission and prevention of parasitic diseases.", "V")
        ]
    }
}

FILE_TO_KEY = {
    "ZOB-101": "zobmj11",
    "ZOB-201": "zobmj21",
    "ZOB-201_OLD": "zobmj21",
    "ZOB-203A": "zobmn21",
    "ZOB-301": "zobmj31",
    "ZOB-401": "zobmj41",
    "ZOB-403A": "zobmn41",
    "ZOB-501": "zobmj51",
    "ZOB-502": "zobmj52",
    "ZOB-503": "zobmj53",
    "ZOB-504": "zobmj54",
    "ZOB-505": "zobmj55",
    "ZOB-601": "zobmj61",
    "ZOB-602": "zobmj62",
    "ZOB-603": "zobmj63",
    "ZOB-604": "zobmj64",
    "ZOB-605": "zobmj65",
}

# =============================================================================
# 2. Text Cleaning & LaTeX Parsing Logic
# =============================================================================
def clean_text(text):
    text = re.sub(r'\\pts\{[^\}]*\}', '', text)
    text = re.sub(r'\\hfill', '', text)
    text = re.sub(r'\\s*\\(small|me|big)skip', '', text)
    text = re.sub(r'\\noindent', '', text)
    text = re.sub(r'\\rule\{[^\}]*\}\{[^\}]*\}', '', text)
    text = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^\}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^\}]*)\}', r'\1', text)
    text = text.replace('~', ' ')
    text = re.sub(r'\\\\(?:\[[^\]]*\])?', ' ', text)
    text = text.replace(r'\[', '$')
    text = text.replace(r'\]', '$')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_code_from_filename(filename):
    m = re.search(r'(ZOB-\d+[A-Z]?(?:_OLD)?)', filename.upper())
    return m.group(1) if m else None

def parse_tex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'(?m)^%.*$', '', content)

    parts_questions = []
    parts_matches = re.finditer(r'\\begin\{(parts|romanparts)\}(.*?)\\end\{\1\}', content, re.DOTALL)
    for match in parts_matches:
        parts_content = match.group(2)
        items = re.split(r'\\item', parts_content)
        for item in items[1:]:
            cleaned = clean_text(item)
            if len(cleaned) > 20:
                parts_questions.append(cleaned)

    main_questions = []
    matches = re.findall(
        r'\\textbf\{\s*Question\s*([0-9]+)\.\}\s*(.*?)(?=\\pts|\\hfill|\\medskip|\\noindent|\\vfill|\\begin\{center\}|\Z)',
        content, re.DOTALL
    )
    for q_num, q_text in matches:
        cleaned = clean_text(q_text)
        short_notes_phrases = ["short notes on", "attempt any", "define or answer", "write notes on any"]
        skip = any(ph in cleaned.lower() for ph in short_notes_phrases)
        if len(cleaned) > 20 and not skip:
            main_questions.append(cleaned)

    return main_questions + parts_questions

# =============================================================================
# 3. Rich Markdown Answer Keys for Zoology
# =============================================================================
def get_answer_key(subject_key, q_text):
    q_lower = q_text.lower()
    
    # 1. Sponges / Canal System
    if "canal system" in q_lower or "sponges" in q_lower:
        return ("1. **Canal System Concept**: Unique water circulation system in sponges (Phylum Porifera) essential for food gathering, respiration, and excretion.\n"
                "2. **Asconoid System** (Simplest):\n- Path: Ostia $\\to$ Spongocoel (lined with choanocytes) $\\to$ Osculum.\n"
                "3. **Syconoid System**:\n- Path: Incurrent canals $\\to$ Prosopyles $\\to$ Radial canals (lined with choanocytes) $\\to$ Apopyles $\\to$ Spongocoel $\\to$ Osculum.\n"
                "4. **Leuconoid System** (Most complex):\n- Path: Incurrent canals $\\to$ Flagellated chambers $\\to$ Excurrent canals $\\to$ Osculum.")
    
    # 2. Fasciola
    elif "fasciola" in q_lower or "liver fluke" in q_lower:
        return ("1. **Life History of Fasciola hepatica**: Digenetic parasite (primary host: sheep/cattle; secondary host: snail *Lymnaea*).\n"
                "2. **Larval Stages**:\n- **Miracidium**: Free-swimming ciliated larva, enters snail.\n- **Sporocyst**: Sac-like structure inside snail, produces Rediae.\n- **Redia**: Has mouth and gut, produces Cercariae.\n- **Cercaria**: Free-swimming tadpole-like larva, leaves snail and encysts on vegetation.\n- **Metacercaria**: Encysted infective stage ingested by sheep.")
    
    # 3. Euglena
    elif "euglena" in q_lower:
        return ("1. **Structure of Euglena viridis**: Unicellular flagellate protist. Spindle-shaped body with a flexible proteinaceous **pellicle**.\n"
                "2. **Key Organelles**:\n- **Flagellum**: Long hair-like structure emerging from the reservoir for locomotion.\n- **Stigma (Eyespot)**: Red-pigmented photoreceptor for phototaxis.\n- **Contractile Vacuole**: Osmo-regulation.\n- **Chloroplasts**: Perform photosynthesis in light.\n"
                "3. **Locomotion**:\n- **Flagellar**: Propulsive movement by flagellum.\n- **Euglenoid movement (Metaboly)**: Peristaltic wave of contraction and expansion of the body.")
    
    # 4. Palaemon / Prawn
    elif "palaemon" in q_lower or "prawn" in q_lower:
        return ("1. **Reproductive System of Palaemon (Prawn)**: Dioecious (separate sexes).\n"
                "2. **Male System**:\n- Pair of elongated testes located above the hepato-pancreas.\n- Vas deferens carries sperm to seminal vesicles.\n- Sperms are released via male genital pores on 5th walking legs.\n"
                "3. **Female System**:\n- Pair of crescent-shaped ovaries.\n- Oviducts open via female genital pores on 3rd walking legs.\n- Fertilization is external, and females carry eggs on their pleopods.")
    
    # 5. Starfish / Water Vascular System
    elif "starfish" in q_lower or "asterias" in q_lower or "water vascular" in q_lower:
        return ("1. **Water Vascular (Ambulacral) System**: Specialized hydrostatic system in starfish (Echinodermata) used for locomotion, respiration, and food capture.\n"
                "2. **Pathway of Water**:\n- Madreporite $\\to$ Stone canal $\\to$ Ring canal $\\to$ Radial canals (along arms) $\\to$ Lateral canals $\\to$ Tube feet.\n"
                "3. **Tube Feet Mechanism**:\n- Each tube foot has an **ampulla** (muscular sac) and a **podium** (sucker).\n- Contraction of the ampulla forces water into the podium, extending it. Contact with substratum and retraction pulls the animal forward.")
    
    # 6. Ascaris
    elif "ascaris" in q_lower:
        return ("1. **Life History of Ascaris lumbricoides**: Monogenetic human intestinal roundworm. Infection occurs by ingesting embryonated eggs containing L2 larvae.\n"
                "2. **Migration Pathway**:\n- Ingested eggs hatch in the small intestine.\n- Larvae penetrate the intestinal wall $\\to$ Portal circulation $\\to$ Liver $\\to$ Heart $\\to$ Lungs (undergo 2nd & 3rd moults).\n- Migrate up the trachea $\\to$ Pharynx $\\to$ Swallowed back into the intestine where they mature (4th moult).\n"
                "3. **Pathogenicity**: Causes **Ascariasis**, characterized by abdominal pain, intestinal blockage, nutritional deficiency, and pulmonary symptoms (Loeffler's syndrome).")
    
    # 7. Cell structures & organelles
    elif "mitochondria" in q_lower or "mitochondrion" in q_lower:
        return ("1. **Structure**: Double-membraned organelle. Outer membrane is smooth; inner membrane is folded into **cristae** containing ATP synthase complexes (F0-F1 particles).\n"
                "2. **Function**: Powerhouse of the cell. Site of aerobic cellular respiration, including Krebs cycle (matrix) and Electron Transport Chain (inner membrane).\n"
                "3. **Semiautonomous nature**: Possesses circular DNA and 70S ribosomes.")
    elif "golgi" in q_lower:
        return ("1. **Structure**: Composed of flattened membrane-bound sacs called **cisternae**, with a cis-face (receiving side) and trans-face (shipping side).\n"
                "2. **Function**: Modifies, packages, and sorts proteins and lipids received from the endoplasmic reticulum. Forms lysosomes and secretes vesicles.")
    
    # 8. Cell Division
    elif "mitosis" in q_lower or "meiosis" in q_lower:
        return ("1. **Mitosis**: Equational division producing two genetically identical diploid daughter cells. Stages: Prophase, Metaphase (chromosomes align at plate), Anaphase (sister chromatids separate), Telophase.\n"
                "2. **Meiosis**: Reductional division producing four genetically diverse haploid gametes. Consists of Meiosis I (homologous chromosomes separate) and Meiosis II (sister chromatids separate).\n"
                "3. **Genetic Variation**: Driven by crossing over (Pachynene stage of Prophase I) and independent assortment during Metaphase I.")
    
    # 9. General Endocrinology / Hormones
    elif "hormone" in q_lower or "endocrin" in q_lower or "pituitary" in q_lower:
        return ("1. **Hormones Concept**: Chemical messengers secreted directly into blood by ductless **endocrine glands** to regulate physiological activities.\n"
                "2. **Pituitary Gland (Master Gland)**:\n- **Adenohypophysis (Anterior)**: Secretes GH, TSH, ACTH, FSH, LH, and Prolactin.\n- **Neurohypophysis (Posterior)**: Releases Oxytocin and Vasopressin (ADH) synthesized by hypothalamus.\n"
                "3. **Feedback Mechanism**: Homeostasis maintained by negative feedback loops (e.g., high thyroid hormone levels inhibit TSH and TRH secretion).")
    
    # 10. Kidney & Excretion
    elif "kidney" in q_lower or "nephron" in q_lower or "counter current" in q_lower:
        return ("1. **Nephron Structure**: Structural and functional unit of kidney. Comprises Bowman's capsule, Glomerulus (filtration), PCT, Loop of Henle, DCT, and Collecting duct.\n"
                "2. **Counter-Current Multiplier System**:\n- Maintained by the Loop of Henle and **Vasa Recta**.\n- Descending limb is permeable to water, concentrating the filtrate. Ascending limb actively pumps out NaCl, diluting the filtrate and building a hyper-osmotic renal medullary interstitium.\n- This allows collecting ducts to reabsorb water, producing concentrated urine.")
    
    # 11. Parasitic Adaptations
    elif "parasitic adaptation" in q_lower or "taenia" in q_lower:
        return ("1. **Taenia (Tapeworm) Adaptations**:\n- **Morphological**: Scolex with hooks and suckers for attachment; thick protective tegument resisting host digestive enzymes; complete loss of digestive system (nutrients absorbed directly through body surface).\n- **Physiological**: Anaerobic respiration; high reproductive capacity (proglottid maturation and self-fertilization).")
    
    # 12. Larval Forms / Trochophore
    elif "trochophore" in q_lower:
        return ("1. **Trochophore Larva**: Free-swimming, pear-shaped ciliated larval form characteristic of marine annelids and molluscs.\n"
                "2. **Features**: Has an apical tuft of sensory cilia at the top, a band of cilia (prototroch) for locomotion and feeding, a complete digestive tract (mouth, stomach, anus), and protonephridia.")
    
    # 13. Torsion
    elif "torsion" in q_lower:
        return ("1. **Torsion in Gastropods**: 180-degree counterclockwise rotation of the visceral mass, mantle, and mantle cavity during larval development.\n"
                "2. **Consequences**: Brings the mantle cavity and anus to the anterior position above the head. Loops the digestive tract and nervous system (streptoneury).\n"
                "3. **Significance**: Provides protection for the head (retracted into shell first) and head-oriented sensory organs.")

    return ("1. **Zoology Core Principle**:\n- Apply fundamental animal biology concepts (anatomy, physiology, cell biology, genetics, or ecology).\n"
            "2. **Mechanisms & Structures**:\n- Detail structural anatomy or biochemical/physiological pathways with precise terminology.\n- Emphasize evolutionary adaptations and functional relationships.\n"
            "3. **Diagrams**:\n- Essential to include labeled sketches showing anatomical cross-sections, body systems, or cellular diagrams.\n"
            "4. **Significance**:\n- Analyze the ecological, evolutionary, or clinical relevance of the topic in animal science.")

# =============================================================================
# 4. Main script execution
# =============================================================================
def main():
    print("=== Populating Zoology PYQ and Exam data ===\n")
    
    latex_dir = "/Users/aryanmaurya/exam portal/aaa/zoology/latex_outputs"
    files = [f for f in os.listdir(latex_dir) if f.endswith('.tex')]
    
    print(f"Found {len(files)} Zoology LaTeX (.tex) files.")

    # 1. Parse and compile questions per subject key
    questions_by_key = {}
    for file_name in files:
        code = get_code_from_filename(file_name)
        if not code:
            continue
        key = FILE_TO_KEY.get(code)
        if not key:
            continue
        
        filepath = os.path.join(latex_dir, file_name)
        try:
            questions = parse_tex_file(filepath)
            if key not in questions_by_key:
                questions_by_key[key] = []
            questions_by_key[key].extend(questions)
        except Exception as e:
            print(f"  Error parsing {file_name}: {e}")

    # 2. Update js/exams-data.js
    exams_js_path = "/Users/aryanmaurya/exam portal/js/exams-data.js"
    with open(exams_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Extract current EXAMS object
    marker = "export const EXAMS = "
    start_idx = js_content.find(marker)
    if start_idx == -1:
        print("ERROR: Could not find EXAMS object in js/exams-data.js")
        return
        
    obj_start = start_idx + len(marker)
    # Parse JSON (cleaning trailing semicolons/comments)
    js_raw_obj = js_content[obj_start:].strip()
    if js_raw_obj.endswith(";"):
        js_raw_obj = js_raw_obj[:-1]
    
    EXAMS = json.loads(js_raw_obj)
    print(f"Current EXAMS object has {len(EXAMS)} subjects.")

    # Populate Zoology exams
    for key, syllabus in ZOOLOGY_SYLLABI.items():
        raw_qs = list(set(questions_by_key.get(key, [])))
        # Pad with standard questions to ensure rich mock test experience
        padding_needed = 20 - len(raw_qs)
        for std_q, unit in syllabus["standard_questions"]:
            if std_q not in raw_qs:
                raw_qs.append(std_q)
        
        formatted_questions = []
        for idx, q_text in enumerate(raw_qs):
            q_id = idx + 1
            
            # Group into units dynamically
            if idx < 5: unit = "I"
            elif idx < 10: unit = "II"
            elif idx < 15: unit = "III"
            elif idx < 20: unit = "IV"
            else: unit = "V"

            ans_key = get_answer_key(key, q_text)
            formatted_questions.append({
                "id": q_id,
                "unit": unit,
                "question": q_text,
                "answerKey": ans_key
            })

        EXAMS[key] = {
            "id": key,
            "title": syllabus["title"],
            "module": syllabus["module"],
            "duration": 60,
            "type": "theory",
            "comingSoon": False,
            "questions": formatted_questions
        }
        print(f"  {key} ({syllabus['title']}): populated with {len(formatted_questions)} questions")

    # Save exams-data.js
    output_str = f"// Automatically generated exam data\nexport const EXAMS = {json.dumps(EXAMS, indent=2)};\n"
    with open(exams_js_path, "w", encoding="utf-8") as f:
        f.write(output_str)
    print("\n[SUCCESS] js/exams-data.js updated!")

    # =============================================================================
    # 5. Update js/nep-data.js with Zoology metadata
    # =============================================================================
    nep_data_path = "/Users/aryanmaurya/exam portal/js/nep-data.js"
    with open(nep_data_path, "r", encoding="utf-8") as f:
        nep_content = f.read()

    # Extract paper metadata from latex headers to build entries
    zoology_nep_metadata = []
    
    # Track existing codes and titles to avoid duplicates
    course_name_map = {}
    for file_name in sorted(files):
        code = get_code_from_filename(file_name)
        if not code:
            continue
        key = FILE_TO_KEY.get(code)
        if not key:
            continue
            
        # Extract title and year
        filepath = os.path.join(latex_dir, file_name)
        with open(filepath, 'r', encoding='utf-8') as f:
            f_content = f.read()
            
        paper_name = None
        paper_line_m = re.search(r'Paper:\s*ZOB-\w+\s*\\*---+\s*(.*?)(?=\\\\|\\\[|\]|\n|\Z)', f_content)
        if paper_line_m:
            paper_name = paper_line_m.group(1).strip().rstrip('}').strip()
        if not paper_name:
            paper_line_m2 = re.search(r'Paper:\s*ZOB-\w+\s*\\*---*\s*(.*?)(?=\\\\|\\\[|\]|\n|\Z)', f_content)
            if paper_line_m2:
                paper_name = paper_line_m2.group(1).strip().rstrip('}').strip()
        
        if paper_name:
            paper_name = re.sub(r'\\textbf\{([^\}]*)\}', r'\1', paper_name)
            paper_name = re.sub(r'\\textit\{([^\}]*)\}', r'\1', paper_name)
            paper_name = paper_name.replace(r'\&', '&').strip()
        else:
            paper_name = ZOOLOGY_SYLLABI.get(key, {}).get("title", code)

        # Semester extraction
        # Normalize and find roman or ordinal semesters
        file_name_upper = file_name.upper()
        sem = 1
        if "VI-SEM" in file_name_upper or "VI_SEM" in file_name_upper or "6TH" in file_name_upper or "SEM-VI" in file_name_upper or "SEM_VI" in file_name_upper or "SEM-6" in file_name_upper:
            sem = 6
        elif "V-SEM" in file_name_upper or "V_SEM" in file_name_upper or "5TH" in file_name_upper or "SEM-V" in file_name_upper or "SEM_V" in file_name_upper or "SEM-5" in file_name_upper:
            sem = 5
        elif "IV-SEM" in file_name_upper or "IV_SEM" in file_name_upper or "4TH" in file_name_upper or "SEM-IV" in file_name_upper or "SEM_IV" in file_name_upper or "SEM-4" in file_name_upper:
            sem = 4
        elif "III-SEM" in file_name_upper or "III_SEM" in file_name_upper or "3RD" in file_name_upper or "SEM-III" in file_name_upper or "SEM_III" in file_name_upper or "SEM-3" in file_name_upper:
            sem = 3
        elif "II-SEM" in file_name_upper or "II_SEM" in file_name_upper or "2ND" in file_name_upper or "SEM-II" in file_name_upper or "SEM_II" in file_name_upper or "SEM-2" in file_name_upper:
            sem = 2
        elif "I-SEM" in file_name_upper or "I_SEM" in file_name_upper or "1ST" in file_name_upper or "SEM-I" in file_name_upper or "SEM_I" in file_name_upper or "SEM-1" in file_name_upper:
            sem = 1

        # Year extraction
        year_m = re.search(r'(\d{4})[-_](\d{2,4})', file_name)
        year = "2023-24"
        if year_m:
            y1 = year_m.group(1)
            y2 = year_m.group(2)
            if len(y2) == 4: y2 = y2[2:]
            year = f"{y1}-{y2}"
        elif "even14" in file_name or "odd14" in file_name:
            year = "2013-14"
        elif "odd16" in file_name:
            year = "2016-17"

        # Generate nepCode and oldCode
        nep_code = ZOOLOGY_SYLLABI.get(key, {}).get("module", code)
        
        zoology_nep_metadata.append({
            "code": code,
            "subject": paper_name,
            "semester": sem,
            "year": year,
            "department": "Zoology",
            "filePath": f"aaa/zoology/latex_outputs/{file_name}",
            "fileName": file_name,
            "nepCode": nep_code,
            "oldCode": code
        })
        
        # Save to course_name_map for updating nep-papers.html later
        course_name_map[nep_code] = paper_name

    # Parse and append to NEP_LATEX_PYQ_DATA list in nep-data.js
    marker_nep = "export const NEP_LATEX_PYQ_DATA = "
    nep_start = nep_content.find(marker_nep)
    if nep_start != -1:
        obj_start_nep = nep_start + len(marker_nep)
        raw_nep_obj = nep_content[obj_start_nep:].strip()
        if raw_nep_obj.endswith(";"):
            raw_nep_obj = raw_nep_obj[:-1]
        
        NEP_DATA = json.loads(raw_nep_obj)
        
        # Remove existing Zoology entries to avoid duplicates
        NEP_DATA = [p for p in NEP_DATA if p.get("department") != "Zoology"]
        
        # Add new ones
        NEP_DATA.extend(zoology_nep_metadata)
        
        # Save js/nep-data.js
        with open(nep_data_path, "w", encoding="utf-8") as f:
            f.write(f"export const NEP_LATEX_PYQ_DATA = {json.dumps(NEP_DATA, indent=2)};\n")
        print(f"[SUCCESS] js/nep-data.js updated with {len(zoology_nep_metadata)} Zoology entries!")

    # =============================================================================
    # 6. Update subjects.html
    # =============================================================================
    subjects_path = "/Users/aryanmaurya/exam portal/subjects.html"
    with open(subjects_path, "r", encoding="utf-8") as f:
        subjects_content = f.read()

    # Generate EXAM_PYQS mapping entries for Zoology
    zoology_pyq_entries = {}
    for item in zoology_nep_metadata:
        ekey = FILE_TO_KEY.get(item["code"])
        if not ekey:
            continue
        entry = {
            "title": f"{item['subject']} {item['year']} LaTeX Code",
            "file": item["filePath"],
            "description": f"Official {item['code']} {item['subject']} {item['year']} LaTeX Paper"
        }
        if ekey not in zoology_pyq_entries:
            zoology_pyq_entries[ekey] = []
        zoology_pyq_entries[ekey].append(entry)

    # Serialize and format lines
    zoology_pyq_block_lines = []
    for key, entries in sorted(zoology_pyq_entries.items()):
        serialized = json.dumps(entries, indent=8)
        serialized = serialized.replace('\n', '\n        ')
        zoology_pyq_block_lines.append(f'        "{key}": {serialized}')
    
    zoology_pyq_block = ",\n".join(zoology_pyq_block_lines)

    # Inject into EXAM_PYQS in subjects.html
    start_marker = 'const EXAM_PYQS = {'
    end_marker = '\n    };'
    start_idx = subjects_content.find(start_marker)
    end_idx = subjects_content.find(end_marker, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        if 'zobmj11' in subjects_content:
            print("Zoology keys already present in subjects.html EXAM_PYQS — removing old ones first.")
            # Remove existing lines between start_idx and end_idx matching zob
            lines = subjects_content[start_idx:end_idx].split('\n')
            cleaned_lines = [l for l in lines if '"zob' not in l]
            # Insert the new ones before the closing marker
            new_inner_content = "\n".join(cleaned_lines) + ",\n" + zoology_pyq_block
            subjects_content = subjects_content[:start_idx] + new_inner_content + subjects_content[end_idx:]
        else:
            insert_point = end_idx
            new_entries_str = ",\n" + zoology_pyq_block
            subjects_content = subjects_content[:insert_point] + new_entries_str + subjects_content[insert_point:]
        print(f"[SUCCESS] subjects.html EXAM_PYQS block updated!")

    # Update isTargetDept and getDeptTag in subjects.html
    old_target = "key.startsWith('mat') || key.startsWith('phy') || key.startsWith('chem') || key.startsWith('sta') || key.startsWith('ggr') || key.startsWith('bob') || key.startsWith('imb')"
    new_target = "key.startsWith('mat') || key.startsWith('phy') || key.startsWith('chem') || key.startsWith('sta') || key.startsWith('ggr') || key.startsWith('bob') || key.startsWith('imb') || key.startsWith('zob')"
    if old_target in subjects_content:
        subjects_content = subjects_content.replace(old_target, new_target)
    
    old_dept_tag = "if (key.startsWith('bob') || key.startsWith('imb')) return 'botany';"
    new_dept_tag = "if (key.startsWith('bob') || key.startsWith('imb')) return 'botany';\n        if (key.startsWith('zob')) return 'zoology';"
    if old_dept_tag in subjects_content:
        subjects_content = subjects_content.replace(old_dept_tag, new_dept_tag)

    with open(subjects_path, "w", encoding="utf-8") as f:
        f.write(subjects_content)
    print("[SUCCESS] subjects.html tags and department methods updated!")

    # =============================================================================
    # 7. Update nep-science.html to activate Zoology
    # =============================================================================
    nep_science_path = "/Users/aryanmaurya/exam portal/nep-science.html"
    with open(nep_science_path, "r", encoding="utf-8") as f:
        science_content = f.read()

    # Replace the Zoology coming soon button with active button linking to nep-papers.html?dept=zoology
    old_zoology_btn = """            <!-- Zoology -->
            <button onclick="showComingSoonModal('Zoology')" class="p-5 md:p-6 rounded-xl border border-border-subtle bg-white/40 backdrop-blur-md text-left flex items-center gap-5 shadow-sm opacity-60 cursor-not-allowed">
                <div class="w-12 h-12 rounded-lg bg-red-500/5 flex items-center justify-center text-red-500/50 shrink-0">
                    <span class="material-symbols-outlined text-2xl">pets</span>
                </div>
                <div class="flex-grow">
                    <div class="flex items-center justify-between">
                        <h3 class="font-bold text-base text-primary/60">Zoology</h3>
                        <span class="bg-neutral-100 text-secondary text-[8px] font-bold px-2 py-0.5 rounded uppercase tracking-wider shrink-0">Coming Soon</span>
                    </div>
                    <p class="text-[11px] text-secondary/60 mt-0.5">Physiology, Classical Genetics, Cell Biology...</p>
                </div>
            </button>"""

    new_zoology_btn = """            <!-- Zoology -->
            <button onclick="window.location.href='nep-papers.html?dept=zoology'" class="p-5 md:p-6 rounded-xl border border-border-subtle bg-white/40 backdrop-blur-md text-left flex items-center gap-5 shadow-sm hover:shadow-md hover:border-red-500/40 transition-all duration-200 group">
                <div class="w-12 h-12 rounded-lg bg-red-500/10 flex items-center justify-center text-red-500 shrink-0 group-hover:bg-red-500/20 transition-colors">
                    <span class="material-symbols-outlined text-2xl">pets</span>
                </div>
                <div class="flex-grow">
                    <div class="flex items-center justify-between">
                        <h3 class="font-bold text-base text-primary">Zoology</h3>
                        <span class="bg-red-500/10 text-red-600 text-[8px] font-bold px-2 py-0.5 rounded uppercase tracking-wider shrink-0">Active</span>
                    </div>
                    <p class="text-[11px] text-secondary/60 mt-0.5">Physiology, Classical Genetics, Cell Biology...</p>
                </div>
            </button>"""

    # Format-independent search & replace or string direct replace
    if old_zoology_btn in science_content:
        science_content = science_content.replace(old_zoology_btn, new_zoology_btn)
    else:
        # Fallback to direct replacement pattern
        science_content = re.sub(
            r'<!-- Zoology -->\s*<button onclick="showComingSoonModal\(\'Zoology\'\)"[^>]*>.*?</button>',
            new_zoology_btn,
            science_content,
            flags=re.DOTALL
        )

    with open(nep_science_path, "w", encoding="utf-8") as f:
        f.write(science_content)
    print("[SUCCESS] nep-science.html Zoology button activated!")

    # =============================================================================
    # 8. Update nep-papers.html
    # =============================================================================
    nep_papers_path = "/Users/aryanmaurya/exam portal/nep-papers.html"
    with open(nep_papers_path, "r", encoding="utf-8") as f:
        papers_content = f.read()

    # Add 'zoology': 'Zoology' to deptLabels
    old_dept_labels = "'botany': 'Botany'"
    new_dept_labels = "'botany': 'Botany',\n        'zoology': 'Zoology'"
    if old_dept_labels in papers_content:
        papers_content = papers_content.replace(old_dept_labels, new_dept_labels)

    # Insert course names into NEP_COURSE_NAMES in nep-papers.html
    # Find start of NEP_COURSE_NAMES
    course_marker = "const NEP_COURSE_NAMES = {"
    course_start_idx = papers_content.find(course_marker)
    if course_start_idx != -1:
        insert_idx = course_start_idx + len(course_marker)
        
        # Build lines to insert
        course_lines = ["\n        // Zoology"]
        for key, val in sorted(course_name_map.items()):
            course_lines.append(f"        '{key}': '{val}',")
        
        # Special manual additions for other codes that might appear
        extra_courses = {
            "ZOOMD11": "Animal Biology",
            "ZOOMJ11": "Animal Diversity and Animal Form & Function",
            "ZOOMN11": "Animal Diversity and Animal Form & Function",
            "ZOOMJ11 / ZOOMN11": "Animal Diversity and Animal Form & Function",
            "ZOOMD21": "Hormones and Diseases",
            "ZOOMJ21": "Fundamentals of Cell Biology and Biochemistry",
            "ZOOMN21": "Fundamentals of Cell Biology and Elementary Physiology",
            "ZOOMJ21 / ZOOMN21": "Fundamentals of Cell Biology and Biochemistry",
            "ZOOSE11": "Applied Zoology",
            "ZOOSE21": "Food, Preservatives and Adulterants",
            "ZOOMD31": "Archaeozoology",
            "ZOOMJ31": "Basic Genetics",
            "ZOOMJ32": "Economic Zoology",
            "ZOOMV31": "Economic Zoology",
            "ZOOSE31": "Microscopy and Histology & Histochemistry",
            "ZOOMJ41": "Fundamental Endocrinology",
            "ZOOMJ42": "Developmental Biology",
            "ZOOMJ41 / ZOOMJ42": "Fundamental Endocrinology and Developmental Biology",
            "ZOOMJ43": "Evolution",
            "ZOOMJ44": "Systematics and Taxonomy",
            "ZOOMN41": "Fundamental Endocrinology",
            "ZOOMJ51": "Functional Anatomy of Non-chordates",
            "ZOOMJ52": "Animal Behaviour",
            "ZOOMJ53": "Immunology",
            "ZOOMJ54": "Biology of Infectious Diseases",
            "ZOOMV51": "Aquaculture",
            "ZOOMJ61": "Functional Anatomy of Chordates",
            "ZOOMJ62": "Environmental Biology",
            "ZOOMJ63": "Cell Biology",
            "ZOOMJ64": "Mammalian Physiology",
            "ZOOMV61": "Clinical Biochemistry"
        }
        
        for k, v in sorted(extra_courses.items()):
            line = f"        '{k}': '{v}',"
            if line not in course_lines and k not in course_name_map:
                course_lines.append(line)
                
        zoology_courses_str = "\n".join(course_lines)
        papers_content = papers_content[:insert_idx] + zoology_courses_str + papers_content[insert_idx:]

    with open(nep_papers_path, "w", encoding="utf-8") as f:
        f.write(papers_content)
    print("[SUCCESS] nep-papers.html course names and labels updated!")

    print("\n=== All Operations Completed Successfully! ===")

if __name__ == "__main__":
    main()
