import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Emulate __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load env variables manually from .env
const rootDir = path.join(__dirname, "..");
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

const scienceDir = path.join(rootDir, "aaa", "all science pyq");
const departments = fs.readdirSync(scienceDir).filter(name => {
  const fullPath = path.join(scienceDir, name);
  return fs.statSync(fullPath).isDirectory() && name !== ".git" && name !== "node_modules";
});

console.log("Departments found:", departments);

function getSemester(fileName) {
  const fn = fileName.toUpperCase();
  if (fn.includes("I_-_SEM") || fn.includes("I-SEM") || fn.includes("1ST_SEM") || fn.includes("SEM-I") || fn.includes("SEM_I") || fn.includes("SEM I") || (fn.includes("SEM") && fn.includes(" I ") || fn.endsWith("-I.PDF"))) {
    // Exclude Sem II/III/IV/V/VI
    if (!fn.includes("II") && !fn.includes("III") && !fn.includes("IV") && !fn.includes("V") && !fn.includes("VI")) {
      return 1;
    }
  }
  // Check higher semesters first to avoid overlap
  if (fn.includes("VI-SEM") || fn.includes("VI-SEM") || fn.includes("6TH_SEM") || fn.includes("SEM-VI") || fn.includes("SEM_VI") || fn.includes("SEM VI")) return 6;
  if (fn.includes("IV-SEM") || fn.includes("IV-SEM") || fn.includes("4TH_SEM") || fn.includes("SEM-IV") || fn.includes("SEM_IV") || fn.includes("SEM IV")) return 4;
  if (fn.includes("V-SEM") || fn.includes("V-SEM") || fn.includes("5TH_SEM") || fn.includes("SEM-V") || fn.includes("SEM_V") || fn.includes("SEM V") || fn.includes("PART-III") || fn.includes("PART_III")) return 5;
  if (fn.includes("III-SEM") || fn.includes("III-SEM") || fn.includes("3RD_SEM") || fn.includes("SEM-III") || fn.includes("SEM_III") || fn.includes("SEM III")) return 3;
  if (fn.includes("II-SEM") || fn.includes("II-SEM") || fn.includes("2ND_SEM") || fn.includes("SEM-II") || fn.includes("SEM_II") || fn.includes("SEM II")) return 2;
  if (fn.includes("I_-_SEM") || fn.includes("I-SEM") || fn.includes("1ST_SEM") || fn.includes("SEM-I")) return 1;
  
  // Additional fallbacks
  if (fn.includes("SEM-1") || fn.includes("SEM1")) return 1;
  if (fn.includes("SEM-2") || fn.includes("SEM2")) return 2;
  if (fn.includes("SEM-3") || fn.includes("SEM3")) return 3;
  if (fn.includes("SEM-4") || fn.includes("SEM4")) return 4;
  if (fn.includes("SEM-5") || fn.includes("SEM5")) return 5;
  if (fn.includes("SEM-6") || fn.includes("SEM6")) return 6;

  return 1; // default fallback to Sem 1
}

const metadata = {};

async function uploadFile(dept, fileName) {
  const filePath = path.join(scienceDir, dept, fileName);
  const fileBuffer = fs.readFileSync(filePath);
  
  // Upload to science/{dept}/{fileName}
  const storagePath = `science/${dept}/${fileName}`;
  const uploadUrl = `https://${projectRef}.supabase.co/storage/v1/object/pyq-pdfs/${encodeURIComponent(storagePath)}`;
  const publicUrl = `https://${projectRef}.supabase.co/storage/v1/object/public/pyq-pdfs/${encodeURIComponent(storagePath)}`;

  console.log(`Uploading [${dept}] ${fileName} to Supabase...`);
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
    return publicUrl;
  } else {
    const text = await response.text();
    console.error(`  Failed to upload ${fileName}: Status ${response.status} - ${text}`);
    // Fallback URL if we want to proceed anyway
    return publicUrl;
  }
}

async function run() {
  for (const dept of departments) {
    metadata[dept] = [];
    const deptPath = path.join(scienceDir, dept);
    const files = fs.readdirSync(deptPath).filter(name => name.endsWith(".pdf"));
    
    console.log(`Processing ${dept}: found ${files.length} PDFs.`);
    
    for (const file of files) {
      const publicUrl = await uploadFile(dept, file);
      const sem = getSemester(file);
      
      // Clean up title for display
      let cleanTitle = file.replace(".pdf", "").replace(/_/g, " ").replace(/-/g, " ");
      
      metadata[dept].push({
        title: cleanTitle,
        fileName: file,
        url: publicUrl,
        semester: sem
      });
    }
  }

  // Write metadata to legacy-data.js in the js folder
  const jsContent = `// Automatically generated legacy curriculum PYQ data
export const LEGACY_PYQ_DATA = ${JSON.stringify(metadata, null, 2)};
`;
  
  const jsPath = path.join(rootDir, "js", "legacy-data.js");
  fs.writeFileSync(jsPath, jsContent, "utf-8");
  console.log(`Metadata successfully written to ${jsPath}`);
}

run().catch(console.error);
