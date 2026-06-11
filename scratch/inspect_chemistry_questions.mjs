import fs from 'fs';

const jsPath = 'js/exams-data.js';
const content = fs.readFileSync(jsPath, 'utf8')
    .replace('export const EXAMS =', 'const EXAMS =') + '\nexport default EXAMS;';

const tempPath = 'scratch/temp_exams_inspect.mjs';
fs.writeFileSync(tempPath, content);

const { default: EXAMS } = await import('./temp_exams_inspect.mjs');
fs.unlinkSync(tempPath);

const chemKeys = Object.keys(EXAMS).filter(k => k.startsWith('che'));
console.log(`Found ${chemKeys.length} chemistry keys in EXAMS.`);

const liveChemKeys = chemKeys.filter(k => EXAMS[k].comingSoon === false);
console.log(`Found ${liveChemKeys.length} live chemistry keys.`);

if (liveChemKeys.length > 0) {
  const firstKey = liveChemKeys[0];
  const exam = EXAMS[firstKey];
  console.log(`\nExample Exam Key: ${firstKey}`);
  console.log(`Title: ${exam.title}`);
  console.log(`Module: ${exam.module}`);
  console.log(`Number of questions: ${exam.questions?.length}`);
  if (exam.questions && exam.questions.length > 0) {
    console.log(`First question structure:`, JSON.stringify(exam.questions[0], null, 2));
  }
}
