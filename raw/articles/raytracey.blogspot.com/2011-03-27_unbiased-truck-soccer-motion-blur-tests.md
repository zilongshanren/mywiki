---
title: 'Unbiased Truck Soccer: motion blur tests'
url: http://raytracey.blogspot.com/2011/03/unbiased-truck-soccer-motion-blur-tests.html
author: Sam Lapere
published: '2011-03-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I made some tests to determine which amount of motion blur (accomplished by accumulating samples from previous frames) is acceptable for relatively fast moving objects.


The picture below shows a comparison of the scene from 'Unbiased Truck Soccer' with different amounts of motion blur: no motion blur (left), averaging the last 3 frames (middle) and averaging the last 6 frames (right). These images were all rendered on a 8600M GT with a frame rate of barely 5 fps, so the comparison is not representative for more powerful GPUs, but it provides a general idea of the "noise freeness" of parts of the image that are static like the walls, floor and ceiling. The three little rectangles at the bottom of the picture show a close-up comparison of a noisy area of the ceiling which is lit only with indirect lighting.




A low-res video:



The truck is performing a looped animation. The camera can be moved by holding the middle mouse button (dragging in image plane) and Shift + middle mouse button (zooming).


The new test can be downloaded from


On a GTX 580 this demo should run at 60 fps at default settings (768x512 resolution, max path length 4, 4 samples per pixel per pass blurred to 12 (motion blur = 1) or 24 (motion blur = 2) samples per pixel).


The picture below shows a comparison of the scene from 'Unbiased Truck Soccer' with different amounts of motion blur: no motion blur (left), averaging the last 3 frames (middle) and averaging the last 6 frames (right). These images were all rendered on a 8600M GT with a frame rate of barely 5 fps, so the comparison is not representative for more powerful GPUs, but it provides a general idea of the "noise freeness" of parts of the image that are static like the walls, floor and ceiling. The three little rectangles at the bottom of the picture show a close-up comparison of a noisy area of the ceiling which is lit only with indirect lighting.

![](../../assets/75bf189f2a305d52.png)

![](../../assets/75bf189f2a305d52.png)

A low-res video:

The truck is performing a looped animation. The camera can be moved by holding the middle mouse button (dragging in image plane) and Shift + middle mouse button (zooming).

The new test can be downloaded from

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)The package contains three executables, with different amounts of motion blur (none, average of last 3 frames and average of last 6 frames).On a GTX 580 this demo should run at 60 fps at default settings (768x512 resolution, max path length 4, 4 samples per pixel per pass blurred to 12 (motion blur = 1) or 24 (motion blur = 2) samples per pixel).

## 2 comments:

I have tested the program on a gtx480, and it runs pretty smooth (40-47fps), but to get usable results, I need to increase the spppp to 128...


The motion bulr looks pretty simple, haven't you thought about doing something more complex? Like tagging your rays with a time value, and intersecting your scene based on that time value? Though the motion blur looks more noisy, but it's better in general.

Hi, thanks for providing the gtx480 numbers. If by usable, you mean noise free, well that depends on your personal taste I suppose. In this particular scene, I find the image quality visually quite pleasing at 32 spp. I actually prefer some graininess in the image over perfectly clean renders. It adds an authentic Monte Carlo rendered touch, which you wouldn't have when using e.g. photon mapping or radiosity. And some games (like Killzone and Kane and Lynch) are in fact adding film grain to achieve a more cinematic look. It basically comes down to artistic preference.



About the motion blur, I think it looks pretty good as long as the framerate is high enough, but it starts to break down at lower framerates, resulting in trailing artefacts.

Btw, the motion blur trick was not coded by myself but by Kerrash (see the posts on Cornell Box Pong), and even if it's a simple trick, it dramatically reduces the noise. That was the purpose of this test. Imo, with motion blur looks much better than without, because you can reuse previously acquired samples without a performance hit. Per-object motion blur would look much better of course, but it also would impact performance.

I want to try out some additions to the code like acceleration structures, a Phong BRDF for glossy materials, support for other primitives than spheres and maybe real motion blur (and hopefully bidirectional path tracing in CUDA), but those will take a while because I've just started to learn programming ;)

Post a Comment