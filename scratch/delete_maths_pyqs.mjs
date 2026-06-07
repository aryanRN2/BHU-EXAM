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

// 1. Read files to delete from js/legacy-data.js before we modify it
const jsContent = fs.readFileSync(path.join(rootDir, "js", "legacy-data.js"), "utf-8");
const jsonText = jsContent.substring(jsContent.indexOf("{")).trim().replace(/;$/, "");
const legacyData = JSON.parse(jsonText);
const mathsPapers = legacyData.maths || [];
const filesToDelete = mathsPapers.map(p => `science/maths/${p.fileName}`);

console.log("Files to delete from Supabase:", filesToDelete);

// 2. Delete files from Supabase Storage
async function deleteSupabaseFiles(prefixes) {
  const deleteUrl = `https://${projectRef}.supabase.co/storage/v1/object/pyq-pdfs`;
  
  console.log(`Sending request to delete files from Supabase Storage...`);
  const response = await fetch(deleteUrl, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "apikey": apiKey,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prefixes })
  });

  if (response.ok) {
    const json = await response.json();
    console.log("Supabase deletion response:", json);
  } else {
    const text = await response.text();
    console.error(`Supabase deletion failed: Status ${response.status} - ${text}`);
  }
}

// 3. Delete physical files from local directories
function deleteLocalFiles() {
  const targetDir = path.join(rootDir, "aaa", "maths", "bhu_maths_pyqs");
  const zipFile = path.join(rootDir, "aaa", "maths", "bhu_maths_pyqs.zip");
  const mergedFile = path.join(rootDir, "aaa", "maths", "bhu_maths_pyqs_merged.pdf");

  if (fs.existsSync(targetDir)) {
    console.log(`Deleting directory recursively: ${targetDir}`);
    fs.rmSync(targetDir, { recursive: true, force: true });
  } else {
    console.log(`Directory does not exist: ${targetDir}`);
  }

  if (fs.existsSync(zipFile)) {
    console.log(`Deleting zip file: ${zipFile}`);
    fs.unlinkSync(zipFile);
  }

  if (fs.existsSync(mergedFile)) {
    console.log(`Deleting merged PDF file: ${mergedFile}`);
    fs.unlinkSync(mergedFile);
  }
}

// 4. Update js/legacy-data.js
function updateMetadataFile() {
  const jsPath = path.join(rootDir, "js", "legacy-data.js");
  const updatedData = { ...legacyData, maths: [] };
  const jsContent = `// Automatically generated legacy curriculum PYQ data
export const LEGACY_PYQ_DATA = ${JSON.stringify(updatedData, null, 2)};
`;
  
  fs.writeFileSync(jsPath, jsContent, "utf-8");
  console.log(`Successfully updated metadata file: ${jsPath}`);
}

async function main() {
  if (filesToDelete.length > 0) {
    await deleteSupabaseFiles(filesToDelete);
  } else {
    console.log("No files found to delete from Supabase.");
  }
  
  console.log("Deleting local files...");
  deleteLocalFiles();
  
  console.log("Updating web metadata...");
  updateMetadataFile();
}

main().catch(console.error);
