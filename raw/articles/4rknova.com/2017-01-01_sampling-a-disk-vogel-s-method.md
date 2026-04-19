---
title: Sampling a Disk, Vogel's Method
url: https://www.4rknova.com/blog/2017/01/01/vogel
author: Nikolaos Papadopoulos
published: '2017-01-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

There are many ways to spread points across the surface of a disk but doing so in an even distribution can be challenging. Vogel’s method solves that problem elegantly. Each sample point is calculated in polar coordinates and then transformed to the equivalent Cartesian set. For each sample we need to specify two quantities, a radius and a theta angle. First the unit disk is divided to N rings of equal areas, where N is the total number of samples. Each ring will have a radius of:

\[t_i = \sqrt{\frac{i}{N}}\]A theta angle offset is applied to each consecutive sample. The most fitting candidate is the golden angle, which is an irrational number. Using such a number with ensure that samples are not aligned in clusters with the center of the disk. In particular, the samples will follow a spiral pattern instead.

\[\phi = \pi(3 - \sqrt{5})\]# Implementation

Below I’ve included my [shadertoy](https://www.shadertoy.com/view/XtXXDN) implementation. Note that I am using a slightly different way of calculating the radius of each ring. That is because I’ve found that the traditional method creates a slightly uneven distribution at the center of the disk for a sufficiently large number of samples (as seen below).

![01](../../assets/5a7bb9ce820b33a6.png)


Also, the golden angle is precalculated to speed up performance.

```
uniform vec4 iResolution;
[...]
#define E 5e-5
#define GA 2.39996322972865332
#define PI 3.14159265359
#define NS 512
vec2 sample(vec2 uv, float a, float i, float n)
{
// The disk is divided to NS rings of equal areas
// and each point is placed on the corresponding ring
// with a theta-offset by the golden angle.
float r = sqrt((i+.5) / n)
, t = i * a;
// Convert from polar coordinates to cartesian.
return r * vec2(cos(t), sin(t));
}
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
vec2 uv = fragCoord.xy / iResolution.xy * 2. - 1.;
uv *= 1.1 * vec2(iResolution.x / iResolution.y, 1);
vec3 col = vec3(0);
for (int i = 0; i < NS; ++i) {
vec2 p = sample(uv, GA, float(i), float(NS))
, d = (p - uv);
float x = E / dot(d,d);
col += vec3(x*x*x);
}
fragColor = vec4(col,1);
}
```


![01](../../assets/4e7a6e3d49761ce4.png)