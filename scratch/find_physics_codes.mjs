import fs from "fs";

const content = fs.readFileSync("js/exams-data.js", "utf-8");
// Extract the JSON portion
const jsonStart = content.indexOf("{");
const jsonEnd = content.lastIndexOf("}");
const jsonStr = content.substring(jsonStart, jsonEnd + 1);

let EXAMS;
try {
  // Try evaluating it in a safe way or using Function since it's a JS object declaration
  EXAMS = Function("return " + jsonStr)();
} catch (e) {
  console.error("Failed to parse via Function:", e);
  process.exit(1);
}

console.log("=== PHYSICS SUBJECTS IN EXAMS-DATA ===");
const phyKeys = Object.keys(EXAMS).filter(key => key.startsWith("phy") || key.includes("physics"));

for (const key of phyKeys) {
  const ex = EXAMS[key];
  console.log(`Key: "${key}", Title: "${ex.title}", Module: "${ex.module}", comingSoon: ${ex.comingSoon}`);
}
