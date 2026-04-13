---
title: 'GM Shaders: Mipmaps'
url: https://mini.gmshaders.com/p/mipmaps
author: Xor
published: '2024-01-20'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mipmaps

### How to downsample textures for quality and performance

Hi everybody,

Today I want to show you a technique called mipmapping, which can be used for dynamically downsampling textures, potentially improving visual quality and performance.

Mipmaps are pre-generated, and we don’t yet have support for mipmapping on surfaces. More on the limitations later.

If you happen to already know about mipmapping, feel free to skip down to the “Extras” section for other great resources. I try to leave something for everybody!

Now let’s begin with the concept of “mip levels”.

# Mip Levels

Mipmapping works by pre-generating downsampled versions of a texture, cutting the width and height in half over and over until you get a 1x1 image. For example, if you start with 512x512, then LOD 0 (Level Of Detail) is 512x512, LOD 1 is 256x256, LOD 2 is 128x128 and so on down to 1x1.

Many people don’t know this, but you can enable mipmapping in any GameMaker game like so:

```
//Enable texture interpolation
gpu_set_texfilter(true);
//Enable mipmapping
gpu_get_tex_mip_enable(mip_on);
```


GameMaker also supports 3 mipmap filters:

**tf_point**: This samples on the mipmap at the nearest LOD, leading to hard transitions between different texture qualities, but also being very cheap to use.**tf_linear**: This is the default setting. It samples at the nearest to LODs and smoothly interpolates between them, eliminating the hard edges, but coming at a slightly higher cost.: Unlike linear or point filter, uses a more complex mipmap that can scale the x and y axes independently, while still producing smooth results. This mipmap looks something like this:[tf_anisotropic](https://en.wikipedia.org/wiki/Anisotropic_filtering)This filtering looks the best, but uses more video memory and makes texture samples more costly because of the more complicated interpolation process. Anisotropic can do anything Isotropic filters can and more.


So to recap: Point filtering is cheap, but doesn’t blend smoothly (might be fine for 2D),

Linear filtering smoothly blends between different levels of detail, at a slightly higher cost to sample and Anisotropic filtering takes direction into account for even better blending, but at a higher sampling cost. I’d generally recommend linear filtering for most cases.

Mipmapping helps you to solve two problems:

When you shrink a texture down really small, (like a scaled down sprite or a distance object in a 3D context), you get too many texels for each pixel on the screen. If a texture has 10 texels for every pixel on the screen, then even with texture filtering, you’re still going to be skipping a bunch of texels, or even worse with nearest filtering. This can lead to moiré patterns, flickering or too much noise. This looks ugly, but it’s also slightly less performant because your GPU is not optimized for skipping texels.

Let’s talk a bit more about how this filtering actually works and what we can do with it.

# Filtering

This part will get a little in depth on how the filtering works under the hood. You don’t strictly need to know this to start using mipmapping, so if you get a little bogged down, feel free to skip this bit and come back to it whenever you’re ready.

To fully understand mipmapping, you’ll want to be somewhat comfortable with the concept of screen derivatives like dFdx and dFdy.

To sample a mipmap texture, you have to know what LOD to use for each fragment. Let’s assume we’re using linear (isotropic) filtering for now and take a look at how things are computed internally so we can better understand the process. To calculate the LOD, we want to approximate how many LOD 0 texels would fit in a given pixel on the screen. Thankfully, we can use derivatives to help us account for any transformations (rotations, scaling, skewing, warping, etc) that might apply to our texture coordinates.

We just need to compute the x and y derivatives of the texelspace coordinates (texture coordinates * texture resolution). This tells us the difference in texels from one pixel/fragment to one of its neighbors, which is a good approximation for the texel size at any given point. Then we compute the lengths of these two derivatives and use whichever is larger (has more texels pack in it). Now we just need the log2 of the length because LOD is stored in an exponential scale (1x, 2x, 4x, 8x, etc.).

My test code looks like this:

```
//Compute texel space derivatives
vec2 dx = dFdx(v_vTexcoord) * tex_res;
vec2 dy = dFdy(v_vTexcoord) * tex_res;
//Maximum derivative length (squared to simplify)
float md = max(dot(dx,dx), dot(dy,dy));
//Compute Level Of Detail (times half for sqrt)
float lod = log2(md) * 0.5;
```


The code above will give us fractional LODs like 0.5 or 3.7. That’s fine. Internally, with linear filtering, a LOD of 0.5 would translate to a 50% blend of LOD 0 and LOD 1.

This works great 99% of the time, but since we’re using screen derivatives which are computed in 2x2 blocks, you have to be careful with discontinuous texture coordinates. Things like: `uv = fract(uv)`

can cause seams at the edges. It’s best to use `gpu_set_texrepeat(true)`

whenever possible. Just being aware of how derivatives are computed can help you avoid some of the artifacts, but more on that later.

# Bias and Blurs

Did you know that `texture2D(sampler, uv, [bias])`

has a third optional argument? This bias argument is where you can add (or subtract) to the internally computed LOD. Which means that if you want to sample the texture at half resolution, you can just do: `texture2D(gm_BaseTexture, v_vTexcoord, 1.0)`

. Sometimes this will work for a cheap blur effect. You can set the bias to any value like and even do a gradient of decreasing detail like in my intro. Some even use the bias factor for cheap [depth of field](https://www.shadertoy.com/view/ws3cDj), soft drop shadows or glow effects. If that for best results, you can combine a cheap blur shader with a mipmapping bias for much stronger results.

I’ve put together a little [GameMaker demo for mipmap blurring here](https://github.com/XorDev/GM_MipBlur).

There’s also `texture2DLod(sampler, uv, lod)`

for setting the LOD directly, but GameMaker does not support it for some reason. For now, we can get around it by computing the LOD ourselves and subtracting that in the bias. For most cases, texture2D will do fine. Now, you may want to use this in your project, but first we need to talk about the factors you’ll need to consider.

# Considerations

Mipmapping is a powerful tool for cheap post-processing, but it’s not without drawbacks.

### Memory Usage

Isotropic texture filtering requires 33% more texture data, so you’ll have to be careful if you have a ton of large textures. Anisotropic filtering 4xs the texture size! You should definitely consider your target hardware needs before going all in on mipmapping. On the bright side, it does tend to make rendering faster at the cost of more VRAM.

### No surfaces!

GameMaker does not support creating mipmaps for surfaces. In other engines, it’s possible to use mipmapping for cheap bloom, blurs, etc, but GameMaker doesn’t have a way to do this. If this something you’d like to see, [please let the GM team know](https://github.com/YoYoGames/GameMaker-Bugs/issues/3003)! It would open many new opportunities.

### Squares and borders

You can only use mipmapping on power of 2 sized, square textures. If your texture isn’t, it gets padded until it is. You also have to think about the borders of your sprite. If you’re going to be doing a blur effect, you have to leave enough empty space around your sprite to blur it without cutting off the edges. This will use a little more VRAM.

Note: *Repeating textures work great with mipmapping because they don’t require any padding. *

### Artifacts and seams

Generally, you want to keep your texture coordinates continuous and smooth when using mipmaps. If you use fract or floor, that may cause visual seams that mess with the LOD. [There are some workarounds](https://www.shadertoy.com/view/7sSGWG), but ideally, don’t make discontinuities!

# Conclusion

Mipmapping often makes rendering look better and run faster at the cost of some extra video memory. Even without the use of shaders it can make a big difference, however, with shaders, you unlock a whole new dimension to your textures. There are countless possibilities from simple blurs, glows, shadows, to depth of field and bloom.

I sincerely hope that GM will implement mipmapping with surfaces. I feel like it’s one of the GLSL infinity stones that we don’t yet have (also looking at depth buffers and compute shaders). Even with the limitations, there’s a lot that can be done as long as you know how to manage memory, sprite borders and potential artifacts.

I hope this lays a strong foundation so that more developers can tap into this.

# Extras

[Ben Golus wrote a very thorough article](https://bgolus.medium.com/distinctive-derivative-differences-cce38d36797b) on how to deal with some mipmapping artifacts. Well worth the read.

DragoniteSpam made a good [video on 3D normal mapping in GameMaker](https://youtu.be/yBEi9l-n_O4). Go over and say hello if you’re into that sort of thing![An analysis of GPU noise functions](https://arugl.medium.com/hash-noise-in-gpu-shaders-210188ac3a3e) by Danil.

That’s it for this week. I’m unavailable next week, but I’ll probably be back the week after. Until then, have a great week!