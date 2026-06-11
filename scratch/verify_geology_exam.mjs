import { chromium } from 'playwright';

async function run() {
  console.log("Launching headless browser to test Geology exam integration...");
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Block external network requests except tailwind to prevent stalls
  await page.route('**/*', (route) => {
    const url = route.request().url();
    if (url.includes('localhost') || url.includes('127.0.0.1') || url.includes('tailwindcss.com')) {
      route.continue();
    } else {
      route.abort();
    }
  });

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

  console.log("Navigating to http://localhost:8000/subjects.html?type=endterm...");
  await page.goto("http://localhost:8000/subjects.html?type=endterm", { waitUntil: "load" });

  // 1. Check if Geology courses are visible and active (not comingSoon)
  console.log("Checking if Geology card is active on the subjects list...");
  const geoCard = page.locator(".glass-panel:has-text('Elementary Physical and Structural Geology')").first();
  await geoCard.waitFor({ state: "visible", timeout: 5000 });
  const cardText = await geoCard.innerText();
  console.log("Geology Card Inner Text:\n", cardText);

  if (cardText.includes("Coming Soon")) {
    throw new Error("Geology exam card is still showing 'Coming Soon'!");
  }

  // 2. Click the card to open the exam modal
  console.log("Clicking the Geology exam card...");
  await geoCard.click();

  // 3. Click the 'Start Exam' button in the modal
  console.log("Waiting for exam modal to display and clicking start button...");
  const startBtn = page.locator("button:has-text('Start Exam'), button:has-text('Start Test'), #startBtn, .btn-primary");
  // Let's find any button in the modal
  const modalStartBtn = page.locator("#modalMainView button").first();
  await modalStartBtn.waitFor({ state: "visible", timeout: 5000 });
  console.log("Clicking Start Exam in modal...");
  await modalStartBtn.click();

  // 4. Verify navigation to exam.html
  console.log("Waiting for navigation to exam.html...");
  await page.waitForURL("**/exam.html", { timeout: 5000 });
  console.log("Successfully navigated to exam.html!");

  // 5. Verify that questions are loaded
  console.log("Waiting for questions to render...");
  await page.waitForSelector("#questionText", { timeout: 10000 });
  const questionText = await page.locator("#questionText").innerText();
  console.log("Loaded Question 1 text:", questionText);

  if (questionText.trim().length === 0) {
    throw new Error("Exam page loaded, but question text is empty!");
  }

  await browser.close();
  console.log("Geology exam interactive mode verified successfully!");
}

run().catch(err => {
  console.error("Geology exam verification failed:", err);
  process.exit(1);
});
