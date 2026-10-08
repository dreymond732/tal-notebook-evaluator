// Browser regression for the standalone semester slides. No notebook execution.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

(async () => {
  const root = path.resolve(__dirname, '..');
  const files = process.argv.slice(2);
  const targets = files.length ? files : ['S1', 'S2', 'S3'].map(s => `Notebooks TD/${s}/Organisation_progression_${s}.html`);
  const artifactDir = process.env.SLIDES_ARTIFACT_DIR;
  if (artifactDir) fs.mkdirSync(artifactDir, { recursive: true });
  const browser = await chromium.launch({ headless: true,
    ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {}),
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--no-zygote'] });
  try {
    for (const file of targets) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 930 } });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(pathToFileURL(path.resolve(root, file)).href);
      const slides = page.locator('main .slide');
      const count = await slides.count();
      assert(count > 0, `${file}: slides missing`);
      assert.equal(await page.locator('#jump option').count(), count);
      const links = await page.locator('a[href]').evaluateAll(nodes => nodes.map(a => a.getAttribute('href')));
      assert(links.every(url => url === 'https://drive.google.com/drive/folders/1mkc-LIA1ModDi0Hst0Se-cV8mMnmW_Te?usp=sharing'), `${file}: unexpected external link`);
      if (!file.includes('/S3/')) assert.equal(links.length, 0, `${file}: no S1/S2 folder supplied`);
      else assert(links.length > 0, `${file}: missing S3 Drive links`);
      assert.equal(await page.locator('script[src], link[rel=stylesheet], img[src], iframe[src]').count(), 0, `${file}: external resource`);
      const css = (await page.locator('style').allTextContents()).join('');
      const cssUrls = Array.from(css.matchAll(/url\s*\(\s*['"]?([^)'"]+)/gi), match => match[1].trim());
      assert(cssUrls.every(url => url.startsWith('#')), `${file}: external CSS resource`);
      const recapFits = () => [...document.querySelectorAll('main .slide.active .recap p')].every(p => {
        const label = p.querySelector('b');
        const text = [...p.childNodes].find(n => n.nodeType === Node.TEXT_NODE && n.textContent.trim());
        if (!label || !text) return true;
        const range = document.createRange();
        range.selectNodeContents(text);
        const rect = range.getClientRects()[0];
        return !rect || label.getBoundingClientRect().right < rect.left;
      });
      const fit = [];
      for (let i = 0; i < count; i++) {
        await page.selectOption('#jump', String(i));
        assert.equal(await page.locator('main .slide.active').getAttribute('id'), `diapo-${i + 1}`);
        const bounds = await page.locator('main .slide.active').evaluate(s => ({
          id: s.id, contentBottom: s.querySelector('.content').getBoundingClientRect().bottom,
          footerTop: s.querySelector('footer').getBoundingClientRect().top,
          horizontalOverflow: s.scrollWidth > s.clientWidth
        }));
        assert(!bounds.horizontalOverflow && bounds.contentBottom < bounds.footerTop, `${file}: content overlaps ${bounds.id}`);
        assert(await page.evaluate(recapFits), `${file}: recap label overlaps text in ${bounds.id}`);
        fit.push(bounds);
        if (artifactDir) await page.screenshot({ path: path.join(artifactDir, `${path.basename(file, '.html')}-${i + 1}.png`) });
      }
      await page.click('#all');
      assert(await page.locator('#overview').isVisible());
      assert.equal(await page.locator('main .slide:visible').count(), 0);
      assert.equal(await page.locator('.overview-item').count(), count);
      await page.locator('.overview-item').nth(Math.min(2, count - 1)).click();
      assert(!(await page.locator('#overview').isVisible()));
      assert.equal(await page.locator('main .slide.active').getAttribute('id'), `diapo-${Math.min(2, count - 1) + 1}`);
      await page.click('#all');
      await page.keyboard.press('Escape');
      assert(!(await page.locator('#overview').isVisible()));
      // Embedded previews may reject the History API. The UI must still work.
      await page.evaluate(() => { history.replaceState = () => { throw new DOMException('Restricted preview', 'SecurityError'); }; });
      await page.click('#all');
      await page.locator('.overview-item').first().click();
      await page.locator('body').click({ position: { x: 10, y: 10 } });
      await page.keyboard.press('ArrowRight');
      assert.equal(await page.locator('main .slide.active').getAttribute('id'), 'diapo-2');
      await page.click('#all');
      await page.setViewportSize({ width: 390, height: 844 });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await page.locator('.overview-item').last().click();
      assert.equal(await page.locator('main .slide.active').getAttribute('id'), `diapo-${count}`);
      await page.setViewportSize({ width: 1440, height: 930 });
      await page.click('#all');
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('main .slide:visible').count(), count);
      assert(!(await page.locator('#overview').isVisible()));
      const printFit = await slides.evaluateAll(nodes => nodes.map(s => ({ id: s.id, contentBottom: s.querySelector('.content').getBoundingClientRect().bottom, footerTop: s.querySelector('footer').getBoundingClientRect().top })));
      assert(printFit.every(s => s.contentBottom < s.footerTop), `${file}: printed content overlaps footer`);
      assert(await page.evaluate(recapFits), `${file}: printed recap label overlaps text`);
      if (artifactDir) await page.pdf({ path: path.join(artifactDir, `${path.basename(file, '.html')}.pdf`), preferCSSPageSize: true, printBackground: true });
      assert.deepEqual(errors, []);
      console.log(JSON.stringify({ file, slides: count, links: links.length, navigation: 'OK', restrictedHistory: 'OK', mobile: 'OK', print: 'OK', fit }));
      await page.close();
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
