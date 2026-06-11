import fs from 'fs';
import path from 'path';

const jsPath = 'js/exams-data.js';
const content = fs.readFileSync(jsPath, 'utf8')
    .replace('export const EXAMS =', 'const EXAMS =') + '\nexport default EXAMS;';

const tempPath = 'scratch/temp_exams.mjs';
fs.writeFileSync(tempPath, content);

const { default: EXAMS } = await import('./temp_exams.mjs');
fs.unlinkSync(tempPath);

console.log('Geography subjects inside EXAMS:');
let activeCount = 0;
let totalCount = 0;
for (const [key, val] of Object.entries(EXAMS)) {
    if (key.startsWith('ggr')) {
        totalCount++;
        const questions = val.questions || [];
        if (!val.comingSoon) {
            activeCount++;
            console.log(`  "${key}": "${val.title}" - ${questions.length} questions, comingSoon: ${val.comingSoon}`);
        }
    }
}
console.log(`Total GGR keys: ${totalCount}, Active/Live: ${activeCount}`);
