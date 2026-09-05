# PennAiR Software Challenge — Design Process & Notes

An overview of the approach taken for each part, the key decisions made, and the
trade-offs behind them.

## Part 1 — Shape detection on a static image

- **Started with colour-based detection.** The first approach identified the grass
  by its green hue in HSV and treated everything else as a shape. This worked for
  four of the five shapes but **failed on the green shape**, whose colour fell inside
  the grass hue range and was erased along with the background.
- **Switched to texture-based detection.** Instead of colour, the detector measures
  local texture (how much pixels vary in a small neighbourhood): grass is busy and
  high-variance, the shapes are smooth and low-variance. This makes detection
  **colour-blind**, so it correctly finds the green shape and any colour of shape.
- **Restructured the code for reuse.** Knowing later parts would need the same
  detection, the core logic was written as a single reusable function returning the
  annotated image, the mask, and the list of shapes — so Parts 2–4 could import and
  reuse it without duplication.
- **Accepted a trade-off in edge quality.** Texture detection produces slightly
  rougher, wobblier outlines than the crisp colour method did. This was judged a
  worthwhile trade-off: robustness to background and colour matters more here than
  pixel-perfect edges.
- **Tuning.** The initial texture threshold, window size, and area floor were not
  accurate out of the box; these were adjusted until all five shapes were cleanly
  detected.
- **Outline colour.** The outline was initially bright green, which was invisible on
  the green shape. It was changed to a distinct colour so every shape's outline is
  clearly visible regardless of the shape's own colour.

## Part 2 — Shape detection on video

- A video is a sequence of frames, so this part reuses the Part 1 detector, applied
  frame by frame as a **streamed input** (one frame read and processed at a time, with
  no knowledge of future frames — the same constraint a live camera has).
- The video needed a **higher area floor** than the static image to reject small
  transient patches of grass that briefly read as smooth. This was passed in per-video
  rather than changing the shared detector.

## Part 3 — Background-agnostic detection

- The **same detector from Part 2 worked on the harder video** with only minor
  calibration of its parameters — no rewrite.
- This is the payoff of the texture approach: because detection never depended on
  colour, it transferred directly from a green grass background to a completely
  different greyscale background. The stricter background needed a lower texture
  threshold and a higher area floor to suppress false positives, but the underlying
  method was unchanged.
- **Known limitation:** texture separation relies on shapes being smoother than the
  background. It works well here, but would struggle if a background contained large
  smooth regions of its own. A natural next step would be to select the texture
  threshold automatically per frame (e.g. Otsu's method) rather than tuning it by hand.

## Part 4 — 3D position (depth)

- A camera discards depth, but if an object's real size is known, depth can be
  recovered from its apparent size using the camera's focal length:
  **Z = (focal length × real radius) / pixel radius**. The real X and Y are then
  back-projected from the centre pixel using the depth.
- **Applied to the circle only**, since the circle's real radius (10 in) is the only
  real-world dimension given. The other shapes have no supplied dimensions, so depth
  cannot be estimated for them from the given information.
- **Assumption:** the supplied intrinsic matrix listed the principal point at (0, 0),
  which is not physically meaningful, so the image centre was used as the principal
  point instead.

---

Thank you so much for putting this challenge together — I had a lot of fun working
through it, and it was a genuinely enjoyable way to learn computer vision from the
ground up. I really appreciate the time you spent reviewing this, and I hope to get
the chance to keep building this kind of thing with the team.
