# 📋 PYQ Verification & Audit Rules (`PYQ_CHECK_RULES.md`)

This document defines the **Mandatory Execution & Verification Protocols** for analyzing, processing, digitizing, and auditing Previous Year Question (PYQ) papers on SCIQB / BHU Exam Portal.

---

## 🚨 Core Rules for PYQ Verification

### 1. 📄 Multi-Paper PDF Rule (Page-by-Page Audit)
- **NEVER assume a single PDF file contains only ONE question paper.**
- Always scan **EVERY page** of a PDF file using multi-page OCR or PDF page extraction.
- Detect all hidden paper boundaries (e.g., Page 1 = 2024-25 Sem I, Page 2 = 2025-26 Sem III, Pages 3–10 = 2024-25 Sem II, Pages 11–18 = 2025-26 Sem II).
- If a PDF contains multiple papers:
  1. Extract each individual sub-paper separately.
  2. Index each paper individually in database and tracking sheets.

---

### 2. 📅 Academic Session & Year Verification Rule
- **Check the exact Academic Year** printed on the question paper header:
  - Example: `2024-25` vs `2025-26` vs `2023-24`.
- **NEVER mark a 2025-26 paper as "ADDED" just because a 2024-25 paper with the same paper code exists.**
- Each academic year MUST have its own separate entry and digitized TeX file if questions or sessions differ.

---

### 3. 📝 Exam Type & Term Identification Rule
- Explicitly identify the exam type for each paper:
  - **End-Term** (Final Semester Examination)
  - **Mid-Term** (Mid-Semester Examination)
  - **Sessional / Internal Assessment**
- Verify duration and maximum marks (e.g., 2:30 Hours / 70 Marks vs 1 Hour / 30 Marks).

---

### 4. 📚 Subject, Department & NEP Course Category Rule
- Verify the exact Paper Code (e.g., `COMMD11`, `COMMD21`, `ESMN111`, `CIMSE11`, `PHYMJ11`).
- Categorize under the correct NEP (New Education Policy) stream:
  - **MJ / MN**: Major / Minor Core Course
  - **MDC**: Multidisciplinary Course
  - **SEC**: Skill Enhancement Course
  - **VAC**: Value Added Course
  - **AEC**: Ability Enhancement Course
- Verify Department / Faculty (e.g., *Faculty of Commerce*, *Department of Geology*, *DST-CIMS*, *Institute of Science*).

---

### 5. 🔖 Reference Code / Ref No. Cross-Verification Rule
- Extract the official Question Paper Reference Code if printed:
  - Examples: `CECONF/P/Sem II/2024-25/13`, `Conf/even/2025-26/4`, `REF NO. CECONF/N/2024-25/26`.
- Cross-verify matching Ref Numbers across digitized TeX files in `aaa/ALL_PYQS_LATEX/`.

---

### 6. 🔍 Database & File Cross-Referencing Rule
Before declaring any paper **"ADDED"** or **"NOT ADDED"**:
1. Check **`js/nep-data.js`** for matching `code`, `year`, `examType`, and `filePath`.
2. Check **`aaa/ALL_PYQS_LATEX/`** for the compiled `.tex` and `.pdf` files.
3. Check **`nep_pyq_tracking_sheet.csv`** for tracking status.
4. Verify BOTH:
   - Does the paper code match?
   - **Does the Academic Year (2024-25 vs 2025-26) AND Term (Mid/End) match EXACTLY?**

---

## 🛠 Quick Audit Verification Matrix Format

When auditing any PYQ PDF, construct a verification table formatted as follows:

| Page Range | Paper Code | Subject & Title | Academic Year | Term (Mid/End) | Ref No. | TeX File Exists? | Added in `nep-data.js`? | Final Status |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| P. 1 | `COMMD11` | Elementary Marketing | 2024-25 | End-Term | — | `COMMD11_...2024-25.tex` | Yes | ✅ ADDED |
| P. 3–10 | `COMMD21` | Basic Accounting | 2024-25 | End-Term | `CECONF/P/Sem II/2024-25/13` | `COMMD21_...2024-25.tex` | Yes | ✅ ADDED |
| P. 11–18 | `COMMD21` | Basic Accounting | 2025-26 | End-Term | `Conf/even/2025-26/4` | No | No | ❌ NOT ADDED |
