---
title: Superfast void-and-cluster Blue Noise in Python (Numpy/Jax)
url: https://bartwronski.com/2021/04/21/superfast-void-and-cluster-blue-noise-in-python-numpy-jax/
published: '2021-04-21'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

This is a super short blog post to accompany [this Colab notebook](https://colab.research.google.com/github/bartwronski/BlogPostsExtraMaterial/blob/master/Jax_Void_and_cluster.ipynb).

It’s not an official part of my [dithering / Blue Noise post series](https://bartwronski.com/2016/10/30/dithering-in-games-mini-series/), but thematically fits it well and be sure to check it out for some motivation why we’re looking at blue noise dither masks!

It is inspired by a [tweet exchange](https://twitter.com/kechogarcia/status/1384885843643584515) with [Alan Wolfe](https://twitter.com/Atrix256) (who has a [great write-up](https://blog.demofox.org/2019/06/25/generating-blue-noise-textures-with-void-and-cluster/) about the original, more complex version of [void and cluster](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/1913/0000/Void-and-cluster-method-for-dither-array-generation/10.1117/12.152707.short?SSO=1) and a lot of blog posts about blue noise and its advantages and cool mathematical properties) and [Kleber Garcia](https://twitter.com/kechogarcia) who has recently released [“Noice”, a fast, general tool](https://github.com/kecho/Noice/releases/tag/1.0.0) for creating various kinds of 2D and 3D noise patterns.

The main idea is – one can write a very simple and very fast version of void-and-cluster algorithm that takes ~50 lines of code including comments!

How did I do it? Again in [Jax](https://bartwronski.com/tag/jax/). 🙂

## Algorithm

The original **void and cluster** algorithm comprises **3 phases** – initial random points and their reordering, removing clusters, and filling voids.

I didn’t understand why three phases are necessary, the paper didn’t explain them, so I went to code a much simpler version with just initialization and a single loop:

1. Initialize the pattern to a few random seed pixels. This is necessary as the algorithm is fully deterministic otherwise, so without seeding it with randomness, it would produce a regular grid.

2. Repeat until all pixel set:

1. Find an empty pixel with the smallest energy.

2. Set this pixel to the index of the added point.

3. Add the energy contribution of this pixel to the accumulated LUT.

4. Repeat until all pixels are set.

## Initial random points

Nothing too sophisticated there, so I decided to use **a jittered grid** – it prevents most clumping and just intuitively seems ok.

Together with those random pixels, I also create a **precomputed energy mask**.

It is a toroidally wrapped Gaussian bell with **a small twist / hack** – in the added point center I place **float “infinity”**. The white pixel in the above plots is this “infinity”. This way I guarantee that this point will never have smaller energy than any unoccupied one. 🙂 This simplifies the algorithm a lot – **no need for any bookkeeping**, all the information is stored in the energy map!

This mask will be added as a contribution of every single point, so will accumulate over time, with our tiny infinities 😉 filling in all pixels one by one.

## Actual loop

For the main loop of the algorithm, I look at the current energy mask, that looks for example like this:

And use **numpy/jax “argmin”** – this function literally returns what we need – index of the pixel with the smallest energy! Beforehand I convert the array to 1D (so that argmin works), get an 1D index, but then easily convert it to 2D coordinates using division and modulo by single dimension size. It’s worth noting that **operations like “flatten” are free in numpy** – they just readjust the array strides and the shape information.

I add this pixel with an increased counter to the final dither mask, and also take our precomputed energy table and **“rotate it” according to pixel coordinates**, and add to the current energy map.

After the update it will look like this (notice how nicely we found the void):

After this update step we continue the loop until all pixels are set.

## Results

The results look pretty good:

I think this is as good as the original void-and-cluster algorithm.

**The performance is 3.27s to generate a 128×128 texture** on a free GPU Colab instance (first call might be slower due to jit compilation) – I think also pretty good!

If there is anything I have missed or any bug, please let me know in the comments!

Meanwhile enjoy [the colab here](https://colab.research.google.com/github/bartwronski/BlogPostsExtraMaterial/blob/master/Jax_Void_and_cluster.ipynb), and check out [my dithering and blue noise blog posts here](https://bartwronski.com/2016/10/30/dithering-in-games-mini-series/).

Pingback: Dithering in games – mini series | Bart Wronski

Pingback: Progressive image stippling and greedy blue noise importance sampling | Bart Wronski

The three phases are due to the different contone levels it tries to fill