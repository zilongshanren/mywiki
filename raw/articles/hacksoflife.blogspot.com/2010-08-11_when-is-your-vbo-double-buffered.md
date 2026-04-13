---
title: When Is Your VBO Double Buffered?
url: http://hacksoflife.blogspot.com/2010/08/when-is-your-vbo-double-buffered.html
author: Benjamin Supnik
published: '2010-08-11'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[three](http://hacksoflife.blogspot.com/2010/02/double-buffering-vbos.html)

[part](http://hacksoflife.blogspot.com/2010/02/double-buffering-part-2-why-agp-might.html)

[post](http://hacksoflife.blogspot.com/2010/02/one-more-on-vbos-glbuffersubdata.html)trying to explain why you never get double-buffered behavior from a VBO unless you orphan it. This is going to be an attempt to explain the issues more succinctly and describe how to stream data through a VBO.

The Problem

The problem that OpenGL developers (myself included) crash into is a stall in the OpenGL pipeline when trying to specify vertex data that changes every frame. You go preparing new VBOs of meshes (for a particle system for example), and when you go into your favorite adaptive sampling profiler, you find that you're blocking in one of glMapBuffer or glBufferSubData.

The problem is that the GPU has a "lock" on your VBO until it finishes drawing from it, preventing you from changing the VBO's contents. You can't put the new mesh in there until the GPU is done with the old one.

To understand why this happens, it helps to play "what if I had to write the GL driver myself" and look at what a total pain in the ass it would be to fix this at the driver level. In particular, even if you did the work, your GL driver might be slower in the general case because of the overhead to be clever in this case.

Your VBO Isn't Really Double-Buffered

Sometimes VBOs are copied from system memory to VRAM to be used. We might naively think that if this were the case, then we could gain access to the original system copy to update it while the GPU uses the VRAM copy.

In practice, this would be insanely hard to implement. First, this scheme would only work when VBOs are being shadowed in VRAM (not the case a lot of the time) and when the VBO has already been copied to VRAM by the time we need to respecify its contents.

If we haven't copied the VBO to VRAM, we'd have to stop and block application code while we DMA the VBO into VRAM (assuming the DMA engine isn't busy doing something else). If DMA operations on the GPU have to be serialized into the general command queue, that means the DMA operation isn't going to happen for a while.

If that hasn't already convinced you that treating VRAM vs. main memory like a double buffer makes no sense, consider also that if main memory is to be released, the VRAM copy is no longer a cached shadow, it is now the only copy! We now have to mark this block as "do not purge". So we might be putting more pressure on VRAM by relying on it as a double buffer.

I won't even try to understand the complexity that a pending glReadPixels into the VBO would have. It should be clear at this point that even if your VBO seems double buffered by VRAM, for the purpose of streaming data, it's not.

Your VBO Isn't Made Up of Regions

You might not be using all of your VBO; you might draw from one half and update the other. glBufferSubData won't figure that out. In order for it to do so, it would have to:

- Know the range of the VBO used by all pending GPU operations. (This is in theory possible with glDrawElementsRange, but not the older glDraw calls.)
- Track the time stamp of each individual range to see how long we have to block for.

One Way To Get a Double Buffer

The one way to get a double buffer on older OpenGL implementations is to re-specify the data with glBufferData and a NULL pointer. Most drivers will recognize that in "throwing out" the contents of your buffer, you are separating the contents of the buffer for future ops from what is already in the queue for drawing. The driver can then allocate a second master block of memory and return that at the next glMapBuffer call. The driver will throw out your original block of memory later at an unspecified time once the GPU is done with it.

Alternatively, if you are on OS X or have a GL 3.0 extension, there are extension that let you check out and operate on a buffer with locking suspended, allowing you to manage sub-regions in your buffer independently.

My typical approach on this problem is, to use double buffers, i.e. for every geometry with dynamic vertices I allocate two distinct VBOs and manipulate them alternating. This may sound memory consuming at first, but in your typical scene there is not so much dynamic geometry; mostly it's particle systems; most meshes are static.

ReplyDelete