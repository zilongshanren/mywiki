---
title: Bidirectional path tracing in OptiX
url: http://raytracey.blogspot.com/2012/02/bidirectional-path-tracing-in-optix.html
author: Sam Lapere
published: '2012-02-16'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

While there are a lot of unidirectional GPU path tracers in the wild, bidirectional path tracers running purely on the GPU are still very uncommon. BDPT helps in speeding up convergence in scenes with lots of indirect lighting, such as the alleys in Sponza and interior scenes and also makes caustics appear much faster than unidirectional path tracers. In late 2010, there was a fantastic demo by Dietger van Antwerpen (former Brigade developer) showing Kelemen-style Metropolis light transport on top of a bidirectional GPU path tracer (see

[http://raytracey.blogspot.com/2010/12/real-time-metropolis-light-transport-on.html](http://raytracey.blogspot.com/2010/12/real-time-metropolis-light-transport-on.html)) and this guy seems to have found a way to make it work on the GPU with OptiX:
Should be interesting to see further results.

## No comments:

Post a Comment