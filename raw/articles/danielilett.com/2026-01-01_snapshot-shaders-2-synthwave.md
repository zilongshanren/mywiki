---
title: Snapshot Shaders 2 - Synthwave
url: https://danielilett.com/snapshot-shaders-2/synthwave/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Overlays a synthwave gridline pattern onto the scene, with the option to replace the original scene color with a block background color.

# Parameters

**Use Scene Color**- Use the scene color instead of*Background Color*?**Background Color**- Color of the background if*Use Scene Color*is turned off.**Line Color 1**- Color of the synthwave lines at the bottom of the screen. HDR colors will glow if a Bloom effect is present.**Line Color 2**- Color of the synthwave lines at the top of the screen. HDR colors will glow if a Bloom effect is present.**Line Color Mix**- Controls the mix between the two line colors. Lower values favour the top color (2). Higher values favor the bottom color (1). A value of 1 is a neutral mix (although it may not appear to be perceptually).**Line Width**- Thickness of the lines in world space units.**Line Softness**- Falloff between synthwave lines and*Background Color*in world space units.**Gap Width**- Space between lines along each axis in world space units.**Line Offset**- Offset from (0, 0, 0) along each axis in world space units.**Start Fadeout Distance**- Distance from the camera where the synthwave lines start to fade out.**End Fadeout Distance**- Distance from the camera where the synthwave lines become completely invisible.**Axis Mask**- Synthwave lines are shown only along these axes. Choose from X, Y, Z, XY, XZ, YZ, or XYZ.