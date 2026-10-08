// Wealth Tank brand design system. Every social creative must be built with these helpers.
// See brand/BRAND_GUIDE.md. Run scripts with: NODE_PATH=$(npm root -g) node <script>.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DIR = __dirname;                                   // brand/
const F = (fam, w, file) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(file://${path.join(DIR, 'fonts', file)})}`;
const fontCss = [600, 700, 800, 900].map(w => F('Montserrat', w, `Montserrat-${w}.ttf`)).join('') + F('Montserrat', 500, 'Montserrat-600.ttf') + F('Bebas', 400, 'BebasNeue.ttf');
const LOGO = 'file://' + path.join(DIR, 'assets', 'wealth-tank-badge.png');

// ---------- icons (stroke line icons) ----------
const I = {
  clock: `<circle cx="50" cy="54" r="34"/><path d="M50 34v21l14 9"/><path d="M40 12h20M50 12v8"/><path d="M80 24l6-6"/>`,
  door: `<rect x="22" y="16" width="44" height="70" rx="4"/><circle cx="56" cy="52" r="3"/><path d="M66 50h22M80 42l8 8-8 8"/>`,
  cal: `<rect x="14" y="20" width="72" height="64" rx="8"/><path d="M14 40h72M32 12v14M68 12v14"/><path d="M50 50v24M38 62h24"/>`,
  shield: `<path d="M50 10l34 12v26c0 22-15 36-34 44C31 84 16 70 16 48V22z"/><path d="M34 50l11 11 22-24"/>`,
  people: `<circle cx="34" cy="32" r="12"/><circle cx="68" cy="32" r="12"/><path d="M12 84c0-14 10-24 22-24s22 10 22 24"/><path d="M46 84c0-14 10-24 22-24s22 10 22 24"/>`,
  warn: `<path d="M50 12l40 72H10z"/><path d="M50 40v20M50 70v2"/>`,
  chat: `<path d="M14 20h72v46H44L26 82V66H14z"/><path d="M32 40h36M32 52h22"/>`,
  cross: `<rect x="14" y="14" width="72" height="72" rx="18"/><path d="M50 32v36M32 50h36"/>`,
};
const icon = (k, size = 120, color = 'var(--gold)') =>
  `<svg width="${size}" height="${size}" viewBox="0 0 100 100" fill="none" stroke="${color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">${I[k]}</svg>`;

const logo = (scale = 1) => `
<div class="logo" style="transform:scale(${scale});transform-origin:left center">
  <img src="${LOGO}" style="width:86px;height:86px;filter:drop-shadow(0 6px 18px rgba(0,0,0,.45))">
  <div><div class="lw">WEALTH TANK</div><div class="ls">Insurance • Loans • Consulting</div></div>
</div>`;

const base = (w, h, body, extraCss = '') => `<!doctype html><html><head><meta charset="utf-8"><style>
${fontCss}
:root{--navy:#030E2C;--navy2:#061E62;--gold:#F0BA28;--gold2:#FFD76E;--red:#FF4757;--mint:#FFD76E;--white:#FFFFFF;--muted:#A9B6DA}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${w}px;height:${h}px;overflow:hidden}
body{font-family:'Montserrat',sans-serif;color:var(--white);background:var(--navy);position:relative}
.bg{position:absolute;inset:0;background:
  radial-gradient(900px 700px at 88% -8%, rgba(240,186,40,.26), transparent 60%),
  radial-gradient(900px 900px at -15% 110%, rgba(14,48,130,.9), transparent 62%),
  linear-gradient(160deg,#0A2A7A 0%,#061E62 38%,#030E2C 100%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(ellipse at 50% 40%,#000 30%,transparent 80%)}
.noise{position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.wrap{position:absolute;inset:0;padding:70px 76px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center}
.logo{display:flex;align-items:center;gap:16px}
.lw{font-family:'Montserrat';font-weight:900;font-size:30px;letter-spacing:3px;color:var(--white)}
.ls{font-size:15px;font-weight:700;color:var(--gold2);letter-spacing:2px;margin-top:2px}
.pill{border:2px solid rgba(240,186,40,.5);color:var(--gold);font-weight:700;font-size:24px;padding:10px 22px;border-radius:999px;letter-spacing:2px;background:rgba(240,186,40,.08)}
.tag{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:24px;letter-spacing:3px;text-transform:uppercase;padding:12px 24px;border-radius:12px}
.anton{font-family:'Bebas',sans-serif;text-transform:uppercase;letter-spacing:1.5px;line-height:.92}
.gold{background:linear-gradient(180deg,#FFE7A3 0%,#F0BA28 55%,#C98E12 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 26px rgba(240,186,40,.4))}
.red{color:var(--red);text-shadow:0 0 40px rgba(255,59,78,.5)}
.mint{color:var(--gold2);text-shadow:0 0 40px rgba(255,215,110,.4)}
.body{font-size:38px;line-height:1.45;font-weight:600;color:#DDE4F8}
.body b{color:var(--gold2);font-weight:800}
.hl{background:linear-gradient(transparent 58%,rgba(240,186,40,.5) 58%);padding:0 4px;color:#fff;font-weight:800}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-size:20px;color:var(--muted)}
.swipe{display:flex;align-items:center;gap:12px;font-weight:700;color:var(--gold);font-size:24px;letter-spacing:3px}
.swipe span{display:inline-grid;place-items:center;width:56px;height:56px;border-radius:50%;background:var(--gold);color:var(--navy);font-size:30px}
.iconbox{width:190px;height:190px;border-radius:44px;display:grid;place-items:center;background:linear-gradient(145deg,rgba(255,255,255,.10),rgba(255,255,255,.02));border:1.5px solid rgba(255,255,255,.14);box-shadow:0 30px 80px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.2)}
.glass{background:linear-gradient(145deg,rgba(255,255,255,.09),rgba(255,255,255,.02));border:1.5px solid rgba(255,255,255,.13);border-radius:32px;box-shadow:0 30px 80px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.18)}
.big{font-family:'Bebas';line-height:.85;letter-spacing:-2px}
${extraCss}
</style></head><body><div class="bg"></div><div class="grid"></div><div class="noise"></div><div style="position:absolute;left:0;right:0;top:0;height:10px;background:linear-gradient(90deg,#C98E12,#FFD76E,#F0BA28,#C98E12)"></div><div style="position:absolute;left:0;right:0;bottom:0;height:10px;background:linear-gradient(90deg,#C98E12,#FFD76E,#F0BA28,#C98E12)"></div><div class="wrap">${body}</div></body></html>`;


// ---------- standard content slide: icon + big number + headline + body + pro tip ----------
function ruleSlide({ n, total = 8, ic, color = 'gold', bigNum, bigLabel, strike, title, titleHl, body, tip, source }) {
  const c = `var(--${color})`;
  return base(1080, 1350, `
  <div class="top">${logo()}<div class="pill">${String(n).padStart(2, '0')} / ${String(total).padStart(2, '0')}</div></div>
  <div style="margin-top:70px;display:flex;align-items:center;gap:44px">
    <div class="iconbox">${icon(ic, 120, c)}</div>
    <div>
      ${strike ? `<div class="anton" style="font-size:72px;color:#6E7798;position:relative;display:inline-block;margin-bottom:26px">${strike}<div style="position:absolute;left:-8px;right:-8px;top:48%;height:9px;background:var(--red);transform:rotate(-6deg);border-radius:6px;box-shadow:0 0 20px rgba(255,59,78,.7)"></div></div>` : ''}
      <div class="big ${color}" style="font-size:200px">${bigNum}</div>
      <div style="font-weight:700;letter-spacing:6px;font-size:26px;color:var(--muted);margin-top:14px">${bigLabel}</div>
    </div>
  </div>
  <div class="anton" style="font-size:96px;margin-top:70px">${title}<br><span class="${color}">${titleHl}</span></div>
  <div style="width:120px;height:8px;border-radius:8px;background:${c};margin:40px 0 34px;box-shadow:0 0 24px ${c}"></div>
  <div class="body" style="font-size:41px">${body}</div>
  ${tip ? `<div class="glass" style="margin-top:44px;padding:26px 32px;display:flex;gap:20px;align-items:center;border-left:6px solid ${c}"><div style="font-size:44px">💡</div><div><div style="font-size:20px;letter-spacing:3px;font-weight:700;color:${c}">PRO TIP</div><div style="font-size:30px;font-weight:600;margin-top:2px">${tip}</div></div></div>` : ''}
  <div class="foot"><div>${source ? 'Source: ' + source : ''}</div><div class="swipe">SWIPE <span>→</span></div></div>`);
}

// Renders [[name, width, height, html], ...] to <outDir>/<name>.png (and .html for tweaking).
async function render(designs, outDir) {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [name, w, h, html] of designs) {
    await page.setViewportSize({ width: w, height: h });
    const f = path.join(outDir, name + '.html');
    fs.writeFileSync(f, html);
    await page.goto('file://' + f);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(outDir, name + '.png') });
    console.log('rendered', name);
  }
  await browser.close();
}

module.exports = { base, logo, icon, ruleSlide, render, LOGO };
