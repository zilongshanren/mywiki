---
title: GPU utilisation and performance improvements
url: https://interplayoflight.wordpress.com/2025/08/29/gpu-utilisation-and-performance-improvements/
author: Kostas Anagnostou
published: '2025-08-29'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Drill deep into a GPU’s architecture and at its heart you will find a large number of [SIMD units](https://www.rastergrid.com/blog/gpu-tech/2022/02/simd-in-the-gpu-world/) whose purpose is to read data, perform some vector or scalar ALU (VALU or SALU) operation on it and write the result out to a rendertarget or buffer. Those units can be found in what Nvidia calls Streaming Multiprocessors (SM) and AMD calls Workgroup Processors (WGP). Achieving good utilisation of the SIMD units and VALU throughput (i.e. keeping them busy with work) is critical for improving the performance of rendering tasks, especially in this era of increasingly wider GPUs with many SIMD units.

To read and write the data they operate on, the SIMD units interact with the rest of the GPU via a number of “fixed function” units, for example the TEX unit to serve data requests, the Register File to store temporary data (VGPRs), the ROP units to write to the rendertargets, a number of caches to store and read data from. This, for example, is the SM of Blackwell’s architecture, showcasing some of the units the VALU (FP32/INT32) units interact with ([source](https://images.nvidia.com/aem-dam/Solutions/geforce/blackwell/nvidia-rtx-blackwell-gpu-architecture.pdf)):

The fixed function units are fast, due the simple nature of their work, but they can still become a bottleneck and starve the VALU units from work, or block it from writing the results out. For that reason, an important part of a graphics programmer’s job is analysing rendering workloads (drawcalls and dispatches) and trying to remove the bottlenecks caused by the fixed function units mentioned above and others like Input Assembler (IA), Raster units, but also memory bandwidth etc, that will reduce VALU utilisation.

Sometimes, due to the nature of the rendering work, the bottlenecks that reduce VALU utilisation/throughput are harder to remove, for example a shadowmap pass would be light on VALU work and bottlenecked more by the IA (World Pipe) and memory (VRAM) which feeds it vertex data, so the SM throughput (code execution) will be low:

![](../../assets/9a19b00562cfc388.png)


![](../../assets/9a19b00562cfc388.png)

Another example would be a compute shader pass that makes a copy of a rendertarget or creates a depth mipchain, where there just isn’t enough work in the shader to keep the VALU units busy. In such cases to achieve the best result, we need to take a step back and view the GPU performance holistically, focusing not on the performance of a single rendering task (drawcall/dispatch) but across rendering tasks and measure improvement across the whole frame. In this blog post I am discussing a few techniques that we can use to achieve that. A disclaimer: the effectiveness of any performance optimisation work depends a lot on the target GPU, the shader compiler, the renderer and the content rendered and is quite hard to generalise. As always, take any advice with a pinch of salt and always profile your use case.

Quick intermission to discuss bottlenecks a bit, I mentioned them a lot, but how can one identify what is actually the bottleneck and what needs going after? Profiling tools like Nsight Graphics ([GPU Trace](https://developer.nvidia.com/blog/optimizing-vk-vkr-and-dx12-dxr-applications-using-nsight-graphics-gpu-trace-advanced-mode-metrics/)), [AMD Radeon Profiler](https://gpuopen.com/rgp/) and [PIX](https://devblogs.microsoft.com/pix/download/) are all good options. Using a profiling tool, the easiest way is to visualise the bottleneck is to graph the utilisation of each GPU unit. In the case of GPU Trace, where the screenshot I posted above is from, it is the various “throughputs” plotted. With such a view, it is easy to see that, for example, the shadowmap pass is mostly bound (meaning it uses that unit/resource the most) by VRAM (memory bandwidth) and vertex input (World Pipe). The GTAO pass is bound by the L2 cache and the ShadowMask pass (which calculates raytraced shadows), by the RT cores. This means that if we want to improve the performance of any of those passes, the main bottleneck is first thing we should go after.

So, to begin with, it is worth stressing that we should first make every effort to reduce the cost/increase VALU utilisation of a single, expensive, drawcall wherever possible, targeting its specific bottlenecks. If for example a drawcall is memory latency bound, i.e. the VALU instructions are waiting for memory to arrive, [increasing the occupancy](https://interplayoflight.wordpress.com/2020/11/11/what-is-shader-occupancy-and-why-do-we-care-about-it/) by reducing VGPR (vector register) allocation, or reworking the shader in order to allow more instructions between memory read issue and memory use by, for example, partially unrolling a loop would be something worth trying. Also, increasing the flow of data to unblock VALU by [packing](https://www.elopezr.com/the-art-of-packing-data/)/compressing shader input and output (this is true for all types of shaders, including vertex shader which the number of exported attributes could become a bottleneck on some GPUs) as well as observing data access patterns and adjusting the data structures used, for example a Structured Buffer [will perform better](https://developer.nvidia.com/content/how-about-constant-buffers) than a Constant Buffer for random access on Nvidia GPUs, are things that will pay off.

If the nature of the bottleneck is such that further performance improvement is not easy, further gains could still be possible, but the approach might be counter-intuitive. For example if the occupancy of a shader is very high this could lead to cache thrashing as different in-flight waves are trying to access the cache. In such cases, lowering the occupancy by either increasing the VGPR allocation (creating a dummy large dynamic branch that never gets taken is one approach), or in case this is a compute shader by performing a dummy groupshared memory (LDS) allocation. LDS allocation to restrict occupancy is preferable if possible, because leaving VGPRs free could be beneficial to some other task running in parallel to this one (on the same graphics pipe but also with Async Compute, more on that later). Increasing the VGPR allocation though could have other, positive, effects, the compiler might take advantage of this and batch texture loads at the start of the shader to reduce memory latency.

Another thing worth considering is what the most suitable shader type for a specific workload is. A pixel shader is part of the GPU’s geometry processing pipeline which means that it depends on fixed function units for inputs (rasteriser and data exported by the Vertex Shader) and output, the ROP units to write to rendertargets, so it can get bottlenecked by either. A screen-space, export bound pixel shader (blocked by the ROP units), or a pixel shader that has divergent execution (i.e. an early out for some pixels in the warp/wave) could benefit more as a compute shader, which is lacking all those dependencies. Additionally, compute shaders have access to another type of memory, groupshared memory (or Local Data Store), which can be used as an intermediate storage to share data between threadgroup threads and speed up execution a lot.

On the other hand, the pixel shader pipeline might have fast paths and functionality in place that don’t exist for compute shaders. For example GCN has a [dedicated cache (“Color cache”)](https://old.hotchips.org/wp-content/uploads/hc_archives/hc24/HC24-3-ManyCore/HC24.28.315-AMD.GCN.mantor_v1.pdf) in the Render Backend Unit to talk to the DRAM directly to read/write colour values, bypassing the L2 cache. This means that writing out to a rendertarget using a pixel shader might be faster than a compute shader as it frees up the L2 cache for other uses. This dedicated cache might not exist on other architectures though. A pixel shader can benefit from hardware VRS as well, reducing the cost, which is worth considering (although “[software VRS](https://interplayoflight.wordpress.com/2022/05/29/accelerating-raytracing-using-software-vrs/)” solutions are possible for compute shaders as well). Pixel shader output can be [DCC compressed](https://gpuopen.com/learn/dcc-overview/), something that might benefit memory bandwidth on subsequent reads of the rendertarget as a texture. Also, pixel shaders, full screen ones as well, can benefit from stencil operations, even depth operations, to speed up processing. Not spawning a wave is faster than spawning it an early-ing out (stopping shader execution due to a condition).

Work distribution differences between each shader type should also be factored in, when deciding where to move work to. For example, the GPU will allocate the whole threadgroup to a specific SM or WGP and all its warps/waves will be executed on the same SM/WGP. This is great for cache coherence and data locality purposes and can put the groupshared memory to good use, especially [for large threadgroups](https://gpuopen.com/learn/optimizing-gpu-occupancy-resource-usage-large-thread-groups/). On the other hand large threadgroups need more resources (VGPRs/LDS) to be available before spawning it on a SM/WGP, which might introduce contention and delays. Pixel shader waves are spawned more predictably, in a tiled fashion [based on screen location](https://developer.nvidia.com/content/life-triangle-nvidias-logical-pipeline) ([source](http://attila.ac.upc.edu/wiki/images/d/db/HPG10_Hot3D_Fermi.pdf)).

![](../../assets/40fc1fae550ce1a6.png)


![](../../assets/40fc1fae550ce1a6.png)

and might lead to faster execution. Moving VALU work to the vertex shader, to reduce pressure on a VALU bound pixel shader, is an option but it comes with caveats: cache coherence and data locality might not be great in a vertex shader due to the wave launch pattern (on GCN [it is one per Compute Unit](https://gpuopen.com/download/GDC2017-Advanced-Shader-Programming-On-GCN.pdf) for eg), vertex shader work that is done for culled triangles/pixels is wasted and also exporting data from the vertex shader to the pixel can become a bottleneck on some GPU architectures. With current triangle counts and densities, moving work to the vertex shader might be less appealing.

On some architectures, where there is a choice of wave size like on RDNA, the shader type might impact execution and performance as well. On RDNA compute shaders are runnning with 32 threads per wave (wave32) and pixel shaders are running with 64 (wave64). A shader that relies heavily on wave intrinsics might benefit more as a wave64 pixel shader as it can get more work done (64 work items as opposed to 32). Also, wave intrinsics is a better way to share data between threads than the groupshared memory mentioned earlier as it is stored in VGPRs, the fastest storage available to the SIMD. On the other hand shaders with divergent execution, eg (stochastic) screen space reflections, might perform better as a wave32 compute shader, as the wave will have a higher chance to finish and retire earlier with less threads. Worth mentioning that since [SM6.6 HLSL defines WaveSize ](https://microsoft.github.io/DirectX-Specs/d3d/HLSL_SM_6_6_WaveSize.html)for compute shaders, so that could be an option to increase the size as well, where supported.

Converting a workload to a compute shader has another potentially big advantage, it opens up the way for it to use [Async Compute](https://interplayoflight.wordpress.com/2025/05/27/async-compute-all-the-things/) to run in parallel to graphics pipe work (i.e. overlap vertex or pixel shader or even other compute shader execution). Async compute is a great tool to increase VALU utilisation, as it can overlap other, potentially fixed function unit bottlenecked passes and use the resource they can’t use. For example, a cache and SM bottlenecked pass (GTAO),

![](../../assets/306f2385f82ba7b7.png)


![](../../assets/306f2385f82ba7b7.png)

can be paired well with an RT Core bound pass (Shadowmask)

![](../../assets/7737b6e87aaee226.png)


![](../../assets/7737b6e87aaee226.png)

to use GPU resource that the pass can’t use. Async compute could also overlap other passes with low VALU utilisation like a z-prepass or a shadow pass which likely will be mainly bottlenecked by geometry throughput, or a pixel shader export bound pass (screen space but also gbuffer fill potentially, depending on the complexity of the material shaders). A couple of things worth considering here, there is currently no API exposed way to control the execution of an async compute task, in terms of priority, throttling to reduce impact on the graphics pipe etc (on DirectX 12, Vulkan exposes VK_AMD_wave_limits I believe), so async compute can have a negative impact on the graphics pipe which might be ok, as long as the 2 tasks running in parallel cost less in total than when running serially on the graphics pipe. Dummy LDS (or, less preferably, VGPR as this is more likely to affect wave launch on the graphics pipe as well) allocations and threadgroup size can be used to affect execution of the async compute task as well, for example small threadgroups will likely overlap better than larger ones, and it will take some experimentation to find the the correct configuration you a particular use case. Finally, on the topic of compute shader overlap and on some GPU architectures, compute work on the graphics pipe can overlap pixel/vertex shader work as long as there are no barriers.

Removing the fixed function and other bottlenecks and allowing the GPU to perform useful work is critical in order to achieve good rendering performance and there are a lot of tools and techniques at our disposal to achieve that, be it single drawcall/dispatch optimisation or overlapping work to take advantage of unused compute resource, even if it comes at an increased cost for the individual rendering tasks. With the large variety of GPU architectures in the market it is tricky to determine which approach will work best though, and it will take some trial and error to decide what works best in each use case as not all approaches will perform equally well on all GPUs.

**Further reading**

- RDNA Performance Guide
[https://gpuopen.com/learn/rdna-performance-guide/](https://gpuopen.com/learn/rdna-performance-guide/) - Advanced shader programming on GCN
[https://gpuopen.com/download/GDC2017-Advanced-Shader-Programming-On-GCN.pdf](https://gpuopen.com/download/GDC2017-Advanced-Shader-Programming-On-GCN.pdf) - Engine Optimization Hot Lap
[https://gpuopen.com/download/gdc_2018_sponsored_engine_optimization_hot_lap.pptx](https://gpuopen.com/download/gdc_2018_sponsored_engine_optimization_hot_lap.pptx) - Advanced API Performance: Shaders
[https://developer.nvidia.com/blog/advanced-api-performance-shaders/](https://developer.nvidia.com/blog/advanced-api-performance-shaders/) - Low-Level Optimizations in The Last of Us Part II
[https://s3.amazonaws.com/nd.images/research/2020_siggraph/Low_Level_Optimizations_In_TLOU2.pptx](https://s3.amazonaws.com/nd.images/research/2020_siggraph/Low_Level_Optimizations_In_TLOU2.pptx)

As ever, lots of specific, detailed info – thank you for continuing to archive and disseminate your knowledge in this practical, digestible format! :)

Great article!

Just a quick correction, when you say:

On RDNA 2 and above, any kind of shader (vertex, fragment, compute, mesh, etc.) can operate in both wave32 and wave64 modes. The mode is not dictated by the shader type. See the RDNA3 ISA (page 9) for reference.

Indeed, my point really was that the shader developer doesn’t control this, it is up to the driver to decide and at the moment it builds compute shaders as wave32 and pixel shaders as wave64 on PC as far as I can tell.

Yes, on PC the driver chooses automatically, and as you mentionned, the WaveSize HLSL attirbute is the only control we have on this right now and only for compute. On consoles it’s a different story though :)