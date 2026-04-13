---
title: Arnold render to have full GPU acceleration in a few years
url: http://raytracey.blogspot.com/2011/01/arnold-render-to-have-full-gpu.html
author: Sam Lapere
published: '2011-01-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've come across this very interesting interview about Arnold render, Sony Image Works' primary production renderer for CG feature films:


Some excerpts from the interview:



Arnold render is a unidirectional path tracer, so it makes a perfect fit for acceleration by GPUs. "Maybe in a few years it will" could be a reference to Project Denver. When Project Denver materializes in future high-end GPUs from Nvidia, there will be a massive speed-up for production renderers like Arnold and other biased and unbiased renderers. The implications for rendering companies will be huge: all renderers will become greatly accelerated and there will no longer be a CPU rendering camp and a GPU rendering camp. Everyone will want to run their renderer on this super-Denver-chip. GPU renderers like Octane, V-Ray RT GPU and iray will have a headstart on this new platform. Real-time rendering (e.g. CryEngine 4) and offline rendering (e.g. Arnold) will converge much faster since they will be using the same hardware.


AMD and Intel will not sit still and recently launched Fusion and Sandy Bridge, which basically follow the same philosophy as project Denver, but coming from the other side: while Nvidia is adding CPU cores to the GPU, AMD and Intel are adding GPU cores to the CPU. Which approach is better remains to be seen, but I think that Nvidia will have the better performing product as usual. Eventually there will no longer be a distinction between CPUs and GPUs, since they will all be merged on the same chip: a few latency-optimized cores (today's CPU cores) which process the parts of the code that are inherently serial and are impossible to parallellize and thousands of throughput-optimized cores (today's GPU cores or stream processors), which handle the parallel parts of the code, all on the same chip using the same shared memory pool.


The coming years will be very exciting for offline and real-time graphics, in particular for raytracing based rendering. Photon mapping for example is a perfect candidate that could become real-time in a couple of years.



[http://www.3dworldmag.com/2011/01/07/pros-and-cons-of-gpu-accelerated-rendering/](http://www.3dworldmag.com/2011/01/07/pros-and-cons-of-gpu-accelerated-rendering/)Some excerpts from the interview:

"The first target for that backend is the CPU, and that’s what we’re using now in production. But the design goals of OSL include having a GPU backend, and if you were to browse on the discussion lists for OSL right now, you would see people working on GPU-accelerated renderers. So that could happen in future: that a component of the rendering could happen on the GPU, even for something like Arnold."

"it doesn’t make sense to cram the kinds of scenes we throw at Arnold every day, with tens of thousands of piece of geometry and millions of textures, at the GPU. Not today. Maybe in a few years it will."

Arnold render is a unidirectional path tracer, so it makes a perfect fit for acceleration by GPUs. "Maybe in a few years it will" could be a reference to Project Denver. When Project Denver materializes in future high-end GPUs from Nvidia, there will be a massive speed-up for production renderers like Arnold and other biased and unbiased renderers. The implications for rendering companies will be huge: all renderers will become greatly accelerated and there will no longer be a CPU rendering camp and a GPU rendering camp. Everyone will want to run their renderer on this super-Denver-chip. GPU renderers like Octane, V-Ray RT GPU and iray will have a headstart on this new platform. Real-time rendering (e.g. CryEngine 4) and offline rendering (e.g. Arnold) will converge much faster since they will be using the same hardware.

AMD and Intel will not sit still and recently launched Fusion and Sandy Bridge, which basically follow the same philosophy as project Denver, but coming from the other side: while Nvidia is adding CPU cores to the GPU, AMD and Intel are adding GPU cores to the CPU. Which approach is better remains to be seen, but I think that Nvidia will have the better performing product as usual. Eventually there will no longer be a distinction between CPUs and GPUs, since they will all be merged on the same chip: a few latency-optimized cores (today's CPU cores) which process the parts of the code that are inherently serial and are impossible to parallellize and thousands of throughput-optimized cores (today's GPU cores or stream processors), which handle the parallel parts of the code, all on the same chip using the same shared memory pool.

The coming years will be very exciting for offline and real-time graphics, in particular for raytracing based rendering. Photon mapping for example is a perfect candidate that could become real-time in a couple of years.

## 1 comment:

Stumbled upon this while googling for GPU rendering and Arnold after reading that the Blender Cycles developer (Brecht van Lommel) was hired by Solid Angle. You must have a crystal ball considering that you posted this in January 2011. Hats off!

Post a Comment