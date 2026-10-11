// Navratri Day 1 (11 Oct 2026, Maa Shailputri): greeting post, 3-slide carousel, story.
// Run: NODE_PATH=$(npm root -g) node content/2026-10-11-navratri-day1-shailputri/source/build.js
const path = require('path');
const { base, logo, icon, render, LOGO } = require('../../../brand/template');

const MANTRA = 'वन्दे वाञ्छितलाभाय चन्द्रार्धकृतशेखराम्।<br>वृषारूढां शूलधरां शैलपुत्रीं यशस्विनीम्॥';
const MARIGOLD = '#F7931E';                          // Day 1 colour (orange), used only in festive ornaments

// ---------- ornaments ----------
const mandala = (size, inner = '') => {
  const petals = n => Array.from({ length: n }, (_, i) => i * 360 / n);
  return `<svg width="${size}" height="${size}" viewBox="-300 -300 600 600" style="overflow:visible">
  <defs>
    <linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE7A3"/><stop offset=".55" stop-color="#F0BA28"/><stop offset="1" stop-color="#C98E12"/></linearGradient>
    <radialGradient id="halo"><stop offset="0" stop-color="rgba(247,147,30,.55)"/><stop offset=".45" stop-color="rgba(240,186,40,.18)"/><stop offset="1" stop-color="rgba(240,186,40,0)"/></radialGradient>
  </defs>
  <circle r="300" fill="url(#halo)"/>
  <g fill="none" stroke="url(#mg)" stroke-width="2.4">
    <circle r="270" opacity=".55"/><circle r="258" stroke-dasharray="2 9" stroke-width="4" stroke-linecap="round"/>
    ${petals(24).map(a => `<path transform="rotate(${a})" d="M0-252 C14-232 14-212 0-196 C-14-212 -14-232 0-252Z"/>`).join('')}
    <circle r="192"/>
    ${petals(16).map(a => `<path transform="rotate(${a})" d="M0-188 C40-160 40-118 0-96 C-40-118 -40-160 0-188Z" opacity=".9"/>`).join('')}
    ${petals(16).map(a => `<path transform="rotate(${a + 11.25})" d="M0-176 C22-156 22-132 0-118 C-22-132 -22-156 0-176Z" opacity=".55"/>`).join('')}
    <circle r="96" stroke-width="3"/><circle r="84" opacity=".5"/>
  </g>
  <g fill="url(#mg)">${petals(48).map(a => `<circle transform="rotate(${a})" cy="-282" r="3.2"/>`).join('')}</g>
  ${inner}
</svg>`;
};

// Diya with flame, drawn around (0,0) inside the mandala viewBox.
const diya = `
  <defs>
    <radialGradient id="fl" cx=".5" cy=".7" r=".6"><stop offset="0" stop-color="#FFF6D5"/><stop offset=".35" stop-color="#FFD76E"/><stop offset=".75" stop-color="${MARIGOLD}"/><stop offset="1" stop-color="rgba(247,147,30,0)"/></radialGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="rgba(255,215,110,.85)"/><stop offset="1" stop-color="rgba(255,215,110,0)"/></radialGradient>
    <linearGradient id="bowl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE7A3"/><stop offset=".5" stop-color="#F0BA28"/><stop offset="1" stop-color="#9C6A08"/></linearGradient>
  </defs>
  <circle cy="-26" r="70" fill="url(#glow)"/>
  <path d="M0-78 C18-52 22-30 0-8 C-22-30 -18-52 0-78Z" fill="url(#fl)"/>
  <path d="M0-50 C7-38 8-26 0-16 C-8-26 -7-38 0-50Z" fill="#FFFDF2"/>
  <path d="M-62 0 H62 C56 30 30 46 0 46 C-30 46 -56 30 -62 0Z" fill="url(#bowl)"/>
  <path d="M-62 0 H62" stroke="#FFF1C2" stroke-width="3"/>
  <path d="M-22 46 L-30 60 H30 L22 46" fill="#C98E12"/>`;

// Marigold toran hanging from the top edge.
const toran = (w, drops = 13) => {
  const gap = w / (drops - 1);
  let s = `<svg width="${w}" height="150" viewBox="0 0 ${w} 150" style="position:absolute;left:0;top:10px;z-index:2">`;
  s += `<path d="M0 14 ${Array.from({ length: drops - 1 }, (_, i) => `Q${gap * i + gap / 2} 44 ${gap * (i + 1)} 14`).join(' ')}" fill="none" stroke="#2E7D32" stroke-width="3"/>`;
  for (let i = 0; i < drops; i++) {
    const x = i * gap, len = i % 2 ? 3 : 4;
    for (let k = 0; k < len; k++) s += `<circle cx="${x}" cy="${26 + k * 22}" r="11" fill="${k % 2 ? '#FFC21A' : MARIGOLD}" stroke="#C25E00" stroke-width="1.5"/>`;
    s += `<path d="M${x} ${26 + len * 22} l-7 14 h14z" fill="#2E7D32"/>`;
  }
  return s + '</svg>';
};

const css = `
.deva{font-family:'Tiro',serif;color:var(--gold2)}
.chip{display:inline-flex;align-items:center;gap:12px;padding:12px 24px;border-radius:999px;border:1.5px solid rgba(240,186,40,.5);background:rgba(240,186,40,.1);font-weight:800;font-size:22px;letter-spacing:2px}
.dot{width:22px;height:22px;border-radius:50%;background:${MARIGOLD};box-shadow:0 0 14px ${MARIGOLD}}
.row{display:flex;gap:26px;align-items:center;padding:36px 32px}
.row .ib{width:96px;height:96px;flex:none;border-radius:24px;display:grid;place-items:center;background:rgba(240,186,40,.10);border:1.5px solid rgba(240,186,40,.35)}
.row .t{font-family:'Bebas';font-size:52px;letter-spacing:1px;line-height:1}
.row .d{font-size:26px;font-weight:600;color:#DDE4F8;line-height:1.45;margin-top:6px}
`;
const handle = `<div style="font-weight:900;font-size:24px;letter-spacing:1px">@wealthtank.in</div>`;
const designs = [];

// ---------- 1. greeting post (4:5) ----------
designs.push(['navratri-day1-greeting', 1080, 1350, base(1080, 1350, `
  ${toran(1080)}
  <div class="top" style="margin-top:96px">${logo()}<div class="pill">NAVRATRI · DAY 1</div></div>
  <div style="text-align:center;margin-top:6px">
    <div style="display:inline-block">${mandala(480, diya)}</div>
    <div class="deva" style="font-size:100px;line-height:1.15;margin-top:-6px;filter:drop-shadow(0 0 22px rgba(240,186,40,.35))">शुभ नवरात्रि</div>
    <div class="anton gold" style="font-size:118px;margin-top:6px">Maa Shailputri</div>
    <div style="font-size:26px;font-weight:700;color:#DDE4F8;margin-top:12px;letter-spacing:1px">Shakti · Sthirta · Nayi Shuruaat</div>
    <div class="deva" style="font-size:30px;line-height:1.55;margin-top:22px;opacity:.95">${MANTRA}</div>
  </div>
  <div class="foot"><span class="chip"><span class="dot"></span>AAJ KA RANG: ORANGE</span><div style="text-align:right"><div style="font-size:20px;color:var(--muted);font-weight:700">Wealth Tank parivaar ki taraf se</div>${handle}</div></div>`, css)]);

// ---------- 2. carousel (3 slides) ----------
designs.push(['navratri-day1-carousel-1', 1080, 1350, base(1080, 1350, `
  ${toran(1080)}
  <div class="top" style="margin-top:96px">${logo()}<div class="pill">01 / 03</div></div>
  <div style="display:flex;align-items:center;gap:20px;margin-top:40px">
    <div style="flex:1">
      <div style="font-weight:800;font-size:22px;letter-spacing:6px;color:var(--gold2)">NAVRATRI · DAY 1</div>
      <div class="anton" style="font-size:140px;margin-top:10px">Maa<br><span class="gold">Shailputri</span></div>
    </div>
    <div style="flex:none;margin-right:-40px">${mandala(400, diya)}</div>
  </div>
  <div class="glass" style="margin-top:40px;padding:34px 38px">
    <div class="deva" style="font-size:34px;line-height:1.5">पर्वतराज हिमालय की पुत्री — स्थिरता और शक्ति का रूप</div>
    <div class="body" style="font-size:31px;margin-top:18px">Navratri ka pehla din <b>neev</b> ka din hai. Is Navratri, apne parivaar ki <span class="hl">suraksha ki neev</span> bhi parvat jaisi mazboot karo.</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px">
    <div class="glass" style="padding:22px;text-align:center"><div style="font-size:18px;font-weight:800;letter-spacing:3px;color:var(--muted)">VAHAN</div><div class="anton gold" style="font-size:44px;margin-top:6px;white-space:nowrap">Nandi</div></div>
    <div class="glass" style="padding:22px;text-align:center"><div style="font-size:18px;font-weight:800;letter-spacing:3px;color:var(--muted)">HAATH MEIN</div><div class="anton gold" style="font-size:44px;margin-top:6px;white-space:nowrap">Trishul · Kamal</div></div>
    <div class="glass" style="padding:22px;text-align:center"><div style="font-size:18px;font-weight:800;letter-spacing:3px;color:var(--muted)">PRATEEK</div><div class="anton gold" style="font-size:44px;margin-top:6px;white-space:nowrap">Sthirta</div></div>
  </div>
  <div class="foot"><span class="chip"><span class="dot"></span>AAJ KA RANG: ORANGE</span><div class="swipe">SWIPE <span>→</span></div></div>`, css)]);

const rows = [
  ['plus', 'Health Insurance', 'Poori family ke liye floater cover, taaki hospital ka bill aapki savings na khaaye.'],
  ['shield', 'Term Insurance', 'Aap na rahein, tab bhi family ke sapne chalte rahein. Thumb rule: saalana income ka 10–15 guna cover.'],
  ['cal', 'Emergency Fund', 'Kam se kam 6 mahine ka ghar ka kharcha alag rakho, FD ya liquid fund mein.'],
];
designs.push(['navratri-day1-carousel-2', 1080, 1350, base(1080, 1350, `
  <div class="top">${logo()}<div class="pill">02 / 03</div></div>
  <div style="margin-top:56px;font-weight:800;font-size:22px;letter-spacing:6px;color:var(--gold2)">PARVAT JAISI MAZBOOT NEEV</div>
  <div class="anton" style="font-size:112px;margin-top:10px">Family suraksha ke<br><span class="gold">3 pillar</span></div>
  <div style="display:flex;flex-direction:column;gap:26px;margin-top:50px">
    ${rows.map(([ic, t, d], i) => `<div class="glass row"><div class="ib">${icon(ic, 60)}</div><div><div class="t"><span class="gold">0${i + 1}</span> ${t}</div><div class="d">${d}</div></div></div>`).join('')}
  </div>
  <div class="foot"><div>Thumb rules for awareness. Actual need depends on your income, age and family.</div><div class="swipe">SWIPE <span>→</span></div></div>`, css)]);

designs.push(['navratri-day1-carousel-3', 1080, 1350, base(1080, 1350, `
  ${toran(1080)}
  <div class="top" style="margin-top:96px">${logo()}<div class="pill">03 / 03</div></div>
  <div style="text-align:center;margin-top:30px">
    <div style="display:inline-block">${mandala(330, diya)}</div>
    <div class="anton" style="font-size:122px;margin-top:4px">Is Navratri,<br><span class="gold">suraksha ki shuruaat</span></div>
  </div>
  <div class="glass" style="margin-top:44px;padding:34px 40px;display:flex;align-items:center;gap:30px;border-color:rgba(240,186,40,.5);box-shadow:0 0 0 6px rgba(240,186,40,.08),0 30px 80px rgba(0,0,0,.4)">
    ${icon('chat', 100)}
    <div><div style="font-size:28px;color:var(--muted);font-weight:700">Comment karo</div>
    <div class="anton gold" style="font-size:84px">"NAVRATRI"</div>
    <div style="font-size:28px;font-weight:800">→ FREE family protection check 🔍</div></div>
  </div>
  <div class="foot"><div style="display:flex;align-items:center;gap:20px"><img src="${LOGO}" style="width:120px;height:120px"><div><div style="font-size:32px;font-weight:900;letter-spacing:2px">WEALTH TANK</div><div style="font-size:24px;font-weight:700;color:var(--gold2)">@wealthtank.in · +91 93051 60843</div></div></div></div>`, css)]);

// ---------- 3. story (9:16) ----------
designs.push(['navratri-day1-story', 1080, 1920, base(1080, 1920, `
  ${toran(1080, 11)}
  <div class="top" style="margin-top:130px">${logo(1.1)}<div class="pill">DAY 1</div></div>
  <div style="text-align:center;margin-top:70px">
    <div style="display:inline-block">${mandala(680, diya)}</div>
    <div class="deva" style="font-size:120px;line-height:1.15;margin-top:10px;filter:drop-shadow(0 0 22px rgba(240,186,40,.35))">शुभ नवरात्रि</div>
    <div class="anton gold" style="font-size:150px;margin-top:10px">Maa Shailputri</div>
    <div style="font-size:30px;font-weight:700;color:#DDE4F8;margin-top:14px;letter-spacing:1px">Shakti · Sthirta · Nayi Shuruaat</div>
    <div class="deva" style="font-size:36px;line-height:1.6;margin-top:36px">${MANTRA}</div>
    <div style="margin-top:50px"><span class="chip" style="font-size:26px"><span class="dot"></span>AAJ KA RANG: ORANGE</span></div>
  </div>
  <div style="margin-top:auto;text-align:center"><div style="font-size:26px;color:var(--muted);font-weight:700">Wealth Tank parivaar ki taraf se</div>${handle}</div>`, css + '.wrap{padding:0 76px 130px}')]);

render(designs, path.join(__dirname, '..'));
