import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.join(__dirname, "..");

// Load env variables manually from .env
const envContent = fs.readFileSync(path.join(rootDir, ".env"), "utf-8");
const env = {};
envContent.split("\n").forEach(line => {
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

// 1. Gather all math-related PDFs referenced in subjects.html
const subjectsHtmlPath = path.join(rootDir, "subjects.html");
const htmlContent = fs.readFileSync(subjectsHtmlPath, "utf-8");

const startIdx = htmlContent.indexOf("const EXAM_PYQS = {");
let braceCount = 1;
let endIdx = startIdx + "const EXAM_PYQS = {".length;
while (braceCount > 0 && endIdx < htmlContent.length) {
  const char = htmlContent[endIdx];
  if (char === "{") braceCount++;
  else if (char === "}") braceCount--;
  endIdx++;
}

const examPyqStr = htmlContent.substring(startIdx + "const EXAM_PYQS = ".length, endIdx).trim();
const EXAM_PYQS = eval(`(${examPyqStr})`);

const filesToDelete = new Set();
const mathPrefixRegex = /^(MTB|Abstract|Algebra|Analysis|Ancillary|Calculus|Combinatorial|Complex|Diff|Discrete|Dynamical|Geometry|Global|Linear|Math|Mechanics|Multivariable|Number|Numerical|Operations|PDE|Probability|Programming|Relativity|Set|Statics|Vector|ode)/i;

for (const [key, items] of Object.entries(EXAM_PYQS)) {
  for (const item of items) {
    if (item.file) {
      const match = item.file.match(/pyq-pdfs\/(.+)$/);
      if (match) {
        const decoded = decodeURIComponent(match[1]);
        if (mathPrefixRegex.test(decoded)) {
          filesToDelete.add(decoded);
        }
      }
    }
  }
}

// Also pro-actively add all files in corrected dir just in case
const correctedDir = path.join(rootDir, "aaa", "latest corrected maths pdf");
const correctedFiles = fs.readdirSync(correctedDir).filter(f => f.endsWith(".pdf"));
for (const file of correctedFiles) {
  filesToDelete.add(file);
}

const fileList = Array.from(filesToDelete);
console.log(`Found ${fileList.length} math-related PDF files to delete from Supabase storage:`, fileList);

// 2. Perform DELETE request to Supabase
async function deleteFiles() {
  const deleteUrl = `https://${projectRef}.supabase.co/storage/v1/object/pyq-pdfs`;
  console.log("Sending DELETE request to Supabase...");
  
  const response = await fetch(deleteUrl, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "apikey": apiKey,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prefixes: fileList })
  });

  if (response.ok) {
    const json = await response.json();
    console.log("DELETE successful response:", json);
  } else {
    const text = await response.text();
    console.error(`DELETE failed: Status ${response.status} - ${text}`);
  }
}

// 3. Upload corrected files
async function uploadFile(fileName) {
  const filePath = path.join(correctedDir, fileName);
  const fileBuffer = fs.readFileSync(filePath);
  const uploadUrl = `https://${projectRef}.supabase.co/storage/v1/object/pyq-pdfs/${encodeURIComponent(fileName)}`;

  console.log(`Uploading ${fileName} to Supabase...`);
  const response = await fetch(uploadUrl, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "apikey": apiKey,
      "Content-Type": "application/pdf",
      "x-upsert": "true"
    },
    body: fileBuffer
  });

  if (response.ok) {
    console.log(`  Success: ${fileName}`);
  } else {
    const text = await response.text();
    console.error(`  Failed to upload ${fileName}: Status ${response.status} - ${text}`);
  }
}

async function run() {
  if (fileList.length > 0) {
    await deleteFiles();
  }
  
  console.log(`\nUploading ${correctedFiles.length} corrected files...`);
  for (const file of correctedFiles) {
    await uploadFile(file);
  }
  
  console.log("\nSupabase sync completed!");
}

run().catch(console.error);
