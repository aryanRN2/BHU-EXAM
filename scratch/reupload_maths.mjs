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

const mathsDir = path.join(rootDir, "aaa", "all science pyq", "maths");
const files = fs.readdirSync(mathsDir).filter(name => name.endsWith(".pdf"));

async function uploadFile(fileName) {
  const filePath = path.join(mathsDir, fileName);
  const fileBuffer = fs.readFileSync(filePath);
  
  const storagePath = `science/maths/${fileName}`;
  const uploadUrl = `https://${projectRef}.supabase.co/storage/v1/object/pyq-pdfs/${encodeURIComponent(storagePath)}`;

  console.log(`Re-uploading maths/${fileName} to Supabase...`);
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
  console.log(`Starting re-upload of ${files.length} Mathematics PDFs...`);
  for (const file of files) {
    await uploadFile(file);
  }
  console.log("Re-upload completed successfully!");
}

run().catch(console.error);
