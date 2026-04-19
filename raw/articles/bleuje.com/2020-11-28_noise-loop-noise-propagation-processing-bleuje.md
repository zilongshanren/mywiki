---
title: Noise loop / noise propagation (Processing) - bleuje
url: https://bleuje.com/tutorial3/
published: '2020-11-28'
source_blog: bleuje
source_site: https://bleuje.com/
category: graphics
fetched: '2026-04-19'
---

This tutorial explains how to loop a value with noise, and then a perfect loop technique that’s similar to periodic function propagation from the [previous tutorial](https://bleuje.com/tutorial2/) but using noise and more advanced technique. I call it “noise propagation”, and it was used to make that animation:

![radial 4d noise propagation](../../assets/6508c8e9ccc07c44.gif)


First of all if you’re not familiar with noise in creative coding you can for example learn about it on the Coding Train ([video about Perlin Noise](https://www.youtube.com/watch?v=Qf4dIN99e2w&list=PLRqwX-V7Uu6bgPNQAdxQZpJuJCjeOr7VD), [video about openSimplexNoise](https://youtu.be/Lv9gyZZJPE0) ).

OpenSimplex noise in Java by Kurt Spencer is used. It has better quality than Processing’s Perlin noise (but different aesthetic) and 4D implementation that will be useful here.

To use it you can paste the code [from here](https://gist.github.com/Bleuje/fce86ef35b66c4a2b6a469b27163591e) in a Processing tab of your sketch. The reason I give this reupload from me of the code and not the original code is that I made few changes so that you can just paste it in a tab. Otherwise you need the tab to be a .java I think.

To use OpenSimplex noise in our sketch we can do this:

Here the noise seed is at 12345, you can use what you want.

OpenSimplex noise implements noise in 2D, 3D and 4D, but 1D can be obtained simply by fixing the value in another dimension:

## Noise loop technique

We want to use noise to get a smooth random periodic function. This can be obtained with a circle in 2D noise:

In the following picture 2D noise is visualized with brightness and the path of a circle is drawn: this is where we take our values to get a periodic function.

![2d noise circle](../../assets/1a1bb9fe99cd4734.png)


The values of the periodic function we obtain can look like this:

![noisy periodic function](../../assets/2ac7d97df87a7a2f.png)


The larger the radius of the circle, the more variation within one period we will have.

So here is an implementation of noisy periodic function, we fix the radius at 1.3.

Looping values with a noise circle like this is already useful: for example if you want small dots that look like shiny stars you can use this to change the size of dots and get a perfect loop.

The rest of this tutorial is about making something more interesting, it shows how to make the animation shown at the beginning, using a “noise propagation technique”. It’s more advanced and not really useful to understand in general. So you can skip to the [next tutorial](https://bleuje.com/tutorial4/) (which is more simple and important) especially if “4D noise” sounds scary to you.

## Noise propagation technique

To sum up the “noise propagation” technique, these things are added to the previous tutorial’s technique:

- using noise to get a smooth periodic function
- using more dimensions of noise to get variation through space

We’re going to displace small transparent dots with it. There will be horizontal and vertical displacement for each dot, so we’re going to need two independant noise values. One way to solve this problem is to have two instances of OpenSimplexNoise, for example noise1 and noise2, constructed from different seeds. I don’t do this: I simply take values from a single noise instance far away from each other for things that I want independant.

So we can rewrite our noisy periodic function like this:

Here is the code to draw all transparent dots and animate them similarly to the [previous tutorial](https://bleuje.com/tutorial2/):

We take a radial offset function:

That gives us something like this (the entire code is given later):

![radial 4d noise propagation](../../assets/e646e3b43afbed8c.gif)


So far we used 2D noise in our periodic function. We can use the two remaining dimensions to smoothly and randomly change the periodic function through 2D space.

Therefore it becomes:

`scl`

stands for “scale”: when one increases this parameter one increases variations.

Here is the entire code to generate the gif frames:

And the result was shown at the beginning of the tutorial.

![radial 4d noise propagation](../../assets/6508c8e9ccc07c44.gif)


You can play with all sorts of offsets, this applies to 3D stuff and the value of the periodic function can be used for something else than displacement.

To be honest I don’t use this precise noise propagation technique very often but this tutorial covers basic things about noise use and it’s worth explaining in my opinion: if I had just made a tutorial about looping values with noise you may wonder about how to get some more structured motion.

Thanks for reading, I hope you learned something or found this interesting!

update: a better opensimplex noise version is available [here](https://github.com/KdotJPG/OpenSimplex2), sorry to have used the old one for so long. This tutorial might be changed one day with it. It has for example faster 4D noise.