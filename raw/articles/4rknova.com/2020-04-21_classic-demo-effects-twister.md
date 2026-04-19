---
title: Classic Demo Effects, Twister
url: https://www.4rknova.com/blog/2020/04/21/twister-effect
author: Nikolaos Papadopoulos
published: '2020-04-21'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

The twister effect is one of the most iconic demoscene effects. It simulates the twisting motion of a cuboid that is made of a soft, pliable material.

# How does it work

The mathematical background behind this visual effect is suprisingly simple.

Imagine a cuboid sliced into thin wafers from top to bottom. For each slice, we essentially have a 2D quad, which is mathematically defined by four points: x0, x1, x2, x3. When we view the geometry standing in front of it, each of these slices will appear as a horizontal line.

Our image is a 2D plane and each of the slices essentially appears and behaves as a 1D line. All we can see is a horizontal line that maps to one of the edges of the respective quad.

For each quad, the 1D position of its points is calculated using the formula below:

\[x_i = sin(a + \frac{\pi}{2} * i )\]where a is a phase value.

Each quad has 4 edges: x1-x2, x2-x3, x3-x4, x4-x1.

We need to draw all of the visible edges. Practically, in most cases there will be two edges visible. When a slice is aligned to 90 degree intervals, there will only be one edge visible.

The following condition can determine whether an edge is visible or not. Occluded edges are obviously not drawn.

\[x_{start} < x_{end}\]# Implementation

Below is an implementation of the twister effect and its live preview in shadertoy.

```
// by Nikos Papadopoulos, 4rknova / 2015
// MIT License.
// Classic demoscene twister: each horizontal slice is a 2D quad; we render the
// visible edge segments and texture them. Background can be transparent.
#define P2 1.57079632679 // pi/2
#define E (0.07) // Edge width (normalized)
#define T iTime // Time
#define C vec3(.15) // Background Color
#define EC vec3(0.0) // Edge Color
#define A vec2(.5,1.5) // Amplitude XY (x = width, y = twist frequency)
#define S(x) texture(iChannel0, vec2(2.43, 1) * x).xyz // Texture sampling
#define TRANSPARENT_BG 1 // 1 = transparent background, 0 = solid C
void mainImage(out vec4 c, vec2 p)
{
// Map pixel coords to normalized space [-1, 1].
vec2 u = p.xy/iResolution.xy*2.-1.;
#if TRANSPARENT_BG
// Start fully transparent and only draw visible edges.
vec3 r = vec3(0.0);
float alpha = 0.0;
#else
vec3 r = C;
float alpha = 1.0;
#endif
float v[4];
// Compute the 4 edge positions for this horizontal slice.
for (int i = 0; i < 4; ++i)
v[i] = A.x * sin(A.y * sin(u.y * cos(T)) + (cos(T) + P2 * float(i)));
// For each edge segment, draw it only if it faces the camera (n - p > 0).
for (int i = 0; i < 4; ++i) {
float n = v[int(mod(float(i)+1.,4.))], p = v[i];
if (n-p > 0. && u.x < n && u.x > p) {
float k = n-p, x = (u.x-p) / k;
vec3 base = k * S(vec2( x * A.x, u.y * A.y));
// Edge falloff for a thin rim highlight.
float l = smoothstep(0., A.x * E, x)
* smoothstep(0., A.x * E, 1.-x);
float edge = pow(l, 32.);
// Blend edge color into the textured slice.
r = mix(EC, base, edge);
alpha = 1.0;
}
}
c = vec4(r, alpha);
}
```