// 用无头 Chromium 把 SVG 栅格化为 PNG。用法: node svg2png.mjs a.svg [b.svg ...]
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
const { chromium } = createRequire(execSync('npm root -g').toString().trim() + '/')('playwright');
import { readFileSync } from 'node:fs';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1672, height: 941 } });
for (const f of process.argv.slice(2)) {
  await page.setContent(`<html><body style="margin:0">${readFileSync(f, 'utf8')}</body></html>`);
  await page.screenshot({ path: f.replace(/\.svg$/, '.png'), clip: { x: 0, y: 0, width: 1672, height: 941 } });
  console.log(f.replace(/\.svg$/, '.png'));
}
await browser.close();
