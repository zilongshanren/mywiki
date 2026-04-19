---
title: Anti-Aliasing, FXAA
url: https://www.4rknova.com/blog/2015/02/15/fxaa
author: Nikolaos Papadopoulos
published: '2015-02-15'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

Fast approximate anti-aliasing (FXAA). Is a post processing depth-aware edge filter. It’s a cheap and fast alternative to MSAA that can produce good visual results. The algorithm consists of two steps:

- Determine whether the shaded pixel is located on an edge.
- Smooth the problematic pixel values by applying a blur filter.

Note that anti-aliasing methods such as FXAA should be applied prior to rendering the UI elements because the filtering process can have a noticeable impact on it as well.

# Implementation

Below is an example implementation in a GLSL fragment shader.

```
uniform vec4 iResolution;
#define RES iResolution.xy
vec3 sample(vec2 p);
vec3 fxaa(vec2 p)
{
float FXAA_SPAN_MAX = 8.0;
float FXAA_REDUCE_MUL = 1.0 / 8.0;
float FXAA_REDUCE_MIN = 1.0 / 128.0;
// 1st stage - Find edge
vec3 rgbNW = sample(p + (vec2(-1.,-1.) / RES));
vec3 rgbNE = sample(p + (vec2( 1.,-1.) / RES));
vec3 rgbSW = sample(p + (vec2(-1., 1.) / RES));
vec3 rgbSE = sample(p + (vec2( 1., 1.) / RES));
vec3 rgbM = sample(p);
vec3 luma = vec3(0.299, 0.587, 0.114);
float lumaNW = dot(rgbNW, luma);
float lumaNE = dot(rgbNE, luma);
float lumaSW = dot(rgbSW, luma);
float lumaSE = dot(rgbSE, luma);
float lumaM = dot(rgbM, luma);
vec2 dir;
dir.x = -((lumaNW + lumaNE) - (lumaSW + lumaSE));
dir.y = ((lumaNW + lumaSW) - (lumaNE + lumaSE));
float lumaSum = lumaNW + lumaNE + lumaSW + lumaSE;
float dirReduce = max(lumaSum * (0.25 * FXAA_REDUCE_MUL)
, FXAA_REDUCE_MIN);
float rcpDirMin = 1. / (min(abs(dir.x), abs(dir.y)) + dirReduce);
dir = min(vec2(FXAA_SPAN_MAX),
max(vec2(-FXAA_SPAN_MAX), dir * rcpDirMin)) / RES;
// 2nd stage - Blur
vec3 rgbA = .5 * (sample(p + dir * (1./3. - .5)) +
sample(p + dir * (2./3. - .5)));
vec3 rgbB = rgbA * .5 + .25 * (
sample(p + dir * (0./3. - .5)) +
sample(p + dir * (3./3. - .5))
);
float lumaB = dot(rgbB, luma);
float lumaMin = min(lumaM, min(min(lumaNW, lumaNE),
min(lumaSW, lumaSE)));
float lumaMax = max(lumaM, max(max(lumaNW, lumaNE),
max(lumaSW, lumaSE)));
return ((lumaB < lumaMin) || (lumaB > lumaMax)) ? rgbA : rgbB;
}
```


# Screenshots

The screenshot below shows FXAA applied to a rendering of the Mandelbrot fractal.

![01](../../assets/a4d2e3c747789115.png)


Below is a zoomed version of the same render. Slide the divider right or left to review the per pixel difference. On the left side, the original image is shown. FXAA is applied on the image on the right side.