import fs from 'fs';
import path from 'path';

const jsPath = 'js/exams-data.js';
const content = fs.readFileSync(jsPath, 'utf8')
    .replace('export const EXAMS =', 'const EXAMS =') + '\nexport default EXAMS;';

const tempPath = 'scratch/temp_exams.mjs';
fs.writeFileSync(tempPath, content);

const { default: EXAMS } = await import('./temp_exams.mjs');
fs.unlinkSync(tempPath);

console.log('Math subjects inside EXAMS:');
for (const [key, val] of Object.entries(EXAMS)) {
    if (key.startsWith('mat') || key.startsWith('sta')) {
        console.log(`  "${key}": "${val.title}" (${val.module || ''})`);
    }
}
