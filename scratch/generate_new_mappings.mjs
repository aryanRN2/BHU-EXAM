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

let braceCount = 1;
let endIdx = startIdx + "const EXAM_PYQS = {".length;
while (braceCount > 0 && endIdx < htmlContent.length) {
  const char = htmlContent[endIdx];
  if (char === "{") braceCount++;
  else if (char === "}") braceCount--;
  endIdx++;
}

const examPyqStr = htmlContent.substring(startIdx + "const EXAM_PYQS = ".length, endIdx).trim();

let EXAM_PYQS;
try {
  EXAM_PYQS = eval(`(${examPyqStr})`);
} catch (e) {
  console.error("Error evaluating EXAM_PYQS:", e);
  process.exit(1);
}

// Find all math subject codes
const mathSubjectKeys = Object.keys(EXAM_PYQS).filter(key => key.startsWith("mat"));
console.log("Math subjects in EXAM_PYQS:", mathSubjectKeys);

// Find files in corrected directory
const correctedFiles = fs.readdirSync(correctedDir).filter(f => f.endsWith(".pdf"));

// For each corrected file, find which subjects it was mapped to in EXAM_PYQS
const mappings = {};
for (const file of correctedFiles) {
  const matchedKeys = [];
  for (const [key, items] of Object.entries(EXAM_PYQS)) {
    for (const item of items) {
      if (item.file && decodeURIComponent(item.file).endsWith(file)) {
        matchedKeys.push(key);
      }
    }
  }
  mappings[file] = matchedKeys;
}

console.log("\nMappings found for each corrected file:");
let unmappedCount = 0;
for (const [file, keys] of Object.entries(mappings)) {
  if (keys.length === 0) {
    unmappedCount++;
    console.log(`❌ Unmapped file: ${file}`);
  } else {
    console.log(`✅ ${file} -> ${keys.join(", ")}`);
  }
}
console.log(`\nTotal unmapped files: ${unmappedCount}`);
