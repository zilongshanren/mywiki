---
title: Hacking AMD OpenGL drivers
url: https://outerra.blogspot.com/2013/07/hacking-amd-opengl-drivers.html
author: Outerra
published: '2013-07-19'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

## Even though the

[logarithmic depth buffer](http://outerra.blogspot.com/2009/08/logarithmic-z-buffer.html)technique works pretty nicely, it has several problems that make its use problematic in some cases. If you use just the vertex shader modification, you can get depth buffer artifacts on longer triangles that are close to the camera, since the depth values aren't correctly interpolated in perspective. It can be helped by a finer tesselation, or by writing the correct values in the fragment shader (possibly just for the geometry that's not tesselated sufficiently). However, writing the fragment depth in shader disables certain hardware depth buffer optimizations like the early depth test, and adds to the bandwidth. That can pose a problem in scenarios with a higher overdraw.

On Direct3D there's a technique that can provide sufficient depth buffer precision - reverse mapping of far/near planes in a normal floating-point depth buffer. In OpenGL it can't be used directly because of a design flaw that causes a huge loss of precision in depth value computation (not just for the floating point depth buffers, see

[here](https://twitter.com/TimothyLottes/status/352169294488010752)). See more detail in

[maximizing depth buffer range and precision](http://outerra.blogspot.sk/2012/11/maximizing-depth-buffer-range-and.html)blog post.

There's a way to work around it on Nvidia hardware thanks to the support of an unclamped glDepthRange extension (glDepthRangedNV). However, on AMD it's not supported and there were indications that it may not even be possible. But here's what I found: with a glDepthRange(-1, 1) call that would solve the problem, the arguments are clamped to (0, 1) as per specification. But if we go into the disassembly of the call and make it skip the instruction that would cause it to clamp the lower bound:

... and the reverse FP buffer technique suddenly starts working! With precision good enough to handle the range needed to cover the whole universe. Projection matrix to use with it looks like this:

There's no

*far*term; the zero depth value is projected to infinity. The precision is very high - for near=0.01m the precision measured on the GPU is around 0.03mm at 100m, 0.003m at 10km, and 0.3m at 1000km and so on.

Of course, hacking the driver this way for normal use would be highly impractical, it was done just to show that actually nothing prevents AMD from supporting the unclamped depth range and getting a depth buffer technique that works with great precision without sacrificing the depth optimizations.

Hoping they will be

[listening](http://devgurus.amd.com/thread/167019).

## No comments:

Post a Comment