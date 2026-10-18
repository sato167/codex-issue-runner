// 逐帧回放 player.html 并编码为无声 MP4。
// 用法: node render.mjs <scenes.json> <timeline.json> <场景序号> <输出.mp4> <字体css路径> [fps]
//       node render.mjs <scenes.json> <timeline.json> stills <输出目录> <字体css路径>
import { createRequire } from 'node:module';
import { execSync, spawn } from 'node:child_process';
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const { chromium } = createRequire(execSync('npm root -g').toString().trim() + '/')('playwright');
const [scenesPath, tlPath, idxStr, outPath, fontCss, fpsStr] = process.argv.slice(2);
const fps = Number(fpsStr || 30);
const here = dirname(fileURLToPath(import.meta.url));

const html = readFileSync(join(here, 'player.html'), 'utf8').replace('FONT_CSS', pathToFileURL(resolve(fontCss)).href);
const tmp = join(mkdtempSync(join(tmpdir(), 'wb-')), 'player.html');
writeFileSync(tmp, html);

const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
await page.goto(pathToFileURL(tmp).href);
await page.evaluate(([d, t]) => init(d, t), [JSON.parse(readFileSync(scenesPath, 'utf8')), JSON.parse(readFileSync(tlPath, 'utf8'))]);
if (idxStr === 'stills') {           // 预览：每幕最后一帧（全部画完）
  const { mkdirSync } = await import('node:fs');
  mkdirSync(outPath, { recursive: true });
  const n = await page.evaluate(() => TL.scenes.length);
  for (let i = 0; i < n; i++) {
    const d = await page.evaluate(i => setup(i), i);
    await page.evaluate(t => frame(t), d);
    await page.screenshot({ path: join(outPath, `s${i + 1}.png`) });
  }
  await browser.close();
  process.exit(0);
}
const duration = await page.evaluate(i => setup(i), Number(idxStr));

const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(fps), outPath], { stdio: ['pipe', 'inherit', 'inherit'] });
const n = Math.ceil(duration * fps);
for (let f = 0; f < n; f++) {
  await page.evaluate(t => frame(t), f / fps);
  const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % (fps * 5) === 0) process.stderr.write(`  场景${Number(idxStr) + 1}: ${(f / fps).toFixed(0)}s / ${duration.toFixed(1)}s\n`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log(`OUTPUT=${outPath}`);
