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

// Copy web asset directories
const directories = ['js', 'css', 'SYLLABUS', 'images'];

directories.forEach(dir => {
  const src = path.join(srcDir, dir);
  const dest = path.join(wwwDir, dir);
  if (fs.existsSync(src)) {
    fs.cpSync(src, dest, { recursive: true });
  }
});

// Helper function to recursively copy only .tex files (preserving folder structure)
function copyTexFilesOnly(sourceSubDir) {
  const sourcePath = path.join(srcDir, sourceSubDir);
  if (!fs.existsSync(sourcePath)) return;

  function walk(currentDir) {
    const items = fs.readdirSync(currentDir);
    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const relPath = path.relative(srcDir, fullPath);
      const destPath = path.join(wwwDir, relPath);

      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        walk(fullPath);
      } else if (item.endsWith('.tex') || item.endsWith('.json') || item.endsWith('.js') || item.endsWith('.md')) {
        const destDir = path.dirname(destPath);
        if (!fs.existsSync(destDir)) {
          fs.mkdirSync(destDir, { recursive: true });
        }
        fs.copyFileSync(fullPath, destPath);
      }
    }
  }

  walk(sourcePath);
}

// Copy all LaTeX files from COMMERCE_LATEX and aaa
copyTexFilesOnly('COMMERCE_LATEX');
copyTexFilesOnly('aaa');

console.log('✓ Comprehensive www directory built successfully with local fallback support!');
