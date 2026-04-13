---
title: One More On VBOs - glBufferSubData
url: http://hacksoflife.blogspot.com/2010/02/one-more-on-vbos-glbuffersubdata.html
author: Benjamin Supnik
published: '2010-02-28'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[timing of VBO updates](http://hacksoflife.blogspot.com/2010/02/double-buffering-part-2-why-agp-might.html)(or rather, my speculations on what is possible with VBO updates), now you're in a position to ask the question: how fast might glBufferSubData be? In particular, developers like myself are often astonished when glBufferSubData does things like block.

In a world before manual synchronizing of VBOs (via the 3.0 buffer management APIs or Apple's buffer range extensions) we can now see why a sub-data buffer on a streamed VBO might perform quite badly.

The naive code goes something like this:

- Fill half the buffer with buffer sub-data.
- Issue a draw call to that half of the buffer.
- Flip which half of the buffer we are using and go back to step 1.

This implementation is going to perform terribly. T sub-data call is going to block until the previous draw call has completed, even though they use opposite halves of the buffer, and we'll lose all of our concurrency. Let's see if we can understand why.

If we go to respecify a VBO in AGP memory using glBufferSubData while that VBO is in progress, glBufferSubData must block; it can't rewrite the buffer until the last draw finishes because we would see the new vertices, not the old, or maybe half and half. In order for the "fill" to complete, the driver would have to be able to determine that the pending draws and the new fill are completely disjoint.

There are two reasons why the driver might not be able to figure this out:

- You've drawn using glDrawElements, and thus the actual part of the vertex VBO you draw from is determined by the index table. The cost of figuring out the "extent" of this draw is to process all of the indices. The cure is worse than the disease. Any sane driver is going to simply assume that
*any*part of the VBO could be used. - Let's assume you use glDrawRangeElements to tell the driver that you're really only going to use half the VBO. Even then, the structure to mark "locked" regions would be a complex one - a series of draws over overlapping regions would require a complex data structure. For this one special case, you're asking the drivers to replace a simple time-stamp based lock (e.g. this VBO is locked until this many commands have executed) with a dynamic range marking structure. If I were a driver writer I'd say "let's keep it simple and not eat this cost on all VBOs."

Can we do anything about this? Besides falling back to an "orphaned" approach where we get a fresh buffer each time, our alternative is to use the more exact APIs from

[ARB_map_buffer_range](http://www.opengl.org/registry/specs/ARB/map_buffer_range.txt)or

[APPLE_flush_buffer_range](http://www.opengl.org/registry/specs/APPLE/flush_buffer_range.txt). With these APIs we can map only the part of the VBO we know is not in use, with the unsynchronized bit set to avoid blocking because the other half is pending. We can use flush explicit to then flush only the areas we modified. (With the 3.0 APIs we can also use the discard range option to simply say "we are rewriting what we map".)

Of course, this technique isn't without peril - all synchronization is up to the client. The main danger is an over-run: your app is so fast that it needs to modify a range that the GL isn't done with - we made it all the way around our ring buffer. Probably the safest way to cope with this is to put explicit fences in place to wait until the last dependent draw call that we issued is finished.

There is really only a need for fences if you want to re-write data in place or do changes on a subsection of a buffer.






ReplyDeleteThe workloads I am used to dealing with, have a variety of batch sizes coming out of client code.

The pattern we would use to deal with them efficiently, once we had the capability of non-blocking map, was to just follow the DirectX style - keep an ascending cursor, and pack subsequent batches into the same buffer until reaching the end, at which point it would be time to orphan. In this fashion, when using a 2 or 4MB buffer, it wasn't uncommon for maps/write/unmaps to outnumber orphaning events by 100 to 1.

If you follow this pattern, and do not have workloads that entail altering already-written data for a followup batch - there is no need for fences or any sync mechanism at all - the orphaning takes care of everything.

On OS X I'm not currently aware of any mechanism involving a VBO where the data does not land in system memory first, but maybe this has changed in Snow Leopard.

When we were working on MapBufferRange, one of the common questions was "why is BufferSubData not good enough?" - one of the key reasons is that BufferSubData must assume the original data is in a copyable form. If the CPU is unpacking something - for example, the height field data that WoW uses for terrain chunks - BufferSubData would only be useful if the CPU first expanded said data into a temp buffer and then BSD'd from there - yielding unwanted cache pollution..

An OpenGL.org thread going on about this that's relevent:



ReplyDeleteVBOs strangely slow?

The posts at the end being the most interesting, particularly Rob's.

paranoidatwork = Rob :)


ReplyDeleteSeems like this topic has been popping up more, that's for sure.