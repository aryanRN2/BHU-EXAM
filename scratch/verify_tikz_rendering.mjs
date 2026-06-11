import { chromium } from 'playwright';

async function run() {
  console.log("Launching headless browser to test TikZ diagram SVG rendering...");
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

  const testUrl = "http://localhost:8000/pyq-viewer.html?file=aaa/latest%20corrected%20maths%20pdf/final%20maths%20export%20latex/DiscreteMathematics_SemVI_2022-23.tex&title=Discrete%20Mathematics%20(DiscreteMathematics_SemVI)%202022-23";
  console.log(`Navigating to ${testUrl}...`);
  await page.goto(testUrl, { waitUntil: "load" });

  // 1. Wait for native render area to display
  console.log("Waiting for native render area to display...");
  await page.waitForSelector("#nativeRenderArea:not(.hidden)", { timeout: 10000 });
  console.log("Native render area is visible!");

  // 2. Wait for TikZJax to compile and insert SVG elements (it takes a moment)
  console.log("Waiting for TikZJax to compile TikZ code to SVG...");
  await page.waitForSelector("#renderedLatexContent svg", { timeout: 15000 });
  
  // 3. Count SVG elements inside renderedLatexContent
  const svgCount = await page.evaluate(() => {
    return document.querySelectorAll('#renderedLatexContent svg').length;
  });
  console.log(`Found ${svgCount} SVG diagram(s) compiled and rendered successfully!`);

  if (svgCount === 0) {
    throw new Error("No SVG elements were rendered for the TikZ picture diagrams!");
  }

  await browser.close();
  console.log("TikZ diagram WebAssembly compile-to-SVG test finished successfully!");
}

run().catch(err => {
  console.error("Test failed:", err);
  process.exit(1);
});
