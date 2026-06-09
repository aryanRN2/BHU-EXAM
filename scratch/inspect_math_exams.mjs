import { EXAMS } from '../js/exams-data.js';

console.log("Exam Keys starting with 'mat':");
for (const key in EXAMS) {
    if (key.startsWith('mat')) {
        const exam = EXAMS[key];
        console.log(`- ${key}: title="${exam.title}", comingSoon=${exam.comingSoon}, type=${exam.type}, questionsCount=${exam.questions ? exam.questions.length : 0}`);
    }
}
