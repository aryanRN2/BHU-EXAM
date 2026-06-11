# SCIQB PYQ Architecture Documentation

This document explains the organization and implementation details of the two different categories of Previous Year Questions (PYQs) hosted on SCIQB.

---

## 1. Older Education Policy (Legacy) PYQs

### Overview
The legacy stream archives original examinations administered under the old college curriculum (pre-NEP). 

### Storage & Source Folder
* **Source Folder:** `aaa/all science pyq`
* **Data Mapping:** Mapped in [legacy-data.js](file:///Users/aryanmaurya/exam%20portal/js/legacy-data.js) under `LEGACY_PYQ_DATA`.
* **Format:** Raw, original PDF documents.

### Key Characteristics
1. **Multi-paper PDFs:** In the legacy curriculum, a single consolidated PDF file often contains multiple question papers. Therefore, the same PDF URL can be reused across different course codes or semester definitions.
2. **Naming & Structure:** Follows legacy naming standards, course codes, and semester assignments (Semesters I through VI).
3. **Delivery:** Renders as downloadable/viewable PDF cards linking directly to Supabase storage objects.

---

## 2. New Education Policy (NEP) PYQs

### Overview
The NEP stream hosts question papers aligned with the modern New Education Policy curriculum introduced at BHU.

### Storage & Source Folder
* **Source Folders:** Located in respective subject directories, e.g.,
  - [aaa/chemistry/tex_files/](file:///Users/aryanmaurya/exam%20portal/aaa/chemistry/tex_files/)
  - [aaa/physics/tex_files/](file:///Users/aryanmaurya/exam%20portal/aaa/physics/tex_files/)
  - etc.
* **Data Mapping:** Managed via [nep-data.js](file:///Users/aryanmaurya/exam%20portal/js/nep-data.js) under `NEP_LATEX_PYQ_DATA`.
* **Format:** Standard LaTeX code (`.tex` files).

### Key Characteristics
1. **Transcribed LaTeX Sheets:** Because BHU transitioned to NEP only 2 years ago, there is a limited corpus of direct NEP papers. To compensate, original legacy papers have been transcribed into professional LaTeX source code and mapped directly onto the new NEP paper codes (e.g., `PHYMJ11`, `MATMJ11`, etc.).
2. **Real-time Rendering:** Renders dynamically inside the web application via [pyq-viewer.html](file:///Users/aryanmaurya/exam%20portal/pyq-viewer.html), parsing and formatting math expressions on-the-fly using MathJax.
3. **No Raw PDFs:** Shows strictly the compiled HTML layout styled in academic print-sheet typography with copyable/downloadable LaTeX code modals.

---

## Technical Partition Verification
* **Legacy Pages:** [legacy-pyq.html](file:///Users/aryanmaurya/exam%20portal/legacy-pyq.html), [legacy-science.html](file:///Users/aryanmaurya/exam%20portal/legacy-science.html), and [legacy-papers.html](file:///Users/aryanmaurya/exam%20portal/legacy-papers.html) only query `legacy-data.js` and link to raw PDFs.
* **NEP Pages:** [nep-pyq.html](file:///Users/aryanmaurya/exam%20portal/nep-pyq.html), [nep-science.html](file:///Users/aryanmaurya/exam%20portal/nep-science.html), and [nep-papers.html](file:///Users/aryanmaurya/exam%20portal/nep-papers.html) query `nep-data.js` and direct students to the real-time LaTeX parsing viewer.
