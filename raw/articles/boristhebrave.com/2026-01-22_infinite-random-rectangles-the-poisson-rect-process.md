---
title: Infinite Random Rectangles – the Poisson Rect process
url: https://www.boristhebrave.com/2026/01/22/infinite-random-rectangles-the-poisson-rect-process/
author: Boris
published: '2026-01-22'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Previously, we looked at how to [sample points randomly at a given density across an infinite plane](https://www.boristhebrave.com/2024/10/30/infinite-uniform-point-distributions/).

It’s harder than it sounds, as I was looking for an algorithm that was not biased by the size/shape of the chunks used to calculate it.

Today let’s extend that to filling the infinite plane with random **non-overlapping** rectangles. As before, that means finding a deterministic chunked algorithm that we can prove is unaffected by the choice of chunking.

This would be easy if we had a finite region. We could generate rectangles one at a time, skipping any that overlap. But with an infinite generator, you can’t rely on a global ordering. This is the same problem I had in [Infinite Modifying in Blocks](https://www.boristhebrave.com/2021/11/08/infinite-modifying-in-blocks/).

Here’s the trick:

- Phase 1: Generate randomly overlapping rectangles:
- Generate random points using a
[poisson point process](https://www.boristhebrave.com/2024/10/30/infinite-uniform-point-distributions/). - Assign a random height/width to each one to make a rectangle
- Also assign a random number to every rectangle, called the sort order

- Generate random points using a
- Phase 2: Remove some rectangles:
- For each rectangle, find the others that it overlaps with
- Retain only the rectangles that have a higher sort order than all their neighbors.


The last condition ensures we never generate overlapping rectangles – for any pair of overlapping rectangles, one will exclude the other.

The separation into two phases means that it is feasible to compute in chunks. First, you compute the rectangles per chunks for phase 1. These can be done completely independently. Then you compute the chunks for phase 2, which each only depend on a fixed number of phase 1 chunks, depending on the maximum width of a rectangle.

It’s probably better illustrated with an animation.

# Increasing density

To increase density, you can’t just increase the density of starting points, as that just results in more being eliminated in phase 2. Instead, compute several sets of rectangles according to the above procedure, then eliminate any overlapping rectangles between them.

# Other shapes

There’s no real reason to stick to rectangles. As long as the random shapes have a maximum size, and you can determine when two of them are overlapping, the algorithm works just as well.

A puzzle that has been on my mind for some time: Could this be modified to produce particular sizes in a particular ratio? E.g. have 20% rectangles of 2×2 and 80% of 1×1?