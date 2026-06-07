import os
from pypdf import PdfReader

files_dir = "aaa/physics final"
output_file = "scratch/all_physics_pyqs_text.txt"

files = sorted([f for f in os.listdir(files_dir) if f.endswith(".pdf") or f.endswith(".PDF")])

print(f"Extracting text from {len(files)} files...")

with open(output_file, "w", encoding="utf-8") as out:
    for file in files:
        pdf_path = os.path.join(files_dir, file)
        try:
            reader = PdfReader(pdf_path)
            out.write(f"=========================================\n")
            out.write(f"FILE: {file}\n")
            out.write(f"=========================================\n")
            for i, page in enumerate(reader.pages):
                out.write(f"--- Page {i+1} ---\n")
                text = page.extract_text()
                if text:
                    out.write(text + "\n")
            out.write("\n\n")
            print(f"Extracted: {file}")
        except Exception as e:
            print(f"Failed to extract {file}: {e}")

print(f"Extraction complete! Saved to {output_file}")
