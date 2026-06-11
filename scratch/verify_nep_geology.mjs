import { chromium } from 'playwright';
import fs from 'fs';

async function run() {
  console.log("Checking database files manually first...");
  
  // 1. Check subjects.html
  const subjectsHtml = fs.readFileSync("subjects.html", "utf-8");
  if (!subjectsHtml.includes('"glbmj41"')) {
    throw new Error("Verification Failed: glbmj41 key not found in subjects.html EXAM_PYQS");
  }
  console.log("Database check: subjects.html contains glbmj41 PYQs mapping!");

  // 2. Check nep-data.js
  const nepData = fs.readFileSync("js/nep-data.js", "utf-8");
  if (!nepData.includes('"department": "Geology"')) {
    throw new Error("Verification Failed: Geology department entries not found in js/nep-data.js");
  }
  console.log("Database check: js/nep-data.js contains Geology paper records!");

  // 3. Playwright browser testing
  console.log("Launching headless browser...");
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

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

  console.log("Navigating to http://localhost:8000/nep-science.html...");
  await page.goto("http://localhost:8000/nep-science.html", { waitUntil: "networkidle" });

  // Verify the Geology button state
  console.log("Checking Geology card on nep-science.html...");
  const geoBtn = page.locator("button:has-text('Geology')");
  const btnText = await geoBtn.innerText();
  console.log("Geology Card Info:\n", btnText);

  if (btnText.includes("Coming Soon")) {
    throw new Error("Geology card is still showing 'Coming Soon' instead of being Active!");
  }

  // Click on Geology card
  console.log("Clicking Geology card...");
  await geoBtn.click();

  // Wait for navigation to nep-papers.html?dept=geology
  console.log("Waiting for nep-papers.html to load...");
  await page.waitForURL("**/nep-papers.html?dept=geology", { timeout: 5000 });
  console.log("Successfully navigated to nep-papers.html!");

  // Wait for the loader to disappear and semesters to render
  console.log("Waiting for semesters to render...");
  await page.waitForSelector("#semestersContainer h2", { timeout: 5000 });

  // Verify semesters are present
  const semHeaders = await page.locator("#semestersContainer h2").allTextContents();
  console.log("Found Semester Headers:", semHeaders);

  if (semHeaders.length === 0) {
    throw new Error("No semester folders were rendered on nep-papers.html!");
  }

  // Verify there are paper download/view buttons
  const viewPdfBtns = await page.locator("a:has-text('View Paper')").all();
  console.log(`Found ${viewPdfBtns.length} active paper view buttons.`);

  if (viewPdfBtns.length === 0) {
    throw new Error("No paper view buttons rendered for Geology papers!");
  }

  // Verify some specific paper details
  const firstPaperTitle = await page.locator("#semestersContainer h4").first().innerText();
  console.log(`First Mapped Paper Details: ${firstPaperTitle}`);

  await browser.close();
  console.log("Verification finished successfully!");
}

run().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
