# SCIQB Notes Architecture Documentation

This document explains the organization, file-system architecture, and frontend integration of student lecture notes hosted on SCIQB.

---

## 1. Directory Structure & Organization

All notes are stored in the root directory under the `NOTES` folder. The folder is partitioned by **Department**, then **Semester**, and contains the lecture notes in PDF format.

```
NOTES/
├── MATHS/
│   └── SEMESTER 4/
│       ├── KM Sir class notes.pdf                  # MATMJ41 Several Variable Calculus
│       ├── Vector and Tensor Analysis notes.pdf    # MATMJ42 Vector and Tensor Analysis
│       ├── Differential equation notes.pdf         # MATMJ43 & MATMN41 Differential Equations
│       └── MECHANICS class notes .pdf              # Mechanics
└── PHY/
    └── [Future Semester folders]
```

### Resource Manifest

| Semester | Course Code | Subject Area | File Name | File Size | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Semester IV | **MATMJ41** | Several Variable Calculus | `KM Sir class notes.pdf` | ~43.9 MB | KM Sir class notes covering limit, continuity, derivatives, and multiple integrals. |
| Semester IV | **MATMJ42** | Vector and Tensor Analysis | `Vector and Tensor Analysis notes.pdf` | ~27.2 MB | Notes covering vector integrations, stokes/divergence theorems, and tensors. |
| Semester IV | **MATMJ43** | Differential Equations (Major) | `Differential equation notes.pdf` | ~37.9 MB | Covers ordinary and partial differential equations. |
| Semester IV | **Mechanics** | Mechanics (General / Major) | `MECHANICS class notes .pdf` | ~30.7 MB | Covers statics, dynamics, rigid body motion, and catenary. |
| Semester IV | **MATMN41** | Differential Equations (Minor) | `Differential equation notes.pdf` | ~37.9 MB | Minor stream ordinary and partial differential equations reference. |

---

## 2. Git & Vercel Deployment Rules

By default, the global `.gitignore` ignores all PDF files (`**/*.pdf`) to prevent large binary files from overloading the git repository. 

To ensure the lecture notes are committed to Git and deployed to Vercel, the following exclusion rule is added to `.gitignore` directly below `**/*.pdf`:

```gitignore
# Exclude the NOTES directory from the global PDF ignore pattern
!NOTES/**/*.pdf
```

---

## 3. UI Navigation Flow & Frontend State Management

The notes are integrated into the primary homepage [index.html](file:///Users/aryanmaurya/exam%20portal/index.html) inside a dynamic modal called `#booksModal`. 

The modal is refactored into a **three-step wizard** styled with glassmorphic CSS tokens:

```
[Step 1: Select Institute] ─(Select Science)─> [Step 2: Select Department] ─(Select Maths)─> [Step 3: Notes List]
```

### Modal State Functions:
* `openBooksModal()`: Automatically resets the navigation to Step 1 and displays the modal window.
* `goToNotesStep(step)`: Toggles class lists (`hidden` vs visible) on step containers (`#notesStepInstitute`, `#notesStepDepartment`, and `#notesStepNotes`).
* `closeBooksModal()`: Dismisses the modal container.
