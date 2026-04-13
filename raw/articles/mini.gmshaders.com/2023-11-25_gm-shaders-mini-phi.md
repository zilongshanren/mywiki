---
title: 'GM Shaders Mini: Phi'
url: https://mini.gmshaders.com/p/phi
author: Xor
published: '2023-11-25'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Phi

### The mathematical constants for distributions

Hi!


Phi is 1.618… You may have heard of it as the [Golden Ratio](https://en.wikipedia.org/wiki/Golden_ratio) or the related Fibonacci sequence. For a long time, all I knew of the Golden Ratio was from seeing this spiral in various places, knowing it had something to do with sunflowers and how it was useful in design.

But Phi has a fascinating property; it is considered the “[most irrational number](https://math.stackexchange.com/questions/395938/why-is-varphi-called-the-most-irrational-number)”, meaning it’s the hardest number to approximate with ratios.

It wasn’t until just a few years ago, that I learned about its uses in evenly distributing points across rectangles, disks, spheres and elsewhere. This method allows you to make a one-pass rectangular blur with any arbitrary size and any with any number of texture samples. Other uses include disk sampling, encoding 2D position into a single index, encoding spherical coordinates (e.g. normals) and much more.

First, let’s look at

# Computing Phi

Phi is defined as the continued fraction 1+1 / (1+1 / (1+1 / (...))) which can be reduced to `(1.0 + sqrt(5.0)) / 2.0`

or my preference: `0.5+sqrt(1.25)`

. Floats only care about the first 6 to 7 digits, so you can also safely use 1.618034 as a good enough approximation and save some computation. I like to store my precomputed constants in macros at the top of my shaders, like so:

```
#define PHI 1.618034
#define TAU 6.283185
```


*Note: If you're doing this outside of GLSL 1.0, and you have support for double-precision, then you may want to use a more precise approximation like 1.618033988749.*

Try computing 1 / 1.618. The answer you get is 0.618… That’s because 1/φ = φ-1!

In the next example, you can try replacing Phi with 0.618034 and see if it makes any difference.

# Rectangle Distribution

Let’s say you need to blur with a rectangular kernel with width “w”, height “h” and number of samples “n”. The simplest way would be start in the bottom-left corner and loop to the top-right corner:

```
for(float i = 0.0; i<n; i++)
{
//i/n gives use a value between 0 and 1
//We can multiply this by our new range
vec2 pos = vec2(i/n, i/n) * vec2(w,h);
//Do stuff with this position
}
```


Here’s a visual of what that looks like:

While this does fill the full range from (0,0) to (w, h) this doesn’t do a good job of filling the space.

Instead, we could try multiplying the y-axis by some odd ratio and have it wrap around with `fract()`

. Here’s what 0.3 looks like:

`vec2 pos = vec2(i/n, fract(i*0.3)) * vec2(w,h);`



I think you can guess where this is going. Use Phi here.

`vec2 pos = vec2(i/n, fract(i*PHI)) * vec2(w, h);`


Now [watch](https://twigl.app?ol=true&ss=-Nk7ZdAI_3TlKmhsputz) what happens when you change the size and number of points.

No matter where you pause the video, the distribution looks good.

I’ve put together a little [ShaderToy rectangle blur demo](https://www.shadertoy.com/view/ctdBRn) to show how this might look in practice.

# Golden Angle

The same principles can be applied to a disk. These are sometimes called Fibonacci Disks or Vogel Disks. Instead of using the Golden Ratio, we need the [Golden Angle](https://en.wikipedia.org/wiki/Golden_angle).

Computed as 𝜏*(2-φ) or 2.399963229728… radians.

```
//Golden Angle, Tau*(2-Phi)
#define G_A 2.399963
//Half pi, Tau/4.0
#define HPI 1.570796
```


You can compute the direction vector, using “i” like so:

```
//Sample direction vector
vec2 dir = cos(i *
````G_A `

+ vec2(0, `HPI`

));


Remember, `sin()`

is just `cos()`

with a half-pi offset, so we can compute the direction vec2 using just one cosine.

So for the radius, we need to divide the sample index, “i”, by the number of points, “n”, to get a value that ranges from 0 to 1. Put that in a square root and multiply it by your desired radius, “r”:

```
//Sample radius
float rad = sqrt(i/n) * r;
```


The square root is important here. Without it, you get too many samples towards the center:


This makes sense when you think about it. When you double (2x) the radius, the area that the points must cover, quadruples (4x). Putting it all together, you should get something like this:

```
//Golden Angle, Tau*(2-Phi)
#define G_A 2.399963
//Half pi, Tau/4.0
#define HPI 1.570796
for(float i = 0.0; i<n; i++)
{
//i/n gives use a value between 0 and 1
//We can multiply this by our new range
vec2 pos = cos(i * G_A + vec2(0, HPI)) * sqrt(i/n) * r;
//Do stuff with this position
}
```


And here’s what it looks like [in action](https://twigl.app?ol=true&ss=-Nk7hrwWCRwm51SlXnbS)!

I’ve also put together a disk blur example on [ShaderToy](https://www.shadertoy.com/view/dttBR8).

# Conclusion

Phi and the Golden Angle do in fact live up to the hype. It’s like the magic formula for breaking, splitting one value into two with minimal repetition. If you need an x and y, an angle and a radius, or [even two angles in 3D](https://www.shadertoy.com/view/7tVSDh), the Golden Ratio and Golden Angle has your back.

If you get extra creative, you can even use it to merge a vec2 back to a float, perhaps for bitpacking or some time of encoding. The possibilities are numerous, and I hope you can find other ways I haven’t thought of to use this. If you do, let me know. I think there’s a lot of hidden potential here.

# Extras

If you’re here, you probably know a good deal about shaders already, but perhaps you want to show others how they can start? If so, Dragonite has a solid introductory video tutorial for them!

SimonDev, a graphics YouTuber has a good course on shaders and on math, which are currently on sale for 50% off: [simondev.teachable.com](https://simondev.teachable.com)

KeeVeeGames [released a great GML library](https://github.com/KeeVeeGames/OKColor.gml) on a more color accurate way to blend colors! I’ll be writing about this topic in detail soon, so it may be good to get a head start there.

That’s it for this week!

Thanks again for reading. Have a good one!