import pypdf
import os

pdf_files = [
    "DynamicalSystems_SemVI_2022-23.pdf",
    "NumberTheory_SemVI_2022-23.pdf",
    "DiscreteMathematics_SemVI_2022-23.pdf",
    "Relativity_SemV_2022-23.pdf",
    "NumericalAnalysis_SemVI_2022-23.pdf",
    "DiffGeometry_SemV_2022-23.pdf"
]

pyq_dir = "aaa/maths/bhu_maths_pyqs"

for file in pdf_files:
    path = os.path.join(pyq_dir, file)
    print(f"\n========================================\nEXTRACTING FROM: {file}\n========================================\n")
    if not os.path.exists(path):
        print("File does not exist")
        continue
    try:
        reader = pypdf.PdfReader(path)
        # Just extract first 2 pages (usually has all key questions)
        for i in range(min(2, len(reader.pages))):
            print(f"--- Page {i+1} ---")
            text = reader.pages[i].extract_text()
            print(text)
    except Exception as e:
        print(f"Error: {e}")
