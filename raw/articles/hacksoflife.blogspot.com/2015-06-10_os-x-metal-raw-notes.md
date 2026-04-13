---
title: OS X Metal - Raw Notes
url: http://hacksoflife.blogspot.com/2015/06/os-x-metal-raw-notes.html
author: Benjamin Supnik
published: '2015-06-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just a few raw notes about Metal as I go through the 2015 WWDC talks. This mostly discusses what has been added to Metal to make it desktop-ready.



The memory model is "common use cases" - that is, they give you a few choices:










Metal for desktop has instancing, sane constant buffers, texture barrier, occlusion query, and draw-indirect. It looks like it does not have transform feedback, geometry shaders or tessellation. (The docs do mention outputting vertices to a buffer with a nil fragment function, but I don't see a way to specify the output buffer for vertex transform. I also don't see any function attach points for geometry shaders or tessellation shaders.)

The memory model is "common use cases" - that is, they give you a few choices:

- Shared - one copy of the data in AGP memory (streaming/dynamic in OpenGL). Coherency is apparently at the command buffer, not continuous, so this apparently does not rely on map-coherent (and I would assume has lower overhead).
- Managed - what we have now for static geometry: a CPU side and GPU side copy that are synced. Sync is explicit by flushing CPU side changes (via didModifyRange). Reading back changes from the GPU is explicit -and- queued via a synchronizeResource call on the blit command encoder. For shared memory devices (e.g. Intel?) there's only one copy (e.g. this backs off to "shared").
- Private - the memory is entirely on the GPU side (possibly in VRAM) - the win here is that the format can be tiled/swizzled/whatever is fastest for the GPU. Therefore this is the right storage option for framebuffers. Access to/from the data is only from blit command encoder operations.
- Auto - a meta-format for textures - turns into shared on IOS (which has no managed) and managed on desktop - so that cross-platform code can do one thing everywhere. (This seems odd to me, because desktop apps will want to have
*some*meshes be managed too.)

There appears to be no access to the parallel command queues that modern GCN2 devices have. Modern GPUs can run blit/DMA operations in parallel with rendering operations; this uses the hardware more efficiently but also introduces an astonishing amount of complexity into APIs like Mantle that tell developers "here's two async queues - good luck staying coherent."

Perhaps Metal internally offloads blit command buffers to the DMA queue and inserts a wait in the rendering encoder for the bad-luck case where the blit doesn't finish enough ahead of time.

Unlike Mantle, there is no requirement to manually manage the reference pool for the resources that a command queue has access to - this also simplifies things.

Finally, Mantle has a more complex memory model; in Mantle, you get big pools of memory from the driver and then jam resources into them yourself, letting games create pool allocators as desired. In Metal, everything's just a resource; you don't really know how much VRAM you have access to or how stuffed it is, and paging the managed pool is entirely within the driver. (One exception: you can create a buffer

*directly*off of a VM page with no copy, but this still isn't the same as what Mantle gives you.)
As the guy who would have to code to these APIs, I definitely like Apple's simpler, more automatic model a lot more than the state change rules for Mantle; naively (having not coded it) it seems like the app logic to handle state change would be either very complex and finicky or non-optimal. But I'd have to know what the cost in performance is of letting the driver keep these tasks. Apple's showing huge performance wins over OpenGL, but that doesn't validate the idea of driver-managed resource coherency; you'd have to compare to Mantle to see who should own the task.

I can imagine AAA game developers being annoyed that there isn't a pooling abstraction like in Mantle, since the "pool of memory you subdivide" model works well with what console games do on their own to keep memory use under control.

Overall, based on what I've read of the API, Metal looks a solid, well-thought-out next generation API; similar to Mantle in how it reorganizes work-flow, but less complex. It's still missing some modern desktop GPU functionality, but moving Metal to discrete hardware with discrete memory hasn't turned the API into a swamp.

Finally, from an adoption stand-point: it looks to me that Metal on OS X gives Apple a way to try to leverage its strong position in mobile gaming to move titles to the desktop, which is a more viable sell than trying to use a more modern OpenGL to move titles from PC. (Only having a DirectX clone would help with that.)

Regarding Metal's support for geometry shaders and transform feedback — my understanding is that you can combine compute and graphics shaders into a single command buffer, so you could use a compute shader to alter the geometry and store it in a private buffer, then use graphics shaders to render that buffer.

ReplyDeleteCertainly for transform feedback, I would expect you can use compute as a drop-in replacement.


DeleteGeometry shaders and the tessellator are both interesting because they give you streaming at a not 1:1 ratio without having to use atomic counters from a compute shader. Certainly in the case of the tessellator you can get huge amounts of geometry amplification with very little speed penalty, something that would be hard to do from a compute shader I think.