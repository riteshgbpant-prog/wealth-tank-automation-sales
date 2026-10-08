# Wealth Tank Brand Guide

Every social media creative (posts, carousels, reel covers, stories, thumbnails, flyers) uses this style. Do not use Canva, stock templates or any other design pattern.

Reference designs: `assets/example-cover.png`, `assets/example-content-slide.png`, `assets/example-cta.png`, `assets/example-reel-cover.png`. Full approved set: `content/2026-10-08-health-insurance-room-rent/`.

## Logo
- File: `assets/wealth-tank-badge.png` (gold tank in a hexagon shield, "WEALTH TANK" in navy). Rendered from `video-editing/masterclass/logo.py`.
- Header lockup on every design: badge (86 px) + "WEALTH TANK" (Montserrat 900, white, letter-spaced) + tagline "Insurance • Loans • Consulting" (Montserrat 700, light gold).
- Final / CTA slide: large badge (120 px) with "WEALTH TANK" and @wealthtank.in.
- Never redraw, recolour or replace the logo.

## Colours
| Role | Hex |
|---|---|
| Navy (brand) | `#061E62` |
| Navy deep (background base) | `#030E2C` |
| Navy light (gradient top) | `#0A2A7A` |
| Gold (brand) | `#F0BA28` |
| Gold light | `#FFD76E` |
| Gold dark (metallic shading) | `#C98E12` |
| Red (warnings, losses only) | `#FF4757` |
| Muted text | `#A9B6DA` |

Navy and gold only. Red is reserved for danger/loss words ("NAHI", a lost amount, a trap). No other accent colours.

## Fonts (in `fonts/`)
- Headlines and big numbers: **Bebas Neue**, uppercase.
- Labels, logo wordmark, buttons: **Montserrat 800/900**.
- Body text: **Montserrat 600**; bold words in light gold.

## Layout and effects
- Sizes: feed / carousel 1080×1350 (4:5), reel cover and story 1080×1920 (9:16).
- Background: navy gradient (light top-left to deep bottom-right), soft gold glow top-right, faint grid, light film grain.
- Gold gradient bars (10 px) across the very top and bottom.
- Headline keywords in metallic gold gradient with glow; one key phrase underlined with a gold highlighter stroke.
- Glass cards (frosted, rounded 32 px) for comparisons, tips and CTAs.
- Icon tile (rounded square, glass) with a gold line icon next to a giant Bebas number.
- Top-right pill shows slide number (`02 / 08`) or a tag ("Claim Alert", "Quick Poll").
- Footer: source line (left) and gold "SWIPE →" button (right) on carousel slides.
- Language: Hinglish, short punchy lines, one idea per slide.
- Compliance: cite the source (e.g. IRDAI circular), mark examples "Illustrative", add "Awareness only" on insurance content.

## How to build a new creative
1. Create `content/<YYYY-MM-DD>-<topic>/source/build.js` (copy the 2026-10-08 one as a starting point).
2. Import helpers: `const { base, logo, icon, ruleSlide, render } = require('../../../brand/template');`
3. Use `ruleSlide({...})` for standard content slides and `base(w, h, html)` for covers / CTAs.
4. Run: `NODE_PATH=$(npm root -g) node content/<folder>/source/build.js` (renders PNGs into the content folder).
5. Look at every PNG before sending; fix overlaps, orphan words and empty space.
