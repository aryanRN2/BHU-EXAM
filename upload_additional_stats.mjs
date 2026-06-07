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

const statsDir = "stats";
const filesToUpload = [
    "STA505_Practical_based_on_Course_No_STB_501_and_STB_502_2022_23.pdf",
    "STB_501___Applied_Statistics_2016_17.pdf",
    "STB_501___Applied_Statistics_2022_23.pdf"
];

async function uploadFile(fileName) {
  const filePath = path.join(statsDir, fileName);
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
  for (const file of filesToUpload) {
    await uploadFile(file);
  }
}

run().catch(console.error);
