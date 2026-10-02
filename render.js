// Screenshots index.html at 800x480 for the e-ink display (used by the GitHub Action).
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 480 }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('page:', m.text()));
  await page.goto('http://localhost:8000/index.html', { waitUntil: 'networkidle' });
  await page.waitForSelector('body[data-ready]', { timeout: 30000 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'plan.png' });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
