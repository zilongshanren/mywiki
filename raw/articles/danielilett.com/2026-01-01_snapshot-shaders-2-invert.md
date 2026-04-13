---
title: Snapshot Shaders 2 - Invert
url: https://danielilett.com/snapshot-shaders-2/invert/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

This effect inverts the screen’s colors in an HDR-friendly manner. This means that color data will be inverted, but the shader will try and conserve luminance values.

# Parameters

**Strength**- How strongly to blend between a normal and inverted image. A value of 0.5 will result in a grey image, although some areas may turn out bright white if HDR is used and this filter happens before any tonemapping.