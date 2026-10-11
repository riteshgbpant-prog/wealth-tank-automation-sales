// Week of 12-18 Oct 2026 (approved calendar): Navratri Day 2-8 Stories, "3 pillars" carousel (Wed),
// Room Rent Trap carousel slide 8 with a question CTA (Fri), and a LinkedIn PDF of the Room Rent carousel.
// Run: NODE_PATH=$(npm root -g) node content/2026-10-12-week-plan/source/build.js
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const { base, logo, icon, render, LOGO } = require('../../../brand/template');
const { mandala, diya, toran, festiveCss } = require('../../../brand/festive');

const OUT = path.join(__dirname, '..');
const handle = `<div style="font-weight:900;font-size:24px;letter-spacing:1px">@wealthtank.in</div>`;
const designs = [];

// ---------- Navratri Day 2-8 stories (9:16) ----------
const DAYS = [
  [2, 'Brahmacharini', 'ब्रह्मचारिण्यै', 'Tapasya · Sanyam · Dhairya', 'White', '#FFFFFF'],
  [3, 'Chandraghanta', 'चन्द्रघण्टायै', 'Saahas · Shaanti · Suraksha', 'Red', '#E53935'],
  [4, 'Kushmanda', 'कूष्माण्डायै', 'Urja · Ujala · Nayi Shuruaat', 'Royal Blue', '#2F5BEA'],
  [5, 'Skandamata', 'स्कन्दमातायै', 'Mamta · Suraksha · Aashirwad', 'Yellow', '#FFD21F'],
  [6, 'Katyayani', 'कात्यायन्यै', 'Shakti · Himmat · Vijay', 'Green', '#2EAD4B'],
  [7, 'Kalaratri', 'कालरात्र्यै', 'Bhay ka Naash · Saahas', 'Grey', '#9AA0A6'],
  [8, 'Mahagauri', 'महागौर्यै', 'Pavitrata · Shaanti · Sukh', 'Purple', '#8E44AD'],
];
for (const [n, name, deva, words, colour, hex] of DAYS) {
  designs.push([`story-day${n}-${name.toLowerCase()}`, 1080, 1920, base(1080, 1920, `
  ${toran(1080, 11)}
  <div class="top" style="margin-top:130px">${logo(1.1)}<div class="pill">DAY ${n}</div></div>
  <div style="text-align:center;margin-top:70px">
    <div style="display:inline-block">${mandala(680, diya)}</div>
    <div class="deva" style="font-size:120px;line-height:1.15;margin-top:10px;filter:drop-shadow(0 0 22px rgba(240,186,40,.35))">शुभ नवरात्रि</div>
    <div class="anton gold" style="font-size:${name.length > 11 ? 124 : 150}px;margin-top:10px;white-space:nowrap">Maa ${name}</div>
    <div style="font-size:30px;font-weight:700;color:#DDE4F8;margin-top:14px;letter-spacing:1px">${words}</div>
    <div class="deva" style="font-size:44px;line-height:1.6;margin-top:36px">ॐ देवी ${deva} नमः॥</div>
    <div style="margin-top:50px"><span class="chip" style="font-size:26px"><span class="dot" style="background:${hex};box-shadow:0 0 14px ${hex}"></span>AAJ KA RANG: ${colour.toUpperCase()}</span></div>
  </div>
  <div style="margin-top:auto;text-align:center"><div style="font-size:26px;color:var(--muted);font-weight:700">Wealth Tank parivaar ki taraf se</div>${handle}</div>`, festiveCss + '.wrap{padding:0 76px 130px}')]);
}

// ---------- Wed: "Family suraksha ke 3 pillar" carousel (general Navratri theme) ----------
const css3 = festiveCss + `
.row{display:flex;gap:26px;align-items:center;padding:36px 32px}
.row .ib{width:96px;height:96px;flex:none;border-radius:24px;display:grid;place-items:center;background:rgba(240,186,40,.10);border:1.5px solid rgba(240,186,40,.35)}
.row .t{font-family:'Bebas';font-size:52px;letter-spacing:1px;line-height:1}
.row .d{font-size:26px;font-weight:600;color:#DDE4F8;line-height:1.45;margin-top:6px}`;

designs.push(['pillars-1', 1080, 1350, base(1080, 1350, `
  ${toran(1080)}
  <div class="top" style="margin-top:96px">${logo()}<div class="pill">01 / 03</div></div>
  <div style="display:flex;align-items:center;gap:20px;margin-top:40px">
    <div style="flex:1">
      <div style="font-weight:800;font-size:22px;letter-spacing:6px;color:var(--gold2)">NAVRATRI SPECIAL</div>
      <div class="anton" style="font-size:132px;margin-top:10px">Shakti aur<br><span class="gold">Sthirta</span></div>
    </div>
    <div style="flex:none;margin-right:-40px">${mandala(400, diya)}</div>
  </div>
  <div class="glass" style="margin-top:40px;padding:34px 38px">
    <div class="deva" style="font-size:34px;line-height:1.5">नौ दिन, नौ रूप — हर रूप में शक्ति और सुरक्षा</div>
    <div class="body" style="font-size:31px;margin-top:18px">Maa ki shakti ki tarah, aapke parivaar ki suraksha bhi ek <span class="hl">mazboot neev</span> pe khadi honi chahiye. Ye rahe uske <b>3 pillar</b>.</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px">
    ${[['plus','Health'],['shield','Term'],['cal','Emergency Fund']].map(([ic,t]) => `<div class="glass" style="padding:22px;text-align:center">${icon(ic, 54)}<div class="anton gold" style="font-size:40px;margin-top:8px;white-space:nowrap">${t}</div></div>`).join('')}
  </div>
  <div class="foot"><div style="font-size:20px;color:var(--muted);font-weight:700">Save karo · Family ko bhejo</div><div class="swipe">SWIPE <span>→</span></div></div>`, css3)]);

const rows = [
  ['plus', 'Health Insurance', 'Poori family ke liye floater cover, taaki hospital ka bill aapki savings na khaaye.'],
  ['shield', 'Term Insurance', 'Aap na rahein, tab bhi family ke sapne chalte rahein. Thumb rule: saalana income ka 10–15 guna cover.'],
  ['cal', 'Emergency Fund', 'Kam se kam 6 mahine ka ghar ka kharcha alag rakho, FD ya liquid fund mein.'],
];
designs.push(['pillars-2', 1080, 1350, base(1080, 1350, `
  <div class="top">${logo()}<div class="pill">02 / 03</div></div>
  <div style="margin-top:56px;font-weight:800;font-size:22px;letter-spacing:6px;color:var(--gold2)">PARVAT JAISI MAZBOOT NEEV</div>
  <div class="anton" style="font-size:112px;margin-top:10px">Family suraksha ke<br><span class="gold">3 pillar</span></div>
  <div style="display:flex;flex-direction:column;gap:26px;margin-top:50px">
    ${rows.map(([ic, t, d], i) => `<div class="glass row"><div class="ib">${icon(ic, 60)}</div><div><div class="t"><span class="gold">0${i + 1}</span> ${t}</div><div class="d">${d}</div></div></div>`).join('')}
  </div>
  <div class="foot"><div>Thumb rules for awareness. Actual need depends on your income, age and family.</div><div class="swipe">SWIPE <span>→</span></div></div>`, css3)]);

designs.push(['pillars-3', 1080, 1350, base(1080, 1350, `
  ${toran(1080)}
  <div class="top" style="margin-top:96px">${logo()}<div class="pill">03 / 03</div></div>
  <div style="text-align:center;margin-top:30px">
    <div style="display:inline-block">${mandala(300, diya)}</div>
    <div class="anton" style="font-size:116px;margin-top:4px">Aapke ghar mein<br><span class="gold">kitne pillar hain?</span></div>
  </div>
  <div class="glass" style="margin-top:40px;padding:32px 40px;display:flex;align-items:center;gap:30px;border-color:rgba(240,186,40,.5);box-shadow:0 0 0 6px rgba(240,186,40,.08),0 30px 80px rgba(0,0,0,.4)">
    ${icon('chat', 96)}
    <div><div style="font-size:30px;font-weight:800">Comment mein batao: <span class="gold">1, 2 ya 3?</span></div>
    <div style="font-size:24px;color:#DDE4F8;font-weight:600;margin-top:10px">Free family protection check:<br><b style="color:var(--gold2);font-size:28px">WhatsApp +91 93051 60843</b></div></div>
  </div>
  <div class="foot" style="flex-direction:column;align-items:flex-start;gap:12px"><div style="display:flex;align-items:center;gap:20px"><img src="${LOGO}" style="width:110px;height:110px"><div><div style="font-size:30px;font-weight:900;letter-spacing:2px">WEALTH TANK</div><div style="font-size:24px;font-weight:700;color:var(--gold2)">@wealthtank.in</div></div></div><div style="font-size:17px">For awareness only, not advice. Insurance is the subject matter of solicitation.</div></div>`, css3)]);

// ---------- Fri: Room Rent Trap carousel, slide 8 with a question CTA ----------
const SRC = 'IRDAI Master Circular on Health Insurance, 2024';
designs.push(['roomrent-08-cta', 1080, 1350, base(1080, 1350, `
  <div class="top">${logo()}<div class="pill">08 / 08</div></div>
  <div class="anton" style="font-size:128px;margin-top:90px">Aapki policy<br>mein kya<br><span class="gold">likha hai?</span></div>
  <div class="glass" style="margin-top:56px;padding:38px 40px;display:flex;align-items:center;gap:34px;border-color:rgba(240,186,40,.5);box-shadow:0 0 0 6px rgba(240,186,40,.08),0 30px 80px rgba(0,0,0,.4)">
    ${icon('chat', 104)}
    <div><div style="font-size:30px;color:var(--muted);font-weight:600">Room rent limit hai? Comment karo</div>
    <div class="anton gold" style="font-size:76px">Haan / Nahi / Pata nahi</div>
    <div style="font-size:26px;font-weight:700">Free policy check: WhatsApp +91 93051 60843</div></div>
  </div>
  <div class="body" style="margin-top:40px;font-size:34px">🔁 Us dost ko bhejo jiske <b>parents ki policy</b> hai</div>
  <div class="foot" style="flex-direction:column;align-items:flex-start;gap:14px"><div style="display:flex;align-items:center;gap:22px"><img src="${LOGO}" style="width:120px;height:120px"><div><div style="font-size:34px;font-weight:900;letter-spacing:2px">WEALTH TANK</div><div style="font-size:26px;font-weight:700;color:var(--gold2)">@wealthtank.in</div></div></div><div style="font-size:18px">Source: ${SRC}. For awareness only; terms vary by policy. Insurance is the subject matter of solicitation.</div></div>`)]);

(async () => {
  await render(designs, OUT);
  // Copy approved Room Rent slides 1-7 and build the LinkedIn PDF (8 pages, 1080x1350).
  const RR = path.join(__dirname, '../../2026-10-08-health-insurance-room-rent');
  const names = fs.readdirSync(RR).filter(f => /^carousel-0[1-7].*\.png$/.test(f)).sort();
  names.forEach((f, i) => fs.copyFileSync(path.join(RR, f), path.join(OUT, `roomrent-0${i + 1}.png`)));
  const pages = [...names.map((_, i) => `roomrent-0${i + 1}.png`), 'roomrent-08-cta.png'];
  const html = `<html><body style="margin:0">${pages.map(p => `<img src="file://${path.join(OUT, p)}" style="display:block;width:1080px;height:1350px;page-break-after:always">`).join('')}</body></html>`;
  const tmp = path.join(OUT, 'roomrent-pdf.html');
  fs.writeFileSync(tmp, html);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + tmp);
  await page.pdf({ path: path.join(OUT, 'Room-Rent-Trap-Wealth-Tank.pdf'), width: '1080px', height: '1350px', printBackground: true });
  await browser.close();
  fs.unlinkSync(tmp);
  fs.readdirSync(OUT).filter(f => f.endsWith('.html')).forEach(f => fs.unlinkSync(path.join(OUT, f)));
  console.log('pdf done');
})();
