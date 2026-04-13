---
title: Zooming and panning
url: https://apoorvaj.io/building-a-fast-modern-image-editor
published: '2015-07-03'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

Over the past month, I’ve been working on a fun project in my spare
time—[Papaya](https://github.com/ApoorvaJ/Papaya), an open
source GPU-powered image editor built using C++ and OpenGL.

In this short time, I’ve realized that a lot of widely used image editors—both, open source and proprietary - are surprisingly easy to surpass in terms of performance. I’m not talking about shaving off a few milliseconds; I’m talking big, noticeable speed differences, especially when dealing with large images.

Before I go into details, here’s a GIF of the performance comparison of GIMP vs Papaya while drawing with a brush of diameter 2048 pixels on a 4096 x 4096 pixel image.

![](../../assets/43702ed09012b2b2.gif)


While this difference in performance is glaringly apparent on large images, it is also easily felt on images as small as 512 x 512 pixels. So why is Papaya faster? In short, it is fast because it uses the GPU instead of making the CPU do the heavy lifting.

I haven’t looked at GIMP’s code, but from its overall performance, I’m convinced that it uses the CPU for almost everything. This includes calculating the pixels to show on screen when you zoom or pan an image. The application has to use filters when zooming - nearest neighbor while magnification and linear while minification. This takes time on the CPU.

In Papaya, I’m using the [Windows API](https://en.wikipedia.org/wiki/Windows_API) to
create a borderless window and I’m rendering to it with OpenGL. I’m
using the awesome [ImGui
library by Omar Cornut](https://github.com/ocornut/imgui) for the UI. All the interface elements
(including the min, max, close buttons) are actually textured quads. The
main canvas is also a textured quad. Because of this, zooming in/out
using the appropriate filtering method is basically free as far as the
CPU is concerned. The result: extremely smooth zooming in/out.

Papaya is faster than GIMP (and faster than all other image editors I tested) at this. To understand why, let’s have a look at how the brush tool works.

![](../../assets/f622f8f99f99a82e.png)


In its simplest form, the brush tool requires a circle filling
algorithm. Given a mouse click position and a brush of diameter
`n`

, the program has to perform a distance test on a square
of size `n x n`

around the mouse. If the distance from the
given pixel is less than or equal to the radius, the pixel has to be
filled. This algorithm becomes exponentially slower as `n`

increases linearly.

![](../../assets/183d911708c95f36.png)


Things get even worse when you consider that the user drags the brush around. So instead of just filling in a circle, you have to fill in all the circles along a line between the user’s last drag position and the user’s current drag position. Some image editors reduce the computation involved by only filling in circles periodically along the line. This leads to nasty dimples, though.

GIMP doesn’t try to alleviate the problem in any way, and hence is
atrociously slow. In Papaya, I’m using a GLSL shader to draw the brush
stroke. The fragment shader samples the primary texture and renders the
output to an auxiliary texture through a custom frame buffer, and then
swaps the auxiliary texture handle and the primary texture handle. You
can check out the WebGL-based version of the fragment shader on [Shadertoy](https://www.shadertoy.com/view/XtlXz7). This
implementation means that the execution time does not depend on the
brush size at all. Based on my tests, it runs extremely fast compared to
a CPU implementation. Here’s a performance comparison of the GLSL
version against my naive CPU implementation.

![](../../assets/c4cfb05fcaf46a24.png)


*CPU cycles were recorded using __rdtsc() and
milliseconds were recorded using QueryPerformanceCounter on
the optimized release build.*


Now that the proof of concept is done, I will be cleaning up the code and adding features like anti-aliasing and opacity to the brush tool. This is a spare-time hobby project and development will take time, but I hope to experiment with more GPU-centric workflows and learn a lot along the way.