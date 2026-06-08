const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // Listen for console messages and errors
  page.on('console', msg => {
    console.log(`[BROWSER CONSOLE] ${msg.type().toUpperCase()}: ${msg.text()}`);
  });
  page.on('pageerror', err => {
    console.error('[BROWSER EXCEPTION]', err);
  });

  try {
    console.log('Navigating to http://localhost:8000/nep-science.html...');
    await page.goto('http://localhost:8000/nep-science.html');

    // Find the Mathematics card
    console.log('Finding Mathematics card...');
    const mathCard = page.locator('button:has-text("Mathematics")');
    await mathCard.click();
    console.log('Clicked Mathematics card.');

    // Wait for modal to be visible
    console.log('Waiting for modal to appear...');
    const modal = page.locator('#comingSoonModal');
    await modal.waitFor({ state: 'visible', timeout: 5000 });
    console.log('Modal is now visible.');

    // Find Acknowledge button
    console.log('Finding Acknowledge button...');
    const ackButton = modal.locator('button:has-text("Acknowledge")');
    
    // Click Acknowledge button
    console.log('Clicking Acknowledge button...');
    await ackButton.click();
    console.log('Clicked Acknowledge button.');

    // Wait for modal to be hidden
    console.log('Waiting for modal to be hidden...');
    await modal.waitFor({ state: 'hidden', timeout: 5000 });
    console.log('Success! Modal is now hidden.');

  } catch (err) {
    console.error('Error during test execution:', err);
  } finally {
    await browser.close();
  }
})();
