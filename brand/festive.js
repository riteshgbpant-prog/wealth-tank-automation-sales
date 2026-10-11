// Festive ornaments for Wealth Tank festival creatives: gold mandala, diya, marigold toran.
// Usage: const { mandala, diya, toran, festiveCss } = require('../../../brand/festive');
const MARIGOLD = '#F7931E';
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


// Shared CSS for festival designs. `.dot` colour is set inline per day (style="background:...").
const festiveCss = `
.deva{font-family:'Tiro',serif;color:var(--gold2)}
.chip{display:inline-flex;align-items:center;gap:12px;padding:12px 24px;border-radius:999px;border:1.5px solid rgba(240,186,40,.5);background:rgba(240,186,40,.1);font-weight:800;font-size:22px;letter-spacing:2px}
.dot{width:22px;height:22px;border-radius:50%;border:2px solid rgba(255,255,255,.6)}
`;

module.exports = { MARIGOLD, mandala, diya, toran, festiveCss };
