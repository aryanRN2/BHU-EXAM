import fs from "fs";
import path from "path";

// Mappings for Geography subjects to GGR Keys
const UNIQUE_TO_ACTIVE = {
  "ggrmj11": ["ggrmj11", "ggrmn11", "ggrmd11"],
  "ggrmj21": ["ggrmj21", "ggrmn21"],
  "ggrse11": ["ggrse11"],
  "ggrmj31": ["ggrmj31"],
  "ggrmj52": ["ggrmj52"],
  "ggrmj43": ["ggrmj43", "ggrmj83i"],
  "ggrmj33": ["ggrmj33"],
  "ggrmj62": ["ggrmj62"],
  "ggrmj53": ["ggrmj53", "ggrmj74b", "ggrmj7r4b"],
  "ggrmj83f": ["ggrmj83f"],
  "ggrmj51": ["ggrmj51"],
  "ggrmj41": ["ggrmj41", "ggrmj74a", "ggrmj7r4a"],
  "ggrmj74d": ["ggrmj74d", "ggrmj7r4d"],
  "ggrmj65b": ["ggrmj65b"],
  "ggrse21": ["ggrse21"],
  "ggrmj67": ["ggrmj67"]
};

const subjectToNepCode = {
  "PHYSICALBASIS": "GGRMJ11 / GGRMN11 / GGRMD11",
  "HUMANGEOGRAPHY": "GGRMJ21 / GGRMN21",
  "MANANDENVIRONMENT": "GGRSE11",
  "ECONOMICGEOGRAPHY": "GGRMJ31",
  "REGIONALGEOGRAPHY": "GGRMJ52",
  "GEOMORPHOLOGY": "GGRMJ43 / GGRMJ83i",
  "GEOGRAPHYOFINDIA": "GGRMJ33",
  "OCEANOGRAPHY": "GGRMJ62",
  "POPULATIONGEOGRAPHY": "GGRMJ53 / GGRMJ74b / GGRMJ7r4b",
  "AGRICULTURALGEOGRAPHY": "GGRMJ83f",
  "CLIMATOLOGY": "GGRMJ51",
  "EVOLUTIONOFGEOGRAPHICALTHOUGHT": "GGRMJ41 / GGRMJ74a / GGRMJ7r4a",
  "REGIONALDEVELOPMENT": "GGRMJ74d / GGRMJ7r4d",
  "REGIONALPLANNING": "GGRMJ74d / GGRMJ7r4d",
  "SETTLEMENTGEOGRAPHY": "GGRMJ65b",
  "BASICSOFREMOTESENSING": "GGRSE21",
  "POLITICALGEOGRAPHY": "GGRMJ67"
};

function getGgrMapping(fileName) {
  const fn = fileName.toUpperCase();
  if (fn.includes("PHYSICALBASIS")) return "ggrmj11";
  if (fn.includes("HUMANGEOGRAPHY")) return "ggrmj21";
  if (fn.includes("MANANDENVIRONMENT")) return "ggrse11";
  if (fn.includes("ECONOMICGEOGRAPHY")) return "ggrmj31";
  if (fn.includes("REGIONALGEOGRAPHY")) return "ggrmj52";
  if (fn.includes("GEOMORPHOLOGY")) return "ggrmj43";
  if (fn.includes("GEOGRAPHYOFINDIA")) return "ggrmj33";
  if (fn.includes("OCEANOGRAPHY")) return "ggrmj62";
  if (fn.includes("POPULATIONGEOGRAPHY")) return "ggrmj53";
  if (fn.includes("AGRICULTURALGEOGRAPHY")) return "ggrmj83f";
  if (fn.includes("CLIMATOLOGY")) return "ggrmj51";
  if (fn.includes("EVOLUTIONOFGEOGRAPHICALTHOUGHT")) return "ggrmj41";
  if (fn.includes("REGIONALDEVELOPMENT") || fn.includes("REGIONALPLANNING")) return "ggrmj74d";
  if (fn.includes("SETTLEMENTGEOGRAPHY")) return "ggrmj65b";
  if (fn.includes("BASICSOFREMOTESENSING")) return "ggrse21";
  if (fn.includes("POLITICALGEOGRAPHY")) return "ggrmj67";
  return null;
}

function parseFilename(fileName) {
  const base = fileName.slice(0, -4); // remove extension
  const parts = base.split('_');

  const code = parts[0] || "";
  const rawTopic = parts[1] || "";
  const semStr = parts[2] || "SemI";
  const year = parts[3] || "";
  const degree = parts[4] || "";

  // Semester mapping
  let semester = 1;
  if (semStr.includes("II")) semester = 2;
  if (semStr.includes("III")) semester = 3;
  if (semStr.includes("IV")) semester = 4;
  if (semStr.includes("V")) semester = 5;
  if (semStr.includes("VI")) semester = 6;

  // Topic formatting
  let topic = rawTopic
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .trim();

  // Handle minor naming details
  topic = topic.replace("Of", "of").replace("And", "and").replace("To", "to");

  // Create clean title
  const title = `${topic} ${year} (${degree}) LaTeX Code`;
  const description = `Official ${code} ${topic} ${year} LaTeX Paper`;

  // Determine nepCode
  let nepCode = "GGRMJ11";
  for (const [key, codeVal] of Object.entries(subjectToNepCode)) {
    if (rawTopic.toUpperCase().includes(key)) {
      nepCode = codeVal;
      break;
    }
  }

  return { code, topic, semester, year, degree, title, description, nepCode };
}

const geoDir = "aaa/geography";
const files = fs.readdirSync(geoDir);
const texFiles = files.filter(f => f.endsWith(".tex")).sort();

async function run() {
  console.log(`Scanning Geography directory: Found ${texFiles.length} LaTeX papers...`);

  // 1. Build EXAM_PYQS mapping for subjects.html directly to local .tex files
  const geoPyqMapping = {};
  for (const tex of texFiles) {
    const baseKey = getGgrMapping(tex);
    if (!baseKey) {
      console.warn(`Could not determine GGR key mapping for ${tex}`);
      continue;
    }

    const { title, description } = parseFilename(tex);
    const localTexUrl = `aaa/geography/${tex}`;
    const pyqEntry = { title, file: localTexUrl, description };

    // Map to all active alternative keys
    const targetKeys = UNIQUE_TO_ACTIVE[baseKey] || [baseKey];
    targetKeys.forEach(k => {
      if (!geoPyqMapping[k]) geoPyqMapping[k] = [];
      geoPyqMapping[k].push(pyqEntry);
    });
  }

  // 2. Update subjects.html's EXAM_PYQS
  console.log("Updating subjects.html...");
  const subjectsPath = "subjects.html";
  let subjectsHtml = fs.readFileSync(subjectsPath, "utf-8");

  const startMarker = "const EXAM_PYQS = {";
  const startIndex = subjectsHtml.indexOf(startMarker);
  const mergeMarker = "// Merge redundant Major and Minor";
  const markerIndex = subjectsHtml.indexOf(mergeMarker);

  if (startIndex === -1 || markerIndex === -1) {
    throw new Error("Could not find start or merge markers in subjects.html!");
  }

  const endIndex = subjectsHtml.lastIndexOf("};", markerIndex);
  if (endIndex === -1 || endIndex < startIndex) {
    throw new Error("Could not find matching closing brace }; for EXAM_PYQS in subjects.html");
  }

  // Extract old EXAM_PYQS JS block and convert to JSON
  const pyqBlockText = subjectsHtml.substring(startIndex + startMarker.length - 1, endIndex + 1);
  const currentExamPyqs = Function(`return ${pyqBlockText}`)();

  // Merge the new Geography entries
  for (const [k, arr] of Object.entries(geoPyqMapping)) {
    currentExamPyqs[k] = arr;
  }

  // Serialize back to formatted JS
  const serialized = "const EXAM_PYQS = " + JSON.stringify(currentExamPyqs, null, 8)
    .replace(/\n\s*\]/g, '\n        ]')
    .replace(/\n\s*\}/g, '\n    }') + ";";

  const preBlock = subjectsHtml.substring(0, startIndex);
  const postBlock = subjectsHtml.substring(endIndex + 2);
  
  const updatedSubjectsHtml = preBlock + serialized + postBlock;
  fs.writeFileSync(subjectsPath, updatedSubjectsHtml, "utf-8");
  console.log("subjects.html successfully updated!");

  // 3. Update js/nep-data.js
  console.log("Updating js/nep-data.js...");
  const nepDataPath = "js/nep-data.js";
  let nepDataContent = fs.readFileSync(nepDataPath, "utf-8");

  // Parse existing array
  const arrStart = nepDataContent.indexOf("[");
  const arrEnd = nepDataContent.lastIndexOf("]");
  const arrayText = nepDataContent.substring(arrStart, arrEnd + 1);
  const currentNepData = JSON.parse(arrayText);

  // Generate and append Geography entries
  const newNepEntries = [];
  for (const tex of texFiles) {
    const { code, topic, semester, year, nepCode } = parseFilename(tex);
    const relativePath = `aaa/geography/${tex}`;

    const newEntry = {
      code,
      subject: topic,
      semester,
      year,
      department: "Geography",
      filePath: relativePath,
      fileName: tex,
      nepCode,
      oldCode: code
    };
    newNepEntries.push(newEntry);
  }

  // Deduplicate and merge
  const dedupedNepData = [...currentNepData];
  newNepEntries.forEach(entry => {
    // Overwrite/update if already exists to ensure correct parameters
    const existingIndex = dedupedNepData.findIndex(e => e.fileName === entry.fileName);
    if (existingIndex !== -1) {
      dedupedNepData[existingIndex] = entry;
    } else {
      dedupedNepData.push(entry);
    }
  });

  const updatedNepData = "export const NEP_LATEX_PYQ_DATA = " + JSON.stringify(dedupedNepData, null, 2) + ";\n";
  fs.writeFileSync(nepDataPath, updatedNepData, "utf-8");
  console.log("js/nep-data.js successfully updated!");

  console.log("All LaTeX Geography integrations completed successfully!");
}

run().catch(console.error);
