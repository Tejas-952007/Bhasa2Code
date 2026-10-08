import puppeteer from 'puppeteer-core';

async function main() {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    headless: 'new',
    defaultViewport: {
      width: 1600,
      height: 1000,
      deviceScaleFactor: 1.1, // 110% zoom as user requested
    },
  });

  const page = await browser.newPage();
  await page.goto('http://localhost:5173/', { waitUntil: 'networkidle0' });

  // 1. Capture base workspace with 110% zoom
  await page.screenshot({
    path: '/home/tejas/.gemini/antigravity-ide/brain/25b3a121-79cb-4711-9b86-404f509b1cb4/workspace_110zoom_elevated.png',
  });
  console.log('Saved workspace_110zoom_elevated.png');

  // 2. Click Study Mode button in header
  const studyButton = await page.waitForSelector('button:has-text("Study")', { timeout: 3000 }).catch(() => null);
  if (studyButton) {
    await studyButton.click();
  } else {
    // Alternatively click the toggle or sidebar
    const buttons = await page.$$('button');
    for (const b of buttons) {
      const text = await page.evaluate(el => el.textContent, b);
      if (text.includes('Study')) {
        await b.click();
        break;
      }
    }
  }

  await new Promise(r => setTimeout(r, 600));

  // Scroll down to the flowchart
  await page.evaluate(() => {
    const headings = Array.from(document.querySelectorAll('h4'));
    const flowchartHeading = headings.find(h => h.textContent.includes('Flowchart'));
    if (flowchartHeading) {
      flowchartHeading.scrollIntoView({ behavior: 'instant', block: 'start' });
    }
  });

  await new Promise(r => setTimeout(r, 600));

  await page.screenshot({
    path: '/home/tejas/.gemini/antigravity-ide/brain/25b3a121-79cb-4711-9b86-404f509b1cb4/study_flowchart_visual_diagram.png',
  });
  console.log('Saved study_flowchart_visual_diagram.png');

  // 3. Open settings modal
  const settingsBtn = await page.$('button[aria-label="Open settings"], button[title="Settings"]');
  if (settingsBtn) {
    await settingsBtn.click();
    await new Promise(r => setTimeout(r, 500));
    await page.screenshot({
      path: '/home/tejas/.gemini/antigravity-ide/brain/25b3a121-79cb-4711-9b86-404f509b1cb4/simplified_settings_modal.png',
    });
    console.log('Saved simplified_settings_modal.png');
  }

  await browser.close();
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
