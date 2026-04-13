---
title: Optimizing Vulkan for AMD and the tale of two Vulkan drivers
url: https://anki3d.org/optimizing-vulkan-for-amd-and-the-tale-of-two-vulkan-drivers/
author: Panagiotis Christopoulos Charitos
published: '2018-05-08'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

The first GPU AnKi run, almost a decade ago, was in fact an ATI Radeon 9800 Pro. The first version of the deferred shading renderer run in that GPU and not only that. AnKi was running on Linux and the fglrx driver. I don’t remember experiencing many game breaking bugs back then, but then again, AnKi was quite simplistic at the time. One thing I remember was some depth buffer corruption that I had to workaround using a copy. Many years later I understood that this was a driver bug.

The love with ATI didn’t last long and AnKi end up being developed exclusively using nVidias. For many years AMD’s OpenGL driver didn’t have the quality or the features I wanted. Fast forward to today, things are looking far better. Firstly, Mesa has a quite decent OpenGL implementation, secondly, there is a very competitive Mesa Vulkan driver (RADV) and on top of that there is an second opensource Vulkan driver directly from AMD (AMDVLK). The cherry on top is a very good profiler for Vulkan and AMDVLK called Radeon GPU profiler. AMD regularly releases lots of documentation and optimization tips as part of their GPUOpen initiative. This is a great period to own AMD hardware for graphics development that’s why I had to get my hands on an AMD GPU.

In this post I’ll focus on some AMD specific optimizations and I’ll be comparing the two opensource Vulkan drivers.


# Initial impressions

The first thing that I’ve tried was to run a lightweight demo using RADV. For the most part it appeared correct but it was missing some geometry. I quickly realized that the H/W doesn’t support R16G16B16 formats for vertex attributes. This was an easy fix. The next issue was vertex related again and more precisely in the vertex tangents (more on that later).

After fixing the R16G16B16 issue I decided to try AMDVLK. Building and using it is very straightforward. Running AnKi though was crashing the driver so I decided get my hands dirty and debug. Building with debug symbols and running AnKi revealed some assertions deep into their LLVM compiler. After some back and forth with some AMD engineers ([github.com/GPUOpen-Drivers/AMDVLK/issues/27](https://github.com/GPUOpen-Drivers/AMDVLK/issues/27)) we’ve managed to fix my crash and make everything work fine.

The second issue I’ve bumped into was some excessive CPU usage inside AMDVLK. The perf profiler revealed a high number of page faults inside vkAllocateCommandBuffer. Apparently I had a bug in my command buffer recycling and I ended up creating more command buffers than I had to. What’s interesting is that nVidia’s Vulkan driver and RADV didn’t have any performance loss compared to AMD’s driver. That’s perfectly acceptable though since it was my fault.

The third issue is with VK_PRESENT_MODE_FIFO_KHR and AMDVLK. Even with FIFO AMDVLK has choppy frames. For that I haven’t found a solution yet. On the other hand RADV and nVidia run like butter so it might not be my fault.

Now I’ll go back to my tangent problem. In AnKi I encode the tangets in VK_FORMAT_A2B10G10R10_SNORM_PACK32 where alpha holds the sign of the bitangent. In RADV the result is always signed and in AMDVLK I was getting the compiler crash mentioned above. Maybe I missed the memo but I find VK_FORMAT_A2B10G10R10_SNORM_PACK32 quite convenient for storing tangents.

# Optimizing with Radeon GPU Profiler

At this point I’ll have to give credit to AMD because RGP is a well designed and a very intuitive tool. I really like the microscopic and macroscopic view of a frame. The fact that AMD had shared so many info about their architecture makes the interpretation of the results easy.

The first thing I noticed was some high VGRP (Vector General Purpose Register) usage for some of the render/compute passes. After some minor optimizations I’ve managed to decrease VGPR usage and increase occupancy.

The next thing I tried was to start using **control flow attributes** (unroll, loop, flatten, branch) since I already knew that AMD compiler makes use of those. HLSL and SPIR-V had support for those attributes since forever but GLSL only recently gained support (GL_EXT_control_flow_attributes extension). Using control flow arguments gave some easy gains in VGPR usage. In one occasion I had a graphics pipeline that was running in less than 8 waves. By adding a [[loop]] argument in a while loop in the fragment shader of that pipeline I managed to get the full 8 wave occupancy. At this point it’s worth noting that only AMDVLK supports those attributes and RADV ignores them. I dropped an email to the Mesa mailing list to ask them to add support but my request didn’t get far.

AnKi’s rendergraph batches the volumetric fog and SSAO passes together. Both of them were graphics passes with volumetic fog having very bad occupancy. To solve that problem I converted the SSAO pass to compute and I observed some nice overlapping that allowed those passes to saturate the GPU better. That decreased the overall time of the frame. The preferable solution would have been to run the SSAO in async compute but that will have to wait until the rendergraph gains support for multiple queues.

![](../../assets/5be9fffaa9022ab3.png)


![](../../assets/5be9fffaa9022ab3.png)

# AMDVLK vs RADV vs SPIRV-opt

AMD created a very neat Vulkan extension named **VK_AMD_shader_info**. This extension, among other things, provides various performance information for pipelines and more precisely register usage. Both AMDVLK and RADV support it just fine.

AnKi is using **glslang** to compile GLSL down to SPIR-V. glslang’s translation to SPIR-V is very naive and it relies on a library called **spirv-opt** to perform various transformations to the SPIR-V binary. spirv-opt is part of **SPIR-V tools** and its two primary functions are to legalize SPIR-V generated by various HLSL backends (glslang’s and M$’s DirectX shader compiler) and decrease the size of the generated SPIR-V. Lately, spirv-opt gained some more optimization passes targeting performance.

In my test I run (1) without spirv-opt, (2) with the default passes glslang has enabled for SPIR-V size reduction and legalization and (3) I also tried all performance optimization passes (see RegisterPerformancePasses() method in spirv-opt) and (4) finally without control flow attributes. I run my AnKi demo and dumped VGPR and SGPR for every pipeline it was creating. The demo created 250 different pipelines in total. At the end I summed up the register usage per pipeline stage. I haven’t tried to factor in the importance of the pipelines in the frame so these results only compare compilers and nothing more.

| Vert VGPRs | Vert SGPRs | Frag VGPRs | Frag SGPRs | Compute VGPRs | Compute SGPRs | |
|---|---|---|---|---|---|---|
| AMDVLK spirv-opt off | 3946 | 5116 | 5757 | 5658 | 176 | 240 |
| AMDVLK spirv-opt size | 3946 | 5116 | 5757 | 5658 | 175 | 264 |
| AMDVLK spirv-opt perf | 3946 | 5116 | 5757 | 5660 | 175 | 264 |
| AMDVLK no control flow args | 3946 | 5116 | 5848 | 6134 | 181 | 304 |
| RADV spirv-opt off | 5280 | 6250 | 3884 | 5040 | 196 | 248 |
| RADV spirv-opt size | err | err | err | err | err | err |
| RADV spirv-opt perf | err | err | err | err | err | err |

The first thing to note is that **spirv-opt passes have zero impact in register usage**.

The second interesting thing is that **RADV is crashing when spirv-opt is enabled**. I haven’t tried to find out which transformation is the culprit but when I have some time I may will.

Disabling control flow arguments increases register usage so go ahead and use them.

And now the interesting part. **RADV has higher VGPR usage on vertex and compute shaders and lower on fragment**. I’m not a compiler expert but this difference is quite weird given that both drivers use LLVM. It feels like vertex and fragment is swapped in RADV.

# Conclusion and I would like to see in the future

The jump to AMD proved less painful that I imagined. As we move forward and Vulkan becomes the defacto backend for AnKi, developing using AMD H/W becomes even more attractive. I would go even further and say that Vulkan developers should switch to Linux and get the benefit of having 3 opensource Vulkan drivers (counting Intel’s driver as well) to work with.

The second point that I’d like to make is that RADV is surprisingly competitive and stable. I’m really impressed with the work of its developers.

As for RGP, I’d like to see more information displayed especially around bandwidth. It seems that AMD completely disregards bandwidth and that is not very wise. ALU improves at a faster rate than bandwidth.

Nice post, but probably need some updating, because RADV is now basically outperforming AMDVLK, especially when using RADV-ACO. But even RADV-LLVM with most recent LLVM does really well.

AMDVLK is useful for older “enterprise” distros that can’t afford to update whole Mesa and LLVM stack in stable LTS branches, and when you need to use newest hardware quickly after release.

I guess, AMDVLK support for Radeon GPUProfiler is a added bonus. I hope Radeon GPUProfiler does support RADV & Mesa one day (maybe they don’t want to do that because it would be probably to easy also to profile Intel / anv driver maybe), and it would be nice overall.

Hi Wlktor, I was planning to do a followup since it’s an interesting subject. Unfortunately AMDVLK’s quality proved to be questionable and I gave up. I often find myself in a situation where something works on RADV, on AMD’s proprietary on Windows and on nVidia but it fails on AMDVLK. So even if we exclude performance, quality-wise RADV seems superior.

What I want to try is compare ACO and LLVM. Hopefully I’ll find some time.

There is some preliminary work to support GPUProfiler on RADV. Looking forward to it. https://www.phoronix.com/scan.php?page=news_item&px=RADV-Radeon-GPU-Profiler

Thank for sharing and it is interesting. In the post you said that VGPR and SGPR were dumped for every pipeline, and I also want to do that. Could you tell me how to do it?

Thanks.

Hi. AMD GPUs expose the VK_AMD_shader_info extension that can be used to dump a few shader information given a VkPipeline.

Thanks for the reply. I am using NVidia RTX card and it does not such extension. Do you know how to get such information using NVidia GPUs?