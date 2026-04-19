---
title: 'The MRS Fractal: Mirror, Rotate, Scale'
url: https://www.4rknova.com/blog/2025/06/22/mrs-fractal
author: Nikolaos Papadopoulos
published: '2025-06-22'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Fractal rendering is usually introduced with Mandelbrot or Julia sets, but those are not the only way to generate rich self-similar structure. The MRS fractal is a small iterative system based on three geometric operations:

- Mirror space across one or more planes.
- Rotate the point around a fixed axis.
- Scale and offset the point before the next iteration.

The name is literal; MRS stands for Mirror, Rotate, Scale.

# Core idea

Given a 3D point \(p_0\), we iterate:

\[p_{n+1} = s \cdot R\left(M\left(p_n\right)\right) - o\]where:

- \(M\) is a mirror operator.
- \(R\) is a rotation matrix.
- \(s > 1\) is a scalar growth factor.
- \(o\) is a constant offset vector.

This loop folds space back on itself, then expands it. Repeating that process creates nested structure at many scales.

# Reference shader snippet

```
uniform int uPalette;
uniform int uIterations;
uniform float uZoom;
uniform float uRotSpeed;
uniform float uMirrorStart;
uniform float uScaleDecay;
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
vec2 uv = max(uZoom, 0.0001) * fragCoord.xy / iResolution.y;
float t = iTime * uRotSpeed;
float k = cos(t), l = sin(t);
float s = uMirrorStart;
int iters = clamp(uIterations, 1, 128);
for (int i = 0; i < 128; ++i) {
if (i >= iters) break;
uv = abs(uv) - s; // mirror
uv *= mat2(k, -l, l, k); // rotate
s *= uScaleDecay; // scale decay
}
float x = 0.5 + 0.5 * cos(6.28318530718 * 40.0 * length(uv));
vec3 col = vec3(x); // palette selection omitted for brevity
fragColor = vec4(col, 1.0); // vignette/alpha applied in full shader
}
```