---
title: 'Functions: Dot Product'
url: https://mini.gmshaders.com/p/gm-shaders-mini-the-dot-product-1329407
author: Xor
published: '2022-09-03'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Functions: Dot Product

### An introduction to vector dot products

Good day,

Today we're going to talk about the vector "dot product"; what it is and its many uses in shaders. Once you learn all the ways it can be used, you won't look back!

## What is dot(a, b)?

A dot product is a function that takes in two vectors and returns a scalar (float). It is computed like so:

```
float dot(vec a, vec b)
{
return a[0]*b[0] + a[1]*b[1] ...a[n]*b[n];
}
```



So, in practice for vec2s, the dot product is computed like this:

```
float dot(vec2 a, vec2 b)
{
return a.x*b.x + a.y*b.y;
}
```



Now you're probably wondering what this might be useful for. Great, let's talk about it!

## The Math

For my Trigonometry fans, this can be thought of as a cheap way of computing this:

`dot(a, b) == length(a) * length(b) * cos(theta)`



Where 'theta' is the angle between 'a' and 'b'. Shaders don't compute them this way, but it can be a useful insight if you're working with trig functions.

Here's a diagram:

For the non-trig fans, basically, all you need to know here is that cosine ("cos") will be 1.0 if 'a' and 'b' are facing the same direction, 0.0 if they're perpendicular, -1.0 if opposite, and every value in between.

That means if `length(a) == 1.0`

and `length(b) == 2.0`

, then we know that `dot(a, b)`

will range between -2.0 and +2.0 depending on the vectors' alignment.

It's a little hard to visualize, so let's clear it up with some real examples:

The first example is computing a color's grayscale value, but we already covered that [here](https://gmshaders.com/tutorials/basic_colors/#grayscale).

## Stripes

Suppose you want to make an object stripy. You would probably do something like this:

`stripe = mod(floor(position.x), 2.0);`



This will return 0.0 for all even x-positions and 1.0 for odd values.

But what if you want the stripes along a diagonal direction?

This is where dot products can come in handy:

`stripe = mod(floor(dot(position, direction), 2.0);`



Here's the result when the direction is vec3(1.0, 1.0, 1.0).

**Note:** The length of 'direction' is important here. If the length is 1.0, the stripes will appear every 1 unit, but a length of 2 increases the frequency by 2, making it appear every 1/2 unit.

## Attenuation

You might know that light attenuates inversely proportional to the square of the distance to the source. That means that 2 units away is 1/4 the intensity of 1 unit away. This can be cheaply calculated with dot!

Suppose 'a' is the distance from the surface to the light source:

`attenuation = 1.0 / dot(a, a);`



If you think about it, this makes sense from our definitions above. `dot(a, a)`

is computed as `a.x*a.x + a.y*a.y`

, which is just the Pythagorean Theorem.

## Lambertian Lighting

[This is how](https://en.wikipedia.org/wiki/Lambertian_reflectance) lighting is typically computed in games. You simply get the dot product of the surface's normal and the normalized direction toward the light.

This returns a value between +1.0 and -1.0, depending on how aligned they are. Values less than 0.0 mean the normal is not facing the light and can be ignored.

## Conclusion

Dot products show up everywhere. They're used for colors, coordinates, and lighting, and they are extremely helpful to understand before approaching matrices and rotation math.

Hopefully, this tutorial sparked some interesting ideas and helped you understand the power of the dot.

Thanks for reading and have a great night!

Lovely explanation!

Great!