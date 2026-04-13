---
title: Analytic Fog Rendering With Volumetric Primitives
url: https://matejlou.blog/2025/02/11/analytic-fog-rendering-with-volumetric-primitives/
author: Matejlou
published: '2025-02-11'
source_blog: matejlou.blog
source_site: https://matejlou.blog
category: Graphics Programming Weekly — Jendrik Illner → linked
fetched: '2026-04-13'
---

In this post I’m going to cover a neat technique for rendering regions of fog with varying density. I’ll start by covering some of the basic principles behind fog rendering and a few common solutions before describing the technique itself. There will be a bit of maths involved – you’ve been warned!

## A Brief Review of Fog Rendering

For those unfamiliar, rendering fog boils down to simulating the behaviour of light as it passes through a medium. The simplest behaviour we can model and the one we’re going to focus on is *absorption*, or the loss of light energy. In basic terms, the more ‘stuff’ that light has to pass through, the more energy it loses.

![](../../assets/c69cf7fb7e541470.png)

The ratio of outgoing light to incoming light after a given ray passes through a medium is called the [transmittance](https://en.wikipedia.org/wiki/Transmittance), its value defined as:


Where is the amount of light entering the medium and

is the amount coming out. The relationship between the density of the medium and transmittance is described by the

[Beer-Lambert Law](https://en.wikipedia.org/wiki/Beer–Lambert_law). The equation is:

Where is the total density encountered by the light path going through the medium. Once we have the transmittance, we can just multiply it by

to find out how much outgoing light reaches us through the ray. If the medium is just an area of constant density

, then

simply evaluates to the length

of the portion of the light ray passing through the medium times the density:


This is more or less the approach the approach used to render simple [distance fog](https://en.wikipedia.org/wiki/Distance_fog) in games. Sometimes the Beer-Lambert Law is foregone completely and just the total density along the ray is used to fade objects in the distance. Either way this approach not only assumes a medium of constant density, but that the medium itself covers the entire viewable area.


![](../../assets/23c49ad6c76f4c7c.png)

By constraining our medium within a bounded region we can give ourselves a bit more flexibility on the appearance of fog within a scene. The simplest approach is to use primitives such as planes, spheres or boxes as bounding volumes. By determining the intersection of our view ray with these primitives we can find the length of the ray through the volume and calculate the total density using the same formula, once again assuming a constant density within the entire primitive.


![](../../assets/8dc4a1c8cb9ec5cf.png)

I won’t cover ray-primitive intersection here as it’s beyond the scope of this post and there are loads of resources describing efficient algorithms to do this already. [Inigo Quilez](https://iquilezles.org/) has a number of great examples on how to implement these on his website.

## Heterogenous Volumes

In reality it’s rare that we can take a medium’s density as constant throughout its entire area, especially when it comes to clouds or smoke. When a medium has a non-constant density we say that it is *heterogenous*. A greater range of effects can be simulated if we take this into account when rendering. Unfortunately this can complicate the equation quite a bit. Now is no longer a simple product but an integral over the light ray:


Here, and

are the start and end points of the portion of the ray passing through the bounding volume, respectively. The function

describes the density of the medium at a given point in space

. Because not all functions have a closed-form solution for their integral, we often resort to numerical methods to evaluate it, i.e. moving along the ray in small steps and adding up the area of rectangular ‘slices’ of density along the way.


![](../../assets/5ed3ecef60292576.png)

This is effectively what ray-marching does and is pretty much the bread and butter of modern volume rendering. It’s extremely flexible – we don’t care what the density function is, and in fact we may not even *know* what it is, but as long as we can sample it at arbitrary points (e.g. via a volume texture) we can numerically evaluate the integral.

![](../../assets/d66a379bba06e253.png)

Ray-marching does have its drawbacks however, most notably in the form of [aliasing](https://en.wikipedia.org/wiki/Aliasing) as a result of using too few samples to approximate the integral. While analytic solutions are less flexible, they will never alias and are often faster to compute, which is good motivation for finding analytic expressions for different types of media.

## Radial Functions

A function that depends on the distance of some point relative to the origin can be considered a

[radial function](https://en.wikipedia.org/wiki/Kernel_(statistics)). These are nice as they’re often simple to work with and let us define volumes where the density varies over a region. By combining many of these radial density functions we can create more complex fog- or smoke-like effects.

![](../../assets/2bf6b1da34288966.png)

Getting the integral along a line segment is not too difficult for simple functions. Recall that a radial function is dependent on the distance of a point to the centre, which for the sake of simplicity we’ll take to be the point at zero. So the distance is simply:


The equation for a point on a ray with origin and direction

at a distance

is given by:


So the distance to any point along the ray can be expressed as:

Where:

For a given radial function we can rewrite it in terms of to get a new function that we can (hopefully) integrate. For a more intuitive visual understanding, consider the new function as one that describes the change in density through a

*cross-section* of the original function.

![](../../assets/66f72767588b8442.png)

We can apply linear transformations to the ray origin and direction

to place arbitrary scaled and rotated volumes anywhere in space without having to change any of the following calculations. This is done by multiplying the ray equation by a transformation matrix

in the following way, yielding the transformed ray origin and direction

and

:


All that’s left is to find the [antiderivative](https://en.wikipedia.org/wiki/Antiderivative#:~:text=In%20calculus%2C%20an%20antiderivative%2C%20inverse,symbolically%20as%20F'%20%3D%20f.) of our new function and evaluate it at the limits corresponding to the start and end of the ray. If is the antiderivative of

, then:


However, it’s possible that we run into issues with numerical precision when the ray origin is far away from the primitive. We can fix this by moving to the beginning of the interval at

, then setting new limits at 0 and

, reducing the equation to:


Now I’m going to go through a few radial functions and find the antiderivative of the density along a given ray. You know – for fun!

## Linear Density

This function corresponds to a [triangular function](https://en.wikipedia.org/wiki/Triangular_function) in 1D or a cone in 2D. It’s described by the following equation:

![](../../assets/0fef5575d2d28635.png)

Using the same logic as above, we can define the function for the density along an arbitrary cross-section, which we’ll call :


To find the antiderivative start by pulling out the constant

and completing the square:


Then by setting:

We can use the following identity:

Which gives us the final equation, still using and

for brevity:


It might be a good idea to add a small offset to the value inside the logarithm, avoiding precision errors near 0. Here’s what all that looks like in code:

```
float antiderivativeLinear(float a, float b, float c, float t)
{
float u = t + b / a;
float v = (b * b - a * c) / (a * a);
float radical = sqrt(u * u + v);
return t - sqrt(a) * (u * radical - v * log(0.001f + u + radical)) / 2.0f;
}
```

## Quadratic Density

This function resembles a [parabola](https://en.wikipedia.org/wiki/Parabola) and is described by:

![](../../assets/3930abaa65429edb.png)

Its cross-section along a ray is given by:

Which is nice because we don’t have to deal with any square roots. The equation is a quadratic polynomial in and the antiderivative is easy to solve for:


```
float antiderivativeQuadratic(float a, float b, float c, float t)
{
return t * (t * (t * a / -3.0f - b) - c + 1.0f);
}
```

## Quartic Density

This function is given by:

![](../../assets/97f8c3f02d98295b.png)

And its cross-section along a ray is:

This function is particularly nice because its derivative is zero at the boundaries, similar to [smoothstep](https://en.wikipedia.org/wiki/Smoothstep). The cross-section is a quartic polynomial in t, and the antiderivative is also easy to find:

```
float antiderivativeQuartic(float a, float b, float c, float t)
{
return
t * (t * (t * (t * (a * a * t / 5.0f + a * b) +
(2.0f * b * b + a * c - a) * 2.0f / 3.0f) +
(b * c - b) * 2.0f) + (c * c - 2.0f * c + 1.0f));
}
```

## Spiky Density

This is a density function which peaks sharply in the centre and falls off smoothly to zero at the boundaries. It’s defined as:

![](../../assets/184a44d95ed9d9fc.png)

It’s cross-section is given by:

To find the antiderivative, start by expanding out the brackets:

We can deal with the term the same way we did with the linear density function. The rest of the terms are straightforward. This gives us:


Where once again:

```
float antiderivativeSpiky(float a, float b, float c, float t)
{
float u = t + b / a;
float v = (b * b - a * c) / (a * a);
float radical = sqrt(u * u - v);
return
t * (t * (t * a / 3.0f + b) + c + 1.0f) -
sqrt(a) * (u * radical - v * log(0.001f + u + radical));
}
```

## Gaussian Density

This is the well-known [Gaussian](https://en.wikipedia.org/wiki/Gaussian_function) function, defined as:

![](../../assets/b80403b2a52c6248.png)

It’s cross-section along a ray is:

To find the antiderivative we need to use a function known as the [error function](https://en.wikipedia.org/wiki/Error_function), defined as:

To start, we can complete the square in the exponent, which lets us pull out some constant terms from the main integral:

Now we’ll rearrange the exponent so that it’s in the form :


Which lets us use the following substitution:

Yielding:

And after substituting back into our original equation, we arrive at the following solution:

The Gaussian is the only function we’ve covered that doesn’t fall to 0 when , rather it approaches 0 as

goes to infinity. In practice it’s often enough to scale

and

by a constant factor until the discontinuity isn’t noticeable.


```
// Approximation of erf.
float erf(z)
{
float az = abs(z);
return
sign(z) * (1.0f - 1.0f / pow(1.0f + az * (0.278393f + az *
(0.230389f + az * (0.000972f + az * 0.078108f))), 4.0f));
}
float antiderivativeGaussian(float a, float b, float c, float t)
{
float sqrtA = sqrt(a);
return sqrt(PI) * exp(b * b / a - c) * erf((a * t + b) / sqrtA) / (2.0f * sqrtA);
}
```

## Extra Stuff

One thing I’ve left out is how to make these volumes respond convincingly to light and shadow. Unfortunately the full equation describing this physical behaviour is too complex to solve analytically. However, a quick hack is to apply a very simple shading model to each individual primitive in the hopes that, as a whole, the medium appears to react to light as we expect it to.

![](../../assets/01fb0c4f352cff98.png)

Representing fog as a collection of primitives opens up some neat possibilities as well. For example, it shouldn’t be too hard to hook these primitives up to a particle system to achieve dynamic or animated fog effects. If we want to be clever we can also use [boolean operations](https://en.wikipedia.org/wiki/Constructive_solid_geometry) to create more complex bounding volumes. This could be used to produce a simple [fog of war](https://en.wikipedia.org/wiki/Fog_of_war#Simulations_and_games) effect for instance.

![](../../assets/d704f7e63a187529.png)

I hope you’ve found this technique interesting and find some potential uses for it in your projects. If you’d like a visualisation of all these density functions along with their source code, please take a look at this [Shadertoy](https://www.shadertoy.com/view/lX3cz8) implementation I put together. Thanks for reading!

## 1 Comment