const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '../js/exams-data.js');
let content = fs.readFileSync(filePath, 'utf8');

// Replace export const EXAMS = with global.EXAMS =
content = content.replace('export const EXAMS =', 'global.EXAMS =');

// Eval the code
eval(content);

console.log("Exam Keys starting with 'mat':");
for (const key in global.EXAMS) {
    if (key.startsWith('mat')) {
        const exam = global.EXAMS[key];
        console.log(`- ${key}: title="${exam.title}", comingSoon=${exam.comingSoon}, type=${exam.type}, questionsCount=${exam.questions ? exam.questions.length : 0}`);
    }
}
