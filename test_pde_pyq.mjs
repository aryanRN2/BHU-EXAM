import fs from "fs";

function verifyExams() {
  console.log("Reading and evaluating js/exams-data.js...");
  const content = fs.readFileSync("./js/exams-data.js", "utf-8");
  
  // Replace ES export with a global assignment so we can eval it in Node.js
  const codeToEval = content.replace("export const EXAMS =", "globalThis.EXAMS =");
  eval(codeToEval);
  
  const EXAMS = globalThis.EXAMS;
  if (!EXAMS) {
    throw new Error("Failed to load EXAMS object from js/exams-data.js");
  }

  const subjectsToCheck = ["matmj43", "matmn41"];

  subjectsToCheck.forEach(subjectId => {
    const exam = EXAMS[subjectId];
    if (!exam) {
      throw new Error(`Subject ${subjectId} not found in EXAMS!`);
    }

    console.log(`\nVerifying subject: ${subjectId} (${exam.title})`);
    console.log(`Total questions: ${exam.questions.length}`);

    if (exam.questions.length !== 46) {
      throw new Error(`Expected 46 questions for ${subjectId}, but got ${exam.questions.length}`);
    }

    // Verify properties of the newly added questions
    for (let id = 26; id <= 46; id++) {
      const q = exam.questions.find(item => item.id === id);
      if (!q) {
        throw new Error(`Question ID ${id} not found in ${subjectId}`);
      }

      if (!q.unit) {
        throw new Error(`Question ${id} in ${subjectId} is missing "unit" field`);
      }

      if (!q.question || typeof q.question !== "string" || q.question.trim() === "") {
        throw new Error(`Question ${id} in ${subjectId} has invalid "question" field`);
      }

      if (!q.answerKey || typeof q.answerKey !== "string" || q.answerKey.trim() === "") {
        throw new Error(`Question ${id} in ${subjectId} has invalid "answerKey" field`);
      }
    }

    console.log(`Successfully verified all questions from 1 to 46 for ${subjectId}`);
  });

  console.log("\nAll checks PASSED successfully!");
}

try {
  verifyExams();
} catch (error) {
  console.error("Verification FAILED:", error.message);
  process.exit(1);
}
