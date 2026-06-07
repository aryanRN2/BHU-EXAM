import fs from "fs";
import path from "path";

// Helper function to capitalize/space camelcase names
function formatSubjectName(name) {
  // e.g. MechanicsandRelativity -> Mechanics and Relativity
  // We first separate lowercase conjunctions/prepositions between camelcase components
  let clean = name
    .replace(/([a-z])(and|in|of|to)([A-Z])/g, "$1 $2 $3")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/\s+/g, " ")
    .trim();
  
  return clean;
}

const filesDir = "aaa/physics final";
const files = fs.readdirSync(filesDir).filter(f => f.endsWith(".pdf"));

const examPyqMapping = {};
const legacyEntries = [];

files.forEach(file => {
  const nameWithoutExt = file.replace(".pdf", "");
  const parts = nameWithoutExt.split("_");
  const code = parts[0];
  const namePart = parts[1] || "";
  const semPart = parts[2] || "";
  const yearPart = parts[3] || "";

  // Parse semester number
  let semester = 1;
  if (semPart.toUpperCase().includes("SEMVI")) semester = 6;
  else if (semPart.toUpperCase().includes("SEMV")) semester = 5;
  else if (semPart.toUpperCase().includes("SEMIV")) semester = 4;
  else if (semPart.toUpperCase().includes("SEMIII")) semester = 3;
  else if (semPart.toUpperCase().includes("SEMII")) semester = 2;
  else if (semPart.toUpperCase().includes("SEMI")) semester = 1;

  // Format title and subject name
  let formattedName = formatSubjectName(namePart);
  // Manual overrides for nice formatting
  if (formattedName.toLowerCase() === "mechanicsand relativity") formattedName = "Mechanics and Relativity";
  if (formattedName.toLowerCase() === "thermal physics") formattedName = "Thermal Physics";
  if (formattedName.toLowerCase() === "optics") formattedName = "Optics";
  if (formattedName.toLowerCase() === "electromagnetic theory") formattedName = "Electromagnetic Theory";
  if (formattedName.toLowerCase() === "mathematical physics") formattedName = "Mathematical Physics";
  if (formattedName.toLowerCase() === "classical mechanics") formattedName = "Classical Mechanics";
  if (formattedName.toLowerCase() === "quantum mechanics") formattedName = "Quantum Mechanics";
  if (formattedName.toLowerCase() === "electronic devicesand circuits") formattedName = "Electronic Devices and Circuits";
  if (formattedName.toLowerCase() === "statistical mechanics") formattedName = "Statistical Mechanics";
  if (formattedName.toLowerCase() === "solid state physics") formattedName = "Solid State Physics";
  if (formattedName.toLowerCase() === "elementsof nuclear physics") formattedName = "Elements of Nuclear Physics";
  if (formattedName.toLowerCase() === "atomic physicsand lasers") formattedName = "Atomic Physics and Lasers";
  if (formattedName.toLowerCase() === "topicsin modern physics") formattedName = "Topics in Modern Physics";
  if (formattedName.toLowerCase() === "elementary nanoscience") formattedName = "Elementary Nanoscience";
  if (formattedName.toLowerCase() === "ancillary physics i") formattedName = "Ancillary Physics-I";
  if (formattedName.toLowerCase() === "ancillary physics ii") formattedName = "Ancillary Physics-II";
  if (formattedName.toLowerCase() === "ancillary physics") formattedName = "Ancillary Physics";

  // Year formatting
  const year = yearPart;

  // 1. Legacy entry structure
  const legacyTitle = `${formattedName} (${code}) (${year})`;
  const fileUrl = `https://sajmognuphnrvivtmuux.supabase.co/storage/v1/object/public/pyq-pdfs/${file}`;
  
  legacyEntries.push({
    title: legacyTitle,
    fileName: file,
    url: fileUrl,
    semester: semester
  });

  // 2. EXAM_PYQS entry mapping
  let targetKeys = [];
  if (code.startsWith("BPT-101")) {
    targetKeys = ["phymj11", "phymn11"];
  } else if (code.startsWith("BPT-201")) {
    targetKeys = ["phymj21", "phymn21"];
  } else if (code.startsWith("BPT-301")) {
    targetKeys = ["phymj31"];
  } else if (code.startsWith("BPT-401") && nameWithoutExt.includes("Electromagnetic")) {
    targetKeys = ["phymj41", "phymn41"];
  } else if (code.startsWith("BPT-401") && nameWithoutExt.includes("Electronics")) {
    targetKeys = ["phymj61"];
  } else if (code.startsWith("BPT-501")) {
    targetKeys = ["phymj42"];
  } else if (code.startsWith("BPT-502")) {
    targetKeys = ["phymj52"];
  } else if (code.startsWith("BPT-503")) {
    targetKeys = ["phymj51"];
  } else if (code.startsWith("BPT-504")) {
    targetKeys = ["phymj32"];
  } else if (code.startsWith("BPT-505")) {
    targetKeys = ["phymj41", "phymn41"];
  } else if (code.startsWith("BPT-601")) {
    targetKeys = ["phymj53"];
  } else if (code.startsWith("BPT-602")) {
    targetKeys = ["phymj62"];
  } else if (code.startsWith("BPT-603")) {
    targetKeys = ["phymj64"];
  } else if (code.startsWith("BPT-604")) {
    targetKeys = ["phymj63"];
  } else if (code.startsWith("BPE-601")) {
    targetKeys = ["phymj63"];
  } else if (code.startsWith("BPE-602")) {
    targetKeys = ["phymj75"];
  } else if (code.startsWith("BSCU7A")) {
    targetKeys = ["phymn11"];
  } else if (code.startsWith("BP-Anc-I")) {
    targetKeys = ["phymn21"];
  } else if (code.startsWith("BSC-07A") || code === "PHYSICS") {
    targetKeys = ["phymn41"];
  }

  targetKeys.forEach(k => {
    if (!examPyqMapping[k]) examPyqMapping[k] = [];
    
    // Add title formatting for subjects.html
    const pyqTitle = `${formattedName} ${year} PDF`;
    const pyqDesc = `Official ${code} ${formattedName} ${year} paper`;
    examPyqMapping[k].push({
      title: pyqTitle,
      file: fileUrl,
      description: pyqDesc
    });
  });
});

// Sort legacy entries by semester then title/year
legacyEntries.sort((a, b) => {
  if (a.semester !== b.semester) return a.semester - b.semester;
  return a.title.localeCompare(b.title);
});

// Output results to a temporary JSON file for inspection
const output = {
  legacyEntries,
  examPyqMapping
};

fs.writeFileSync("scratch/generated_physics_data.json", JSON.stringify(output, null, 2));
console.log("Generated mapping file written to scratch/generated_physics_data.json");
console.log(`Legacy Entries count: ${legacyEntries.length}`);
console.log(`Mapped Subject Keys: ${Object.keys(examPyqMapping).length}`);
console.log(Object.keys(examPyqMapping).map(k => `${k}: ${examPyqMapping[k].length} papers`).join(", "));
