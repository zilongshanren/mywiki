---
title: Dithering in games – mini series
url: https://bartwronski.com/2016/10/30/dithering-in-games-mini-series/
published: '2016-10-30'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

This an opening post of mini blog post series about various uses of dithering for quantization and sampling in video games. It is something most of us use intuitively in every day work, so wanted to write down some of those concepts, explain and analyze them in Mathematica.

This post is just a table of contents.

* Update April 2020*: I didn’t expect to come back to blue noise a few years later, but I

[wrote a small additional blog post](https://bartwronski.com/2020/04/26/optimizing-blue-noise-dithering-backpropagation-through-fourier-transform-and-sorting/)on alternative method for generating blue noise patterns for dithering by “optimizing” frequency spectrum. You can treat it as

**part three-point-five**. 🙂

**Update April 2021**: I [described and posted a tiny](https://bartwronski.com/2021/04/21/superfast-void-and-cluster-blue-noise-in-python-numpy-jax/), very fast and very readable Python Jax/numpy implementation of the void and cluster algorithm. You can treat it as **part three-point-seventy-five**. 🙂

**Update August 2022**: I have explored [the idea of “progressive blue-noise stippling”](https://bartwronski.com/2022/08/31/progressive-image-stippling-and-greedy-blue-noise-importance-sampling/) where one dithers an image using blue-noise patterns with an increasing sample count. It’s a pretty cool, artistic effect with potential use for importance sampling.

You can find some supplemental material for posts here: [https://github.com/bartwronski/BlogPostsExtraMaterial/tree/master/DitheringPostSeries](https://github.com/bartwronski/BlogPostsExtraMaterial/tree/master/DitheringPostSeries)

Pingback: Dithering part one – simple quantization | Bart Wronski

Pingback: Dithering part two – golden ratio sequence, blue noise and highpass-and-remap | Bart Wronski

Pingback: Dithering part three – real world 2D quantization dithering | Bart Wronski

Pingback: Small float formats – R11G11B10F precision | Bart Wronski

Pingback: When Random Numbers Are Too Random: Low Discrepancy Sequences « The blog at the bottom of the sea

Pingback: “Optimizing” blue noise dithering – backpropagation through Fourier transform and sorting | Bart Wronski

Pingback: Superfast void-and-cluster Blue Noise in Python (Numpy/Jax) | Bart Wronski

Pingback: Transforming “noise” and random variables through non-linearities | Bart Wronski

Pingback: Progressive image stippling and greedy blue noise importance sampling | Bart Wronski