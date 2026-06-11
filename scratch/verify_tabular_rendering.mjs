import { chromium } from 'playwright';

async function run() {
  console.log("Launching headless browser to test tabular table rendering...");
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

  const testUrl = "http://localhost:8000/pyq-viewer.html?file=aaa/STATISTIC/tex_files/STA_STB-504_OperationsResearch_SemV_2016-17_BSc.tex&title=Operations%20Research%20(STA_STB-504)%202016-17";
  console.log(`Navigating to ${testUrl}...`);
  await page.goto(testUrl, { waitUntil: "networkidle" });

  // 1. Wait for native render area to display
  console.log("Waiting for native render area to display...");
  await page.waitForSelector("#nativeRenderArea:not(.hidden)", { timeout: 10000 });
  console.log("Native render area is visible!");

  // 2. Check if table elements exist inside renderedLatexContent
  const tableCount = await page.evaluate(() => {
    return document.querySelectorAll('#renderedLatexContent table').length;
  });
  console.log(`Found ${tableCount} tables rendered inside the document.`);

  if (tableCount === 0) {
    throw new Error("No HTML table elements were rendered for the tabular environment!");
  }

  // 3. Verify that the "Unknown environment 'tabular'" error text is NOT present
  const innerText = await page.innerText("#renderedLatexContent");
  if (innerText.includes("Unknown environment 'tabular'")) {
    throw new Error("Found 'Unknown environment tabular' error on the page!");
  }
  console.log("Confirmed: No 'Unknown environment tabular' error found!");

  await browser.close();
  console.log("Tabular environment table conversion test finished successfully!");
}

run().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
