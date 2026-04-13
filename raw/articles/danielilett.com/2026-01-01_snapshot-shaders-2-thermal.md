---
title: Snapshot Shaders 2 - Thermal
url: https://danielilett.com/snapshot-shaders-2/thermal/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Calculates color bands in the image based on the luminance of each pixel and tints each band a different color, ideally starting from cold colors and transitioning to warm colors. This effect has a special interaction with the mask texture, which can be used to render the effect normally but artificially tag specific objects as ‘extra bright’.

# Parameters

## Thermal Settings

**Enabled**- Should the effect run?**Thermal Mask Mode**- Choose to only render masked objects, or render everything but masked objects are brighter than usual.**Mask Blur**- When a mask is enabled, how much should it be blurred? This can ensure a nice falloff between highlighted and background objects.**Mask Blur Step Size**- The blur algorithm can skip over some pixels, resulting in a sparse kernel for efficiency.**Add Brightness To Mask**- How much brightness should be added to masked objects?

## Colors and Thresholds

**Color 0 - 5**- Color to use for each color band of the image. There are six available color bands.**Threshold 0 - 4**- Luminance thresholds to use between each pair of color bands. There are five thresholds between the six color bands.