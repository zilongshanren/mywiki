---
title: Porting AnKi to Vulkan part 2
url: https://anki3d.org/porting-anki-to-vulkan-part-2/
author: Panagiotis Christopoulos Charitos
published: '2017-05-16'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

In my [Porting AnKi to Vulkan](https://anki3d.org/porting-anki-to-vulkan/) post I went into detail describing how AnKi’s interfaces changed to accommodate the Vulkan backend and how this backend looked like. Eight months have passed since then and a few things changed mainly towards greater flexibility. This post describes what are the differences with the older interfaces, how is the performance currently and what new extensions AnKi is using now.


# Pipelines

The first thing that was changed is how static state is handled. Previously, the pipelines mapped almost exactly to VkPipeline and they were exposed as an individual object by the graphics abstraction. That was ofcource quite optimal but it caused some headaches. The first issue was with materials. Materials were and still hold a view of the shaders. Previously they were holding the pipelines as well and that forced them to know all kinds of state. State that was tightly coupled with the renderer. Another issue was with image layouts and permutations. Having to track image layouts to permutate on input was quite challenging.

So for the new interface I removed the pipeline object from the public interfaces and introduced the **shader program object**. The shader program accepts only the shaders when initialized. Internally though it holds a cache of pipelines. The rest of the state was moved to the command buffer. The command buffer now has a number of setters for state (like setPrimitiveRestart or setDepthCompareOperation) that internally update a state tracker. At drawcall time, the state tracker communicates with the shader program to retrieve from the cache or create new pipelines.

# Descriptor sets

Previously, the descriptor sets were unique objects just like the pipelines. Again due to low flexibility and high maintenance cost the descriptor sets were removed from the public interface altogether. Now there are bindXXX methods for buffers and textures that bind directly to the command buffer. On every drawcall there are some light dirty bit checks and if the descriptors have changed then we retrieve a descriptor set from a cache or create a new one.

Unfortunately there is no object that can hold this descriptor set cache in a similar fashion to shader program and because of that I had do create a complex caching mechanism. So, there is a descriptor set cache that is global and provides per-thread caching of descriptor sets. The command buffer does some state tracking and requests a descriptor set from that global cache. The downside of this system is that it’s a bit complex especially when recycling descriptors.

# New extensions

After the initial Vulkan release lots of new extensions started to appear. Most of them are not relevant to AnKi, at least at the moment, but some of them offer some interesting new possibilities.

The first extension that is currently mandatory is **VK_KHR_maintenance1**. This extension fixes (to some degree) the viewport flip problem. How it works now is that on every offscreen render pass I just render the image flipped but with opposite polygon winding (in AnKi winding is not configurable and it’s always counter-clockwise but for Vulkan offscreen render passes I use clockwise). When rendering to the swapchain image though the winding goes back to normal and I use a feature of VK_KHR_maintenance1 that allows me to flip the viewport by negating the viewport height.

The next interesting extension is the **VK_NV_dedicated_allocation**. Apparently there is some hardware out there that supports implicitly handled framebuffer compression. Vulkan has the option to potentially alias memory and that seems to prevent the use of this compression scheme. **VK_NV_dedicated_allocation** allows dedicated allocations for objects and AnKi makes use of that extension on all of its framebuffer textures. Using this extension for all framebuffer images gives a 10FPS uplift (from 75FPS to 85FPS) on an nVidia 1060.

One interesting development is that RADV driver (unofficial Vulkan driver for AMD GPUs) also gained support for **VK_NV_dedicated_allocation**. That makes me wonder why **VK_NV_dedicated_allocation** is useful for AMD since image layouts were specifically designed to sutisfy AMD’s framebuffer/texture compression/decompression scheme.

# Performance

I haven’t managed to run many performance tests or try different HW yet but on nVidia and for **GPU bound** scenarios GL and Vulkan are almost identical. More specifically, on an nVidia 1060 and at 4K resolution the performance between the two APIs is the same. On a nVidia 760 and at 1440p Vulkan is 9% slower. Overall this is quite promising given the fact that I haven’t used a profiler for the Vulkan backend at all.