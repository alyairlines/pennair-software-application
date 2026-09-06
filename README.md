# PennAiR Software Challenge — Shape Detection

Detecting solid shapes on a background, tracing their outlines, marking their centres, and estimating the circle's 3D position. Initially across a static image, then two videos, including a harder background-agnostic case.

## The approach

Detection is based on texture, not colour. The shapes are smooth and the background is busy, so measuring how much pixels vary in a small neighbourhood separates them. And because it never looks at colour, it works no matter what colour the shapes or background are. The core detector is written once and reused across all four parts. Full reasoning is in [DESIGN_NOTES.md](DESIGN_NOTES.md).

## What's in the repo

| File | What it does |
|------|--------------|
| `part1.py` | The core detector. Finds shapes in the static image, outlines them, marks centres. |
| `part2.py` | Runs the detector frame-by-frame on the standard video. |
| `part3.py` | Runs it on the harder, different-background video. |
| `part4.py` | Estimates the circle's real-world position (x, y, depth). |
| `DESIGN_NOTES.md` | My decisions and tradeoffs for each part. |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate 
pip install opencv-python numpy
```

Then put the challenge files in this folder, renamed to `static.png`, `dynamic.mp4`, and `hard.mp4`.

## Running it

```bash
python part1.py     # -> part1_output.png, mask.png
python part2.py     # -> part2_output.mp4
python part3.py     # -> part3_output.mp4
python part4.py     # -> part4_output.png (circle labelled with its depth)
```

## Results

### Part 1 — Static image
All five shapes detected, outlined, and centre-marked.

![Part 1 output](part1_output.png)

### Part 2 — Video
[![Part 2 demo](part1_output.png)](PASTE_YOUR_YOUTUBE_LINK_HERE)

### Part 3 — Harder background
The same detector, unchanged, on a completely different background.

[![Part 3 demo](part1_output.png)](PASTE_YOUR_YOUTUBE_LINK_HERE)

### Part 4 — 3D position
The circle, labelled with its estimated depth.

![Part 4 output](part4_output.png)

## A couple of notes

- The detection settings (`texture_thresh`, `win`, `min_area`) are passed in per video rather than hard-coded, so each input can be tuned without touching the shared detector.
- Part 4 only applies to the circle, since it's the only shape with a given real dimension.
