import fs from "fs";
import path from "path";

// Load env variables manually from .env
const envContent = fs.readFileSync(".env", "utf-8");
const env = {};
envContent.split("\n").forEach(line => {
  const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
  if (match) {
    const key = match[1];
    let value = match[2] || "";
    // remove quotes if present
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

const filesDir = "aaa/physics final";
const files = fs.readdirSync(filesDir).filter(f => f.endsWith(".pdf"));

async function uploadFile(fileName) {
  const filePath = path.join(filesDir, fileName);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    return;
  }

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
    console.log(`Successfully uploaded: ${fileName}`);
  } else {
    const text = await response.text();
    console.error(`Failed to upload ${fileName}: Status ${response.status} - ${text}`);
  }
}

async function run() {
  console.log(`Starting upload of ${files.length} files...`);
  for (const file of files) {
    await uploadFile(file);
  }
  console.log("Upload sequence completed!");
}

run().catch(console.error);
