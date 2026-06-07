import fs from "fs";
import path from "path";

const examsContent = fs.readFileSync("js/exams-data.js", "utf-8");
const jsonStart = examsContent.indexOf("{");
const jsonEnd = examsContent.lastIndexOf("}");
const EXAMS = Function("return " + examsContent.substring(jsonStart, jsonEnd + 1))();

const filesDir = "aaa/physics final";
const files = fs.readdirSync(filesDir).filter(f => f.endsWith(".pdf"));

const keyToFiles = {};
const unmappedFiles = [];

files.forEach(file => {
  const nameWithoutExt = file.replace(".pdf", "");
  const firstPart = nameWithoutExt.split("_")[0];
  let targetKeys = [];
  
  if (firstPart.startsWith("BPT-101")) {
    targetKeys = ["phymj11", "phymn11"];
  } else if (firstPart.startsWith("BPT-201")) {
    targetKeys = ["phymj21", "phymn21"];
  } else if (firstPart.startsWith("BPT-301")) {
    targetKeys = ["phymj31"];
  } else if (firstPart.startsWith("BPT-401") && nameWithoutExt.includes("Electromagnetic")) {
    targetKeys = ["phymj41", "phymn41"];
  } else if (firstPart.startsWith("BPT-401") && nameWithoutExt.includes("Electronics")) {
    targetKeys = ["phymj61"]; // Or phymj32
  } else if (firstPart.startsWith("BPT-501")) {
    targetKeys = ["phymj42"];
  } else if (firstPart.startsWith("BPT-502")) {
    targetKeys = ["phymj52"];
  } else if (firstPart.startsWith("BPT-503")) {
    targetKeys = ["phymj51"];
  } else if (firstPart.startsWith("BPT-504")) {
    targetKeys = ["phymj32"];
  } else if (firstPart.startsWith("BPT-505")) {
    targetKeys = ["phymj41", "phymn41"];
  } else if (firstPart.startsWith("BPT-601")) {
    targetKeys = ["phymj53"];
  } else if (firstPart.startsWith("BPT-602")) {
    targetKeys = ["phymj62"];
  } else if (firstPart.startsWith("BPT-603")) {
    targetKeys = ["phymj64"];
  } else if (firstPart.startsWith("BPT-604")) {
    targetKeys = ["phymj63"];
  } else if (firstPart.startsWith("BPE-601")) {
    targetKeys = ["phymj63"]; // Or we can create another key if needed, but atomic/nuclear/laser fits
  } else if (firstPart.startsWith("BPE-602")) {
    targetKeys = ["phymj75"]; // Nano science
  } else if (firstPart.startsWith("BSCU7A")) {
    targetKeys = ["phymn11"];
  } else if (firstPart.startsWith("BP-Anc-I")) {
    targetKeys = ["phymn21"];
  } else if (firstPart.startsWith("BSC-07A") || firstPart === "PHYSICS") {
    targetKeys = ["phymn41"];
  }

  if (targetKeys.length === 0) {
    unmappedFiles.push(file);
  } else {
    targetKeys.forEach(k => {
      if (!keyToFiles[k]) keyToFiles[k] = [];
      keyToFiles[k].push(file);
    });
  }
});

console.log("=== SUMMARY ===");
console.log(`Total PDF files found in directory: ${files.length}`);
console.log(`Unmapped files: ${unmappedFiles.length}`);
if (unmappedFiles.length > 0) {
  console.log("Unmapped filenames:", unmappedFiles);
}

console.log("\nMapped Keys and their files:");
Object.keys(keyToFiles).sort().forEach(k => {
  console.log(`Key: "${k}" (${EXAMS[k] ? EXAMS[k].title : "MISSING!"})`);
  keyToFiles[k].forEach(f => {
    console.log(`  - ${f}`);
  });
});
