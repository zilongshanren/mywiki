---
title: 'OpenCL path tracing tutorial 3: OpenGL viewport, interactive camera and defocus
  blur'
url: http://raytracey.blogspot.com/2017/01/opencl-path-tracing-tutorial-3-opengl.html
author: Sam Lapere
published: '2017-01-11'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Part 1**

**Setting up an OpenGL window**

[https://github.com/straaljager/OpenCL-path-tracing-tutorial-3-Part-1](https://github.com/straaljager/OpenCL-path-tracing-tutorial-3-Part-1)

**Part 2**

**Adding an interactive camera, depth of field and progressive rendering**

[https://github.com/straaljager/OpenCL-path-tracing-tutorial-3-Part-2](https://github.com/straaljager/OpenCL-path-tracing-tutorial-3-Part-2)

Thanks to Erich Loftis and Brandon Miles for useful tips on improving the generation of random numbers in OpenCL to avoid the distracting artefacts (showing up as a sawtooth pattern) when using defocus blur (still not perfect but much better than before).

The next tutorial will cover rendering of triangles and triangle meshes.

## 4 comments:

Thanks Sam! Can't wait to try this out on my machine! Thanks for the mention in your post. I am glad to contribute in some small way. Looking forward to the accompanying write-up for this post. Thanks again for all your hard work!

-Erich

Interesting but I'm more interested in volume rendering path tracing.

When I run this on nVidia GTX 660 I get some noticeably lighter pixels, they form a grid pattern within the resultant image. Any idea how to get past that?

@ Jan Vlietinck: long time no see! How are things? Path tracing for medical volume rendering is something I want to look into quite soon-ish, Siemens "cinematic rendering" (https://www.youtube.com/watch?v=703Zzl8YYJk) produces stunning images


Dave: The pattern is caused by a poor random number generator. Some people have contributed code improvements to make the RNG more "random" and less prone to artefacts, but it's still not as good as CUDA's quasi-random Sobol RNG.

Post a Comment