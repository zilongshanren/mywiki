---
title: 'Ray Tracing In One Weekend (in Lisp, and n-dimenions) :: nklein software'
url: http://nklein.com/2024/09/ray-tracing-in-one-weekend-book-1/
author: Pat
published: '2024-09-27'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

Earlier this year, I started working through the online book ** Ray Tracing In One Weekend (Book 1)**. I have been following along with it in Common Lisp, and I have been extending it all from 3-dimensional to n-dimensional.

I reproduced 4-dimensional versions of all of the book images which you can see on [my weekend-raytracer github page](https://github.com/nklein/weekend-raytracer).

Here is the final image. This is a 250-samples-per-pixel, 640x360x10 image plane of three large hyperspheres (one mirrored, one diffuse, one glass) atop a very large, diffuse hypersphere. Also atop this very large hypersphere are a bunch of smaller hyperspheres of varying colors and materials. The image is rendered with some defocus-blur.

![Image described in detail in post.](../../assets/e5a13676eb714e54.png)


![Image described in detail in post.](../../assets/e5a13676eb714e54.png)

**Caveat:** This depends on a patched version of the policy-cond library that is not in the current Quicklisp distribution but should be in the next.

[…] I added CSG (Constructive Solid Geometry) operators to the ray-tracer that I mentioned in the previous post. I added intersections, complements, and […]