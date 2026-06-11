const fs = require('fs');
const path = require('path');

// 1. Find all PDF URLs in subjects.html
const subjectsHtml = fs.readFileSync(path.join(__dirname, '..', 'subjects.html'), 'utf8');
const pdfRegex = /"file":\s*"(https:\/\/sajmognuphnrvivtmuux\.supabase\.co\/storage\/v1\/object\/public\/pyq-pdfs\/([^"]+)\.pdf)"/g;
let match;
const pdfFiles = [];

while ((match = pdfRegex.exec(subjectsHtml)) !== null) {
    pdfFiles.push({
        url: match[1],
        filename: match[2]
    });
}

console.log(`Found ${pdfFiles.length} PDF links in subjects.html`);

// 2. Recursively find all .tex files in aaa/
function getTexFiles(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat && stat.isDirectory()) {
            results = results.concat(getTexFiles(fullPath));
        } else if (file.endsWith('.tex')) {
            results.push({
                relativePath: path.relative(path.join(__dirname, '..'), fullPath),
                name: file.replace('.tex', ''),
                fullPath: fullPath
            });
        }
    });
    return results;
}

const texFiles = getTexFiles(path.join(__dirname, '..', 'aaa'));
console.log(`Found ${texFiles.length} .tex files in aaa/`);

// Helper to normalize strings for comparison
function normalize(str) {
    return str.toLowerCase().replace(/[^a-z0-9]/g, '');
}

// 3. Find matches and mismatches
const matches = [];
const mismatches = [];

pdfFiles.forEach(pdf => {
    // Try exact match
    let found = texFiles.find(tex => tex.name === pdf.filename);
    if (found) {
        matches.push({ pdf: pdf.filename, tex: found.relativePath, type: 'exact' });
        return;
    }

    // Try normalized match
    const normPdf = normalize(pdf.filename);
    found = texFiles.find(tex => normalize(tex.name) === normPdf);
    if (found) {
        matches.push({ pdf: pdf.filename, tex: found.relativePath, type: 'normalized' });
        return;
    }

    // Try fuzzy match (does the normalized pdf filename match a substring of the normalized tex name or vice versa)
    found = texFiles.find(tex => {
        const normTex = normalize(tex.name);
        return normTex.includes(normPdf) || normPdf.includes(normTex);
    });
    if (found) {
        matches.push({ pdf: pdf.filename, tex: found.relativePath, type: 'fuzzy' });
        return;
    }

    // Special stats/code extraction match
    // E.g., STB_501 -> STB-501
    const codeMatch = pdf.filename.match(/([A-Z]{3})[-_](\d{3})/i);
    const yearMatch = pdf.filename.match(/(\d{4}[-_]\d{2})/);
    if (codeMatch && yearMatch) {
        const code = codeMatch[1].toUpperCase() + '-' + codeMatch[2];
        const year = yearMatch[1].replace('_', '-');
        
        found = texFiles.find(tex => {
            const nameUpper = tex.name.toUpperCase();
            return (nameUpper.includes(code) || nameUpper.includes(code.replace('-', '_'))) && 
                   nameUpper.includes(year);
        });
        if (found) {
            matches.push({ pdf: pdf.filename, tex: found.relativePath, type: 'code-year' });
            return;
        }
    }

    mismatches.push(pdf.filename);
});

console.log(`\nMatches found: ${matches.length}`);
console.log(`Mismatches (no matching local .tex file): ${mismatches.length}`);

if (mismatches.length > 0) {
    console.log('\n--- MISMATCHED FILENAMES ---');
    mismatches.forEach(m => {
        console.log(`PDF: ${m}`);
        // Let's print potential candidates in texFiles
        const normM = normalize(m);
        const candidates = texFiles.filter(tex => {
            const normTex = normalize(tex.name);
            // check if they share first 6 characters of normalized name
            return normTex.substring(0, 6) === normM.substring(0, 6);
        }).map(tex => tex.relativePath);
        if (candidates.length > 0) {
            console.log(`  Potential candidates: ${candidates.join(', ')}`);
        } else {
            console.log('  No candidates found with similar prefix.');
        }
    });
}
