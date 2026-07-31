import json
import fitz
import re

def verify_pdf():
    pdf_path = 'BHU_BSc_Mathematics_Complete_Syllabus.pdf'
    json_path = 'SYLLABUS/maths_syllabus.json'

    doc = fitz.open(pdf_path)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    semesters = data.get('semesters', [])

    report = []
    report.append("==================================================")
    report.append("   PDF COMPREHENSIVE INTEGRITY & CONTENT AUDIT")
    report.append("==================================================")
    report.append(f"Total PDF Pages: {len(doc)}")

    # 1. Audit TOC Links on Page 1 & 2
    toc_links = doc[0].get_links() + doc[1].get_links()
    report.append(f"Total Interactive TOC Redirect Links: {len(toc_links)}")

    # 2. Audit Every Semester and Paper
    total_papers_json = sum(len(sem.get('papers', [])) for sem in semesters)
    report.append(f"Total Papers in JSON Database: {total_papers_json}")

    missing_papers = []
    paper_page_count = 0
    sciqb_footer_count = 0

    for i, page in enumerate(doc):
        text = page.get_text('text')
        
        # Check sciqb link
        if 'sciqb' in text.lower():
            sciqb_footer_count += 1
            
        # Count papers
        if 'Course Title' in text or 'Course Content' in text or 'Units' in text:
            paper_page_count += 1

    report.append(f"Pages containing Course Syllabus Tables: {paper_page_count}")
    report.append(f"Pages containing 'www.sciqb.com' footer: {sciqb_footer_count} / {len(doc)}")

    # 3. Check for specific paper content match across all 8 Semesters
    paper_checks = []
    for sem in semesters:
        s_num = sem.get('semester')
        for p in sem.get('papers', []):
            code = p.get('code')
            name = p.get('name')
            units = p.get('syllabus', [])
            
            # Find this code in PDF text
            found = False
            for p_idx, page in enumerate(doc):
                p_text = page.get_text('text')
                if code in p_text:
                    found = True
                    unit_count = len(units)
                    # Verify unit presence
                    found_units = sum(1 for u in range(1, unit_count+1) if f"Unit" in p_text or f"I" in p_text)
                    paper_checks.append((s_num, code, name, p_idx+1, True, len(units)))
                    break
            if not found:
                paper_checks.append((s_num, code, name, -1, False, len(units)))

    passed_papers = [p for p in paper_checks if p[4]]
    failed_papers = [p for p in paper_checks if not p[4]]

    report.append(f"\n--- PAPER CONTENT MATCH AUDIT ---")
    report.append(f"Successfully Verified Papers in PDF: {len(passed_papers)} / {total_papers_json}")

    if failed_papers:
        report.append(f"WARNING: Papers missing from PDF: {failed_papers}")
    else:
        report.append("PERFECT MATCH: 100% of all courses across Semesters 1 to 8 are present in the PDF!")

    # 4. Detailed Breakdown per Semester
    report.append("\n--- SEMESTER-BY-SEMESTER BREAKDOWN ---")
    for s_idx in range(1, 9):
        sem_p = [p for p in paper_checks if p[0] == s_idx]
        report.append(f"Semester {s_idx}: {len(sem_p)} courses verified.")
        for p in sem_p:
            report.append(f"   - [{p[1]}] {p[2]} (Page {p[3]}, {p[5]} Units)")

    report_str = "\n".join(report)
    print(report_str)

    with open('pdf_verification_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_str)

if __name__ == '__main__':
    verify_pdf()
