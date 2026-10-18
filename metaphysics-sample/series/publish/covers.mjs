// 生成封面：合集 4:3，单集竖屏 3:4 + 横屏 4:3。
// 用法: node covers.mjs <输出目录> <字体css> [meta.json] [项目目录]
//   （需先跑过各集的 make.py --preview 生成 <项目>/build/epXX/scenes.json；默认本系列）
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const { chromium } = createRequire(execSync('npm root -g').toString().trim() + '/')('playwright');
const [outDir, fontCss, metaArg, rootArg] = process.argv.slice(2);
const here = dirname(fileURLToPath(import.meta.url));
const series = rootArg ? resolve(rootArg) : resolve(here, '..');
const meta = JSON.parse(readFileSync(metaArg ? resolve(metaArg) : join(here, 'meta.json'), 'utf8'));
const BRAND = meta.brand || '白话《形而上学》';
mkdirSync(outDir, { recursive: true });

const html = readFileSync(join(here, 'cover.html'), 'utf8').replace('FONT_CSS', pathToFileURL(resolve(fontCss)).href);
const tmp = join(mkdtempSync(join(tmpdir(), 'cover-')), 'cover.html');
writeFileSync(tmp, html);

const VOL = ['一 Α', '二 α', '三 Β', '四 Γ', '五 Δ', '六 Ε', '七 Ζ', '八 Η', '九 Θ', '十 Ι', '十一 Κ', '十二 Λ', '十三 Μ', '十四 Ν'];
const LAYOUT = {
  landscape: { w: 1440, h: 1080, brand: [72, 56], brandSize: 44, chip: [72, 140], chipSize: 34,
               title: [66, 226, 1300], titleSize: 128, hook: [76, 400, 1300], hookSize: 50,
               art: [60, 480, 1320, 560], corner: [1180, 60], cornerSize: 30 },
  portrait:  { w: 1080, h: 1440, brand: [64, 64], brandSize: 44, chip: [64, 150], chipSize: 34,
               title: [58, 240, 960], titleSize: 120, hook: [68, 0, 960], hookSize: 48,
               art: [40, 0, 1000, 0], corner: [840, 70], cornerSize: 30 },
};

function wrap(text, perLine) {
  if (text.length <= perLine) return text;
  const at = text.indexOf('不') > 0 ? text.indexOf('不') + 1 : Math.ceil(text.length / 2);  // “数不是｜万物的原因”
  return text.slice(0, at + 1) + '\n' + text.slice(at + 1);
}

const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
async function shoot(spec, file) {
  const page = await browser.newPage({ viewport: { width: spec.w, height: spec.h } });
  await page.goto(pathToFileURL(tmp).href);
  await page.evaluate(s => render(s), spec);
  await page.screenshot({ path: join(outDir, file) });
  await page.close();
  console.log(file);
}

const scenesOf = ep => JSON.parse(readFileSync(join(series, 'build', `ep${String(ep).padStart(2, '0')}`, 'scenes.json'), 'utf8')).elements;

for (const e of meta.episodes) {
  const elements = scenesOf(e.ep);
  const num = String(e.ep).padStart(2, '0');
  for (const kind of ['landscape', 'portrait']) {
    const L = structuredClone(LAYOUT[kind]);
    const title = kind === 'portrait' ? wrap(e.cover, 7) : e.cover;
    const lines = title.split('\n').length;
    if (kind === 'portrait') {
      L.hook[1] = L.title[1] + lines * L.titleSize * 1.12 + 30;
      L.art[1] = L.hook[1] + 110;
      L.art[3] = 1400 - L.art[1];
    }
    await shoot({ w: L.w, h: L.h, layout: L, brand: BRAND, chip: e.chip || `第${e.ep}集 · 卷${VOL[e.ep - 1]}`,
                  title, hook: e.hook, corner: '', elements, ids: e.ids },
                `第${num}集_${kind === 'portrait' ? '竖屏3比4' : '横屏4比3'}.png`);
  }
}

// 合集封面（4:3）
{
  const c = meta.collection;
  const L = structuredClone(LAYOUT.landscape);
  L.title = [66, 150, 1300];
  L.titleSize = 136;
  L.chip = [76, 340];
  L.hook = [80, 430, 1300];
  L.art = [0, 510, 1440, 570];
  L.artAlign = metaArg ? 'xMidYMid meet' : 'xMidYMid slice';
  await shoot({ w: L.w, h: L.h, layout: L, brand: '', chip: c.chip || '全 14 集 · 一卷一集', title: c.cover_title || '白话《形而上学》', hook: c.hook,
                corner: '', elements: scenesOf(c.elements.ep), ids: c.elements.ids, crop: 'crop' in c ? c.crop : (metaArg ? null : [0, 110, 1600, 640]) },
              '合集封面_横屏4比3.png');
}
await browser.close();
