---
title: Various noise functions
url: https://gametorrahod.com/various-noise-functions/
author: Sirawat Pitaksarit
published: '2018-10-27'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

They are all generated using Unity.Mathematics library. But the general definition could be applied elsewhere.

**Unity-Technologies/Unity.Mathematics***A prototype of a C# math library providing vector types and math functions with a shader like syntax …*[github.com](https://github.com/Unity-Technologies/Unity.Mathematics)

## cnoise

cnoise is a classic perlin noise. It works by assigning random gradients on a grid and set that exact point as a middle value like 0.5. These points are called lattice points.

If your input landed exactly at those gradient point you get 0.5, but at any other points in between it will try to “slide” according to surrounding gradients. Because those gradient were randomized you will get interesting patterns that appears to oscillate back and forth around 0.5

![](../../assets/41a3f432854452db.png)

This image is a 500x500 texture from 0.0f ~ 5.0f input to cnoise . For example at pixel 150x200 it would be an input new float2(1.5f, 2.0f) to the noise function. I tried checking on the integer coordinate and the result is always 0.

That means Unity used each integer as a lattice point + middle value is 0 instead of 0.5. Meaning that output would be -1.0 ~ 1.0 and not 0.0 ~ 1.0. So, I used math.unlerp(-1,1, value) to map back to 0~1 to be able to paint it black to white.

Look closely you can see Unity editor’s grid. This is exactly 10x10 grid and we have 0.0 ~ 5.0f mapped, at the grid points like (0,0) (0,2) (0,4) (0,6) (1,6) (5,0) the color is exactly middle grey. Also look at 4 corners, it is obviously 0.5 grey.

![](../../assets/c549354513de49dc.png)

Using this as a base you can create things that resembles nature like clouds, water texture, stone marble, random but not that random movement/brownian movement. Better than using a naive random noise. (That would look like a television with wrong tuning)

## snoise

Stands for simplex noise, which improves on the original perlin noise by using a different space filling grid that is not a simple square. (A squashed rhombus or something) Also better performance-wise because it optimized the function that average the gradients but I think Unity’s version of cnoise should have already integrated those optimizations?

Plot it using the same procedure you see that it is “less directional”. (the previous version had overall perfect vertical and horizontal appearance)

![](../../assets/1c020680b2b3a14e.png)

To see better I have truncated the minus part of the output to improve the contrast. Left : cnoise Right : snoise

![](../../assets/38660cca4d866db7.png)

![](../../assets/382f618eeb9a0a6a.png)

## cellular

Stands for Cellular Noise or Worley Noise. The algorithm generates a pattern that looks like irregularity of a cell. Is this mean we have won against nature by being able to compute it!? (jk)

**Worley noise - Wikipedia***Worley noise is a noise function introduced by Steven Worley in 1996. In computer graphics it is used to create…*[en.wikipedia.org](https://en.wikipedia.org/wiki/Worley_noise)

**Cellular noise - Wikipedia***Cellular noise is random variability in quantities arising in cellular biology. For example, cells which are…*[en.wikipedia.org](https://en.wikipedia.org/wiki/Cellular_noise)

### F1

This time the return value is a float2 but not really x in y in cartesian coordinate sense. The x is called F1, a distance to the nearest (1) “nucleus” (feature point).

![](../../assets/ce38cf10bca48eff.png)

Being based on “nearest” meaning that at some point where you vary your coordinate smoothly it would abruptly switch over to the other nucleus giving a segmented impression.

### Optimization

The image had the returned value directly mapped to black — white and it looked quite ok, so I assume this time x is in the range of 0~1 ?

The original paper states that we could make a unit cube sized at integer position then use Poisson distribution where we could control the mean density, to see how many points that should be in this cube. (with some clamping, etc) Then for 2D cellular we slice a 2D plane out of the cube.

But this exact implementation that Unity took from stegu is following this paper :

It is this code

**stegu/webgl-noise***GLSL procedural noise functions compatible with WebGL - stegu/webgl-noise*[github.com](https://github.com/stegu/webgl-noise/blob/master/src/cellular2D.glsl)

Which looks like, we get a fixed 1 feature point per integer grid (not cube). See these box I sampled. Exactly 1 feature point is in there.

![](../../assets/025fc5fba8055bd3.png)

### F2

F2 simply means instead of the nearest we go for the distance to the 2nd nearest instead. It is stored in y. Visually this is always brighter than the previous F because obviously it is further away. Artistically it looked quite like ice crystals. Also, we no longer see obviously where is the feature point which is a part that make it looks cool.

![](../../assets/87b1412601a8758c.png)

By definition we could go for F3, F4, … but Unity only returns 2 level of result. And the paper states that we can compute every F at the same time with no additional cost.

## cellular2x2

Speed up version with a shortcut in searching for the nearest feature point. Instead of 3x3 search we use a smaller 2x2 area. It makes F2 useless (because it is not large enough to find the 2nd nearest which could be 2 integer grids away?) and F1 less ideal.

![](../../assets/cb70d1eb9acf7615.png)

![](../../assets/2cdf067c0755a1bf.png)

From the look of F2, it means if you are only going to input 0.0~1.0 F2 is kinda usable.

cellular3D takes 3D input and its faster version is cellular2x2x2 .

## psrdnoise2D

This is a simplex noise with additional features :

- d = Returns a derivative too. The return value is now float3 instead of float , which I guess the y and z is the 2D partial derivative (that is a gradient). Meaning that if you grab the y and z and make it a new float2(y,z) then that is a unit vector describing a slope at that point. Could be useful to know not just the value but also the direction where it is going?
- p =Periodic (you can tile it)
- r = Rotating gradient (apply more rotation to all randomized gradients manually)

### Periodic

I used psrnoise here because I don’t want the D.. The period argument is float2 , I tried new float2(3,0) and you see that it loops after going over input x = 3. It does not loop vertically because I put 0 in there. (You could also use just pnoise , if you want a periodic version of cnoise )

![](../../assets/63c3b68dcacda916.png)

Interesting idea with small y and x = 2

![](../../assets/d38955e6d6141dc9.png)

### Rotating gradient

Each step is math.PI/25 . Remeber that the lattice point stays at the same spot. It gives an impression of patterns circling around some reference point. (This is with periodic new float2(2,2) )

![](../../assets/c2bb7c003cf2c460.gif)

Awesome learning material about noises :

**The Book of Shaders***It's time for a break! We've been playing with random functions that look like TV white noise, our head is still…*[thebookofshaders.com](https://thebookofshaders.com/11/)