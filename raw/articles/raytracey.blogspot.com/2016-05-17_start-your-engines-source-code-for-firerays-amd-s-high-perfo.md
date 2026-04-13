---
title: 'Start your engines: source code for FireRays (AMD''s high performance OpenCL
  based GPU ray tracing framework) available'
url: http://raytracey.blogspot.com/2016/05/start-your-engines-source-code-for.html
author: Sam Lapere
published: '2016-05-17'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

AMD has just released

[the full source code of FireRays](http://gpuopen.com/firerays-2-0-open-sourcing-and-customizing-ray-tracing/), their OpenCL based GPU renderer which was first available as a SDK library since August 2015 (see http://raytracey.blogspot.co.nz/2015/08/firerays-amds-opencl-based-high.html). This is an outstanding move by AMD which significantly lowers the threshold for developers to enter the GPU rendering arena and create an efficient OpenCL based path tracing engine that is able to run on hardware from AMD, Intel and Nvidia without extra effort.
Here's an ugly sample render of FireRays provided by AMD:

And an old video from one of the developers:

Nvidia open sourced their

[high performance CUDA based ray tracing framework](https://code.google.com/archive/p/understanding-the-efficiency-of-ray-traversal-on-gpus/)in 2009, but hasn't updated it since 2012 (presumably due to the lack of any real competition from AMD in this area) and has since focused more on developing OptiX, a CUDA based closed source ray tracing library. Intel open sourced

[Embree](https://embree.github.io/)in 2011, which is being actively developed and updated with new features and performance improvements. They even released another open source high performance ray tracer for scientific visualisation called

[OSPRay](http://www.ospray.org/).

FireRays seems to have some advanced features such as ray filtering, geometry and ray masking (to make certain objects invisible to the camera or selectively ignore effects like shadows and reflections) and support for volumetrics. Hopefully AMD will also release some in-depth documentation and getting started tutorials in order to maximise adoption of this new technology among developers who are new to GPU ray tracing.

## 7 comments:

its toos low compared to native cuda, sorry.

We'll see how this gets adopted by the crowd, and that could take quite some time until we have first feedback from some projects :/

So time will tell...

Sorry AMD... slow by today's standards.

Never got firerays working. Maybe now I can.

Maybe fire rays is not that important if CUDA will run on AMD cards in the near


future.

Btw AMD delivers 6 tflop @ 200 Dollars with the new Polaris chip.

If someone would spend a few thousand bucks on those, he would already have a good

realtime path tracing machine.

Can anyone here even slightly imagine how fast a path tracer could become if all the memory(reg) would be situated right above the FPU`s?



How i found out, many leading chip manufacturers are working on realizing a 3D(not 2.5D) chip , though it isnt really that easy.

http://www.businesswire.com/news/home/20150830005041/en/Tezzaron-Announces-World%E2%80%99s-Eight-Layer-Active-Wafer-Stack

I also saw on a Nvidia talk that now with the disapperaing memory wall there would be a new wall, namely a memory power wall, exceeding 160W at 3.2TBytes/s just to fetch it.

http://wccftech.com/nvidia-pascal-volta-gpus-sc15/#ixzz4AEQhhFzp

So the solution would be to put the memory right on top of the executing circuits. Am i right or not?

@Retina - That seems to be the trend, bringing memory and compute as close as physically possible (I've even seen some that claim to merge the two concepts of memory and compute into one, to imitate a "neuron").


I would say the future of pathtracing is quite healthy already though, there is still so much room for algorithmic improvements, and GPUs are getting super fast. I also don't think we have to go entirely noise-free to have a viable realtime rendering, a little noise actually looks kind of good

Post a Comment