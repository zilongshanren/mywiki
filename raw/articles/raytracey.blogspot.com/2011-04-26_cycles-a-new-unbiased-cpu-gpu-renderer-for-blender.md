---
title: Cycles, a new unbiased CPU/GPU renderer for Blender
url: http://raytracey.blogspot.com/2011/04/cycles-new-cpugpu-path-tracer-for.html
author: Sam Lapere
published: '2011-04-26'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The GPU path tracing virus keeps spreading at an incredible rate: Blender is soon going to have a fully integrated physically based renderer, codenamed 'Cycles', which can use the CPU or the GPU for rendering (GPU path tracing starts at 1:18).




Changing materials, moving objects around and adding/deleting new objects can be done in real-time and the Cycles rendering engine can also rebuild the acceleration structure of the Suzanne model at lightning fast speeds. The source code will be available in about two weeks! It's going to be really cool when you can modify your model and immediately see the changes rendered in real-time in photoreal quality. Speaking of real-time editing and rendering, one of Luxrender's developers has made an utterly amazing video showing live editing of a physics simulation inside Blender and rendering it in real-time with Luxrender's PathGPU2 (a 100% OpenCL path tracer and part of SmallLuxGPU v1.8 with a heavy focus on animation rendering):




The video was rendered on a Core i7 920 + 2x ATI HD4890's, certainly not a bad system, but the HD4000 series was not exactly conceived with OpenCL computing in mind. I would love to see a GTX580 rendering this scene though. According to


[http://code.blender.org/index.php/2011/04/modernizing-shading-and-rendering/](http://code.blender.org/index.php/2011/04/modernizing-shading-and-rendering/)Changing materials, moving objects around and adding/deleting new objects can be done in real-time and the Cycles rendering engine can also rebuild the acceleration structure of the Suzanne model at lightning fast speeds. The source code will be available in about two weeks! It's going to be really cool when you can modify your model and immediately see the changes rendered in real-time in photoreal quality. Speaking of real-time editing and rendering, one of Luxrender's developers has made an utterly amazing video showing live editing of a physics simulation inside Blender and rendering it in real-time with Luxrender's PathGPU2 (a 100% OpenCL path tracer and part of SmallLuxGPU v1.8 with a heavy focus on animation rendering):

[http://www.youtube.com/watch?v=bSQoJW9ajmU](http://www.youtube.com/watch?v=bSQoJW9ajmU)(real-time part starts at 1:23)The video was rendered on a Core i7 920 + 2x ATI HD4890's, certainly not a bad system, but the HD4000 series was not exactly conceived with OpenCL computing in mind. I would love to see a GTX580 rendering this scene though. According to

[the graph below from Anandtech](http://www.anandtech.com/show/4209/amds-radeon-hd-6990-the-new-single-card-king/17)depicting the performance of SmallLuxGPU 1.7, I can imagine that card would just fly in this scene and make the video that much more awesome!![](../../assets/4de51734ef36acb5.png)


![](../../assets/4de51734ef36acb5.png)

Update: SmallLuxGPU 1.8beta (which incorporates Metropolis light transport in OpenCL) is now available for download from the Luxrender forum

Update2: A lot of useful information and implementation details on the Cycles renderer can be found on

[http://wiki.blender.org/index.php/Dev:2.5/Source/Cycles](http://wiki.blender.org/index.php/Dev:2.5/Source/Cycles)under the header "Design"

## 4 comments:

Nice post about Cycles. I also wrote one: http://jaydez-tech.blogspot.com/2011/05/cycles-new-blender-renderer.html

Thanks!

Hello..thnks for the info...

I would like to get in touch wth u,,im new to blender 2•70...im computer programmer.

GPU rendering is what allows using graphics card for rendering, instead of CPU. This helps speeding up rendering, because modern GPUs are so designed to do quite a lot number crunching. Read More

Post a Comment