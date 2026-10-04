# Wealth Tank video editing template

Adds Wealth Tank motion graphics, branded text, sound effects, background music and colour/audio clean-up to a talking-head video.

- `output/WealthTank_Edited_v1.mp4`: first edited test video
- `render.py`: colour grade, punch-in zooms and animated graphics (intro title, name bar, service chips, call-to-action, progress bar)
- `sfx.py`: generates the sound effects (`sfx.wav`) and a soft music bed (`music.wav`); no external audio files needed
- `fonts/`: Montserrat (SIL Open Font License)

## How to run (needs ffmpeg, Python 3, Pillow and numpy)

```bash
cd video-editing
python3 sfx.py 13.4                       # length of the video in seconds
python3 render.py input.mp4 video_only.mp4
ffmpeg -i input.mp4 -i music.wav -i sfx.wav -filter_complex "
[0:a]highpass=f=80,afftdn=nf=-25,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,asplit=2[v][vsc];
[1:a]volume=0.55[m];[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[mduck];
[2:a]volume=0.85[fx];
[v][mduck][fx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]" -map "[a]" mix.wav
ffmpeg -i video_only.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

Text, timings and colours are set at the top of each graphics function in `render.py`. The sound-effect timings are in the `EVENTS` list in `sfx.py`.
