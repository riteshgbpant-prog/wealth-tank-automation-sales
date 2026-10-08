// Renders Wealth Tank health-insurance creatives to PNG with headless Chromium.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const OUT = path.join(DIR, 'out');
fs.mkdirSync(OUT, { recursive: true });
const F = (fam, w, file) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(file://${path.join(DIR, 'fonts', file)})}`;
const fontCss = [600, 700, 800, 900].map(w => F('Montserrat', w, `Montserrat-${w}.ttf`)).join('') + F('Montserrat', 500, 'Montserrat-600.ttf') + F('Bebas', 400, 'BebasNeue.ttf');
const LOGO = 'file://' + path.join(DIR, 'logo.png');

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

const SRC = 'IRDAI Master Circular on Health Insurance, 2024';

// ---------- content slide template ----------
function ruleSlide({ n, ic, color = 'gold', bigNum, bigLabel, strike, title, titleHl, body, tip, source = SRC }) {
  const c = `var(--${color})`;
  return base(1080, 1350, `
  <div class="top">${logo()}<div class="pill">0${n} / 08</div></div>
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
  <div class="foot"><div>Source: ${source}</div><div class="swipe">SWIPE <span>→</span></div></div>`);
}

const designs = [];

// 01 cover
designs.push(['carousel-01-cover', 1080, 1350, base(1080, 1350, `
  <div class="top">${logo()}<div class="pill">01 / 08</div></div>
  <div style="margin-top:80px"><span class="tag" style="background:rgba(255,59,78,.14);color:var(--red);border:2px solid rgba(255,59,78,.45)">● Health Insurance Alert</span></div>
  <div class="anton" style="font-size:146px;margin-top:44px;line-height:.98">Hospital<br>aapko yeh<br><span class="gold">5 baatein</span></div>
  <div style="display:flex;align-items:center;gap:30px;margin-top:26px">
    <div class="anton" style="font-size:150px;color:#fff;background:var(--red);padding:6px 34px 0;border-radius:18px;transform:rotate(-4deg);box-shadow:0 20px 60px rgba(255,59,78,.55)">NAHI</div>
    <div class="anton" style="font-size:110px">batayega <span style="font-size:96px">🤫</span></div>
  </div>
  <div class="body" style="margin-top:64px;font-size:40px">IRDAI ke naye rules —<br><span class="hl">jo aapke lakhs bacha sakte hain 💰</span></div>
  <div class="foot"><div style="font-size:24px;font-weight:600;color:var(--gold)">🔖 SAVE karo · 🔁 Family ko bhejo</div><div class="swipe">SWIPE <span>→</span></div></div>`)]);

designs.push(['carousel-02-cashless', 1080, 1350, ruleSlide({ n: 2, tip: 'TPA desk pe request ka time note karwao', ic: 'clock', bigNum: '1', bigLabel: 'GHANTA · MAX', title: 'Cashless approval', titleHl: 'sirf 1 ghante mein', body: 'Cashless request aane ke baad insurer ko <b>1 ghante ke andar</b> decision dena hota hai. <span class="hl">Ghanto intezaar nahi.</span>' })]);
designs.push(['carousel-03-discharge', 1080, 1350, ruleSlide({ n: 3, tip: 'Discharge wale din subah se file shuru karwao', ic: 'door', color: 'mint', bigNum: '3', bigLabel: 'GHANTE · DISCHARGE', title: 'Discharge approval', titleHl: '3 ghante mein', body: 'Final discharge approval <b>3 ghante</b> mein. Delay hua toh extra hospital charge <span class="hl">insurer bharega, aap nahi.</span>' })]);
designs.push(['carousel-04-waiting', 1080, 1350, ruleSlide({ n: 4, tip: 'Policy lete waqt har bimari sach-sach batao', ic: 'cal', strike: '4 saal', bigNum: '3', bigLabel: 'SAAL · MAX WAITING', title: 'Pehle se bimari?', titleHl: 'Max 3 saal wait', body: 'BP, sugar, thyroid jaisi pre-existing bimari ka waiting period ab <b>maximum 3 saal</b>. Pehle yeh 4 saal tak tha.' })]);
designs.push(['carousel-05-moratorium', 1080, 1350, ruleSlide({ n: 5, tip: 'Policy port karo — purane saal jud jaate hain', ic: 'shield', color: 'mint', bigNum: '5', bigLabel: 'SAAL · MORATORIUM', title: '5 saal ke baad', titleHl: 'claim almost pakka', body: '5 saal lagatar premium ke baad, non-disclosure ke naam pe <span class="hl">claim reject nahi ho sakta</span> (fraud ke case ke alawa).' })]);
designs.push(['carousel-06-age', 1080, 1350, ruleSlide({ n: 6, tip: 'Parents ke liye co-pay aur waiting period check karo', ic: 'people', bigNum: '65+', bigLabel: 'AGE · NO LIMIT', title: 'Parents 65+?', titleHl: 'Ab bhi policy milegi', body: 'Naya health insurance lene ki <b>age limit hata di gayi hai</b>. Mummy-papa ke liye bhi <span class="hl">option khula hai.</span>' })]);

// 07 trap
designs.push(['carousel-07-room-rent-trap', 1080, 1350, base(1080, 1350, `
  <div class="top">${logo()}<div class="pill" style="color:var(--red);border-color:rgba(255,59,78,.6);background:rgba(255,59,78,.1)">07 / 08</div></div>
  <div style="margin-top:60px"><span class="tag" style="background:var(--red);color:#fff;box-shadow:0 10px 40px rgba(255,59,78,.5)">⚠ Bonus Trap</span></div>
  <div class="anton" style="font-size:140px;margin-top:30px">Room Rent<br><span class="red">Limit</span></div>
  <div class="glass" style="margin-top:44px;padding:36px 40px">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:26px">
      <div><div style="color:var(--muted);font-size:22px;letter-spacing:2px;font-weight:600">LIMIT (1% of ₹5L)</div><div class="anton mint" style="font-size:78px;margin-top:6px">₹5,000<span style="font-size:36px">/day</span></div></div>
      <div><div style="color:var(--muted);font-size:22px;letter-spacing:2px;font-weight:600">AAPNE LIYA</div><div class="anton red" style="font-size:78px;margin-top:6px">₹10,000<span style="font-size:36px">/day</span></div></div>
    </div>
    <div style="height:2px;background:rgba(255,255,255,.12);margin:28px 0"></div>
    <div class="body" style="font-size:33px">Ab katauti sirf kamre pe nahi — <b>doctor, nursing, OT</b> sab pe <span class="hl">proportionate deduction.</span></div>
  </div>
  <div class="foot"><div>Illustrative example. Terms vary by policy.</div><div class="swipe" style="color:var(--red)">SWIPE <span style="background:var(--red);color:#fff">→</span></div></div>`)]);

// 08 CTA
designs.push(['carousel-08-cta', 1080, 1350, base(1080, 1350, `
  <div class="top">${logo()}<div class="pill">08 / 08</div></div>
  <div class="anton" style="font-size:128px;margin-top:90px">Aapki policy<br>mein kya<br><span class="gold">likha hai?</span></div>
  <div class="glass" style="margin-top:60px;padding:40px;display:flex;align-items:center;gap:34px;border-color:rgba(240,186,40,.5);box-shadow:0 0 0 6px rgba(240,186,40,.08),0 30px 80px rgba(0,0,0,.4)">
    ${icon('chat', 110)}
    <div><div style="font-size:30px;color:var(--muted);font-weight:600">Comment karo</div>
    <div class="anton gold" style="font-size:84px">"PATA NAHI"</div>
    <div style="font-size:30px;font-weight:700">→ FREE policy check 🔍</div></div>
  </div>
  <div class="body" style="margin-top:44px;font-size:34px">🔁 Us dost ko bhejo jiske <b>parents ki policy</b> hai</div>
  <div class="foot" style="flex-direction:column;align-items:flex-start;gap:14px"><div style="display:flex;align-items:center;gap:22px"><img src="${LOGO}" style="width:120px;height:120px"><div><div style="font-size:34px;font-weight:900;letter-spacing:2px">WEALTH TANK</div><div style="font-size:26px;font-weight:700;color:var(--gold2)">@wealthtank.in</div></div></div><div style="font-size:18px">Source: ${SRC}. Awareness only; terms vary by policy. Not a solicitation.</div></div>`)]);

// Reel cover (4:5 feed & 9:16 cover)
const coverBody = (tall) => `
  <div class="top">${logo(tall ? 1.1 : 1)}<span class="tag" style="background:rgba(255,59,78,.14);color:var(--red);border:2px solid rgba(255,59,78,.5);font-size:22px">● Claim Alert</span></div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
  <div class="glass" style="padding:40px 44px;transform:rotate(-2deg);position:relative;margin-top:${tall ? 0 : 30}px">
    <div style="display:flex;justify-content:space-between;color:var(--muted);font-size:24px;font-weight:600;letter-spacing:2px"><span>🏥 HOSPITAL BILL</span><span>#IPD-2026</span></div>
    <div class="anton" style="font-size:${tall ? 250 : 215}px;margin-top:10px">₹4 Lakh</div>
    <div style="position:absolute;right:30px;bottom:-30px;transform:rotate(10deg);border:6px solid var(--red);color:var(--red);font-family:Bebas;font-size:44px;padding:4px 20px;border-radius:12px;background:rgba(7,13,36,.85)">PARTIALLY PAID</div>
  </div>
  <div style="font-size:90px;text-align:center;margin:${tall ? 50 : 26}px 0;color:var(--gold);line-height:1">↓</div>
  <div class="anton" style="font-size:${tall ? 132 : 125}px;text-align:center;white-space:nowrap">Claim mila sirf <span style="font-size:.9em">😱</span></div>
  <div class="anton red" style="font-size:${tall ? 262 : 255}px;text-align:center;margin-top:10px;white-space:nowrap">₹2.5 Lakh</div>
  <div style="text-align:center;margin-top:${tall ? 50 : 30}px"><span class="anton" style="font-size:${tall ? 92 : 76}px;background:var(--gold);color:var(--navy);padding:10px 30px 4px;border-radius:14px;display:inline-block;transform:rotate(-1.5deg);box-shadow:0 18px 50px rgba(240,186,40,.45)">Room Rent Trap</span></div>
  </div>
  <div class="foot"><div>Illustrative example. Awareness only.</div><div style="font-weight:800;color:#fff;font-size:26px">@wealthtank.in</div></div>`;
designs.push(['reel-cover-4x5', 1080, 1350, base(1080, 1350, coverBody(false))]);
designs.push(['reel-cover-9x16', 1080, 1920, base(1080, 1920, coverBody(true), '.wrap{padding:110px 76px 120px}')]);

// Story poll
designs.push(['story-poll', 1080, 1920, base(1080, 1920, `
  <div class="top">${logo(1.1)}<span class="tag" style="background:rgba(240,186,40,.12);color:var(--gold);border:2px solid rgba(240,186,40,.5);font-size:22px">Quick Poll</span></div>
  <div style="margin-top:140px;text-align:center">
    <div style="display:inline-block" class="iconbox">${icon('cross', 120, 'var(--red)')}</div>
    <div class="anton" style="font-size:118px;margin-top:60px">Aapki health<br>policy mein</div>
    <div class="anton" style="font-size:150px;margin-top:10px"><span style="background:var(--gold);color:var(--navy);padding:8px 26px 0;border-radius:16px;display:inline-block;transform:rotate(-2deg)">Room Rent</span></div>
    <div class="anton" style="font-size:118px;margin-top:20px">Limit <span class="gold">hai?</span></div>
  </div>
  <div style="margin:80px auto 0;width:760px;height:300px;border:4px dashed rgba(255,255,255,.18);border-radius:40px;display:grid;place-items:center;color:rgba(255,255,255,.25);font-size:26px;letter-spacing:3px;font-weight:600">POLL STICKER YAHAN</div>
  <div style="margin-top:auto;text-align:center">
    <div style="font-size:42px;font-weight:700">Jawab aaj <span class="gold">7:30 PM</span> reel mein 👀</div>
    <div style="font-size:26px;color:var(--muted);margin-top:16px">@wealthtank.in</div>
  </div>`, '.wrap{padding:120px 76px 140px}')]);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [name, w, h, html] of designs) {
    await page.setViewportSize({ width: w, height: h });
    const f = path.join(OUT, name + '.html');
    fs.writeFileSync(f, html);
    await page.goto('file://' + f);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(OUT, name + '.png') });
    console.log('rendered', name);
  }
  await browser.close();
})();
