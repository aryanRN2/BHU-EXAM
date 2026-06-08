import os
import subprocess
import re

pdf_dir = "/Users/aryanmaurya/exam portal/aaa/latest corrected maths pdf"
latex_dir = "/Users/aryanmaurya/exam portal/aaa/latest corrected maths pdf/final maths export latex"

pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])[:10]

print(f"Checking first 10 PDF files:")
for f in pdf_files:
    print(f" - {f}")

print("\n--- Starting Verification ---")

def clean_text(text):
    # Remove extra spaces, newlines, and non-alphanumeric chars to make matching robust
    return re.sub(r'\s+', ' ', text).strip()

for pdf_name in pdf_files:
    base_name = os.path.splitext(pdf_name)[0]
    tex_name = base_name + ".tex"
    
    pdf_path = os.path.join(pdf_dir, pdf_name)
    tex_path = os.path.join(latex_dir, tex_name)
    
    if not os.path.exists(tex_path):
        print(f"[ERROR] LaTeX file missing for {pdf_name} (expected {tex_name})")
        continue
        
    # Extract text from PDF using pdftotext
    try:
        txt_path = os.path.join(pdf_dir, base_name + ".txt")
        subprocess.run(["pdftotext", pdf_path, txt_path], check=True)
        with open(txt_path, "r", encoding="utf-8", errors="ignore") as pf:
            pdf_text = pf.read()
        os.remove(txt_path) # cleanup
    except Exception as e:
        print(f"[ERROR] Failed to extract text from {pdf_name}: {e}")
        continue
        
    # Read LaTeX code
    with open(tex_path, "r", encoding="utf-8", errors="ignore") as tf:
        tex_text = tf.read()
        
    # We want to find some sample text/questions from the PDF and see if they exist in the tex file.
    # Let's extract lines of text from the PDF that look like questions (contain text)
    pdf_lines = [line.strip() for line in pdf_text.split("\n") if len(line.strip()) > 15]
    
    # Take a few sample lines (up to 5) from the PDF
    samples = []
    for line in pdf_lines:
        # Avoid headers/footers/common labels
        cleaned = clean_text(line)
        if any(w in cleaned.lower() for w in ["banaras", "university", "page", "maximum", "time", "marks"]):
            continue
        # Take a substring of the line to search (e.g. 20-30 characters) to avoid minor latex/typesetting diffs
        search_snippet = cleaned[:40]
        if len(search_snippet) > 15:
            samples.append(search_snippet)
        if len(samples) >= 5:
            break
            
    if not samples:
        print(f"[WARNING] Could not extract sufficient text snippets from {pdf_name}")
        continue
        
    matches = 0
    clean_tex = clean_text(tex_text).lower()
    
    # Try to find math equations or text in the LaTeX file
    # Note: LaTeX might have math symbols like $x$, so we'll do substring searches of the alphanumeric parts
    for sample in samples:
        # Simplify the sample to search
        sample_words = [w for w in re.findall(r'[a-zA-Z0-9]+', sample) if len(w) > 2]
        if not sample_words:
            continue
        # Check if the words appear in order or close to each other in the LaTeX file
        # We can just check if all of the major words in the sample are in the LaTeX file
        word_matches = [w.lower() in clean_tex for w in sample_words]
        if len(word_matches) > 0 and sum(word_matches) / len(word_matches) >= 0.7:
            matches += 1
            
    match_percentage = (matches / len(samples)) * 100 if samples else 0
    if match_percentage >= 60:
        print(f"[OK] {pdf_name} <--> {tex_name} (Match Confidence: {match_percentage:.1f}%)")
        print(f"     Sample verified: '{samples[0]}...' found in LaTeX source.")
    else:
        print(f"[FAIL] Low match confidence for {pdf_name} <--> {tex_name} ({match_percentage:.1f}%)")
        print(f"     Samples checked: {samples}")
        print(f"     LaTeX preview: {tex_text[:300]}")
