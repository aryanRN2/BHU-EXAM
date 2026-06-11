import fs from 'fs';

const fileContent = fs.readFileSync('js/exams-data.js', 'utf-8');
// Since exams-data.js is a JS file exporting EXAMS, we can extract the JSON part or parse it using Function
const jsonStart = fileContent.indexOf('{');
const jsonEnd = fileContent.lastIndexOf('}');
const exams = Function(`return ${fileContent.substring(jsonStart, jsonEnd + 1)}`)();

console.log("Analyzing GLB (Geology) keys in EXAMS...");
const glbKeys = Object.keys(exams).filter(k => k.toLowerCase().startsWith('glb'));
console.log(`Found ${glbKeys.length} GLB keys:`);
for (const key of glbKeys) {
  const exam = exams[key];
  console.log(` - Key: ${key}, Title: "${exam.title}", comingSoon: ${exam.comingSoon}, questionsCount: ${exam.questions ? exam.questions.length : 0}`);
}
