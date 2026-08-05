const fs = require('fs');
const path = require('path');

const srcDir = __dirname;
const wwwDir = path.join(__dirname, 'www');

// Ensure www directory exists
if (fs.existsSync(wwwDir)) {
  fs.rmSync(wwwDir, { recursive: true, force: true });
}
fs.mkdirSync(wwwDir, { recursive: true });

// Copy essential web root files
const rootFiles = [
  'index.html',
  'contributors.html',
  'subjects.html',
  'syllabus.html',
  'nep-papers.html',
  'nep-science.html',
  'nep-pyq.html',
  'notes.html',
  'results.html',
  'exam.html',
  'pyq-viewer.html',
  'legacy-papers.html',
  'legacy-pyq.html',
  'legacy-science.html',
  'privacy.html',
  'terms.html',
  'styles.css',
  'robots.txt',
  'sitemap.xml'
];

rootFiles.forEach(file => {
  const src = path.join(srcDir, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(wwwDir, file));
  }
});

// Copy specific web directories
const directories = ['js', 'css', 'SYLLABUS', 'images'];

directories.forEach(dir => {
  const src = path.join(srcDir, dir);
  const dest = path.join(wwwDir, dir);
  if (fs.existsSync(src)) {
    fs.cpSync(src, dest, { recursive: true });
  }
});

// Copy ONLY aaa/ALL_PYQS_LATEX (excluding raw multi-hundred MB PDF scans)
const latexSrc = path.join(srcDir, 'aaa', 'ALL_PYQS_LATEX');
const latexDest = path.join(wwwDir, 'aaa', 'ALL_PYQS_LATEX');
if (fs.existsSync(latexSrc)) {
  fs.mkdirSync(path.join(wwwDir, 'aaa'), { recursive: true });
  fs.cpSync(latexSrc, latexDest, { recursive: true });
}

console.log('✓ Optimized www directory built successfully!');
