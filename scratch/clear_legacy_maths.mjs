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

// 1. Read js/legacy-data.js
const legacyDataPath = path.join(rootDir, "js", "legacy-data.js");
const jsContent = fs.readFileSync(legacyDataPath, "utf-8");
const jsonText = jsContent.substring(jsContent.indexOf("{")).trim().replace(/;$/, "");
const legacyData = JSON.parse(jsonText);

const mathsPapers = legacyData.maths || [];
const filesToDelete = mathsPapers.map(p => `science/maths/${p.fileName}`);

console.log(`Found ${filesToDelete.length} legacy maths papers to delete from Supabase:`, filesToDelete);

// 2. Delete from Supabase
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
    body: JSON.stringify({ prefixes: filesToDelete })
  });

  if (response.ok) {
    const json = await response.json();
    console.log("DELETE successful response:", json);
  } else {
    const text = await response.text();
    console.error(`DELETE failed: Status ${response.status} - ${text}`);
  }
}

// 3. Clear maths in legacyData and write back
function clearLegacyData() {
  legacyData.maths = [];
  const updatedJsContent = `// Automatically generated legacy curriculum PYQ data
export const LEGACY_PYQ_DATA = ${JSON.stringify(legacyData, null, 2)};
`;
  fs.writeFileSync(legacyDataPath, updatedJsContent, "utf-8");
  console.log("Successfully cleared maths key in js/legacy-data.js");
}

// 4. Delete local maths folder under all science pyq
function deleteLocalDir() {
  const targetDir = path.join(rootDir, "aaa", "all science pyq", "maths");
  if (fs.existsSync(targetDir)) {
    console.log(`Deleting local directory recursively: ${targetDir}`);
    fs.rmSync(targetDir, { recursive: true, force: true });
  } else {
    console.log(`Directory does not exist: ${targetDir}`);
  }
}

async function main() {
  if (filesToDelete.length > 0) {
    await deleteFiles();
  }
  clearLegacyData();
  deleteLocalDir();
  console.log("Legacy maths cleanup complete!");
}

main().catch(console.error);
