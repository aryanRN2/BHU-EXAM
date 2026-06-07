import fs from "fs";

const content = fs.readFileSync("js/exams-data.js", "utf-8");
const jsonStart = content.indexOf("{");
const jsonEnd = content.lastIndexOf("}");
const EXAMS = Function("return " + content.substring(jsonStart, jsonEnd + 1))();

const keys = [
  "phymj11", "phymn11",
  "phymj21", "phymn21",
  "phymj31",
  "phymj32",
  "phymj41", "phymn41",
  "phymj42",
  "phymj51",
  "phymj52",
  "phymj53",
  "phymj61",
  "phymj62",
  "phymj63",
  "phymj64",
  "phymj75"
];

console.log("=== Active Physics Subjects Questions ===");
keys.forEach(k => {
  const exam = EXAMS[k];
  if (exam) {
    const qCount = exam.questions ? exam.questions.length : 0;
    console.log(`Key: "${k}", Title: "${exam.title}", comingSoon: ${exam.comingSoon}, Questions Count: ${qCount}`);
  } else {
    console.log(`Key: "${k}" NOT FOUND!`);
  }
});
