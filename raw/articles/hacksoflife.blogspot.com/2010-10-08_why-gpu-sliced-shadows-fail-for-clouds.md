---
title: Why GPU Sliced Shadows Fail For Clouds
url: http://hacksoflife.blogspot.com/2010/10/why-gpu-sliced-shadows-fail-for-clouds.html
author: Benjamin Supnik
published: '2010-10-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[here](http://developer.download.nvidia.com/compute/cuda/sdk/website/C/src/smokeParticles/doc/smokeParticles.pdf)) doesn't work well for a flight simulator cloud system. When reading a white paper, it can be hard to judge the appropriateness of an algorithm for a particular application; here's what went wrong in our case.

The Basic Algorithm

The basic algorithm is something like this:

- Sort the particles to be directional for both the light source and the viewer. (This can require rendering front-to-back to the viewer at times.)
- Along this direction, slice the particles up. For each slice, plot first, then update our shadows.
- Composite the finished system to screen (necessary if we are going front-to-back).

The algorithm does work well; for a test case with a cloud built to meet the algorithm's requirements, the shadows were soft, real-time, and quite plausible.

Performance Bottlenecks

The algorithm has two basic performance bottlenecks:

- Like all over-drawn particle system algorithms, it is fill rate limited if we overlap too many particles.
- Slicing requires finishing rasterization to a texture and then using the texture, so the algorithm is bound by the number of slices. (The slicing can affect both time spent in the driver rebuilding the pipeline, including costs of changing the render target, and it can stall depending on how smart your driver is about requiring pending rasterization to complete.)

Overdraw and Alpha

The algorithm is a little bit mismatched to a flight simulator cloud system because a flight simulator cloud system typically uses a smaller number of more opaque cloud particles to avoid fill-rate issues. This causes problems because the algorithm doesn't naturally diminish self-shadowing; it depends on the fact that we haven't accumulated a large number of particles to keep shadows very light when two particles are near each other.

So the first problem in general use is that the quality of the shadows fights with the optimization of relatively opaque particles. As soon as we make fewer, smaller, more opaque particles (which can be coped with via texturing) the quality of the shadows becomes quite poor.

Slicing and Bucketing

The second problem is that for a general large-scale particle field we need some kind of bucketing, and this fights with slicing. We want to break our particles into a bucket grid for two reasons:

- It gives us a way to rapidly cull a lot of particles.
- The bucket grid has a traversal order that is back to front, so we only need to Z-sort within a bucket, saving a lot of sorting time.

Slices are really quite expensive due to the GPU setup overhead, and even a small number of buckets means that we can't afford enough slices. NVidia recommends 32-128 slices, but with buckets, you'll be lucky to get 8 slices per bucket.

Low Slice Count = Ugly

It goes without saying that having a small number of slices is going to produce less correct shadows. But there is another, more serious problem: as you rotate the camera, the slicing plane changes. Nearby particles that are in the same plane will not shadow each other, but when/how this happens is a function of how wide the slicing plane is and which way it goes.

What this means is: as we rotate the camera, some particles will suddenly stop shadowing each other as the slicing planes rotate, causing noticeable popping artifacts.

The really bad artifact comes when we go from having the sun slightly facing to us to slightly facing away from us. At that point the algorithm will switch between back-to-front and front-to-back rendering, and the slicing plane will jump by 90 degrees almost instantly. This produces a huge number of artifacts when the number of slices is small.

Summary

The algorithm fails when:

- We have mostly opaque particles and
- We can't afford enough slices and
- There are external constraints (like culling) artificially "wasting" slices.

## No comments:

## Post a Comment