import fs from 'fs';
import path from 'path';

const botanyDir = 'aaa/BOTANY';
const files = fs.readdirSync(botanyDir).filter(f => f.endsWith('.tex'));

const papers = [];

for (const file of files) {
    const content = fs.readFileSync(path.join(botanyDir, file), 'utf8');
    
    // Find paper title
    let title = '';
    
    // Try to find title in \begin{center} ... \end{center}
    const centerMatch = content.match(/\\begin\{center\}(.*?)\\end\{center\}/s);
    if (centerMatch) {
        const centerText = centerMatch[1];
        // Look for: Paper: BOB-101 --- Cryptogams or Paper: BOB-101 - Cryptogams or Paper: BOB-101 Cryptogams
        // Or just the line below Botany
        const lines = centerText.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        
        // Let's search for the line starting with "Paper:"
        const paperLine = lines.find(l => l.toLowerCase().includes('paper:'));
        if (paperLine) {
            const parts = paperLine.split(/---|\b-\b|---|---/);
            if (parts.length > 1) {
                title = parts.slice(1).join(' ').trim();
            } else {
                // Try split by colon
                const colonParts = paperLine.split(':');
                if (colonParts.length > 1) {
                    title = colonParts.slice(1).join(':').trim();
                } else {
                    title = paperLine;
                }
            }
        }
    }
    
    if (!title) {
        // Fallback: search anywhere in file for "Paper:"
        const paperMatch = content.match(/Paper:\s*(.*?)(?:\\\\|---|\n|\$|\])/i);
        if (paperMatch) {
            const pVal = paperMatch[1];
            if (pVal.includes('---')) {
                title = pVal.split('---')[1].trim();
            } else {
                title = pVal.trim();
            }
        }
    }
    
    // Clean up title
    title = title
        .replace(/\\bfseries/g, '')
        .replace(/\\large/g, '')
        .replace(/\\normalsize/g, '')
        .replace(/\\\[.*?\]/g, '')
        .replace(/[\{\}\\]/g, '')
        .trim();

    // Extract code from filename
    const code = file.split('_').pop().replace('.tex', '');
    
    // Extracted digit-based semester
    const digitMatch = code.match(/\d/);
    const semester = digitMatch ? parseInt(digitMatch[0], 10) : 1;

    papers.push({
        file,
        code,
        title,
        semester
    });
}

papers.sort((a, b) => a.semester - b.semester || a.code.localeCompare(b.code));
console.log(JSON.stringify(papers, null, 2));
