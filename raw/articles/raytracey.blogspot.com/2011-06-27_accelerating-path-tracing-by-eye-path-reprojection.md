---
title: Accelerating Path Tracing by Eye Path Reprojection
url: http://raytracey.blogspot.com/2011/06/accelerating-path-tracing-by-eye-path.html
author: Sam Lapere
published: '2011-06-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just stumbled upon this upcoming paper about interactive GPU path tracing from Niklas Henrich. The


[abstract](http://www.uni-koblenz.de/%7Enikhen/)sounds very promising:"Recently, path tracing has gained interest for real-time global illumination since it allows to simulate an unbiased result of the rendering equation. However, path tracing is still too slow for real-time applications and shows noise when displayed at interactive frame rates. The radiance of a pixel is computed by tracing a path, starting from the eye and connecting each point on the path with the light source. While conventional path tracing uses the information of a path for a single pixel only, we demonstrate how to distribute the intermediate results along the path to other pixels in the image. We show that this reprojection of an eye path can be implemented efficiently on graphics hardware with only a small overhead. This results in an overall improvement of the whole image since the number of paths per pixel increases. The method is especially useful for many indirections, which is often circumvented to save computation time. Furthermore, instead of improving the quality of the rendering, our method is able to increase the rendering speed by reusing the reprojected paths instead of tracing new paths while maintaining the same quality."

## 3 comments:

I'm not sure I understand, but it sounds like they're temporarily storing random vertices as anisotropic point sources.

I think the technique for reprojecting eye paths is going to be similar to the one described in "Accelerating path tracing by re-using paths" by Bekaert et al. This paper is behind a paywall unfortunately, but here's a small excerpt:


"we propose to re-use paths shot through nearby pixels in order to reduce noise. We do so by tracing a single shadow ray per

pair of paths in a group, connecting points x(i) with y(j), i, j = 1, 2, 3 and i != j as indicated by the dashed lines. Stated roughly, this results in additional paths at the cost of single rays. With appropriately chosen combination weights, no bias is introduced."

The figures in the paper are much more explanatory though.

Hi. The updated link is http://userpages.uni-koblenz.de/~nikhen/. It has several interesting papers.

Post a Comment