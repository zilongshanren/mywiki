---
title: Graphics Programming weekly - Issue 22 — January 14, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-22/
author: Jendrik Illner
published: '2018-01-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[The Rendering of Middle Earth: Shadow of Mordor](http://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor/) [[wayback-archive]](http://web.archive.org/web/20180103010340/http://www.elopezr.com/the-rendering-of-middle-earth-shadow-of-mordor/)

- gbuffer breakdown
- blood rendering as gbuffer modifier
- tessellation
- uses a point cloud as input and a tessellation shader calculates the polygons

- SSAO has two distinct channels that get applied to specular and diffuse separately
- top-down projection texture used to add extra information to sun lighting
- static lighting uses a light volume texture
- Rayleigh + Mie scattering system for atmospheric fog
- alpha blended objects are rendered directly to the Low Dynamic Range (after tone mapping)
- gpu based rain system
- two bloom systems, one applied to everything and a radian blur that is only applied to the sky
- UI is rendered into a separate render target and blended with the 3D scene

[Reverse Z Cheat Sheet](http://www.intrinsic-engine.com/reverse-z-cheat-sheet/) [[wayback-archive]](https://web.archive.org/web/20180109193258/http://www.intrinsic-engine.com/reverse-z-cheat-sheet/)

- reverse depth buffer from [near=0 to far=1] to use [near=1 to far=0]
- how to adjust the projection matrix
- what changes are required in addition to this
- how to linearize depth buffer values without a matrix multiplication

[Optimizing tile-based light culling](https://turanszkij.wordpress.com/2018/01/10/optimizing-tile-based-light-culling/) [[wayback-archive]](https://web.archive.org/web/20180112222626/https://turanszkij.wordpress.com/2018/01/10/optimizing-tile-based-light-culling/)

- problems of frustum-sphere culling
- refine with AABB culling

- improve depth discontinuity with bitmasks to detect lights not hitting any geometry
- spot light culling
- decal probe box
- other performance considerations

- overview of different views
- high level view of GCN hardware
- wavefronts, latency hiding, occupancy

- detect pipeline stalls
- read the pipeline state view to get details about pipeline statistics
- detect opportunities for async compute

[Fixing Camera Shake on Single Precision GPUs](http://hacksoflife.blogspot.ca/2018/01/fixing-camera-shake-on-single-precision.html) [[wayback-archive]](https://web.archive.org/web/20180114133847/http://hacksoflife.blogspot.ca/2018/01/fixing-camera-shake-on-single-precision.html)

- 100x100 km chunks with 1 cm precision in 32 bits
- problem once 1 cm of world space > 1 pixel on screen
- using doubles on the CPU for transforms
- change order of operation to apply an offset (single subtract) to bring the mesh close to the camera
before rotation is applied
- this offset updated infrequently

- this offset updated infrequently

- computes error introduced by approximations vs results from path tracer
- fits a curve to this error, and uses this curve to compensate for the error in the original approximation

[Perceptually uniform color space for image signals including high dynamic range and wide gamut](https://www.osapublishing.org/oe/fulltext.cfm?uri=oe-25-13-15131&id=368272) [[wayback-archive]](https://web.archive.org/web/20180109165820/https://www.osapublishing.org/captcha/?guid=969782CD-D2CF-AAB4-5E63-86F5FB1672F2&AspxAutoDetectCookieSupport=1)

- overview of existing color spaces
- comparison against new proposed color space

[Indirect illumination using cubemaps](http://renderdiagrams.org/2018/01/05/indirect-illumination-using-cubemaps/) [[wayback-archive]](https://web.archive.org/web/20180109170012/http://renderdiagrams.org/2018/01/05/indirect-illumination-using-cubemaps/)

- explanation of how indirect illumination is stored in cube maps
- including interactive diagrams to explain the principles

[Next power of two in HLSL](https://turanszkij.wordpress.com/2018/01/05/next-power-of-two-in-hlsl/amp/) [[wayback-archive]](https://web.archive.org/web/20180109170108/https://turanszkij.wordpress.com/2018/01/05/next-power-of-two-in-hlsl/amp/)

- how to calculate the next larger power of two with bit level instructions

[Cloth Shading](https://knarkowicz.wordpress.com/2018/01/04/cloth-shading/amp/) [[wayback-archive]](https://web.archive.org/web/20180109193033/https://knarkowicz.wordpress.com/2018/01/04/cloth-shading/amp/?__twitter_impression=true)

- comparison of the Ashikhmin sheen and Imageworks Charlie sheen
- including shader toy implementation

[Screen Space Path Tracing – Diffuse](http://tuxedolabs.blogspot.ca/2018/01/screen-space-path-tracing-diffuse.html?m=1) [[wayback-archive]](https://web.archive.org/web/20180109193220/http://tuxedolabs.blogspot.ca/2018/01/screen-space-path-tracing-diffuse.html?m=1)

- ray marching against depth buffer
- on hit fetch light re-projected from previous frame
- denoising with temporal re-projected filter + smoothing groups + temporal AA

[Alternative definition of Spherical Harmonics for Lighting](https://grahamhazel.com/blog/2017/12/18/alternative-definition-of-spherical-harmonics-for-lighting/) [[wayback-archive]](https://web.archive.org/save/https://grahamhazel.com/blog/2017/12/18/alternative-definition-of-spherical-harmonics-for-lighting/)

- explanation of the math for Spherical Harmonics
- simplified definition by specializing for the use case required for lighting (but not limited to it)

[Converting SH Radiance to Irradiance](https://grahamhazel.com/blog/2017/12/22/converting-sh-radiance-to-irradiance/) [[wayback-archive]](https://web.archive.org/web/20180112222529/https://grahamhazel.com/blog/2017/12/22/converting-sh-radiance-to-irradiance/)

- use definition from part 1 to convert radiance (incoming light) to irradiance (outgoing bounced light)
- improving the conversion with a non-linear reconstruction

[Moment-Based Methods for Real-Time Shadows and Fast Transient Imaging](http://hss.ulb.uni-bonn.de/2017/4918/4918.htm) [[wayback-archive]](https://web.archive.org/web/20180112222551/http://hss.ulb.uni-bonn.de/2017/4918/4918.htm)

- summary of the theory of moments from mathematics
- replacement for inverse Fourier transforms of positive functions with many benefits
- techniques for opaque and translucent occludes, soft shadows and single scattering
- filterable shadow maps using 64 bits per texel compared to other filterable techniques
- more efficient at high resolutions compared to classical shadow maps

- index buffer compression added
- index buffer to a triangle strip conversion added
- quantize float option added
- improvements to exisiting analyzers

[Making floating point numbers smaller](http://www.ctrl-alt-test.fr/?p=535) [[wayback-archive]](https://web.archive.org/web/20180112222650/http://www.ctrl-alt-test.fr/?p=535)

- how to reduce the precisions of floats (so that they can be compressed better)