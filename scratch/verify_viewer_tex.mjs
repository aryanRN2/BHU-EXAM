import { chromium } from 'playwright';

async function run() {
  console.log("Launching headless browser to test pyq-viewer.html with a .tex file...");
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

  const testUrl = "http://localhost:8000/pyq-viewer.html?file=aaa/geography/GRA-101_PhysicalBasisOfGeography_SemI_2022-23_BA.tex&title=Physical%20Basis%20of%20Geography%20(GRA-101)%202022-23";
  console.log(`Navigating to ${testUrl}...`);
  await page.goto(testUrl, { waitUntil: "networkidle" });

  // 1. Wait for loader to disappear and native render area to be visible
  console.log("Waiting for native render area to display...");
  await page.waitForSelector("#nativeRenderArea:not(.hidden)", { timeout: 10000 });
  console.log("Native render area is visible!");

  // 2. Verify loader is hidden
  const loaderClassList = await page.evaluate(() => document.getElementById('viewerLoader').className);
  console.log("Loader classes:", loaderClassList);
  if (!loaderClassList.includes("hidden")) {
    throw new Error("Loader is still visible!");
  }

  // 3. Verify that the toggle view button does not exist in the DOM (since PDF view is removed)
  const toggleBtnExists = await page.evaluate(() => {
    return document.getElementById('toggleViewBtn') !== null;
  });
  console.log("Does toggle view button exist?", toggleBtnExists);
  if (toggleBtnExists) {
    throw new Error("Toggle View button should not exist in the DOM!");
  }

  // 4. Verify that the latex content has been rendered
  const renderedHtml = await page.innerHTML("#renderedLatexContent");
  console.log("Length of rendered HTML:", renderedHtml.length);
  if (renderedHtml.trim().length === 0) {
    throw new Error("Rendered LaTeX content is empty!");
  }

  // 5. Check if MathJax successfully processed equations
  const hasMathJaxElements = await page.evaluate(() => {
    return document.querySelectorAll('mjx-container').length > 0;
  });
  console.log("Has MathJax mjx-container elements?", hasMathJaxElements);

  await browser.close();
  console.log("Viewer native rendering test finished successfully!");
}

run().catch(err => {
  console.error("Viewer native rendering test failed:", err);
  process.exit(1);
});
