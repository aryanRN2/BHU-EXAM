const fs = require('fs');
const path = require('path');

const srcDir = __dirname;
const wwwDir = path.join(__dirname, 'www');

// Ensure www directory exists
if (fs.existsSync(wwwDir)) {
  fs.rmSync(wwwDir, { recursive: true, force: true });
}
fs.mkdirSync(wwwDir, { recursive: true });

const filesToCopy = [
  'index.html',
  'contributors.html',
  'subjects.html',
  'syllabus.html',
  'js',
  'css',
  'SYLLABUS',
  'aaa'
];

filesToCopy.forEach(item => {
  const srcPath = path.join(srcDir, item);
  const destPath = path.join(wwwDir, item);
  
  if (fs.existsSync(srcPath)) {
    const stat = fs.statSync(srcPath);
    if (stat.isDirectory()) {
      fs.cpSync(srcPath, destPath, { recursive: true });
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
    console.log(`Copied: ${item}`);
  }
});

console.log('✓ www directory built successfully!');
