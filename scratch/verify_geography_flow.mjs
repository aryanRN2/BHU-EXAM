import { chromium } from 'playwright';

async function run() {
  console.log("Launching headless browser...");
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Log console and error events
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.error(`[BROWSER ERROR] ${msg.text()}`);
    } else {
      console.log(`[BROWSER LOG] [${msg.type()}] ${msg.text()}`);
    }
  });

  page.on('pageerror', err => {
    console.error("[BROWSER EXCEPTION]", err);
  });

  console.log("Navigating to http://localhost:8000/subjects.html...");
  await page.goto("http://localhost:8000/subjects.html", { waitUntil: "networkidle" });

  // Wait for the exam list to render
  await page.waitForSelector(".glass-panel");

  // Verify that the key 'ggrmj11' exists and is interactive
  const cardLocator = page.locator("div[onclick*='ggrmj11']");
  const count = await cardLocator.count();
  if (count === 0) {
    throw new Error("Could not find interactive card for key ggrmj11");
  }
  console.log("Found interactive card for ggrmj11!");

  const cardText = await cardLocator.innerText();
  console.log("Card Info:\n", cardText);

  if (cardText.includes("Coming soon")) {
    throw new Error("Geography exam ggrmj11 is showing 'Coming soon' instead of being active!");
  }

  // Click on the card to open the modal
  console.log("Clicking on ggrmj11 card...");
  await cardLocator.click();

  // Wait for the proceed button and click it to go to the exam
  const proceedBtn = page.locator("button:has-text('Start Preparation Exam'), button[onclick*='proceedToExam']").first();
  await proceedBtn.waitFor({ state: 'visible', timeout: 3000 });
  console.log("Clicking proceed/start exam button...");
  await proceedBtn.click();

  // Wait for navigation or load of exam.html
  console.log("Waiting for exam.html to load...");
  try {
    await page.waitForURL("**/exam.html*", { timeout: 10000 });
    console.log("Successfully navigated to exam.html!");
  } catch (err) {
    console.log(`Failed to navigate. Current URL is: ${page.url()}`);
    throw err;
  }

  // Verify that the question text element is loaded
  await page.waitForSelector("#questionText", { timeout: 5000 });
  
  // Get details from exam page
  const examTitle = await page.locator("#examSubjectTitle").innerText().catch(() => "Unknown");
  console.log(`Exam Subject Title: ${examTitle}`);

  const questionText = await page.locator("#questionText").innerText().catch(() => "Unknown");
  console.log(`First Question Text:\n${questionText}`);

  // Mock an image upload to make the evaluate button visible
  console.log("Mocking answer image upload...");
  await page.evaluate(() => {
    // Access state manager and retrieve active exam
    const activeExam = localStorage.getItem('bhu_active_exam');
    if (!activeExam) throw new Error("No active exam found in localStorage");
    
    const examState = JSON.parse(activeExam);
    const questions = examState.selectedQuestions;
    const currentQ = questions[examState.currentQuestionIndex];
    
    // Inject mock base64 image into uploadedImages in memory
    window.uploadedImages = window.uploadedImages || {};
    window.uploadedImages[currentQ.id] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==";
    
    // Initialize answer metadata
    examState.answers[currentQ.id] = {
      evaluated: false,
      marks: 0,
      suggestions: '',
      hasImage: true,
      imageName: 'student_answer_sheet.png',
      tutorChat: []
    };
    
    localStorage.setItem('bhu_active_exam', JSON.stringify(examState));
    
    // Call global render function to update the DOM
    window.renderQuestion(examState.currentQuestionIndex, false);
  });

  // Verify the evaluate button is now visible
  const evalBtn = page.locator("#aiEvaluateBtn");
  await evalBtn.waitFor({ state: 'visible', timeout: 3000 });
  console.log("AI Evaluate button is now visible!");

  // Click the AI Evaluate button to start grading
  console.log("Clicking AI Evaluate button...");
  await evalBtn.click();

  // Wait for the mock grading process to finish (simulates for 2s)
  console.log("Waiting for AI Grading to complete...");
  await page.waitForSelector("#theoryGradingDisplay:not(.hidden)", { timeout: 10000 });
  console.log("AI Grading completed!");

  // Get explanation/reference solution details
  const scoreText = await page.locator("#theoryScoreVal").innerText().catch(() => "0/10");
  const suggestionsText = await page.locator("#theorySuggestionsVal").innerText().catch(() => "None");
  const refSolutionText = await page.locator("#theoryReferenceSolutionVal").innerText().catch(() => "None");

  console.log(`\n=== AI EVALUATION RESULTS ===`);
  console.log(`Score: ${scoreText}`);
  console.log(`AI Rationale / Suggestions:\n${suggestionsText}`);
  console.log(`\nOfficial Reference Solution & Rubric:\n${refSolutionText}`);
  console.log(`=============================\n`);

  await browser.close();
  console.log("Verification finished successfully!");
}

run().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
