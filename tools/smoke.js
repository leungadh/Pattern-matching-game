/*
 * Browser smoke test for both editions.
 *
 * Needs Node and Playwright once:   npm install playwright && npx playwright install chromium
 * Run from the repo root:           node tools/smoke.js
 *
 * Checks, for classic/ and bible/: 36 tiles are dealt, 18 pairs are announced,
 * an answer image loads, clicking two tiles opens them, and nothing errors in
 * the console. Then checks both links on the landing page.
 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  let bad = 0;

  for (const ed of ['classic', 'bible']) {
    const page = await browser.newPage();
    const errs = [], failed = [];
    page.on('pageerror', e => errs.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('requestfailed', r => failed.push(r.url()));

    await page.goto('file://' + path.resolve(ed, 'index.html'));
    await page.waitForTimeout(1200);

    const tiles = await page.locator('#grid > *').count();
    const total = await page.locator('#totalPairs').innerText();
    const answerBg = await page.locator('#answerLayer')
      .evaluate(el => getComputedStyle(el).backgroundImage);

    await page.locator('#grid > *').nth(0).click();
    await page.locator('#grid > *').nth(1).click();
    await page.waitForTimeout(400);
    const opened = await page.locator('#grid .open, #grid .matched').count();

    const ok = tiles === 36 && total === '18' && answerBg.includes('answers/')
            && opened >= 1 && errs.length === 0 && failed.length === 0;
    if (!ok) bad++;
    console.log(`\n[${ed}] ${ok ? 'PASS' : 'FAIL'}  tiles=${tiles} pairs=${total} opened=${opened}`);
    if (errs.length)   console.log('  JS errors: ' + errs.slice(0, 3).join(' | '));
    if (failed.length) console.log('  failed requests: ' + failed.slice(0, 5).join(' | '));
    await page.close();
  }

  const page = await browser.newPage();
  await page.goto('file://' + path.resolve('index.html'));
  for (const name of ['Classic', 'Bible']) {
    await page.locator(`a.card:has-text("${name}")`).click();
    await page.waitForTimeout(800);
    const title = await page.title();
    console.log(`\n[landing -> ${name}] title="${title}"`);
    if (!title.includes('Pattern Match')) bad++;
    await page.goBack();
    await page.waitForTimeout(200);
  }

  await browser.close();
  console.log(bad === 0 ? '\n=== ALL CHECKS PASSED ===' : `\n=== ${bad} FAILURE(S) ===`);
  process.exit(bad === 0 ? 0 : 1);
})();
