# Diagrams

Rendered from source, not hand-drawn. Fix a diagram by editing `render_animations.py`
and re-running it, so a correction is a commit rather than an issue.

| File | Shows |
| --- | --- |
| `three-levels.mp4` / `.gif` | Dispatcher, owners, specialists; ownership outliving a session |
| `self-evolving-loop.mp4` / `.gif` | Collect, require evidence, propose, refute, promote, roll back |

All are 1080 × 1350, 24 fps, no audio. Captions are embedded.

## Re-rendering

```
pip install pillow
python3 render_animations.py
```

`render_animations.py` writes the MP4s and cover images into this directory. It
requires `ffmpeg` on `PATH` for encoding, and the Arial faces from macOS
`/System/Library/Fonts/Supplemental`. On other platforms, adjust the `FONT` and
`BOLD` constants at the top of the file.

The animations are schematic. They illustrate the roles and the loop sequence; they
do not encode measurements, and none of the numbers in the documents appear in them.

## A note on the storyboard

If you change the structure, update the caption arrays (`CAP1`, `CAP2`) together with
the layout functions in the same file. The captions and the node positions are
independent, so it is possible to change one and leave the other stale — which
produces a diagram that labels the wrong stage.
