---
title: 'Mini: Optimization'
url: https://mini.gmshaders.com/p/gm-shaders-mini-optimization-1497479
author: Xor
published: '2022-12-10'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Optimization

### How to optimize your shaders

Good day,

Let's go over some general shader tricks that can help you write more efficient code! I've actually [written about this ](https://gmshaders.com/tutorials/tips_and_tricks/)before, however, I believe this topic deserves a whole tutorial for itself.

Time to dig in!

## Misconceptions

First, I want to mention some common optimization misconceptions. If statements are not bad! In fact, in many cases, they are faster than the alternatives. I often see code like this used to avoid a conditional operation:

`return mix(A, B, step(x,y));`


When a ternary operator or if statement would work just fine.

`return (x > y) ? A : B;`


Modern hardware and modern compilers are extremely efficient when it comes to handling if statements. The vast majority of the time, our if statement alternatives end up involving extra operations, so they shouldn't be considered necessary. There are some specific edge cases (involving threads and warps) where if-statements can be slow, but it's a bit too complicated to cover here. As a general rule, though you want to minimize the difference in processing across pixels. If every pixel is doing a completely different process than its neighbors, it's no longer using the full parallel power of the GPU. Think parallel!

## Look Up Textures

A simple trick that you can use in many shaders: "LUTs". So let's say you have an expensive noise function. Instead of calculating it in real-time for every pixel, you could compute it once on a texture (add tiling if necessary) and use this texture instead of your noise function!

You may remember LUTs from the [Colors Extended tutorial](https://gmshaders.com/tutorials/colors_extended/), which showed how they can be used to apply any complex color grading operations to any color.

These can also be used to simplify complex math operations. It's a good idea to think about pre-computing any expensive processes that are repeated across many pixels.

LUTs also have the added bonus of being editable by hand!

You'll have to experiment to make sure the LUT is indeed faster. Find the correct balance with texture size, number of textures, number of samples, etc. There are many factors to consider, so it's best to try several options and see how it affects your results.

## Multipasses

Another powerful trick is to consider if parts of the shader can be pre-computed in a separate shader "pass". This means you run the shader on your object or texture and store that on a surface, then you apply a second shader on the surface for two shader passes. [I've written about this method in more detail here](https://www.getrevue.co/profile/xordev/issues/gm-shaders-mini-recursive-shaders-1308459).

Let me give a few examples to show how this can be used:

**Separable Box Blur**: In a box blur, you have to compute the average color of several pixels on a texture. Say you have a 9x9 blur. Instead of sampling 81 points for every fragment, you can sample 9 horizontally in one pass, and then sample the horizontally blurred image 9 times vertically. In the end, each pass only required 9 samples (18 total across both passes), but effectively computed the average of 81 samples!**Bloom**: Bloom typically has two parts. First, you isolate the glowing pixels, which are above a threshold brightness, then you apply the blur to the glowing pixels. This can be separated into 2 (or more for separable blur) stages, saving the GPU from extra work applied to every single pixel.**Outlines**:Typically, outline shaders are a lot like blur shaders. You sample the neighboring pixels, and if any one of them has an alpha value above some threshold (and the current pixel is not), you set it to the outline color. However, just like the blur shader, it can be split into multiple passes so that it can produce the same results in fewer samples.**Floodfill**: There are plenty of flood fill algorithms out there, and they are all multipass!

## Shader Stages

Another important factor to consider is shader stages. I'm talking about vertex and pixel shaders. It's a good idea to think about where your calculations are happening. Make sure you are not calculating things more often than necessary. If you're computing something like lighting for every pixel, it may be possible to move the calculations to a vertex shader.

This can make a big difference in the efficiency of your code!

## Expressions

Expressions like ** float PHI = (sqrt(5.0) + 1.0) / 2.0,** do not have much performance cost because the compiler recognizes the constant value and pre-computes it. Expressions with variable factors cannot be pre-computed, but you still don't have to worry about stuff like:

`x / `


`pow`

`(256.0, 3.0)`

because the division part can be simplified and pre-computed.These sorts of expressions do not have much of an impact, however, for-loops could. Obviously, you'll want to keep the loop size as low as possible, but it can also help to break a loop early using `break`

.

On low-end devices, lower precision qualifiers make a big difference. Use lowp for colors, mediump for uvs, and highp for positions.

## Conclusion

So to summarize, don't avoid conditionals, pre-compute as much as possible using LUTs, vertex shaders, or even uniforms. I know when I began learning about shader optimization, I was confused about where to start. I heard a lot of conflicting information about if-statements, but after years of experience, hopefully, this will save you some of the trouble!

Thanks for reading. Enjoy your night!