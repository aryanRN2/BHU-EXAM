import fs from "fs";
import path from "path";

const correctedDir = "aaa/latest corrected maths pdf";
const files = fs.readdirSync(correctedDir).filter(f => f.endsWith(".pdf"));

const semRoman = {
  1: 'Semester I',
  2: 'Semester II',
  3: 'Semester III',
  4: 'Semester IV',
  5: 'Semester V',
  6: 'Semester VI'
};

function getSemester(fileName) {
  const fn = fileName.toUpperCase();
  if (fn.includes("SEMVI") || fn.includes("SEM-VI") || fn.includes("SEM VI")) return 6;
  if (fn.includes("SEMV") || fn.includes("SEM-V") || fn.includes("SEM V")) return 5;
  if (fn.includes("SEMIV") || fn.includes("SEM-IV") || fn.includes("SEM IV")) return 4;
  if (fn.includes("SEMIII") || fn.includes("SEM-III") || fn.includes("SEM III")) return 3;
  if (fn.includes("SEMII") || fn.includes("SEM-II") || fn.includes("SEM II")) return 2;
  if (fn.includes("SEMI") || fn.includes("SEM-I") || fn.includes("SEM I")) return 1;
  return 1;
}

function parseFilename(file) {
  const nameWithoutExt = file.replace(".pdf", "");
  const semNum = getSemester(file);
  const semLabel = semRoman[semNum];
  
  // 1. Extract course code (e.g. MTB-101, MTB-AM-203, MTB-203A)
  let code = "";
  const codeMatch = nameWithoutExt.match(/^(MTB-[A-Z0-9-]+|MTB-[0-9]+[A-Z]?)/i);
  if (codeMatch) {
    code = codeMatch[1];
  }
  
  // 2. Extract year (e.g. 2022-23, 2013-14)
  let year = "";
  const yearMatch = nameWithoutExt.match(/(\d{4}-\d{2}|\d{4}-\d{4})/);
  if (yearMatch) {
    year = yearMatch[1];
  } else {
    const singleYearMatch = nameWithoutExt.match(/(\d{4})/);
    if (singleYearMatch) {
      year = singleYearMatch[1];
    }
  }

  // 3. Extract degree (BA / BSc)
  let degree = "";
  if (nameWithoutExt.includes("_BA_") || nameWithoutExt.includes("_BA-") || nameWithoutExt.endsWith("_BA")) {
    degree = "BA";
  } else if (nameWithoutExt.includes("_BSc_") || nameWithoutExt.includes("_BSc-") || nameWithoutExt.endsWith("_BSc")) {
    degree = "BSc";
  }
  
  // 4. Extract subject name (by removing code, year, degree, semester markers, and cleaning separators)
  let cleanName = nameWithoutExt;
  if (code) cleanName = cleanName.replace(code, "");
  if (year) cleanName = cleanName.replace(year, "");
  
  // Remove semester markers
  cleanName = cleanName.replace(/_Sem-?[I|V]+/i, "").replace(/-Sem-?[I|V]+/i, "").replace(/_Sem\s?[I|V]+/i, "");
  // Remove degree markers
  cleanName = cleanName.replace(/_BA_/g, "").replace(/_BSc_/g, "").replace(/_BA/g, "").replace(/_BSc/g, "").replace(/BA-/g, "").replace(/BSc-/g, "");
  // Remove "Old" marker
  let isOld = false;
  if (cleanName.includes("Old")) {
    isOld = true;
    cleanName = cleanName.replace(/_Old/i, "").replace(/-Old/i, "").replace(/Old/i, "");
  }

  // Clean remaining underscores, double spaces, etc.
  cleanName = cleanName
    .replace(/_/g, " ")
    .replace(/-/g, " ")
    .trim();
  
  // Add spaces between camelCase if present
  cleanName = cleanName.replace(/([a-z])([A-Z])/g, '$1 $2');
  
  // Construct formatted title
  let formattedTitle = `${semLabel}: ${cleanName}`;
  if (code) {
    formattedTitle += ` (${code})`;
  }
  if (degree) {
    formattedTitle += ` - ${degree}`;
  }
  if (year) {
    formattedTitle += ` [${year}]`;
  }
  if (isOld) {
    formattedTitle += " (Old)";
  }
  
  return formattedTitle;
}

console.log("Testing Title Formatter on all files:");
files.forEach(file => {
  console.log(`${file} \n  => ${parseFilename(file)}`);
});
