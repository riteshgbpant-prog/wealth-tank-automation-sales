# Wealth Tank: LIC Development Officers Sales Masterclass highlight video

Outputs are in `../output/`:

| File | Use |
|---|---|
| `WealthTank_Sales_Masterclass_LIC_16x9.mp4` | YouTube, LinkedIn, Facebook (1080p) |
| `WealthTank_Sales_Masterclass_LIC_WhatsApp.mp4` | WhatsApp groups (720p, small) |
| `WealthTank_Sales_Masterclass_LIC_9x16_Reels.mp4` | Instagram Reels, YouTube Shorts, WhatsApp Status |
| `WealthTank_Masterclass_teaser.gif` | Logo-reveal teaser GIF |

Scripts:
- `logo.py`: vector redraw of the Wealth Tank badge logo
- `soundtrack.py`: 120 BPM music track and transition sound effects, synced to the cuts
- `edit.py`: timeline, transitions (flash, whip-pan, glitch, gold wipe, zoom), animated captions, number counters, logo intro and outro
- `vertical_overlay.py`: top and bottom branding for the 9:16 version

Inputs expected next to the scripts: `src1.mp4`, `src2.mp4`, `src3.mp4` (SDR-converted clips) and the photos in `../../images/`.
Caption text and timings are in the `s_*` segment functions in `edit.py`.
