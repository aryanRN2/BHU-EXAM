import fs from "fs";
import path from "path";

const subjectsHtmlPath = "subjects.html";
const correctedDir = "aaa/latest corrected maths pdf";

const htmlContent = fs.readFileSync(subjectsHtmlPath, "utf-8");

// Extract EXAM_PYQS object
const startIdx = htmlContent.indexOf("const EXAM_PYQS = {");
if (startIdx === -1) {
  console.error("Could not find EXAM_PYQS in subjects.html");
  process.exit(1);
}

// Find matching closing brace
let braceCount = 1;
let endIdx = startIdx + "const EXAM_PYQS = {".length;
while (braceCount > 0 && endIdx < htmlContent.length) {
  const char = htmlContent[endIdx];
  if (char === "{") braceCount++;
  else if (char === "}") braceCount--;
  endIdx++;
}

const examPyqStr = htmlContent.substring(startIdx + "const EXAM_PYQS = ".length, endIdx).trim();

// Parse using eval to handle JS object literal format
let EXAM_PYQS;
try {
  EXAM_PYQS = eval(`(${examPyqStr})`);
} catch (e) {
  console.error("Error evaluating EXAM_PYQS string:", e);
  process.exit(1);
}

console.log("Found subject keys:", Object.keys(EXAM_PYQS));

// Get all files in correctedDir
const correctedFiles = fs.readdirSync(correctedDir).filter(f => f.endsWith(".pdf"));
console.log(`\nFound ${correctedFiles.length} files in corrected directory.`);

// Check which files from subjects.html match
const htmlFiles = new Set();
for (const [key, items] of Object.entries(EXAM_PYQS)) {
  for (const item of items) {
    if (item.file) {
      const match = item.file.match(/pyq-pdfs\/(.+)$/);
      if (match) {
        const decoded = decodeURIComponent(match[1]);
        htmlFiles.add(decoded);
      }
    }
  }
}

console.log(`\nUnique files in subjects.html: ${htmlFiles.size}`);
console.log("Files in corrected directory but not in subjects.html:");
for (const file of correctedFiles) {
  if (!htmlFiles.has(file)) {
    console.log(" -", file);
  }
}

console.log("\nFiles in subjects.html but not in corrected directory:");
for (const file of htmlFiles) {
  // Only check math files or files starting with letters commonly in math (e.g. MTB, Abstract, Calculus, etc.)
  const isMath = /^(MTB|Abstract|Calculus|Complex|Diff|Discrete|Dynamical|Geometry|Global|Linear|Math|Mechanics|Multivariable|Number|Numerical|Operations|PDE|Probability|Programming|Relativity|Set|Statics|Vector|Ancillary)/i.test(file);
  if (isMath && !correctedFiles.includes(file)) {
    console.log(" -", file);
  }
}
