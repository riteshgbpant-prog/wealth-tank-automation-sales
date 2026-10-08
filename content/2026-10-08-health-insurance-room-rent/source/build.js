// Health insurance "Room Rent Trap" creatives, 8 Oct 2026. Built on the brand template.
// Run: NODE_PATH=$(npm root -g) node content/2026-10-08-health-insurance-room-rent/source/build.js
const path = require('path');
const { base, logo, icon, ruleSlide, render, LOGO } = require('../../../brand/template');

const SRC = 'IRDAI Master Circular on Health Insurance, 2024';


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

designs.push(['carousel-02-cashless', 1080, 1350, ruleSlide({ source: SRC, n: 2, tip: 'TPA desk pe request ka time note karwao', ic: 'clock', bigNum: '1', bigLabel: 'GHANTA · MAX', title: 'Cashless approval', titleHl: 'sirf 1 ghante mein', body: 'Cashless request aane ke baad insurer ko <b>1 ghante ke andar</b> decision dena hota hai. <span class="hl">Ghanto intezaar nahi.</span>' })]);
designs.push(['carousel-03-discharge', 1080, 1350, ruleSlide({ source: SRC, n: 3, tip: 'Discharge wale din subah se file shuru karwao', ic: 'door', color: 'mint', bigNum: '3', bigLabel: 'GHANTE · DISCHARGE', title: 'Discharge approval', titleHl: '3 ghante mein', body: 'Final discharge approval <b>3 ghante</b> mein. Delay hua toh extra hospital charge <span class="hl">insurer bharega, aap nahi.</span>' })]);
designs.push(['carousel-04-waiting', 1080, 1350, ruleSlide({ source: SRC, n: 4, tip: 'Policy lete waqt har bimari sach-sach batao', ic: 'cal', strike: '4 saal', bigNum: '3', bigLabel: 'SAAL · MAX WAITING', title: 'Pehle se bimari?', titleHl: 'Max 3 saal wait', body: 'BP, sugar, thyroid jaisi pre-existing bimari ka waiting period ab <b>maximum 3 saal</b>. Pehle yeh 4 saal tak tha.' })]);
designs.push(['carousel-05-moratorium', 1080, 1350, ruleSlide({ source: SRC, n: 5, tip: 'Policy port karo — purane saal jud jaate hain', ic: 'shield', color: 'mint', bigNum: '5', bigLabel: 'SAAL · MORATORIUM', title: '5 saal ke baad', titleHl: 'claim almost pakka', body: '5 saal lagatar premium ke baad, non-disclosure ke naam pe <span class="hl">claim reject nahi ho sakta</span> (fraud ke case ke alawa).' })]);
designs.push(['carousel-06-age', 1080, 1350, ruleSlide({ source: SRC, n: 6, tip: 'Parents ke liye co-pay aur waiting period check karo', ic: 'people', bigNum: '65+', bigLabel: 'AGE · NO LIMIT', title: 'Parents 65+?', titleHl: 'Ab bhi policy milegi', body: 'Naya health insurance lene ki <b>age limit hata di gayi hai</b>. Mummy-papa ke liye bhi <span class="hl">option khula hai.</span>' })]);

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

render(designs, path.join(__dirname, '..'));
