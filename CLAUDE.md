# Wealth Tank: project rules

Wealth Tank sells insurance (life, health, general) and loans (home, vehicle, LAP), and consults for insurance companies. Content is in Hinglish for salaried and middle-class audiences, mainly in Lucknow / UP.

## Design: always use the Wealth Tank brand style
- Every social media design (post, carousel, reel cover, story, thumbnail, flyer, poster) must follow `brand/BRAND_GUIDE.md` and be built with `brand/template.js`.
- Use the official logo `brand/assets/wealth-tank-badge.png` on every design. Never draw a different logo.
- Navy + gold palette, Bebas Neue headlines, Montserrat text, as in the reference designs in `brand/assets/example-*.png`.
- Do NOT use Canva or any other template or design pattern unless the founder explicitly asks.
- Render with headless Chromium (Playwright): `NODE_PATH=$(npm root -g) node <script>.js`. Check every PNG visually before delivering.
- Save each campaign in `content/<YYYY-MM-DD>-<topic>/` (PNGs + `source/build.js`).

## Video
- Video editing scripts live in `video-editing/` and use the same navy/gold colours, Montserrat and Bebas Neue fonts and badge logo (`video-editing/masterclass/logo.py`).
