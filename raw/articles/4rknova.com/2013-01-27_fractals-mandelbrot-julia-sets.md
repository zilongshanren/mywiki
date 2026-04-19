---
title: Fractals, Mandelbrot & Julia Sets
url: https://www.4rknova.com/blog/2013/01/27/fractals-mandelbrot
author: Nikolaos Papadopoulos
published: '2013-01-27'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Mandelbrot Set

The Mandelbrot set is perhaps the most popular fractal. It was named after the mathematician Benoit B. Mandelbrot. The mathematical background is quite simple to understand, especially if you are familiar with the complex numbers theory. The following recursive equation is used:

\[z_{n+1} = z_{n}^2 + c\]with:

\[z_n \in \mathbb{C} \\\ \lim_{n \rightarrow \infty}\| z_{n} \| \ne \infty \\\ z_{0} = c\]It’s mathematically proven that for given \(c\) if the above limit exceeds 2 then \(c\) does not belong to the set, therefore:

\[\{\; c \;\colon\; c \in \mathbb{C},\;\; \lim_{n \rightarrow \infty}\vert z_{n} \vert \lt 2\;\}\]A complex 2D number is defined as follows on the Cartesian complex plane:

\[z_n = a + bi\]where

\[a,b \in \mathbb{R} \\\]and

\[i = \sqrt{−1}\]finally the square of a complex number is calculated as below:

\[z_n^2 = (a^2 - b^2) + (ab + ba)i \\\ z_n^2 = (a^2 - b^2) + (2 * ba)i\]## Implementation

Below is an example implementation of the Mandelbrot set in a GLSL fragment shader.

```
#define ZOOM 1.4
#define ITER 128 // Max number of iterations
vec3 fractal(vec2 p)
{
vec2 z = vec2(0);
for (int i = 0; i < ITER; ++i) {
z = vec2(z.x * z.x - z.y * z.y, 2. * z.x * z.y) + p;
if (dot(z,z) > 4.) {
float s = .125662 * float(i);
return vec3(vec3(cos(s + .9)
, cos(s + .3)
, cos(s + .2))
* .4 + .6);
}
}
return vec3(0);
}
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
vec2 c = (fragCoord.xy / iResolution.xy * 2. - 1.)
* vec2(iResolution.x / iResolution.y, 1)
* ZOOM - vec2(.5,0.);
fragColor = vec4(fractal(c), 1);
}
```


## Samples

The points that are colored black belong to the set. The rest of the points are colored based on the number of iteration it took to reject them.

![Mandelbrot sample near the main cardioid with escape-time coloring.](../../assets/401108d4ab51207c.png)

![Another Mandelbrot zoom region showing boundary complexity.](../../assets/ed222e133dca706e.png)

![Mandelbrot detail view highlighting self-similar structures.](../../assets/41a48390803a7bdc.png)

# Julia Sets

For every point on the complex plane, a julia set can be generated. Julia sets use the same formula as Mandelbrot, however it introduces the following parameters:

| Symbol | Meaning |
|---|---|
| \(c\) | an arbitrary complex number |
| \(z_0\) | the current pixel coordinate |

- Pick one complex number \(c\) and keep it fixed.
- Run the iteration for all starting points \(z_0\) on the plane.
- The points that stay bounded form the Julia set for that specific \(c\).

Now repeat this for many different values of \(c\). The Mandelbrot set is the set of all those \(c\) values where the corresponding Julia set is connected (one piece), instead of broken into disconnected dust-like pieces.

## Implementation

```
#define ZOOM 1.3
#define OFFSET vec2(-.5,0)
#define ITER 128 // Max number of iterations
#define C vec2(cos(iTime*0.0926), sin(iTime*0.0613))
vec3 fractal(vec2 p, vec2 c)
{
vec2 z = p - OFFSET;
for (int i = 0; i < ITER; ++i) {
z = vec2(z.x * z.x - z.y * z.y, 2. * z.x * z.y) + c;
if (dot(z,z) > 4.) {
float s = .125662 * float(i);
return vec3(vec3(cos(s + .9)
, cos(s + .3)
, cos(s + .2))
* .4 + .6);
}
}
return vec3(0);
}
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
vec2 c = (fragCoord.xy / iResolution.xy * 2. - 1.)
* vec2(iResolution.x / iResolution.y, 1)
* ZOOM - vec2(.5,0.);
fragColor = vec4(fractal(c * ZOOM, C), 1);
}
```


## Samples

Again, the points that are colored black belong to the set. The rest of the points are colored based on the number of iteration it took to reject them.

![Julia set sample.](../../assets/96b80d54ca0be583.png)

# Interactive demo

The demo below lets you switch between Mandelbrot and Julia rendering modes and adjust the key uniforms in real time.