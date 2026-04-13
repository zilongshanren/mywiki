---
title: Real-time path tracing of animated meshes on the GPU (1)
url: http://raytracey.blogspot.com/2011/10/real-time-animation-path-tracing-on-gpu.html
author: Sam Lapere
published: '2011-10-14'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another experiment: no spheres this time, but a real-time animated triangle mesh (the hand is from

[the Utah 3D Animation Repository](http://www.sci.utah.edu/~wald/animrep/), a textured mesh containing 15,855 triangles). The goal was to create a simple animated scene and achieve a look as close to photorealism as possible with completely dynamic, physically accurate global illumination in real-time using path tracing.The following animation was rendered in real-time on a GTS 450 (stretching the compute capabilities of my GPU to the max):

Details will follow.

The image below was rendered with path tracing at 26 samples per pixel in 0.8 seconds on a GeForce GTS 450 (192 cuda cores at factory clocks, it would render 3 to 4 times faster on a GTX 580, which has 512 cuda cores and is clocked higher):

## No comments:

Post a Comment