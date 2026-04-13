---
title: Snapshot Shaders 2 - Dithering
url: https://danielilett.com/snapshot-shaders-2/dithering/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Overlays a dither pattern onto the screen based on the luminance (brightness) of each pixel. The dither pattern provides a pleasing gradient between dark and light areas of the screen.

# Parameters

**Noise Texture**- Texture pattern to use as dither thresholds (I recommend using a Bayer matrix or blue noise pattern, both of which are included in the asset pack).**Noise Size**- Size of the dither pattern tiled across the screen.**Luminance Threshold**- An additional offset applied to each pixel’s luminance before thresholding.**Dark Color**- Color of the areas whose luminance fall under the threshold.**Use Scene Color**- When enabled, the Light Color is replaced by the original screen color.**Light Color**- Color of the areas whose luminance exceed the threshold.