---
title: 'GM Shaders: Blur Philosophy 2'
url: https://mini.gmshaders.com/p/blur2
author: Xor
published: '2024-03-02'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

Last week, we talked about Blur Philosophy, an introduction on how to write better blur shaders, specifically talking about sample count, Gaussian distribution, pre-computed weights and multi-pass blurs:

Now, we’ll continue where we left off with some extra tips for improving quality and performance.

Using Interpolation

Texture interpolation is quite optimized. In my testing, it’s quite a bit faster than sampling 4 adjacent texels (texture pixels) without interpolation enabled, and interpolating between them manually. We can use this to our advantage! Instead of sampling every texel, we can sample halfway between them.

Instead of sampling each texel individually (left), we can sample fewer times by sampling in between texels (right)

So to apply this, we first need to enable texture interpolation (In GameMaker we use can use gpu_set_texfilter(true) or texture_set_interpolation in GM:S 1). We can do a 3x3 blur with just 4 texture samples and some interpolation:

Sampling the 4 red points, covers all the yellow texels

By sampling the 4 points in between the texels, we’re effectively sampling the average of all 9 of the yellow texels. Here’s a code example:

//Texture color sum and weight sum for computing the average color
vec4 tex_sum = vec4(0);
//Jump offset
const vec2 off = vec2(-0.5, 0.5);
//Four samples, covering 9 texels
tex_sum += 0.25 * texture(tex, uv + off.xx * texel);
tex_sum += 0.25 * texture(tex, uv + off.yx * texel);
tex_sum += 0.25 * texture(tex, uv + off.xy * texel);
tex_sum += 0.25 * texture(tex, uv + off.yy * texel);

You might notice that the central texel is covered by all 4 samples, the middles edges by 2 samples each and the outer corner by only one sample each. This gives the central texel 4x the weight of the outer samples. This actually somewhat matches what we’d expect with a Gaussian blur, and we get it for free.

Note: if you need each sample to have equal weight, I believe an offset values of ±sqrt(0.5) would do the trick. Tweaking the offset value, gives you control over the interpolation blending, which can give you some control over the texel weights.

Mobile devices (and Nintendo Switch) really with shaders that use a lot of texture samples, so this method, works well if you repeat it recursively. But if you need to blur a large area, 3x3 blurs would take many passes. We can do a little better.

Continue reading this post for free, courtesy of Xor.