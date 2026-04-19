---
title: Classic Demo Effects, Fire
url: https://www.4rknova.com/blog/2019/03/17/fire-effect
author: Nikolaos Papadopoulos
published: '2019-03-17'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

One of the most popular effects in the early days of demoscene is the fire effect. Various versions of the effect have been implemented, not only for tech demos but also games. Amongst other titles, it can be seen in the intro of ‘Teen Agent’ masked by the text of the game’s title [1] and various ports of Doom, most notably the ones for Sega Saturn, Nintendo 64 and Sony PSX

.

[[3]](https://www.4rknova.com#REF-3)The entire effect is simulated in 2D and using a transform feedback buffer. There are multiple variants of the effect but the basic mechanics behind the animation are quite simple. At first the framebuffer is initialized to 0. Then, at each update, the bottom row of the framebuffer is re-initialized with random scalar values in the [0,1] range to serve as the heat source. The value of a pixel is calculated as a weighted average of the values of nearby pixels below. By updating the calculation at each frame for each pixel, the seeding values at the bottom row dissipate as they propagate upwards. That creates the effect of cooling off as the heated particles rise.

Once we have a ‘heat value’ for each pixel, we can index a LUT to map that value to a color. Usually this takes the form of a color gradient going from black to red to yellow to white so as to simulate the tones we typically see in a fire. Different LUTs can be used to generate more exotic visuals.

# Implementation

In the first pass we generate the heatmap as described above.

```
#define GRID_SIZE (75.000)
#define COEF ( 0.193)
// Randomization utilities
float hash(vec2 p)
{
return fract(sin(dot(p,vec2(127.1,311.7))) * 43758.5453123);
}
float noise(vec2 p)
{
vec2 i = floor(p), f = fract(p);
f *= f*f*(3.-2.*f);
return mix(mix(hash(i + vec2(0.,0.)),
hash(i + vec2(1.,0.)), f.x),
mix(hash(i + vec2(0.,1.)),
hash(i + vec2(1.,1.)), f.x), f.y);
}
float fbm(in vec2 p)
{
return .5000 * noise(p)
+.2500 * noise(p * 2.)
+.1250 * noise(p * 4.)
+.0625 * noise(p * 8.);
}
void mainImage(out vec4 c, in vec2 p)
{
// Divide the screen in cells
float f = 1. / GRID_SIZE;
vec2 ac = vec2(iResolution.x / iResolution.y, 1);
vec2 uv = (p / iResolution.xy * 2. - 1.) * ac;
vec2 iuv = floor(GRID_SIZE * uv);
// Initialize the bottom row to a random value.
if (iuv.y < -GRID_SIZE + 1.) {
c = vec4(fbm((iuv * f + iTime)*3.), 0, 0, 1) - .1;
return;
}
// For all other rows, calculate the weighted average
// value below the current pixel
iuv = (uv / ac + 1.) *.5;
float c0 = texture(iChannel0, iuv + vec2(.0,-f) / ac).x;
float c1 = texture(iChannel0, iuv + vec2( f,-f) / ac).x;
float c2 = texture(iChannel0, iuv + vec2( f,-f) / ac).x;
float c3 = texture(iChannel0, iuv + vec2( f,-f * 2.) / ac).x;
float c4 = texture(iChannel0, iuv + vec2(-f,-f * 2.) / ac).x;
c = vec4((c0+c1+c2+c3+c4) * COEF, 0, 0, 1);
}
```


In a second pass we sample the generated map from the first pass and sample a function to generate the color values. As described above, instead of a procedural function, we could have used a 1D texture with a precalculated gradient.

```
void mainImage(out vec4 c, vec2 p)
{
c = texture(iChannel0, p.xy / iResolution.xy);
c = 1. - cos(c*3.14159/1.3); // Contrast
c = vec4( min(c.x*1.7, 1.)
, pow(c.x, 2.6)
, pow(c.x, 10.)
, 1
); // Palette
}
```


Note that the code above is divided in two passes for the purpose of clearly demonstrating the components of the effect. Alternatively, we could store the heat values in the alpha channel and simply do the color value mapping at the end of the first pass, storing the result in the other 3 channels.

Below is a live preview of the effect, implemented in GLSL.