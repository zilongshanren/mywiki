---
title: Double-Buffering VBOs
url: http://hacksoflife.blogspot.com/2010/02/double-buffering-vbos.html
author: Benjamin Supnik
published: '2010-02-24'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One more bit of background: I don't know

*squat*about Direct3D. I have never worked on Direct3D applications code, I have never used the API, and I couldn't even list all of the classes. I only became aware of D3D's locking APIs recently when I found some comparisons between OGL and D3D when it comes to buffer management. So whatever I say about D3D, just assume it's wrong in subtle ways that are important but hard to detect.

If you only want to draw a mesh, but never change it, life is easy.

- Create a static-draw VBO.
- Fill it with geometric goodness with glMapBuffer or glBufferData.
- Draw it many times.
- Hilarity ensues.

*every frame*. So you do some math and realize that PCIe buses are really quite fast and this is a non-issue. Yet the actual performance isn't that fast.

The non-obvious cost is synchronization. When you map your buffer to place the new vertices using glMapBuffer, you're effectively waiting on a mutex that can be owned by you or the GPU - the GPU will keep that lock from when you issue the draw call until the draw call completes. If the GPU is 'running behind' (that is, commands are completing significantly later than they are issued) you'll block on the lock.

Why is there a lock that we can block on? Well, there are basically two cases:

- The "AGP" case: your VBO lives in system memory and is visible to the GPU via the GART. That is, it is mapped into the GPU and CPU's space. In this case, there is only one buffer, and changing the buffer on the CPU will potentially change the buffer before the draw happens on the GPU. In this case we really do have to block.
- The "VRAM" case: your VBO lives in both system memory and VRAM - the system memory is a backup/master copy, and the VRAM copy is a cached copy for speed. (This is like a "managed" resource in D3D, if I haven't completely misinterpreted the D3D docs, which I probably have.)

D3D works around this with D3DLOCK_DISCARD. This tells the driver that you want to completely rebuild the buffer. The driver then hands you a possibly unrelated piece of memory to fill in, rather than waiting for the real buffer to be available for locking. The driver makes a note that when the real draw operation is done, the buffer's "live" copy is now free to be reused, and the newly specified buffer is the "live" copy. (This is, of course, classic double-buffering.)

You can achieve the same effect in OpenGL using one of two techniques:

- If you have OpenGL 3.0 or
[GL_map_buffer_range](http://www.opengl.org/registry/specs/ARB/map_buffer_range.txt)you can use the flag GL_MAP_INVALIDATE_BUFFER_BIT on your glMapRange call to signal that the old data can be discarded after GPU usage. - You can simply do a glBufferData with NULL as a base pointer before you map. Since the contents of the buffer are now undefined, the implementation is free to pull the double-buffering optimization. (See the discussion of DiscardAndMapBuffer in the
[VBO extension spec](http://www.opengl.org/registry/specs/ARB/vertex_buffer_object.txt).)

The glMapBufferRange functionality in GL3 has essentially been available on MacOS X since 10.4.7 via the APPLE_flush_buffer_range extension. It allows you to do two things:






ReplyDeletea) disable the blocking behavior on map (but you must accept responsibility for sync/scheduling) - BUFFER_SERIALIZED_MODIFY_APPLE

b) disable the cache flush of the entire buffer at unmap time. This makes a modest difference on x86 and a big difference on PowerPC (though PowerPC did not get this extension until Leopard) -

BUFFER_FLUSHING_UNMAP_APPLE

When you use (b), you will also make an extra call to tell GL which areas you wrote to, before unmapping. That way any ditty cache lines in the CPU can be pushed out and/or any other platform specific coherency things need to be done to make the data GPU visible.

The reason glMapBufferRange is different in GL 3.0 is that it had to encompass more implementations such as GL on Windows and Linux operating under different implementation constraints, a big one being whether every VBO is client memory mirrored or not.

Rob rbarris "at" gmail.com

This comment has been removed by the author.

ReplyDeleteOf course, Rob is 100% right - not surprising, as he is a co-author of the map-buffer-range extension. :-)



ReplyDeleteWe ended up not relying on 'mirroring' of meshes in system memory in our app because while it performed well on some implementations, it didn't perform well on others - in some cases a non-blocking read-only map to "inspect" a mesh would give us a nice fast host copy, and in others we'd get what I can only speculate was some kind of uncached memory, and the actual CPU use of the data would be dreadful.

We decided it was cheaper to burn a little RAM to keep our own copy in those few cases where the data _had_ to be fast and tell the GL "no, you keep the data in VRAM, we don't want it."