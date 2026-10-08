// Ritesh Tripathi / Wealth Tank profile for vehicle-insurance clients (2-page A4 PDF + PNGs).
// Run: NODE_PATH=$(npm root -g) node content/2026-10-08-ritesh-tripathi-profile/source/build.js
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const { base, logo, icon, LOGO } = require('../../../brand/template');

const OUT = path.join(__dirname, '..');
const W = 1240, H = 1754;                                   // A4 @ 150 dpi
const img = f => 'file://' + path.join(__dirname, f);

// Contact and social links. Fill LINKEDIN_* with the full profile URLs.
const PHONE = '+91 93051 60843';
const LINKS = {
  instagram: ['@wealthtank.in', 'https://www.instagram.com/wealthtank.in/'],
  facebook: ['Wealth Tank', 'https://www.facebook.com/908565139013735'],
  linkedinMe: ['Ritesh Tripathi', ''],
  linkedinCo: ['Wealth Tank (Company)', ''],
  youtube: ['wealthtank.in (Ritesh Tripathi)', ''],
};

const css = `
.wrap{padding:66px 84px 60px}
.kicker{font-weight:800;font-size:22px;letter-spacing:6px;color:var(--gold2)}
.h2{font-family:'Bebas';font-size:58px;letter-spacing:2px;line-height:1;text-transform:uppercase}
.rule{width:90px;height:7px;border-radius:7px;background:var(--gold);box-shadow:0 0 18px var(--gold);margin:12px 0 22px}
.stat{flex:1;padding:22px 24px;text-align:left}
.stat .n{font-family:'Bebas';font-size:82px;line-height:.9}
.stat .l{font-size:21px;font-weight:700;color:#DDE4F8;margin-top:8px;line-height:1.3}
.svc{display:flex;gap:18px;align-items:center;padding:18px 20px}
.svc .ib{width:66px;height:66px;flex:none;border-radius:20px;display:grid;place-items:center;background:rgba(240,186,40,.10);border:1.5px solid rgba(240,186,40,.35)}
.svc .t{font-size:23px;font-weight:800}
.svc .d{font-size:17px;font-weight:600;color:var(--muted);margin-top:5px;line-height:1.4}
.why{display:flex;gap:16px;align-items:flex-start;font-size:20px;font-weight:600;line-height:1.4;color:#DDE4F8}
.why b{color:#fff;font-weight:800;display:block;font-size:23px}
.step{flex:1;text-align:center;position:relative}
.step .c{width:70px;height:70px;margin:0 auto;border-radius:50%;background:var(--gold);color:var(--navy);display:grid;place-items:center;font-family:'Bebas';font-size:44px;box-shadow:0 10px 30px rgba(240,186,40,.4)}
.step .t{font-size:21px;font-weight:800;margin-top:12px}
.step .d{font-size:17px;font-weight:600;color:var(--muted);margin-top:6px;line-height:1.35;padding:0 8px}
.person{display:flex;gap:18px;align-items:center;padding:16px 20px}
.av{width:76px;height:76px;flex:none;border-radius:50%;display:grid;place-items:center;font-family:'Bebas';font-size:38px;color:var(--navy);background:linear-gradient(145deg,#FFE7A3,#F0BA28 60%,#C98E12);box-shadow:0 0 0 5px rgba(240,186,40,.18)}
.person .t{font-size:23px;font-weight:800}
.person .r{font-size:16px;font-weight:700;color:var(--gold2);margin-top:4px;line-height:1.35}
.chip{display:inline-block;padding:9px 18px;border-radius:999px;border:1.5px solid rgba(240,186,40,.45);background:rgba(240,186,40,.08);font-weight:700;font-size:18px;margin:0 8px 10px 0}
.soc{display:flex;align-items:center;gap:14px;font-size:20px;font-weight:700;margin-bottom:12px}
.soc small{display:block;font-size:15px;color:var(--muted);font-weight:600;letter-spacing:1px}
.qr{background:#fff;padding:10px;border-radius:16px;width:170px;height:170px}
.qrl{font-size:17px;font-weight:800;letter-spacing:2px;color:var(--gold2);text-align:center;margin-top:10px}
`;

const pageFoot = n => `<div class="foot" style="font-size:18px"><div>Wealth Tank · Insurance • Loans • Consulting · Lucknow, Uttar Pradesh</div><div style="color:var(--gold);font-weight:800;letter-spacing:2px">${n} / 2</div></div>`;

// ---------- page 1: who we are + vehicle solutions ----------
const p1 = base(W, H, `
  <div class="top">${logo(1.15)}<div class="pill">FOUNDER PROFILE</div></div>

  <div style="display:flex;align-items:center;gap:50px;margin-top:44px">
    <div style="flex:1">
      <div class="kicker">FOUNDER, WEALTH TANK</div>
      <div class="anton" style="font-size:132px;margin-top:10px;line-height:.88">Ritesh<br><span class="gold">Tripathi</span></div>
      <div style="font-size:30px;font-weight:800;margin-top:26px">Master Facilitator &amp; Financial Planner</div>
      <div style="font-size:23px;font-weight:600;color:var(--muted);margin-top:10px">Insurance &amp; Loan Experts · Lucknow, Uttar Pradesh</div>
    </div>
    <div style="position:relative;width:290px;height:290px;flex:none">
      <div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 200deg,#C98E12,#FFE7A3,#F0BA28,#C98E12,#FFD76E,#C98E12);box-shadow:0 0 60px rgba(240,186,40,.35)"></div>
      <div style="position:absolute;inset:12px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#0E3082,#030E2C);display:grid;place-items:center">
        <img src="${LOGO}" style="width:190px;height:190px">
      </div>
    </div>
  </div>

  <div class="glass" style="margin-top:40px;padding:28px 34px;font-size:21px;line-height:1.6;font-weight:600;color:#DDE4F8">
    For more than <b style="color:var(--gold2)">12 years</b> I have helped families and business owners protect what they own. Today <b style="color:#fff">Wealth Tank</b> runs with a dedicated team for policy issuance, renewals and claim follow-up, plus a field advisor network across Uttar Pradesh. For vehicle owners we compare plans from multiple insurers, recommend the right cover and stay with you when you need to claim.
  </div>

  <div style="display:flex;gap:18px;margin-top:26px">
    <div class="glass stat"><div class="n gold">12+</div><div class="l">Years in the<br>insurance industry</div></div>
    <div class="glass stat"><div class="n gold">15+</div><div class="l">Team members &amp;<br>field advisors</div></div>
    <div class="glass stat"><div class="n gold">All</div><div class="l">Vehicle types:<br>2W, car, commercial</div></div>
    <div class="glass stat"><div class="n gold">1</div><div class="l">Point of contact<br>for your whole fleet</div></div>
  </div>

  <div style="margin-top:40px"><div class="h2">Vehicle Insurance <span class="gold">Solutions</span></div><div class="rule"></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
    <div class="glass svc"><div class="ib">${icon('car', 50)}</div><div><div class="t">Private Cars</div><div class="d">Comprehensive and own-damage cover</div></div></div>
    <div class="glass svc"><div class="ib">${icon('bike', 50)}</div><div><div class="t">Two-Wheelers</div><div class="d">Bikes and scooters, single or bulk</div></div></div>
    <div class="glass svc"><div class="ib">${icon('truck', 50)}</div><div><div class="t">Goods Carriers &amp; Trucks</div><div class="d">Commercial vehicles of all tonnages</div></div></div>
    <div class="glass svc"><div class="ib">${icon('bus', 50)}</div><div><div class="t">Passenger Vehicles</div><div class="d">Taxis, buses, school vans</div></div></div>
    <div class="glass svc"><div class="ib">${icon('fleet', 50)}</div><div><div class="t">Fleet Policies</div><div class="d">Multiple vehicles under one plan and one renewal calendar</div></div></div>
    <div class="glass svc"><div class="ib">${icon('plus', 50)}</div><div><div class="t">Add-on Covers</div><div class="d">Zero Dep, Engine Protect, RSA, Return to Invoice, NCB Protect</div></div></div>
  </div>
  ${pageFoot(1)}`, css);

// ---------- page 2: why us, process, team, contact ----------
const why = [
  ['Multiple insurers compared', 'Quotes side by side, so you pay the right premium for the right cover.'],
  ['Claim support', 'Help with intimation, surveyor visits, documents and cashless garages.'],
  ['No missed renewals', 'We track every expiry date and remind you well before it lapses.'],
  ['Fast policy issuance', 'Share your RC and previous policy; we handle the paperwork.'],
];
const soc = (ic, label, sub) => `<div class="soc">${icon(ic, 38)}<div>${label}<small>${sub}</small></div></div>`;
const p2 = base(W, H, `
  <div class="top">${logo(1.15)}<div class="pill">WHY WEALTH TANK</div></div>

  <div style="margin-top:40px"><div class="h2">Why vehicle owners <span class="gold">choose us</span></div><div class="rule"></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:22px 36px">
    ${why.map(([t, d]) => `<div class="why">${icon('check', 46)}<div><b>${t}</b>${d}</div></div>`).join('')}
  </div>

  <div style="margin-top:38px"><div class="h2">How we <span class="gold">work</span></div><div class="rule"></div></div>
  <div style="display:flex;position:relative">
    <div style="position:absolute;left:12%;right:12%;top:35px;height:3px;background:linear-gradient(90deg,rgba(240,186,40,.2),rgba(240,186,40,.7),rgba(240,186,40,.2))"></div>
    <div class="step"><div class="c">1</div><div class="t">Share details</div><div class="d">RC copy and current policy of each vehicle</div></div>
    <div class="step"><div class="c">2</div><div class="t">Compare quotes</div><div class="d">Plans from multiple insurers with add-ons</div></div>
    <div class="step"><div class="c">3</div><div class="t">Policy issued</div><div class="d">Quick issuance, documents on WhatsApp and email</div></div>
    <div class="step"><div class="c">4</div><div class="t">Year-round service</div><div class="d">Renewals, endorsements and claim support</div></div>
  </div>

  <div style="margin-top:38px"><div class="h2">Our <span class="gold">Team</span></div><div class="rule"></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div class="glass person"><div class="av">RT</div><div><div class="t">Ritesh Tripathi</div><div class="r">Founder · Master Facilitator &amp; Financial Planner</div></div></div>
    <div class="glass person"><div class="av">AK</div><div><div class="t">Anurag Kesarwani</div><div class="r">Co-Founder · Financial Consultant · MDRT Achiever</div></div></div>
    <div class="glass person"><div class="av" style="font-size:0">${icon('headset', 42, 'var(--navy)')}</div><div><div class="t">Service Desk</div><div class="r">Policy issuance, renewal tracking and claim follow-up</div></div></div>
    <div class="glass person"><div class="av" style="font-size:0">${icon('people', 42, 'var(--navy)')}</div><div><div class="t">Field Advisors</div><div class="r">On-ground support across Uttar Pradesh</div></div></div>
  </div>

  <div style="margin-top:28px">
    <div class="kicker" style="margin-bottom:12px">ALSO FROM WEALTH TANK</div>
    <span class="chip">Health Insurance</span><span class="chip">Life Insurance</span><span class="chip">General Insurance</span><span class="chip">Vehicle Loans</span><span class="chip">Home Loans</span><span class="chip">Loan Against Property</span>
  </div>

  <div class="glass" style="margin-top:18px;padding:26px 32px;display:flex;gap:30px;align-items:center;border-color:rgba(240,186,40,.5)">
    <div style="flex:1">
      <div class="kicker">LET'S CONNECT</div>
      <div style="display:flex;align-items:center;gap:14px;margin:10px 0 16px">${icon('phone', 46)}<div class="anton gold" style="font-size:64px">${PHONE}</div></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 24px">
        ${soc('insta', LINKS.instagram[0], 'INSTAGRAM')}
        ${soc('linkedin', LINKS.linkedinMe[0], 'LINKEDIN')}
        ${soc('fb', LINKS.facebook[0], 'FACEBOOK')}
        ${soc('linkedin', LINKS.linkedinCo[0], 'LINKEDIN')}
        ${soc('yt', 'wealthtank.in', 'YOUTUBE')}
      </div>
    </div>
    <div style="display:flex;gap:22px">
      <div><img class="qr" src="${img('qr-whatsapp.png')}"><div class="qrl">WHATSAPP</div></div>
      <div><img class="qr" src="${img('qr-instagram.png')}"><div class="qrl">INSTAGRAM</div></div>
    </div>
  </div>
  ${pageFoot(2)}`, css);

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const pdfs = [];
  for (const [name, html] of [['profile-page-1', p1], ['profile-page-2', p2]]) {
    const f = path.join(OUT, name + '.html');
    fs.writeFileSync(f, html);
    await page.goto('file://' + f);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    const sh = await page.evaluate(() => document.querySelector('.wrap').scrollHeight);
    if (sh > H) console.warn(`WARNING ${name} overflows: ${sh}px > ${H}px`);
    await page.screenshot({ path: path.join(OUT, name + '.png') });
    const pdf = path.join(OUT, name + '.pdf');
    await page.pdf({ path: pdf, width: `${W}px`, height: `${H}px`, printBackground: true, pageRanges: '1' });
    pdfs.push(pdf);
    fs.unlinkSync(f);
    console.log('rendered', name);
  }
  await browser.close();
  execFileSync('pdfunite', [...pdfs, path.join(OUT, 'Ritesh-Tripathi-Wealth-Tank-Profile.pdf')]);
  pdfs.forEach(p => fs.unlinkSync(p));
})();
