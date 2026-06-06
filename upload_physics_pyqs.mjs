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

const filesToUpload = [
  "BPT_505___Electromagnetic_Theory_2015_16.pdf",
  "BPT_505___Electromagnetic_Theory_2016_17.pdf",
  "BPT_505___Electromagnetic_Theory_2017_18.pdf",
  "BPT_505___Electromagnetic_Theory_2019_20.pdf",
  "BPT_505___Electromagnetic_Theory_2020_21.pdf",
  "BPT_505___Electromagnetic_Theory_2021_22.pdf",
  "BPT_505___Electromagnetic_Theory_2022_23 (1).pdf",
  "BPT_505___Electromagnetic_Theory_2022_23.pdf"
];

async function uploadFile(fileName) {
  const filePath = path.join("physics", fileName);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    return;
  }

  const fileBuffer = fs.readFileSync(filePath);
  // We use the exact filename for the bucket object path
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
  for (const file of filesToUpload) {
    await uploadFile(file);
  }
}

run().catch(console.error);
