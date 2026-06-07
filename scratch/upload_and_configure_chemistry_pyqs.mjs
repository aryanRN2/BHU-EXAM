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

const filesDir = path.join(rootDir, "aaa", "chemistry", "chemistry final");
const files = fs.readdirSync(filesDir).filter(f => f.endsWith(".pdf"));

async function uploadFile(fileName) {
  const filePath = path.join(filesDir, fileName);
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

function getSubjectKeys(fileName) {
  const code = fileName.split("_")[0].toUpperCase();
  if (code.startsWith("CHB-02A")) return ["chemd11"];
  if (code.startsWith("CHB-04A")) return ["chemd21"];
  if (code.startsWith("CHB-101")) return ["chemj11", "chemn11"];
  if (code.startsWith("CHB-201")) return ["chemj21", "chemn21"];
  if (code.startsWith("CHB-301") || code.startsWith("CHB-361")) return ["chemj32", "chemj33"];
  if (code.startsWith("CHB-401")) return ["chemj41", "chemj42"];
  if (code.startsWith("CHB-501")) return ["chemj51"];
  if (code.startsWith("CHB-502")) return ["chemj52"];
  if (code.startsWith("CHB-503")) return ["chemj53"];
  if (code.startsWith("CHB-504")) return ["chemj54"];
  if (code.startsWith("CHB-505")) return ["chemd31"];
  if (code.startsWith("CHB-601")) return ["chemj61"];
  if (code.startsWith("CHB-602")) return ["chemj62"];
  if (code.startsWith("CHB-603")) return ["chemj63"];
  if (code.startsWith("CHB-604")) return ["chemj64"];
  if (code.startsWith("CHB-605") || code.startsWith("CHB-608")) return ["chemj85", "chemj8r5"];
  return [];
}

function formatTitleAndDesc(fileName) {
  const name = fileName.replace(".pdf", "");
  const parts = name.split("_");
  const code = parts[0];
  const paperNameRaw = parts[1] || "";
  const year = parts[3] || "";
  
  // Format paper name nicely: insert space before capital letters
  let paperName = paperNameRaw.replace(/([A-Z])/g, ' $1').trim();
  
  const title = `${paperName} ${year} PDF`;
  const description = `Official ${code} ${paperName} ${year} paper`;
  
  return { title, description };
}

async function run() {
  console.log(`Starting upload of ${files.length} chemistry files...`);
  for (const file of files) {
    await uploadFile(file);
  }
  console.log("Upload sequence completed!");

  // Now read subjects.html
  const htmlPath = path.join(rootDir, "subjects.html");
  let htmlContent = fs.readFileSync(htmlPath, "utf-8");

  // Extract EXAM_PYQS block
  const startStr = "const EXAM_PYQS = {";
  const endStr = "};;";
  
  const startIdx = htmlContent.indexOf(startStr);
  const endIdx = htmlContent.indexOf(endStr, startIdx);
  
  if (startIdx === -1 || endIdx === -1) {
    console.error("Could not find EXAM_PYQS block in subjects.html");
    process.exit(1);
  }
  
  const objText = htmlContent.substring(startIdx + startStr.length - 1, endIdx + 1);
  
  // Evaluate the block to get the JavaScript object
  const EXAM_PYQS = Function(`return ${objText}`)();
  
  // Populate chemistry files into EXAM_PYQS
  files.forEach(file => {
    const keys = getSubjectKeys(file);
    const { title, description } = formatTitleAndDesc(file);
    const fileUrl = `https://${projectRef}.supabase.co/storage/v1/object/public/pyq-pdfs/${encodeURIComponent(file)}`;
    
    keys.forEach(key => {
      if (!EXAM_PYQS[key]) {
        EXAM_PYQS[key] = [];
      }
      // Check if already exists to avoid duplicates
      const exists = EXAM_PYQS[key].some(item => item.file === fileUrl);
      if (!exists) {
        EXAM_PYQS[key].push({
          title,
          file: fileUrl,
          description
        });
      }
    });
  });

  // Convert the updated object back to string
  const updatedObjText = JSON.stringify(EXAM_PYQS, null, 8);
  
  // Replace the old EXAM_PYQS block in subjects.html
  const newHtmlContent = htmlContent.substring(0, startIdx) + 
                         `const EXAM_PYQS = ${updatedObjText};\n    ` + 
                         htmlContent.substring(endIdx + 1);
                         
  fs.writeFileSync(htmlPath, newHtmlContent, "utf-8");
  console.log("Successfully updated subjects.html with chemistry PYQs!");
}

run().catch(console.error);
