---
title: Fractal Texturing
url: https://mini.gmshaders.com/p/gm-shaders-mini-fractal-texturing-1408552
author: Xor
published: '2022-10-15'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Fractal Texturing

### An algorithm for consistent texture detailing at any scale

Hi,

As some of you may have seen, I started developing a small 3D game last week with the hopes of finishing it in just two weeks. I'm still in the middle of it, so for that reason, this tutorial will be brief. You can see the progress I've made so far in this thread below.

## The Problem

As you can see, when you zoom out, textures can appear quite repetitive and artificial. Mipmapping helps smooth the distance textures, but can't help the repetition at all.

When you zoom in, textures lose all detail. I set out to find a solution that solves both issues and mitigates the need for mipmapping (it's been a trouble in this project).

## Texture Scaling

Here's the solution I came up with. The concept is quite simple.

Instead of sampling a texture at one scale, we will scale up pixels that are too small. The scale of the texture is inversely proportional to the depth. So if a pixel 1 unit away has a scale of `x`

, then 2 units away will be `x/2`

or more generally: `x / depth`


To scale up a texture, you need to divide the texture coordinates:

`vec2 scaled_uv = uv / scale;`



So if we want to reverse perspective scaling, we need to use depth:

```
float scale = depth;
vec2 scaled_uv = uv / scale;
```



Or just:

`scaled_uv = uv / depth;`



But we can't have every pixel at a separate scale or none of the pixels will match up with their neighbors, so we should round first:

Since we're dealing with exponentials, we need to take the log before rounding.

`float LOD = log(depth);`



Round down:

`float LOD_floor = floor(LOD);`



Now convert it back to exponential for scaling:

`vec2 scaled_uv = uv / exp(LOD_floor);`



Here's what this looks like:

Distance texture is scaled up and near texture is scaled down, making the level of detail appear roughly the same everywhere. Let's just remove the seams between the different levels!

## Fractal Texturing

Can you guess what comes next? Now we just need to blend the nearest scales, which can be done with an extra two samples. Just sample at the scale above and the scale below, then interpolate between the two:

Here's my code:

```
vec4 fractal_texture(sampler2D tex, vec2 uv, float depth)
{
float LOD = log(depth);
float LOD_floor = floor(LOD);
float LOD_fract = LOD - LOD_floor;
vec2 uv1 = uv / exp(LOD_floor - 1.0);
vec2 uv2 = uv / exp(LOD_floor + 0.0);
vec2 uv3 = uv / exp(LOD_floor + 1.0);
vec4 tex0 = texture2D(tex, uv1);
vec4 tex1 = texture2D(tex, uv2);
vec4 tex2 = texture2D(tex, uv3);
return (tex1 + mix(tex0, tex2, LOD_fract)) * 0.5;
}
```



You'll have to multiply the depth value you provide by some scaling value. It depends on a few factors: depth units, texture scale, and screen resolution (optional). For this particular example, I found this works well for my specific scene (and scales with window resolution):

`depth *= 1e3 / iResolution.y;`



Your scale will be something different. If it's too large, divide it, and if it's too small, multiply it.

Anyway, this is the result!

I created a [live demo on ShaderToy](https://www.shadertoy.com/view/mds3R4), which also includes a version with mipmapping. It's amazing to see how smooth it is.

## Conclusion

This technique is useful for providing a consistent level of detail, regardless of depth. Perfect for natural texturing settings like terrain rendering. Unnatural textures like bricks will not blend as smoothly because they are not designed to be scaled.

Anyway, hope you learned something interesting. Don't forget to check for development updates on [my little game project](https://twitter.com/XorDev/status/1578952412660105216). Thanks for reading.

-Xor