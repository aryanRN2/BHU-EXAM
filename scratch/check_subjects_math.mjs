import fs from 'fs';
import path from 'path';

const htmlPath = 'subjects.html';
const content = fs.readFileSync(htmlPath, 'utf8');

// Match all URLs ending with .pdf
const pdfRegex = /https:\/\/sajmognuphnrvivtmuux\.supabase\.co\/storage\/v1\/object\/public\/pyq-pdfs\/([a-zA-Z0-9_\-\.%]+)/g;
let match;
const foundPdfs = new Set();
while ((match = pdfRegex.exec(content)) !== null) {
    foundPdfs.add(decodeURIComponent(match[1]));
}

console.log('Total unique PDFs found in subjects.html:', foundPdfs.size);

// Read bhu_maths_pyqs directory
const bhuMathsDir = 'aaa/bhu_maths_pyqs';
const bhuMathsFiles = fs.existsSync(bhuMathsDir) ? fs.readdirSync(bhuMathsDir) : [];
console.log('BHU Maths legacy files count:', bhuMathsFiles.length);

// Read mathematics content directory
const mathContentDir = 'mathematics content';
const mathContentFiles = fs.existsSync(mathContentDir) ? fs.readdirSync(mathContentDir) : [];
console.log('Mathematics Content files count:', mathContentFiles.length);

console.log('\nMatches in bhu_maths_pyqs:');
const matchedBhu = [];
for (const file of foundPdfs) {
    if (bhuMathsFiles.includes(file)) {
        matchedBhu.push(file);
    }
}
console.log(matchedBhu.sort());

console.log('\nMatches in mathematics content:');
const matchedContent = [];
for (const file of foundPdfs) {
    // Check direct match or space replaced by underscore match
    const foundDirect = mathContentFiles.includes(file);
    const foundUnderscore = mathContentFiles.includes(file.replace(/_/g, ' '));
    const foundUrlSpace = mathContentFiles.includes(file.replace(/ /g, '_'));
    if (foundDirect || foundUnderscore || foundUrlSpace) {
        matchedContent.push(file);
    }
}
console.log(matchedContent.sort());

console.log('\nOther PDFs (not in either math folder):');
const others = [];
for (const file of foundPdfs) {
    if (!matchedBhu.includes(file) && !matchedContent.includes(file)) {
        others.push(file);
    }
}
console.log(others.sort());
