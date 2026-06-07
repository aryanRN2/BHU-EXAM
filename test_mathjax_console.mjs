import { chromium } from "playwright";

async function run() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  page.on("console", msg => {
    console.log(`[BROWSER LOG] [${msg.type()}] ${msg.text()}`);
  });

  // Inject a hook to intercept Text.prototype.splitText before anything else loads
  await page.addInitScript(() => {
    localStorage.setItem("bhu_user", JSON.stringify({ name: "ARYAN", roll: "12345", profileImage: "images/profile.png" }));
    localStorage.setItem("bhu_active_exam", JSON.stringify({
      examId: "matmj11",
      timeRemaining: 2700,
      currentQuestionIndex: 3, // Q4
      answers: {},
      flagged: {},
      totalQuestions: 10,
      startedAt: Date.now(),
      type: "theory"
    }));

    // Override splitText
    const originalSplitText = Text.prototype.splitText;
    Text.prototype.splitText = function(offset) {
      console.log(`[splitText Hook] Node text: "${this.textContent}", length: ${this.length || this.textContent.length}, offset: ${offset}`);
      try {
        return originalSplitText.call(this, offset);
      } catch (err) {
        console.log(`[splitText ERROR] Failed on node: "${this.textContent}" (length: ${this.length}), offset: ${offset}, error: ${err.message}`);
        throw err;
      }
    };
  });

  console.log("Navigating to http://localhost:8000/exam.html...");
  await page.goto("http://localhost:8000/exam.html", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);

  await page.evaluate(async () => {
    console.log("Manually triggering typesetting of #questionText...");
    const el = document.getElementById('questionText');
    if (window.MathJax && typeof MathJax.typesetPromise === 'function') {
      try {
        await MathJax.typesetPromise([el]);
        console.log("Successfully typeset #questionText manually!");
      } catch (err) {
        console.log("Failed typeset:", err.message);
      }
    }
  });

  await browser.close();
}

run().catch(console.error);
