/*
 * Browser smoke test for both editions.
 *
 * Needs Node and Playwright once:   npm install playwright && npx playwright install chromium
 * Run from the repo root:           node tools/smoke.js
 *
 * Checks, for each edition: the right number of tiles is dealt (scripture: 48 plus
 * an empty centre cell), the pair count is announced, an answer image loads,
 * clicking two tiles opens them, a real pair matches, and nothing errors in the
 * console. Then checks every link on the landing page.
 */
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  let bad = 0;

  const editions = [
    { ed: 'classic',   tiles: 36, pairs: '18', blanks: 0 },
    { ed: 'bible',     tiles: 36, pairs: '18', blanks: 0 },
    { ed: 'scripture', tiles: 48, pairs: '24', blanks: 1 },
  ];
  for (const { ed, tiles: wantTiles, pairs: wantPairs, blanks: wantBlanks } of editions) {
    const page = await browser.newPage();
    const errs = [], failed = [];
    page.on('pageerror', e => errs.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('requestfailed', r => failed.push(r.url()));

    await page.goto('file://' + path.resolve(ed, 'index.html'));
    await page.waitForTimeout(1200);

    const tiles = await page.locator('#grid > .tile').count();
    const blanks = await page.locator('#grid > .tile-blank').count();
    const total = await page.locator('#totalPairs').innerText();
    const answerBg = await page.locator('#answerLayer')
      .evaluate(el => getComputedStyle(el).backgroundImage);

    await page.locator('#grid > .tile').nth(0).click();
    await page.locator('#grid > .tile').nth(1).click();
    await page.waitForTimeout(400);
    const opened = await page.locator('#grid .open, #grid .matched').count();

    // find a real pair via the test hook and play it: pairs count must go up
    const matched = await page.evaluate(async () => {
      const g = window.__game;
      g.newGame(); await new Promise(r => setTimeout(r, 50));
      const ts = g.state.tiles, a = ts[0], b = ts.find(t => t !== a && t.key === a.key);
      g.flipByNumber(a.index + 1); g.flipByNumber(b.index + 1);
      return g.state.pairs === 1;
    });

    const ok = tiles === wantTiles && blanks === wantBlanks && total === wantPairs
            && answerBg.includes('answers/') && opened >= 1 && matched
            && errs.length === 0 && failed.length === 0;
    if (!ok) bad++;
    console.log(`\n[${ed}] ${ok ? 'PASS' : 'FAIL'}  tiles=${tiles} blank=${blanks} pairs=${total} opened=${opened} match=${matched}`);
    if (errs.length)   console.log('  JS errors: ' + errs.slice(0, 3).join(' | '));
    if (failed.length) console.log('  failed requests: ' + failed.slice(0, 5).join(' | '));
    await page.close();
  }

  const page = await browser.newPage();
  await page.goto('file://' + path.resolve('index.html'));
  for (const name of ['Classic', 'Bible Edition', 'Scripture']) {
    await page.locator(`a.card:has-text("${name}")`).click();
    await page.waitForTimeout(800);
    const title = await page.title();
    console.log(`\n[landing -> ${name}] title="${title}"`);
    if (!/Pattern Match|經文配對/.test(title)) bad++;
    await page.goBack();
    await page.waitForTimeout(200);
  }

  await browser.close();
  console.log(bad === 0 ? '\n=== ALL CHECKS PASSED ===' : `\n=== ${bad} FAILURE(S) ===`);
  process.exit(bad === 0 ? 0 : 1);
})();
