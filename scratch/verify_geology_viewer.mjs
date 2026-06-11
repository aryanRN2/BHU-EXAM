import { chromium } from 'playwright';

async function run() {
  console.log("Launching headless browser to test pyq-viewer.html with a Geology .tex file...");
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

  const testUrl = "http://localhost:8000/pyq-viewer.html?file=aaa/geology/GLB-101_ElementaryPhysicalStructuralGeology_SemI_2023-24_BSc.tex&title=Elementary%20Physical%20%26%20Structural%20Geology%20(GLB-101)%202023-24";
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

  // 5. Check if the text matches some geology term from that file
  const pageText = await page.innerText("#renderedLatexContent");
  console.log("Excerpt of rendered text:\n", pageText.slice(0, 300));
  if (!pageText.toUpperCase().includes("GEOLOGY") && !pageText.toUpperCase().includes("EARTH") && !pageText.toUpperCase().includes("PHYSICAL")) {
    throw new Error("Rendered text does not seem to contain expected geology content!");
  }

  await browser.close();
  console.log("Geology viewer rendering test finished successfully!");
}

run().catch(err => {
  console.error("Geology viewer rendering test failed:", err);
  process.exit(1);
});
