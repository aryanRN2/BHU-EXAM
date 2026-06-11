import fs from "fs";
import path from "path";

// Mappings for Geology subjects to GLB Keys
const UNIQUE_TO_ACTIVE = {
  "glbmj11": ["glbmj11", "glbmn11", "glbmd11"],
  "glbmj21": ["glbmj21", "glbmn21"],
  "glbmj31": ["glbmj31"],
  "glbmj41": ["glbmj41"],
  "glbmj51": ["glbmj51"],
  "glbmj52": ["glbmj52"],
  "glbmj53": ["glbmj53"],
  "glbmj61": ["glbmj61"],
  "glbmj62": ["glbmj62"],
  "glbmj63": ["glbmj63"],
  "glbmj64": ["glbmj64"]
};

const keyToNepCode = {
  "glbmj11": "GLBMJ11 / GLBMN11 / GLBMD11",
  "glbmj21": "GLBMJ21 / GLBMN21",
  "glbmj31": "GLBMJ31",
  "glbmj41": "GLBMJ41",
  "glbmj51": "GLBMJ51",
  "glbmj52": "GLBMJ52",
  "glbmj53": "GLBMJ53",
  "glbmj61": "GLBMJ61",
  "glbmj62": "GLBMJ62",
  "glbmj63": "GLBMJ63",
  "glbmj64": "GLBMJ64"
};

const topicMappings = {
  "ELEMENTARYPHYSICALSTRUCTURALGEOLOGY": "Elementary Physical & Structural Geology",
  "ELEMENTSOFGEOLOGYIANCILLARY": "Elements of Geology I (Ancillary)",
  "ELEMENTSOFGEOLOGYIIANCILLARY": "Elements of Geology II (Ancillary)",
  "ELEMENTSOFGEOLOGYII": "Elements of Geology II",
  "ELEMENTSOFEARTHSCIENCEANCILLARY": "Elements of Earth Science (Ancillary)",
  "ELEMENTSOFMINERALOGYCRYSTALLOGRAPHY": "Elements of Mineralogy & Crystallography",
  "PETROLOGYECONOMICGEOLOGY": "Petrology & Economic Geology",
  "PALAEONTOLOGYSTRATIGRAPHY": "Palaeontology & Stratigraphy",
  "PHYSICALSTRUCTURALGEOLOGY": "Physical & Structural Geology",
  "IGNEOUSPETROLOGYMINERALOGYCRYSTALLOGRAPHY": "Igneous Petrology, Mineralogy & Crystallography",
  "SEDIMENTARYMETAMORPHICPETROLOGY": "Sedimentary & Metamorphic Petrology",
  "PALAEONTOLOGY": "Palaeontology",
  "STRATIGRAPHY": "Stratigraphy",
  "HYDROGEOLOGYENVIRONMENTALEXPLORATIONCOMPUTER": "Hydrogeology, Environmental Geology & Exploration",
  "ECONOMICGEOLOGY": "Economic Geology"
};

function getGlbMapping(fileName) {
  const fn = fileName.toUpperCase();
  if (fn.includes("PHYSICALSTRUCTURALGEOLOGY") || fn.includes("ELEMENTARYPHYSICALSTRUCTURALGEOLOGY")) {
    if (fn.includes("SEMI_")) return "glbmj11";
    if (fn.includes("SEMV_")) return "glbmj51";
  }
  if (fn.includes("MINERALOGYCRYSTALLOGRAPHY") || fn.includes("ELEMENTSOFMINERALOGYCRYSTALLOGRAPHY") || fn.includes("ELEMENTSOFGEOLOGYI")) {
    if (fn.includes("SEMII_")) return "glbmj21";
    if (fn.includes("SEMV_")) return "glbmj52";
  }
  if (fn.includes("PETROLOGYECONOMICGEOLOGY")) return "glbmj31";
  if (fn.includes("PALAEONTOLOGYSTRATIGRAPHY") || fn.includes("ELEMENTSOFGEOLOGYII")) return "glbmj41";
  if (fn.includes("SEDIMENTARYMETAMORPHICPETROLOGY")) return "glbmj53";
  if (fn.includes("ELEMENTSOFEARTHSCIENCE")) {
    if (fn.includes("SEMII_")) return "glbmj21"; // minor/ancillary fallback
    if (fn.includes("SEMV_")) return "glbmj53";
  }
  if (fn.includes("PALAEONTOLOGY")) return "glbmj61";
  if (fn.includes("STRATIGRAPHY")) {
    if (fn.includes("SEMIV_")) return "glbmj41";
    if (fn.includes("SEMVI_")) return "glbmj62";
  }
  if (fn.includes("HYDROGEOLOGY")) return "glbmj63";
  if (fn.includes("ECONOMICGEOLOGY")) return "glbmj64";
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
  const matchKey = rawTopic.toUpperCase();
  const topic = topicMappings[matchKey] || rawTopic.replace(/([A-Z])/g, ' $1').trim();

  // Create clean title
  const title = `${topic} ${year} (${degree}) LaTeX Code`;
  const description = `Official ${code} ${topic} ${year} LaTeX Paper`;

  // Determine nepCode
  const mappingKey = getGlbMapping(fileName);
  const nepCode = keyToNepCode[mappingKey] || "GLBMJ11 / GLBMN11 / GLBMD11";

  return { code, topic, semester, year, degree, title, description, nepCode };
}

const geoDir = "aaa/geology";
const files = fs.readdirSync(geoDir);
const texFiles = files.filter(f => f.endsWith(".tex")).sort();

async function run() {
  console.log(`Scanning Geology directory: Found ${texFiles.length} LaTeX papers...`);

  // 1. Build EXAM_PYQS mapping for subjects.html directly to local .tex files
  const geoPyqMapping = {};
  for (const tex of texFiles) {
    const baseKey = getGlbMapping(tex);
    if (!baseKey) {
      console.warn(`Could not determine GLB key mapping for ${tex}`);
      continue;
    }

    const { title, description } = parseFilename(tex);
    const localTexUrl = `aaa/geology/${tex}`;
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

  // Merge the new Geology entries
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

  // Generate and append Geology entries
  const newNepEntries = [];
  for (const tex of texFiles) {
    const { code, topic, semester, year, nepCode } = parseFilename(tex);
    const relativePath = `aaa/geology/${tex}`;

    const newEntry = {
      code,
      subject: topic,
      semester,
      year,
      department: "Geology",
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

  console.log("All LaTeX Geology integrations completed successfully!");
}

run().catch(console.error);
