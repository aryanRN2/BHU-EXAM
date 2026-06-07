# /// script
# dependencies = [
#   "pypdf",
# ]
# ///
import os
import sys
from pypdf import PdfReader

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- Page {i+1} ---\n"
        text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    pdf_path = "aaa/physics final/BPT-101_MechanicsandRelativity_SemI_2016-17.pdf"
    if os.path.exists(pdf_path):
        print(f"Extracting text from {pdf_path}:")
        text = extract_text(pdf_path)
        print(text[:1000]) # print first 1000 characters
    else:
        print(f"File not found: {pdf_path}")
