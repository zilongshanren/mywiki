---
title: Snapshot Shaders 2 - Scanline
url: https://danielilett.com/snapshot-shaders-2/scanline/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Overlays a small texture onto the screen and multiplies its colors by the existing screen colors. This texture can be scrolled downwards over time.

# Parameters

**Scanline Texture**- Small texture containing the scanline pattern which will be tiled over the screen.**Scanline Strength**- How strongly the scanline texture should be multiplied with the original camera texture.**Scanline Size**- How many pixels the scanline texture takes up (i.e. setting this to 4 will tile the texture over 4x4 pixels).**Scanline Scroll Speed**- How quickly the scanlines scroll over the screen vertically.**Use Point Filtering**- Should the scanlines use point filtering for a crisper pattern?