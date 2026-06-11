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

// Safely read and parse LEGACY_PYQ_DATA from js/legacy-data.js
const jsPath = path.join(rootDir, "js", "legacy-data.js");
let LEGACY_PYQ_DATA = {};
if (fs.existsSync(jsPath)) {
  const content = fs.readFileSync(jsPath, "utf-8");
  const startIdx = content.indexOf("{");
  const endIdx = content.lastIndexOf("}");
  if (startIdx !== -1 && endIdx !== -1) {
    const jsonStr = content.substring(startIdx, endIdx + 1);
    try {
      LEGACY_PYQ_DATA = Function("return " + jsonStr)();
    } catch (e) {
      console.error("Error parsing legacy-data.js JSON:", e);
    }
  }
}

const scienceDir = path.join(rootDir, "aaa", "all science pyq");
const departments = fs.readdirSync(scienceDir).filter(name => {
  const fullPath = path.join(scienceDir, name);
  return fs.statSync(fullPath).isDirectory() && name !== ".git" && name !== "node_modules";
});

function getSemester(fileName) {
  const fn = fileName.toUpperCase();
  if (fn.includes("I_-_SEM") || fn.includes("I-SEM") || fn.includes("1ST_SEM") || fn.includes("SEM-I") || fn.includes("SEM_I") || fn.includes("SEM I") || (fn.includes("SEM") && fn.includes(" I ") || fn.endsWith("-I.PDF"))) {
    if (!fn.includes("II") && !fn.includes("III") && !fn.includes("IV") && !fn.includes("V") && !fn.includes("VI")) {
      return 1;
    }
  }
  if (fn.includes("VI-SEM") || fn.includes("VI-SEM") || fn.includes("6TH_SEM") || fn.includes("SEM-VI") || fn.includes("SEM_VI") || fn.includes("SEM VI")) return 6;
  if (fn.includes("IV-SEM") || fn.includes("IV-SEM") || fn.includes("4TH_SEM") || fn.includes("SEM-IV") || fn.includes("SEM_IV") || fn.includes("SEM IV")) return 4;
  if (fn.includes("V-SEM") || fn.includes("V-SEM") || fn.includes("5TH_SEM") || fn.includes("SEM-V") || fn.includes("SEM_V") || fn.includes("SEM V") || fn.includes("PART-III") || fn.includes("PART_III")) return 5;
  if (fn.includes("III-SEM") || fn.includes("III-SEM") || fn.includes("3RD_SEM") || fn.includes("SEM-III") || fn.includes("SEM_III") || fn.includes("SEM III")) return 3;
  if (fn.includes("II-SEM") || fn.includes("II-SEM") || fn.includes("2ND_SEM") || fn.includes("SEM-II") || fn.includes("SEM_II") || fn.includes("SEM II")) return 2;
  if (fn.includes("I_-_SEM") || fn.includes("I-SEM") || fn.includes("1ST_SEM") || fn.includes("SEM-I")) return 1;
  
  if (fn.includes("SEM-1") || fn.includes("SEM1")) return 1;
  if (fn.includes("SEM-2") || fn.includes("SEM2")) return 2;
  if (fn.includes("SEM-3") || fn.includes("SEM3")) return 3;
  if (fn.includes("SEM-4") || fn.includes("SEM4")) return 4;
  if (fn.includes("SEM-5") || fn.includes("SEM5")) return 5;
  if (fn.includes("SEM-6") || fn.includes("SEM6")) return 6;

  return 1;
}

async function uploadFile(dept, fileName) {
  const filePath = path.join(scienceDir, dept, fileName);
  const fileBuffer = fs.readFileSync(filePath);
  
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
    throw new Error(`Status ${response.status} - ${text}`);
  }
}

async function run() {
  const tasks = [];
  const updatedData = { ...LEGACY_PYQ_DATA };

  for (const dept of departments) {
    if (!updatedData[dept]) updatedData[dept] = [];
    const deptPath = path.join(scienceDir, dept);
    const localFiles = fs.readdirSync(deptPath).filter(name => name.endsWith(".pdf"));
    
    for (const file of localFiles) {
      // Check if it already exists in the metadata
      const alreadyPresent = updatedData[dept].some(entry => entry.fileName === file);
      if (!alreadyPresent) {
        console.log(`Found missing PDF in metadata: [${dept}] ${file}`);
        tasks.push({ dept, file });
      }
    }
  }

  if (tasks.length === 0) {
    console.log("All local PDF files are already present in the metadata!");
    return;
  }

  console.log(`Found ${tasks.length} missing files to upload.`);

  // Upload sequential to guarantee success and avoid socket resets for these few files
  for (const { dept, file } of tasks) {
    let retries = 3;
    let success = false;
    let publicUrl = "";
    
    while (retries > 0 && !success) {
      try {
        publicUrl = await uploadFile(dept, file);
        success = true;
      } catch (err) {
        console.error(`Failed to upload ${file}, retries left: ${retries - 1}. Error: ${err.message}`);
        retries--;
        if (retries > 0) {
          // Wait 2 seconds before retry
          await new Promise(r => setTimeout(r, 2000));
        }
      }
    }

    if (success) {
      const sem = getSemester(file);
      let cleanTitle = file.replace(".pdf", "").replace(/_/g, " ").replace(/-/g, " ");
      updatedData[dept].push({
        title: cleanTitle,
        fileName: file,
        url: publicUrl,
        semester: sem
      });
    } else {
      console.error(`Permanent failure uploading [${dept}] ${file}`);
    }
  }

  // Sort entries by semester to keep them neat
  for (const dept of Object.keys(updatedData)) {
    updatedData[dept].sort((a, b) => (a.semester || 1) - (b.semester || 1));
  }

  // Write updated metadata
  const jsContent = `// Automatically generated legacy curriculum PYQ data
export const LEGACY_PYQ_DATA = ${JSON.stringify(updatedData, null, 2)};
`;
  
  fs.writeFileSync(jsPath, jsContent, "utf-8");
  console.log(`Metadata successfully updated at ${jsPath}`);
}

run().catch(console.error);
