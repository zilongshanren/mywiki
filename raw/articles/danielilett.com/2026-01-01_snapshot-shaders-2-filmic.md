---
title: Snapshot Shaders 2 - Filmic
url: https://danielilett.com/snapshot-shaders-2/filmic/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Add filmic effects like black bars based on aspect ratio and random fuzzy gradient noise for film grain.

# Parameters

**Use Film Bars**- Toggle whether to use black bars at the top, bottom, and sides of the screen. This part of the effect ignores any masks applied to the effect.**Aspect Ratio**- If film bars are enabled, this controls the end aspect ratio of the screen. If this is wider than the original image, then bars are drawn on the top and bottom of the screen. If it is not as wide, bars are drawn on the sides of the screen.**Film Bar Color**- Which color to draw the bars if the aspect ratio does not match. This is usually black.**Noise Strength**- How strongly the film grain should be overlaid onto the screen.**Noise Speed**- How quickly the film grain scrolls to the next random value.**Noise Size**- How large each ‘grain’ of noise should appear on screen.**Noise Interpolation**- Which interpolation algorithm to use for smoothing the noise grain values.*Hermite*is faster, while*Quintic*looks very slightly nicer (but you may not notice with fast-scrolling grain).