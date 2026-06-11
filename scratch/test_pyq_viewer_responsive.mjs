import { chromium } from "playwright";

async function run() {
  console.log("Launching headless browser to debug pyq-viewer.html layout responsive widths...");
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 }
  });
  const page = await context.newPage();

  page.on('console', msg => {
    console.log(`[BROWSER LOG] [${msg.type()}] ${msg.text()}`);
  });

  page.on('pageerror', err => {
    console.error("[BROWSER EXCEPTION]", err);
  });

  const testUrl = "http://localhost:8000/pyq-viewer.html?file=aaa/STATISTIC/tex_files/BAS-101_AppliedStatistics_SemI_2022-23_BA.tex&title=Applied%20Statistics%20Sem";
  console.log(`Navigating to ${testUrl}...`);
  await page.goto(testUrl, { waitUntil: "domcontentloaded" });

  console.log("Waiting for native render area to display...");
  await page.waitForSelector("#nativeRenderArea:not(.hidden)", { timeout: 10000 });
  console.log("Native render area is visible! Waiting 1s for mathjax to finish formatting...");
  await page.waitForTimeout(1000);

  // Analyze DOM element dimensions and find any element causing horizontal overflow
  const report = await page.evaluate(() => {
    const windowWidth = window.innerWidth;
    const bodyWidth = document.body.offsetWidth;
    const bodyScrollWidth = document.body.scrollWidth;

    const mainEl = document.querySelector('main');
    const mainWidth = mainEl ? mainEl.offsetWidth : 0;
    const mainScrollWidth = mainEl ? mainEl.scrollWidth : 0;

    const panelEl = document.querySelector('.flex-grow.bg-white.rounded-2xl');
    const panelWidth = panelEl ? panelEl.offsetWidth : 0;
    const panelScrollWidth = panelEl ? panelEl.scrollWidth : 0;

    const renderAreaEl = document.getElementById('nativeRenderArea');
    const renderAreaWidth = renderAreaEl ? renderAreaEl.offsetWidth : 0;
    const renderAreaScrollWidth = renderAreaEl ? renderAreaEl.scrollWidth : 0;

    const latexEl = document.getElementById('renderedLatexContent');
    const latexWidth = latexEl ? latexEl.offsetWidth : 0;
    const latexScrollWidth = latexEl ? latexEl.scrollWidth : 0;

    // Find any element in the entire DOM that extends beyond the window inner width
    const overflowingElements = [];
    const allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.right > windowWidth + 1) {
        // Skip parent containers that naturally span or overflow because of their children
        // We only want leaf elements or elements that have custom style properties causing this
        overflowingElements.push({
          tagName: el.tagName,
          className: el.className,
          id: el.id,
          left: rect.left,
          right: rect.right,
          width: rect.width,
          outerHTML: el.outerHTML.substring(0, 150)
        });
      }
    });

    return {
      windowWidth,
      bodyWidth,
      bodyScrollWidth,
      mainWidth,
      mainScrollWidth,
      panelWidth,
      panelScrollWidth,
      renderAreaWidth,
      renderAreaScrollWidth,
      latexWidth,
      latexScrollWidth,
      overflowingElements
    };
  });

  console.log("\n=== DIMENSIONS REPORT ===");
  console.log(`Window Inner Width: ${report.windowWidth}px`);
  console.log(`Body Offset Width: ${report.bodyWidth}px, Scroll Width: ${report.bodyScrollWidth}px`);
  console.log(`Main Width: ${report.mainWidth}px, Scroll Width: ${report.mainScrollWidth}px`);
  console.log(`Panel Width: ${report.panelWidth}px, Scroll Width: ${report.panelScrollWidth}px`);
  console.log(`Render Area Width: ${report.renderAreaWidth}px, Scroll Width: ${report.renderAreaScrollWidth}px`);
  console.log(`LaTeX Sheet Width: ${report.latexWidth}px, Scroll Width: ${report.latexScrollWidth}px`);
  
  if (report.overflowingElements.length > 0) {
    console.log("\n=== ELEMENTS EXTENDING BEYOND VIEWPORT BOUNDS ===");
    report.overflowingElements.forEach((el, i) => {
      console.log(`${i+1}. <${el.tagName}> id="${el.id}" class="${el.className}"`);
      console.log(`   Left: ${el.left}px, Right: ${el.right}px, Width: ${el.width}px`);
      console.log(`   Snippet: ${el.outerHTML}`);
    });
  } else {
    console.log("\nNo elements extending beyond viewport bounds.");
  }

  await browser.close();
}

run().catch(err => {
  console.error("Debug script failed:", err);
});
