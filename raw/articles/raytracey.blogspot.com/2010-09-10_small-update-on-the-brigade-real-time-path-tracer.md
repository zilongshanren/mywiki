---
title: Small update on the Brigade real-time path tracer
url: http://raytracey.blogspot.com/2010/09/small-update-on-brigade-real-time-path.html
author: Sam Lapere
published: '2010-09-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/7e0fd302de0b378a.jpg)


Jacco Bikker has released two new video's of the progress with his real-time path tracer named Brigade, demonstrating some kind of game where a truck has to push gold containers or something. Looks fun:

1. direct lighting (32 samples per pixel):

[http://www.youtube.com/watch?v=vYxDubDLS6Y](http://www.youtube.com/watch?v=vYxDubDLS6Y)

2. one bounce of indirect lighting (16 spp):

[http://www.youtube.com/watch?v=en1F8k4rjEY](http://www.youtube.com/watch?v=en1F8k4rjEY)

There is also an update from Dietger van Antwerpen on the GPU path tracer (subsystem of Brigade path tracer) running with the more advanced ERPT (energy redistribution path tracing) algorithm. He has improved the ERPT code to produce virtually identical results to the path traced reference and released a high quality image with it (ERPT on the left and path tracing on the right):

![](http://img844.imageshack.us/img844/7282/gpusponzaptvserpt.png)


![](http://img844.imageshack.us/img844/7282/gpusponzaptvserpt.png)

Explanation from Dietger van Antwerpen in

He also released a new video showing improvements to the GPU ERPT code:


As the videos show, ERPT converges considerably faster than standard path tracing and the noise is significantly reduced. Very cool and very impressive. I wonder if the optimized ERPT code will be used in Brigade for real-time animations and games.

[the description at youtube](http://www.youtube.com/watch?v=d9X_PhFIL1o):"After some complains pointing out that in the movie, ERPT is significantly darker then path tracing , I fixed the darkening effect of the ERPT image filter, solving the difference in lighting quality. I made an image ([http://img844.imageshack.us/img844/7...]) using ERPT for the left half, while using path tracing for the right half and waited until the path tracing noise almost vanished. As you can see, the lighting quality between the left and right half is pretty much the same. (The performance and convergence characteristics remain unchanged)"

It would be interesting to know the time for ERPT and for path tracing to achieve these results.


He also released a new video showing improvements to the GPU ERPT code:

[http://www.youtube.com/watch?v=dMxQ2bVL84Y](http://www.youtube.com/watch?v=dMxQ2bVL84Y)As the videos show, ERPT converges considerably faster than standard path tracing and the noise is significantly reduced. Very cool and very impressive. I wonder if the optimized ERPT code will be used in Brigade for real-time animations and games.

## No comments:

Post a Comment