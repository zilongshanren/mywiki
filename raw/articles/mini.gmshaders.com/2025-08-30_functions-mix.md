---
title: 'Functions: Mix'
url: https://mini.gmshaders.com/p/func-mix
author: Xor
published: '2025-08-30'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Functions: Mix

### An overview of the mix function, how it works and some unusual uses

If you have written a few shaders you have probably already used the mix function to blend some colors together. This tutorial will go deeper, understanding math behind mixing and ways to use mix.

**Math Context**

The formula behind mix(x, y, a) is just: `x + (y - x) * a`


A longer formula may be easier to understand: `x * (1.0 - a) + y * a`


This function “linearly interpolates” from “x” to “y” based on the amount “a”. An amount of 0.0 returns x, 1.0 returns y, 0.5 returns halfway x and y, and so on.

These variables can be floats or vectors, and the math works the same. For a color blending example:

At the end of the day, it’s just addition, subtraction, and multiplication. The math works the same with amounts outside of the 0.0 to 1.0 range. This allows you to use mix, not just to interpolate, but also to [extrapolate](https://en.wikipedia.org/wiki/Extrapolation). More on that later.

**Note**: You're generally still better off using built-in hardware functions, as they are very well optimized.

# Color Tricks

So we already know how to blend two colors, but you can do a lot more with mix.

### Saturation

If you want to control saturation, just interpolate between grayscale and full color:

```
//Compute weighted luma
//https://en.wikipedia.org/wiki/Luma_(video)
float gray = dot(col.rgb, vec3(0.2126, 0.7152, 0.0722));
//Interpolate from grayscale to color
col = mix(vec3(gray), col, SATURATION);
```


The best part is that this works with extrapolation, too. You can boost saturation by using an amount greater than 1.0 (negative values invert hue).

### Brightness and Contrast

A simple formula for adjusting contrast and brightness with mix:

`col = mix(vec3(BRIGHTNESS), col, CONTRAST)`


The neat part about this formula is that you can adjust brightness and contrast as a vector, allowing for independent control of each RGB color channel.

# Coordinates

You can use mix for animations, transitions, and motion. It can be used for interpolating between two positions to move something:

`vec2 pos = mix(POS1, POS2, time_factor);`


With an [easing function](https://easings.net), you can also control the acceleration and deceleration.

### Radial Blur

[I have](https://www.shadertoy.com/view/mdXGzs) also used mix for radial blurs, chromatic aberration, and crepuscular rays by mixing the UV coordinates with a focus point:

```
//Iterate 20 times from 0 to 1
for(float i = 0.; i<1.; i+=.05)
{
//Add a texture sample approaching the center (0.5, 0.5)
//This center could moved to change how the direction of aberation
//The mix amount determines the intensity of the radial blur
vec2 tuv = mix(uv, vec2(0.5), i * 0.2);
col += texture(iChannel0, tuv) * 0.05;
}
```


Mixing helps with readability and makes it easy to control the center point.

### Texture Page Coordinates

When working with [texture pages](http://mini.gmshaders.com/p/gm-shaders-mini-two-textures-1376349), you often need to convert from a normalized coordinate range to that of a specific texture on the texture page:

```
//Blend between the top-left and bottom-right uvs
vec2 uv = mix(uvs.xy, uvs.zw, norm_uv);
```


# Remapping Function

One formula that I use all the time is a bit like mix 2.0. `mix(a, b, x)`

takes “x” from the [0.0, 1.0] to the [a, b] range. Remap takes the “x” from [a, b] to the [c, d] range:

```
remap(a, b, c, d, x)
{
return (x-a) / (b-a) * (d-c) + c;
}
```


It’s very useful, especially with texture coordinates

# Extras

I previously wrote about the OkLab colorspace, which is optimized for human color perception. The standard RGB colorspace is not perceptually linear, meaning that blending between two RGB colors can produce unnatural results. If you need to blend colors (hues, luminances, saturations, etc) visually, you want to use OkLab mix:

Here’s a nice video on linear interpolation and other blending functions by SimonDev:

That’s all for tonight. Thanks for reading!