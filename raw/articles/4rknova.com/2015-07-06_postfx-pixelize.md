---
title: PostFX, Pixelize
url: https://www.4rknova.com/blog/2015/07/06/fx-pixelize
author: Nikolaos Papadopoulos
published: '2015-07-06'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Description

Pixelization is one of the simplest post-processing effects to implement. The core idea is to quantize screen-space UVs so nearby fragments sample the same source texel. This collapses local detail and creates the classic blocky look.

The same principle can be extended by changing the cell shape. Instead of rendering each cell as a flat square, we can apply a radial falloff and get a dot-matrix style image that feels closer to print halftoning.

In the interactive demo below, all four techniques are available in one shader with runtime controls.

# Combined demo

## Simple pixelization

For each fragment, we compute a cell size in pixels, snap the incoming fragment coordinates to that grid, and read a single source sample for the whole cell.

```
vec3 applySimplePixelize(vec2 fragCoord) {
float s = max(1.0, uPixelScale * (iResolution.x / 60.0));
vec2 snapped = floor((fragCoord + 0.5) / s) * s;
vec3 col = texture(iChannel0, snapped / iResolution.xy).rgb;
if (uChromaKey) {
float lum = dot(vec3(0.2126, 0.7152, 0.0722), col);
if (lum > max(col.r, col.b) + uChromaBias) {
return uBgColor;
}
}
return col;
}
```


Notes:

`uPixelScale`

controls how coarse the mosaic becomes.- The
`+0.5`

center offset avoids a visible directional bias. - The optional chroma-key test suppresses bright green-screen like regions.

## Dot-matrix effect

This version still samples one color per cell, but applies a circular mask. Fragments near the center of the cell receive more of the sampled color, fragments near the border blend toward background.

```
vec3 applyDotMatrix(vec2 fragCoord) {
vec2 gridsz = uGridSize * vec2(iResolution.x / iResolution.y, 1.0);
vec2 pc = fragCoord / iResolution.xy * gridsz;
vec2 cl = floor(pc) + 0.5;
vec3 col = texture(iChannel0, cl / gridsz).rgb;
float dst = pow(max(0.0, 1.0 - length(pc - cl)), uBias) * uDotScale;
float lum = dot(vec3(0.2126, 0.7152, 0.0722), col);
if (uChromaKey && lum > max(col.r, col.b) + uChromaBias) {
col = uBgColor;
}
return mix(uBgColor, col, min(1.0, dst * lum));
}
```


Notes:

- The
`iResolution.x / iResolution.y`

factor keeps dots circular on wide or tall viewports. `uBias`

tightens or softens the radial falloff curve.`uDotScale`

changes the apparent dot fill amount and contrast.

## Hex mosaic

Hex mode quantizes each fragment into an axial hex grid, rounds to the nearest hex cell center, then samples one color for that cell. The result is a more organic mosaic than square cells, while still preserving large image features.

```
vec3 applyHexPixelize(vec2 fragCoord) {
const float SQRT3 = 1.73205080757;
float aspect = iResolution.x / iResolution.y;
float size = max(0.01, uHexSize);
vec2 uv = fragCoord / iResolution.xy;
vec2 p = vec2(uv.x * aspect, uv.y);
vec2 axial;
axial.x = (SQRT3 / 3.0 * p.x - 1.0 / 3.0 * p.y) / size;
axial.y = (2.0 / 3.0 * p.y) / size;
vec2 h = hexRound(axial);
vec2 center;
center.x = size * SQRT3 * (h.x + 0.5 * h.y);
center.y = size * 1.5 * h.y;
vec2 sampleUv = vec2(center.x / aspect, center.y);
return sampleWithChroma(clamp(sampleUv, vec2(0.0), vec2(1.0)));
}
```


Notes:

- Aspect correction keeps hexes regular on non-square viewports.
`uHexSize`

controls the apparent cell scale.- Clamping the sample UV avoids out-of-bounds fetches at image edges.

## Cross-stitch

Cross-stitch mode uses one color sample per grid cell, then draws an `X`

pattern inside each cell by measuring distance to the two diagonals. This creates a stitched fabric look while keeping scene silhouettes readable.

```
vec3 applyCrossStitch(vec2 fragCoord) {
vec2 gridsz = uGridSize * vec2(iResolution.x / iResolution.y, 1.0);
vec2 pc = fragCoord / iResolution.xy * gridsz;
vec2 cl = floor(pc) + 0.5;
vec3 col = sampleWithChroma(cl / gridsz);
vec2 f = fract(pc);
float d1 = abs(f.x - f.y);
float d2 = abs(f.x + f.y - 1.0);
float d = min(d1, d2);
float stitch = 1.0 - smoothstep(
uCrossThickness, uCrossThickness + uCrossSoftness, d
);
float lum = dot(vec3(0.2126, 0.7152, 0.0722), col);
return mix(uBgColor, col, stitch * clamp(lum * 1.15, 0.0, 1.0));
}
```


Notes:

`uCrossThickness`

sets thread width.`uCrossSoftness`

smooths stitch edges.- Luminance scaling keeps brighter areas more pronounced.

## Controls

The demo exposes the following parameters:

`Mode`

: switch between simple pixelize, dot-matrix, hex mosaic, and cross stitch.`Pixel Scale`

: cell size for the simple mode.`Grid Size`

,`Dot Bias`

,`Dot Scale`

: shape and intensity for dot mode.`Hex Size`

: cell size for hex mode.`Cross Thickness`

,`Cross Softness`

: control stitch width and edge falloff.`Chroma Key`

,`Chroma Bias`

,`Background`

: mask bright keyed regions and replace them with a chosen background color.