# Wealth Tank: project rules

Wealth Tank sells insurance (life, health, general) and loans (home, vehicle, LAP), and consults for insurance companies. Content is in Hinglish for salaried and middle-class audiences, mainly in Lucknow / UP.

## Design: always use the Wealth Tank brand style
- Every social media design (post, carousel, reel cover, story, thumbnail, flyer, poster) must follow `brand/BRAND_GUIDE.md` and be built with `brand/template.js`.
- Use the official logo `brand/assets/wealth-tank-badge.png` on every design. Never draw a different logo.
- Navy + gold palette, Bebas Neue headlines, Montserrat text, as in the reference designs in `brand/assets/example-*.png`.
- Do NOT use Canva or any other template or design pattern unless the founder explicitly asks.
- Render with headless Chromium (Playwright): `NODE_PATH=$(npm root -g) node <script>.js`. Check every PNG visually before delivering.
- Save each campaign in `content/<YYYY-MM-DD>-<topic>/` (PNGs + `source/build.js`).

## Posting guardrails (check before every post or schedule, and warn the founder if any is broken)
Researched October 2026. Before creating or scheduling any post, list what is already published or scheduled for that day and week (AdaptlyPost `list_posts`) and check these limits. If a plan breaks one, say so plainly before posting, even if not asked.

| Platform | Max per day (per account) | Per week | Notes |
|---|---|---|---|
| Instagram feed (reel, carousel, image) | 1 | 3–5 | Stories don't count; 1–3 Stories a day is fine |
| Facebook page | 1 | 3–5 | Same content as Instagram is fine |
| LinkedIn (company page and Ritesh's profile, each) | 1 | 3–5 | Space posts on the same account 18–24 h apart |
| YouTube Shorts | 1 | 3–5 | AdaptlyPost's shared upload quota can fail; retry next day, never loop |
| Threads / X | 1–2 | — | Low reach; never post the same text twice |

Safety rules (to avoid action blocks, shadowbans or a spammy image):
- **Max 5 hashtags** on Instagram posts and Reels (Instagram's cap); 1 on Threads.
- Never publish identical captions twice on the same platform; never repeat the same topic more than 2 days in a row.
- No bulk comment replies, DMs or follows in bursts; reply to comments by hand, with varied text.
- Don't stack posts: keep at least 4 hours between any two feed posts on the same platform.
- Festival / religious days: one greeting post + Story only; no sales CTA on the same day.
- Insurance posts: include "For awareness only, not advice" and, when there is a sales CTA, "Insurance is the subject matter of solicitation." Mark proposals as proposals, examples as illustrative.
- Best windows (IST): weekdays 12:30–1:30 PM and 6:30–8:30 PM; check Instagram Insights monthly and adjust.
- Always show the final post (text, image, accounts, time) and get an explicit "post it" before publishing.

## Video
- Video editing scripts live in `video-editing/` and use the same navy/gold colours, Montserrat and Bebas Neue fonts and badge logo (`video-editing/masterclass/logo.py`).
