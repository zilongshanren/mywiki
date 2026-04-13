---
title: Blur Philosophy
url: https://mini.gmshaders.com/p/blur-philosophy
author: Xor
published: '2024-02-17'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Blur Philosophy

### How to write a better blur shader

Hello,

Today is all about blur shaders. There are many different types like radial, box, Gaussian, linear, disk, twist and more. They all have something in common. Sampling the texture at multiple points and averaging the results. Within that general guideline, there are things you should do and things you should avoid.


I was originally going to make this the first draft only tutorial for free subscribers, but this tutorial is too important, and I need as many people as possible to see it so that I can correct the record. My old “Gaussian” shader is used all over the place (I've seen it on ShaderToy, Godot, Construct and other places) and I need to correct some of the mistakes I’ve made. This is just an introduction to blur shaders, and subsequent tutorials may be released as drafts. Okay, let’s begin.

# How do blur shaders work?

Probably the first blur shader you’ll write is a box blur. It typically looks something like this:

```
//Texture color sum and weight sum for computing the average color
vec4 tex_sum = vec4(0);
float weight_sum = 0.0;
//Loop through desired texel "range"
for(int x = -range; x<=range; x++)
for(int y = -range; y<=range; y++)
{
//Sample texture at given texel and add to sums
//mini.gmshaders.com/p/gm-shaders-mini-texels-and-pixels-1308242
tex_sum += texture2D(gm_BaseTexture, v_vTexcoord + vec2(x,y) * texel);
weight_sum += 1.0;
}
//Compute average
vec4 tex_average = tex_sum / weight_sum;
```


This is fine for a placeholder, but there are some caveats to consider. Firstly, when you increase the blur range, it dramatically slows down.

# Sample count

Why? Well, a range of 1 means the shader is sampling texels -1, 0 and +1 on both axes. So 3 * 3, or 9 samples. If you bump the range up to 2, you’re doing 5*5 or 25 samples! For most applications, I wouldn’t recommend going above 25 samples, unless you know you’re working with decent hardware (no mobile devices or Nintendo Switch).

The next thing to consider, is appearance. Box blurs create “boxy” looking shapes (bit like texture interpolation). It can be really obvious on shapes with distinct edges, like this white square:


Here’s [my ShaderToy demo](https://www.shadertoy.com/view/432GRh).


Gaussian distribution

You’ve probably heard of Gaussian blurs because they’re everywhere, but you might not know why. And what does this fancy formula mean?

Instead of going through the trouble of explaining this formula, let’s look at how it emerges in blurring. The bottom two blurry boxes above, are actually just box blurs repeating two and three times. The more times you iterate, the closer it approximates Gaussian/normal distribution. So this is why we care about Gaussian blurs. [This distribution](https://en.wikipedia.org/wiki/Normal_distribution) occurs in the world all the time from SAT scores, human heights, financial markets to dice rolls. That means if we use a Gaussian blur, we get a smoother, more natural looking blur.

So now that we know why Gaussian is preferred, here’s the formula in GLSL:

```
//Gaussian distribution formula
//x - vector relative to mean
//sigma - range of the distribution
float gaussian(vec2 x, float sigma)
{
return 0.3989423*exp(-0.5*dot(x,x)/(sigma*sigma)) / sigma;
}
```


Here’s a [ShaderToy example](https://www.shadertoy.com/view/XdfGDH) of normal distribution in action.

So in our case, “x” is how far we are from our center texel (0,0). (1,0) is 1 texel away and (0, 2) would be 2. “Sigma” controls for the range of the distribution, with higher values producing softer results closer to box blur and smaller values producing a sharper fall off. Your sigma value will depend on the range and your desired look, but I’d start somewhere around 5 to 8. We could use this as our weight, our box blur like:

```
float weight = gaussian(vec2(x,y), 6.0);
tex_sum += texture2D(gm_BaseTexture, v_vTexcoord + vec2(x,y) * texel) * weight;
weight_sum += weight;
```


This method is really expensive though and has some redundancies. It can be improved upon. The next step is to do some pre-computing.

# Kernels

The Gaussian formula is quite slow, with exp() and some divisions being computed for every sample. Instead of calculating the weights inside the shader, we can pre-compute a list of weights. These pre-computed weight lists are often called “kernels”.

Gaussian has two nice properties. It’s symmetrical and the gaussian of (x, y) is the same as the gaussian of (x, 0) times gaussian (0, y).

This means we can just store 1 axis of the weights and use it for both the x and y (or any number of dimensions).

Here’s a pre-computed list of 9 weights:

```
//Pre-computed Gaussian 9 weights (sigma 5), renormalized to sum to 1
float w[9];
w[0] = 0.080497596;
w[1] = 0.078903637;
w[2] = 0.074308647;
w[3] = 0.067237244;
w[4] = 0.058453252;
w[5] = 0.048824260;
w[6] = 0.039182387;
w[7] = 0.030211641;
w[8] = 0.022381334;
```


Here’s a horizontal blur example to show how it can make use of weight symmetry.

```
//Texture color sum and weight sum for computing the average color
vec4 tex_sum = texture2D(gm_BaseTexture, v_vTexcoord) * w[0];
float weight_sum = w[0];
//Loop through 8 texels both right and left
for(int x = 1; x<=8; x++)
{
//Sample in both directions for symmetry
tex_sum += texture2D(gm_BaseTexture, v_vTexcoord + vec2(x,0) * texel) * w[x];
tex_sum += texture2D(gm_BaseTexture, v_vTexcoord - vec2(x,0) * texel) * w[x];
weight_sum += w[x]*2.0;
}
//Compute average
vec4 tex_average = tex_sum / weight_sum;
```



Here we aren’t computing any Gaussian fanciness in the shader, but we pre-computed it instead. It works well when we already know how many samples we need. Outside the loop, we start with the center texel, because we don’t want to sample it twice, then in the loop, we sample to the right “x” units and to the left “x” units, with the same weight values for both.

# Separable blurs

The shader above used 17 (8 to the left, 1 in the middle and 8 to the right) samples for just one axis. If we wanted to do a box blur at this scale for both axes, that would require 17*17 or 289 samples, right? If you wanted to do it in one shader, yes. But you could also do a horizontal blur with 17 samples, draw that to a surface, and then draw that surface with a vertical blur for 17 samples.

Now you’ve broken that super costly process into very manageable pieces while still only sampling 17 texels at a time. This is a much better way to do a large scale Gaussian blur compared to where we started.

This seems like a good place to stop, and we’ll continue from here next time. There are some cases, where two pass blurring is not practical, but there are other solutions for that. We’re not even close to finishing our optimizations yet, but we’ve already come a long way from a simple box blur.

# Conclusion

The best place to start with blur shaders is the box blur. Not because it’s the most efficient, but because it’s the easiest to pick up. Box blurs can quickly get out of hand though and aren’t suitable for large scale blurring by themselves. It’s also can look quite unnatural with hard edges in some places, due to its “boxiness”.

The Gaussian blur improves the look of the shader, but computing its distribution in the shader, can add a lot of expense. We can approximate Gaussian blurs by repeating box blurs, but this can add complication with diminishing returns.

Pre-compute the weights is generally preferred, making use of the symmetry and axes separation. In most cases, separating the blur into horizontal and vertical passes will greatly improve performance and extending how far you can blur.

Here’s a quick overview of what is to come (we’ve covered the first two so far):

### Dos

**Separable blurs**: Break the shader into multiple passes if possible.**Pre-compute weights**: If you can, it’s a good idea to pre-compute sample weights (kernels) and sample points.**Use linear filtering**: Enable and utilize texture interpolation for smoother results with fewer samples.**Gamma correction**: You want to blur in linear color space, not sRGB.**Downscale**: Blur at a lower resolution when you can. Or jump in powers of 2.

### Avoid

**Lots of samples**: Texture sampling is expensive, especially on mobile devices. More passes are generally preferable over more samples.**Edges**: It can be difficult dealing with sprite/texture edges. Sometimes clamping, or texture wrapping is fine, other times you’ll want to pad your sprites.**Lots of surfaces**: Most of the time, two surfaces are enough for[ping-ponging](https://mini.gmshaders.com/p/gm-shaders-mini-recursive-shaders-1308459).**Avoid trig**:`cos()`

and`sin()`

are expensive. Try to keep complex calculations outside the for-loop.

# Extras

[The “Dual-Kawase” blur](https://github.com/XorDev/Dual-Kawase/wiki) is an efficient blur shader which makes use of downscaling and only a few texture samples for a high-quality Gaussian blur. It scales logarithmically, so doubling the blur radius adds only 2 blur passes.

Tero Hannula has had quite the month, releasing 3 powerful shader-based open source projects:

[TiteGPUMath](https://github.com/HannulaTero/TiteGpuMath) - utilizing the GPU to do bulk math (since we don’t yet have compute shaders)

[QuackCollision](https://github.com/HannulaTero/QuackCollision) - Collisions with quads (including particles, text) through some shader magic.

[JFA_rgba8unorm](https://github.com/HannulaTero/JFA_rgba8unorm) - How to do jump flooding with a standard 8-bit surface.

That’s it for this week. Until next time, take care!

-Xor