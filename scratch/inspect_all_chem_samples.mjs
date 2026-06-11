import fs from 'fs';

const jsPath = 'js/exams-data.js';
const content = fs.readFileSync(jsPath, 'utf8')
    .replace('export const EXAMS =', 'const EXAMS =') + '\nexport default EXAMS;';

const tempPath = 'scratch/temp_exams_inspect2.mjs';
fs.writeFileSync(tempPath, content);

const { default: EXAMS } = await import('./temp_exams_inspect2.mjs');
fs.unlinkSync(tempPath);

const chemKeys = Object.keys(EXAMS).filter(k => k.startsWith('che'));
const liveChemKeys = chemKeys.filter(k => EXAMS[k].comingSoon === false);

for (const key of liveChemKeys) {
  const exam = EXAMS[key];
  console.log(`\n=========================================`);
  console.log(`Key: ${key} | Title: ${exam.title} | Module: ${exam.module}`);
  console.log(`Questions Count: ${exam.questions?.length}`);
  if (exam.questions && exam.questions.length > 0) {
    console.log("Units represented:", [...new Set(exam.questions.map(q => q.unit))]);
    console.log("Sample Questions (first 3):");
    exam.questions.slice(0, 3).forEach((q, idx) => {
      console.log(`  ${idx + 1}. [Unit ${q.unit}] ${q.question.slice(0, 120)}...`);
    });
  }
}
