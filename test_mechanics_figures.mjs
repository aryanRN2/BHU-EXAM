import { chromium } from "playwright";

async function runTest() {
  console.log("=== Launching verification test for MATMJ44 Mechanics figures ===");
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  page.on("console", msg => {
    if (msg.type() === "error") {
      console.log(`[BROWSER ERROR] ${msg.text()}`);
    }
  });

  page.on("pageerror", err => {
    console.error("[BROWSER EXCEPTION]", err);
  });

  // 1. Inject student session and pre-select the Mechanics exam
  await page.addInitScript(() => {
    localStorage.setItem("bhu_user", JSON.stringify({
      name: "Aryan Test",
      roll: "BHU-TEST-001",
      profileImage: "images/profile.png"
    }));
    localStorage.setItem("bhu_active_exam", JSON.stringify({
      examId: "matmj44",
      timeRemaining: 7200,
      currentQuestionIndex: 0,
      answers: {},
      flagged: {},
      totalQuestions: 50,
      startedAt: Date.now(),
      type: "theory"
    }));
  });

  // 2. Navigate to exam workstation
  console.log("Navigating to exam.html...");
  await page.goto("http://localhost:8000/exam.html", { waitUntil: "networkidle" });
  
  // 3. Verify Q1 Displays SVG figure
  const badgeText = await page.locator("#questionBadge").innerText();
  const questionText = await page.locator("#questionText").innerText();
  console.log(`Current position: ${badgeText}`);
  console.log(`Question 1 text: "${questionText.substring(0, 60)}..."`);
  
  const isFigureVisible = await page.locator("#questionFigureContainer").isVisible();
  console.log(`Question 1 Figure Container visible: ${isFigureVisible}`);
  
  const figureHTML = await page.locator("#questionFigureContainer").innerHTML();
  const hasSVG = figureHTML.includes("<svg") && figureHTML.includes("arrow-p");
  console.log(`Question 1 Figure has expected SVG content: ${hasSVG}`);

  if (!isFigureVisible || !hasSVG) {
    throw new Error("Verification failed: Q1 figure diagram was not rendered correctly.");
  }

  // 4. Navigate to Question 8 and verify
  console.log("Navigating to Question 8...");
  await page.evaluate(() => renderQuestion(7)); // 0-indexed, so 7 is Q8
  await page.waitForTimeout(200);

  const q8Text = await page.locator("#questionText").innerText();
  console.log(`Question 8 text: "${q8Text.substring(0, 60)}..."`);
  const isQ8FigureVisible = await page.locator("#questionFigureContainer").isVisible();
  const q8FigureHTML = await page.locator("#questionFigureContainer").innerHTML();
  const q8HasSVG = q8FigureHTML.includes("rect x=\"60\"") && q8FigureHTML.includes("4P");
  console.log(`Question 8 Figure visible: ${isQ8FigureVisible}, has expected SVG: ${q8HasSVG}`);

  if (!isQ8FigureVisible || !q8HasSVG) {
    throw new Error("Verification failed: Q8 figure diagram was not rendered correctly.");
  }

  // 5. Submit the exam
  console.log("Submitting the Mechanics exam...");
  await page.evaluate(() => submitExam());
  await page.waitForNavigation({ url: "**/results.html", waitUntil: "networkidle" });
  console.log("Successfully redirected to results.html");

  // 6. Verify figures in results audit log
  const auditContainerHTML = await page.locator("#incorrectAuditContainer").innerHTML();
  const auditHasQ1SVG = auditContainerHTML.includes("arrow-p");
  const auditHasQ8SVG = auditContainerHTML.includes("4P");
  console.log(`Audit log displays Q1 SVG diagram: ${auditHasQ1SVG}`);
  console.log(`Audit log displays Q8 SVG diagram: ${auditHasQ8SVG}`);

  if (!auditHasQ1SVG || !auditHasQ8SVG) {
    throw new Error("Verification failed: SVG diagrams were not persisted/displayed in results.html.");
  }

  console.log("=== All checks passed successfully! ===");
  await browser.close();
}

runTest().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
