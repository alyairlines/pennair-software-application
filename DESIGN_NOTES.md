# PennAiR Software Challenge — Design Notes

My process for each part, and the main decisions I made along the way.

## Part 1 — Static image

I started by trying to detect the shapes through color; find the green grass in HSV and treat everything else as a shape. This worked for four shapes but failed on the green one, because its color fell into the same range as the grass and got erased with the background.

So I switched to detecting by texture instead of colour. The idea is that grass is busy (pixels vary a lot in a small area) while the shapes are smooth (pixels barely vary). Measuring that local variation makes the detection completely color-blind, so it finds the green shape and any other color too.

I also knew I'd be reusing this in the later parts, so I wrote the detection as one function that returns everything I'd need later (the outlined image, the mask, and the list of shapes), rather than something I'd have to rewrite each time.

One tradeoff was that texture detection gives slightly rougher, wobblier outlines than the clean color method did. I decided that was worth it because being accurate to color and background matters more than perfect edges.

The starting values for the texture threshold, window size and area floor weren't quite right, so I played around with them until all five shapes came out cleanly. I also changed the outline color, since it was bright green at first and you couldn't see it at all on the green shape.

## Part 2 — Video

A video is just a sequence of frames, so this part reuses the Part 1 function and runs it on each frame one at a time (a streamed input). The only change I needed was a higher area floor than the static image, to ignore small bits of grass that briefly looked smooth.

## Part 3 — Background agnostic

The same detector from Part 2 worked here too, just with a few tweaks to the values. Because the Part 2 detector never cared about color, it moved straight from green grass to a completely different background without a rewrite. The harder background needed a stricter texture threshold and a higher area floor to stop false detections, but the method itself didn't change.

The limitation is that this relies on the shapes being smoother than whatever's behind them. It works well here, but it would struggle if a background had big smooth patches of its own. If I took it further I'd probably pick the threshold automatically per frame instead of tuning it by hand.

## Part 4 — 3D position

I used the calculation for depth = (focal length × real radius) / pixel radius. Once I had the depth I worked out the real x and y of the center from the center pixel.

I only did this for the circle, since its real radius (10 in) is the only real-world measurement given. The other shapes don't have any given dimensions, so there's nothing to compare their apparent size against. The given intrinsic matrix also listed the principal point as (0,0), which doesn't make physical sense, so I used the image center instead.

---

Thank you so much for putting this together! I genuinely had a lot of fun with it, and it was a really nice way to learn a bit of computer vision. I appreciate you taking the time to look through it, and I'd love the chance to keep working on this kind of thing with the team.
