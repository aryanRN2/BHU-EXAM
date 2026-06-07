import fs from "fs";

// Load generated data for baseline comparison
const { legacyEntries, examPyqMapping } = JSON.parse(fs.readFileSync("scratch/generated_physics_data.json", "utf-8"));

// 1. Validate subjects.html
function validateSubjectsHtml() {
  const htmlContent = fs.readFileSync("subjects.html", "utf-8");
  const startMarker = "const EXAM_PYQS = ";
  const startIndex = htmlContent.indexOf(startMarker);
  const endMarker = "};;";
  const endIndex = htmlContent.indexOf(endMarker, startIndex);
  
  if (startIndex === -1 || endIndex === -1) {
    throw new Error("Validation Failed: EXAM_PYQS block not found in subjects.html");
  }

  const pyqBlock = htmlContent.substring(startIndex + startMarker.length, endIndex + 1);
  const examPyqs = Function("return " + pyqBlock)();

  // Verify that all 17 keys are mapped correctly
  for (const [key, papers] of Object.entries(examPyqMapping)) {
    const htmlPapers = examPyqs[key];
    if (!htmlPapers) {
      throw new Error(`Validation Failed: Key "${key}" not found in subjects.html EXAM_PYQS`);
    }
    if (htmlPapers.length !== papers.length) {
      throw new Error(`Validation Failed: Key "${key}" has ${htmlPapers.length} papers, expected ${papers.length}`);
    }
    
    // Verify each paper url points directly to the bucket root
    htmlPapers.forEach(p => {
      if (!p.file.startsWith("https://sajmognuphnrvivtmuux.supabase.co/storage/v1/object/public/pyq-pdfs/")) {
        throw new Error(`Validation Failed: Invalid file URL: ${p.file}`);
      }
    });
  }

  // Check that the custom physics icon condition is present
  if (!htmlContent.includes("key.includes('phy') || (exam.module && exam.module.startsWith('PHY'))")) {
    throw new Error("Validation Failed: Custom physics icon condition not found in subjects.html");
  }

  console.log("subjects.html validation passed successfully!");
}

// 2. Validate js/legacy-data.js
function validateLegacyData() {
  const legacyContent = fs.readFileSync("js/legacy-data.js", "utf-8");
  const startIdx = legacyContent.indexOf("{");
  const endIdx = legacyContent.lastIndexOf("}");
  
  if (startIdx === -1 || endIdx === -1) {
    throw new Error("Validation Failed: Legcy data object not found in js/legacy-data.js");
  }

  const jsonStr = legacyContent.substring(startIdx, endIdx + 1);
  const legacyData = Function("return " + jsonStr)();

  const physicsEntries = legacyData.physics;
  if (!physicsEntries) {
    throw new Error("Validation Failed: physics array not found in js/legacy-data.js");
  }

  if (physicsEntries.length !== legacyEntries.length) {
    throw new Error(`Validation Failed: physics legacy array has ${physicsEntries.length} entries, expected ${legacyEntries.length}`);
  }

  physicsEntries.forEach(entry => {
    if (!entry.title || !entry.fileName || !entry.url || !entry.semester) {
      throw new Error(`Validation Failed: Missing fields in legacy entry: ${JSON.stringify(entry)}`);
    }
    if (!entry.url.startsWith("https://sajmognuphnrvivtmuux.supabase.co/storage/v1/object/public/pyq-pdfs/")) {
      throw new Error(`Validation Failed: Invalid legacy URL: ${entry.url}`);
    }
  });

  console.log("js/legacy-data.js validation passed successfully!");
}

try {
  validateSubjectsHtml();
  validateLegacyData();
  console.log("All validations passed successfully!");
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
