import fs from 'fs';

const jsPath = 'js/exams-data.js';
const content = fs.readFileSync(jsPath, 'utf8')
    .replace('export const EXAMS =', 'const EXAMS =') + '\nexport default EXAMS;';

const tempPath = 'scratch/temp_exams_verify.mjs';
fs.writeFileSync(tempPath, content);

const { default: EXAMS } = await import('./temp_exams_verify.mjs');
fs.unlinkSync(tempPath);

const targetKeys = [
  "chemd11", "chemd21", "chemd31",
  "chemj11", "chemn11", "chemj21", "chemn21",
  "chemj31", "chemj32", "chemj33", "chemj34",
  "chemj41", "chemj42", "chemj43", "chemn41", "chemj44", "chemn42",
  "chemj51", "chemj52", "chemj53", "chemj54",
  "chemj61", "chemj62", "chemj63", "chemj64",
  "chemj85", "chemj8r5"
];

console.log("=== VERIFYING CHEMISTRY EXAMS ===");
let allOk = true;

targetKeys.forEach(key => {
  const exam = EXAMS[key];
  if (!exam) {
    console.error(`ERROR: Key "${key}" not found in EXAMS database!`);
    allOk = false;
    return;
  }
  
  const qCount = exam.questions ? exam.questions.length : 0;
  const comingSoon = exam.comingSoon;
  
  if (comingSoon !== false) {
    console.error(`ERROR: Key "${key}" has comingSoon = ${comingSoon} (expected false)`);
    allOk = false;
  }
  
  if (qCount !== 50) {
    console.error(`ERROR: Key "${key}" has ${qCount} questions (expected 50)`);
    allOk = false;
  } else {
    console.log(`OK: Key "${key}" is live with ${qCount} questions. Title: "${exam.title}"`);
  }
});

if (allOk) {
  console.log("\nSUCCESS: All chemistry subjects verified successfully!");
} else {
  console.error("\nFAILURE: Some errors were found in chemistry validation.");
  process.exit(1);
}
