import fs from 'fs';

console.log("Analyzing CS Exam and PYQ Mapping...");

// Read exams-data.js
const examsContent = fs.readFileSync('./js/exams-data.js', 'utf8')
  .replace('export const EXAMS =', 'const EXAMS =')
  .replace(/export\s+/g, '');
const evalExamsEnv = new Function(examsContent + '; return EXAMS;');
const EXAMS = evalExamsEnv();

// Read nep-data.js
const nepContent = fs.readFileSync('./js/nep-data.js', 'utf8')
  .replace('export const NEP_LATEX_PYQ_DATA =', 'const NEP_LATEX_PYQ_DATA =')
  .replace(/export\s+/g, '');
const evalNepEnv = new Function(nepContent + '; return NEP_LATEX_PYQ_DATA;');
const NEP_LATEX_PYQ_DATA = evalNepEnv();

const csExams = Object.keys(EXAMS).filter(k => k.startsWith('csc'));
console.log(`Total CS Exams in exams-data.js: ${csExams.length}`);

const csPapers = NEP_LATEX_PYQ_DATA.filter(p => p.department && p.department.toLowerCase().includes('computer'));
console.log(`Total CS Papers in nep-data.js: ${csPapers.length}`);

// Check which CS exams have papers mapped
const mappedExams = {};
csPapers.forEach(paper => {
  if (!paper.nepCode) return;
  const rawCodes = paper.nepCode.split('/').map(c => c.trim().toLowerCase());
  rawCodes.forEach(code => {
    if (code.startsWith('csc')) {
      if (!mappedExams[code]) mappedExams[code] = [];
      mappedExams[code].push(paper);
    }
  });
});

console.log("\nCS Exams with PYQ papers mapped:");
Object.keys(mappedExams).forEach(code => {
  console.log(`- ${code}: ${mappedExams[code].length} papers (${EXAMS[code] ? EXAMS[code].title : 'NOT FOUND IN EXAMS'})`);
});

console.log("\nCS Exams with NO PYQ papers mapped:");
csExams.forEach(code => {
  if (!mappedExams[code]) {
    console.log(`- ${code}: ${EXAMS[code].title} (${EXAMS[code].module})`);
  }
});
