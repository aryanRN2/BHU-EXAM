import fs from 'fs';
import path from 'path';

const commerceDir = '/Users/aryanmaurya/exam portal/COMMERCE_LATEX';
const results = [];

function walk(dir) {
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            walk(fullPath);
        } else if (file.endsWith('.tex')) {
            results.push(fullPath);
        }
    });
}

walk(commerceDir);

console.log(`Found ${results.length} tex files.`);

const parsedFiles = results.map(filePath => {
    const relativePath = path.relative('/Users/aryanmaurya/exam portal', filePath);
    const fileName = path.basename(filePath);
    
    // Read the first 45 lines to search for titles/codes
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n').slice(0, 45);
    
    // Attempt to parse metadata from comments or text
    let paperLine = lines.find(l => l.includes('% Paper:') || l.includes('Paper No.'));
    let paperTitle = '';
    let paperCode = '';
    
    if (paperLine) {
        // e.g. % Paper: BCH-122 : Financial Accounting - II
        // or {\large\bfseries Paper No. BCH-122: Financial Accounting - II}
        const match = paperLine.match(/(?:Paper(?:\s+No\.)?:?\s*)([A-Z0-9\-_]+)\s*[:\-]\s*(.*)/i);
        if (match) {
            paperCode = match[1].trim();
            paperTitle = match[2].replace(/[\}\\]/g, '').trim();
        }
    }
    
    // If not found in those formats, parse from filename
    // e.g., BCH214_CostAccounting_SemIII_2016-17.tex
    const fnMatch = fileName.match(/^([A-Z0-9]+)_(.*?)_(Sem[IVXLC\d]+)_(\d{4}-\d{2})\.tex$/i);
    let codeFromFn = '';
    let subjectFromFn = '';
    let semFromFn = '';
    let yearFromFn = '';
    
    if (fnMatch) {
        codeFromFn = fnMatch[1];
        subjectFromFn = fnMatch[2].replace(/([A-Z])/g, ' $1').trim();
        semFromFn = fnMatch[3];
        yearFromFn = fnMatch[4];
    } else {
        // backup match
        const fnMatch2 = fileName.match(/^([A-Z0-9]+)_(.*?)_([A-Za-z0-9\-]+)\.tex$/i);
        if (fnMatch2) {
            codeFromFn = fnMatch2[1];
            subjectFromFn = fnMatch2[2].replace(/([A-Z])/g, ' $1').trim();
        }
    }
    
    // Normalize semester
    let semester = 1;
    const semLower = (semFromFn || fileName).toLowerCase();
    if (semLower.includes('sem_i') || semLower.includes('semi_') || semLower.includes('sem-i') || semLower.includes('semi')) semester = 1;
    if (semLower.includes('sem_ii') || semLower.includes('semii_') || semLower.includes('sem-ii') || semLower.includes('semii')) semester = 2;
    if (semLower.includes('sem_iii') || semLower.includes('semiii_') || semLower.includes('sem-iii') || semLower.includes('semiii')) semester = 3;
    if (semLower.includes('sem_iv') || semLower.includes('semiv_') || semLower.includes('sem-iv') || semLower.includes('semiv')) semester = 4;
    if (semLower.includes('sem_v') || semLower.includes('semv_') || semLower.includes('sem-v') || semLower.includes('semv')) semester = 5;
    if (semLower.includes('sem_vi') || semLower.includes('semvi_') || semLower.includes('sem-vi') || semLower.includes('semvi')) semester = 6;
    
    return {
        fileName,
        filePath: relativePath,
        code: paperCode || codeFromFn,
        subject: paperTitle || subjectFromFn,
        semester,
        year: yearFromFn || (fileName.match(/\d{4}-\d{2}/) ? fileName.match(/\d{4}-\d{2}/)[0] : '')
    };
});

fs.writeFileSync('/Users/aryanmaurya/exam portal/scratch/commerce_parsed.json', JSON.stringify(parsedFiles, null, 2));
console.log('Written parsed files to scratch/commerce_parsed.json');
