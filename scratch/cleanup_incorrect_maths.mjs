import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.join(__dirname, '..');

// 1. Read files in bhu_maths_pyqs
const bhuMathsDir = path.join(rootDir, 'aaa', 'bhu_maths_pyqs');
if (!fs.existsSync(bhuMathsDir)) {
  console.error("Directory not found: " + bhuMathsDir);
  process.exit(1);
}

const bhuMathsFiles = fs.readdirSync(bhuMathsDir).filter(f => f.endsWith('.pdf'));
console.log(`Found ${bhuMathsFiles.length} PDF files in bhu_maths_pyqs directory.`);

// 2. Load env variables manually from .env
const envContent = fs.readFileSync(path.join(rootDir, '.env'), 'utf-8');
const env = {};
envContent.split('\n').forEach(line => {
  const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
  if (match) {
    const key = match[1];
    let value = match[2] || "";
    if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
    if (value.startsWith("'") && value.endsWith("'")) value = value.slice(1, -1);
    env[key] = value;
  }
});

const projectRef = env.SUPABASE_PROJECT_REF;
const apiKey = env.SUPABASE_SERVICE_ROLE_KEY;

if (!projectRef || !apiKey) {
  console.error("Error: Missing Supabase credentials in .env");
  process.exit(1);
}

// 3. Delete files from Supabase Storage
async function deleteSupabaseFiles() {
  const deleteUrl = `https://${projectRef}.supabase.co/storage/v1/object/pyq-pdfs`;
  console.log(`Sending request to delete ${bhuMathsFiles.length} files from Supabase Storage...`);
  
  // Supabase delete accepts batches of 100 paths
  const response = await fetch(deleteUrl, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'apikey': apiKey,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ prefixes: bhuMathsFiles })
  });

  if (response.ok) {
    const json = await response.json();
    console.log("Supabase deletion response:", json);
  } else {
    const text = await response.text();
    console.error(`Supabase deletion failed: Status ${response.status} - ${text}`);
  }
}

// 4. Delete local files and folders
function deleteLocalFiles() {
  if (fs.existsSync(bhuMathsDir)) {
    console.log(`Deleting local directory recursively: ${bhuMathsDir}`);
    fs.rmSync(bhuMathsDir, { recursive: true, force: true });
  }

  const zipPath = path.join(rootDir, 'aaa', 'bhu_maths_pyqs.zip');
  if (fs.existsSync(zipPath)) {
    console.log(`Deleting local zip file: ${zipPath}`);
    fs.unlinkSync(zipPath);
  }
}

// 5. Clean up subjects.html references
function cleanSubjectsHtml() {
  const htmlPath = path.join(rootDir, 'subjects.html');
  const htmlContent = fs.readFileSync(htmlPath, 'utf8');

  const startMarker = 'const EXAM_PYQS = ';
  const startIndex = htmlContent.indexOf(startMarker);
  if (startIndex === -1) {
    console.error("Could not find start of EXAM_PYQS in subjects.html");
    return;
  }

  // Find the closing brace of the EXAM_PYQS block.
  const endMarker = '};';
  const endIndex = htmlContent.indexOf(endMarker, startIndex);
  if (endIndex === -1) {
    console.error("Could not find end of EXAM_PYQS in subjects.html");
    return;
  }

  const pyqBlock = htmlContent.substring(startIndex + startMarker.length, endIndex + 1);
  
  let examPyqs;
  try {
    examPyqs = new Function(`return ${pyqBlock}`)();
  } catch (e) {
    console.error("Failed to parse EXAM_PYQS block: ", e);
    return;
  }

  let removedCount = 0;
  const newExamPyqs = {};
  for (const [subjCode, papers] of Object.entries(examPyqs)) {
    const filtered = papers.filter(paper => {
      const filename = paper.file.split('/').pop();
      const isIncorrect = bhuMathsFiles.includes(filename);
      if (isIncorrect) {
        removedCount++;
      }
      return !isIncorrect;
    });
    newExamPyqs[subjCode] = filtered;
  }

  console.log(`Filtered out ${removedCount} incorrect papers from EXAM_PYQS.`);

  // Format the new block nicely with tab formatting to match the page's styling
  const formattedBlock = JSON.stringify(newExamPyqs, null, '\t')
    .replace(/\n/g, '\n    ') // adjust indentation
    .replace(/\t/g, '        '); // replace tabs with spaces

  const newHtmlContent = htmlContent.substring(0, startIndex + startMarker.length) + 
                         formattedBlock + 
                         htmlContent.substring(endIndex + 1);

  fs.writeFileSync(htmlPath, newHtmlContent, 'utf8');
  console.log("Successfully updated subjects.html to remove incorrect references.");
}

async function main() {
  await deleteSupabaseFiles();
  deleteLocalFiles();
  cleanSubjectsHtml();
  console.log("Cleanup completed successfully!");
}

main().catch(console.error);
