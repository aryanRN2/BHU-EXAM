import fs from "fs";
import path from "path";

// 1. Load the generated physics data
const generatedData = JSON.parse(fs.readFileSync("scratch/generated_physics_data.json", "utf-8"));
const { legacyEntries, examPyqMapping } = generatedData;

// 2. Apply updates to subjects.html
function updateSubjectsHtml() {
  const htmlPath = "subjects.html";
  let htmlContent = fs.readFileSync(htmlPath, "utf-8");

  // A. Find and update EXAM_PYQS
  const startMarker = "const EXAM_PYQS = ";
  const startIndex = htmlContent.indexOf(startMarker);
  if (startIndex === -1) {
    throw new Error("Could not find start of EXAM_PYQS in subjects.html");
  }

  const endMarker = "};;";
  const endIndex = htmlContent.indexOf(endMarker, startIndex);
  if (endIndex === -1) {
    throw new Error("Could not find end of EXAM_PYQS (};;) in subjects.html");
  }

  const pyqBlock = htmlContent.substring(startIndex + startMarker.length, endIndex + 1);
  let examPyqs = Function("return " + pyqBlock)();

  // Clear existing keys starting with "phy"
  for (const key of Object.keys(examPyqs)) {
    if (key.startsWith("phy")) {
      delete examPyqs[key];
    }
  }

  // Add all the new physics mappings
  for (const [key, papers] of Object.entries(examPyqMapping)) {
    examPyqs[key] = papers;
  }

  // Sort examPyqs keys to keep it clean (and ensure physics keys are grouped nicely)
  const sortedExamPyqs = {};
  Object.keys(examPyqs).sort().forEach(k => {
    sortedExamPyqs[k] = examPyqs[k];
  });

  // Format the block nicely
  const formattedBlock = JSON.stringify(sortedExamPyqs, null, "\t")
    .replace(/\n/g, "\n    ")
    .replace(/\t/g, "        ");

  htmlContent = htmlContent.substring(0, startIndex + startMarker.length) + 
                formattedBlock + 
                htmlContent.substring(endIndex + 1);

  // B. Update icon rendering logic in subjects.html
  const oldIconBlock = `                    let icon = 'menu_book';
                    if (key.includes('math') || key.includes('calc') || (exam.module && exam.module.startsWith('MAT'))) icon = 'calculate';
                    else if (key.includes('geo') || key.includes('glb') || (exam.module && exam.module.startsWith('GLB'))) icon = 'terrain';
                    else if (key.includes('bot') || key.includes('bob') || (exam.module && exam.module.startsWith('BOB'))) icon = 'eco';`;

  const newIconBlock = `                    let icon = 'menu_book';
                    if (key.includes('math') || key.includes('calc') || (exam.module && exam.module.startsWith('MAT'))) icon = 'calculate';
                    else if (key.includes('geo') || key.includes('glb') || (exam.module && exam.module.startsWith('GLB'))) icon = 'terrain';
                    else if (key.includes('bot') || key.includes('bob') || (exam.module && exam.module.startsWith('BOB'))) icon = 'eco';
                    else if (key.includes('phy') || (exam.module && exam.module.startsWith('PHY'))) icon = 'insights';`;

  if (htmlContent.includes(oldIconBlock)) {
    htmlContent = htmlContent.replace(oldIconBlock, newIconBlock);
    console.log("Updated subjects.html icon rendering logic.");
  } else {
    // Let's check if spaces differ
    const normalizedContent = htmlContent.replace(/\s+/g, " ");
    const normalizedOld = oldIconBlock.replace(/\s+/g, " ");
    if (normalizedContent.includes(normalizedOld)) {
      console.warn("Icon block found but whitespaces differ. Please verify/replace manually.");
    } else {
      console.warn("Could not find the target icon block in subjects.html.");
    }
  }

  fs.writeFileSync(htmlPath, htmlContent, "utf-8");
  console.log("Successfully updated subjects.html EXAM_PYQS mappings!");
}

// 3. Apply updates to js/legacy-data.js
function updateLegacyDataJs() {
  const legacyPath = "js/legacy-data.js";
  const content = fs.readFileSync(legacyPath, "utf-8");

  const startIdx = content.indexOf("{");
  const endIdx = content.lastIndexOf("}");
  if (startIdx === -1 || endIdx === -1) {
    throw new Error("Could not find object braces in js/legacy-data.js");
  }

  const jsonStr = content.substring(startIdx, endIdx + 1);
  let legacyData = Function("return " + jsonStr)();

  // Overwrite the physics array
  legacyData.physics = legacyEntries;

  // Format and write back
  const formattedContent = `// Automatically generated legacy curriculum PYQ data
export const LEGACY_PYQ_DATA = ${JSON.stringify(legacyData, null, 2)};
`;

  fs.writeFileSync(legacyPath, formattedContent, "utf-8");
  console.log("Successfully updated js/legacy-data.js physics array!");
}

try {
  updateSubjectsHtml();
  updateLegacyDataJs();
  console.log("All updates applied successfully!");
} catch (error) {
  console.error("Error applying updates:", error);
  process.exit(1);
}
