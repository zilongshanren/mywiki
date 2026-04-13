---
title: glMapBuffer No Longer Cool
url: http://hacksoflife.blogspot.com/2015/06/glmapbuffer-no-longer-cool.html
author: Benjamin Supnik
published: '2015-06-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**TL;DR:**when streaming uniforms, glMapBuffer is not a great idea; glBufferSubData may actually work well in some cases.

**I just fixed a nasty performance bug in X-Plane, and what I found goes directly against stuff I posted here, so I figured a new post might be in order.**


[A long time](http://hacksoflife.blogspot.com/2010/02/one-more-on-vbos-glbuffersubdata.html)ago I more or less wrote this:

- When you want to stream new data into a VBO, you need to either orphan it (e.g. get a new buffer) or use the new (at the time) unsynchronized mapping primitives and manage ranges of the buffer yourself.
- If you don't do one of these two things, you'll block your thread waiting for the GPU to be done with the data that was being used before.
- glBufferSubData can't do any better, and is probably going to do worse.

Everything about not blocking on the GPU with map buffer is still true - if you do a synchronized map buffer, you're going to block hard. Never do that!

But...these days on Windows, the OpenGL driver is running in a separate thread from your app. When you issue commands, it just marshals them into a FIFO as fast as it can and returns. The idea is to keep the app rendering time and driver command buffer assembly from being sequential.

The first problem is: glMapBuffer has to return an actual buffer pointer to you! Since your thread isn't actually doing real work, this means one of two things:

- Blocking the app thread until the driver actually services the requests, then returning the result. This is bad. I saw some slides a while back where NVidia said that this is what happens in real life.
- In theory under just the right magic conditions glMapBuffer could return scratch memory for use later. It's possible under the API if a bunch of stuff goes well, but I wouldn't count on it. For streaming to AGP memory, where the whole point was to get the
*real*VBO, this would be fail.

*isn't that fast*. We still push some data into the driver via client arrays (I know, right?) because when measuring unsynchronized glMapBufferRange vs just using client arrays and letting the driver memcpy, the later was never slower and in some cases much faster.*

#### Can glBufferSubData Do Better?

Here's what surprised me: in at least one case, glBufferSubData*is*actually pretty fast. How is this possible?

A naive implementation of glBufferSubData might look like this:

void glBufferSubData(GLenum target, GLintptr offset, GLsizeiptr size, const GLvoid * data)

{

GLvoid * ptr = glMapBuffer(target,GL_WRITE_ONLY);

memcpy(ptr, data, size);

glUnmapBuffer(target);

}

The synchronized map buffer up top is what gets you a stall on the GPU, the thing I was suggesting is "really really bad" five years ago.

But what if we want to be a little bit more aggressive?

void glBufferSubData(GLenum target, GLintptr offset, GLsizeiptr size, const GLvoid * data)

{

if(offset == 0 && size == size_of_currently_bound_vbo)

glBufferData(target,size,NULL,last_buffer_usage);

GLvoid * ptr = glMapBuffer(target,GL_WRITE_ONLY);

memcpy(ptr, data, size);

glUnmapBuffer(target);

}

In this case, we have, in the special case of

*completely*replacing the VBO, removed the block on the GPU. We know it's safe to simply orphan and splat.

What's interesting about this code is that the API to glBufferSubData is one-way - nothing is returned, so the code above can run in the driver thread, and the inputs to glBufferSubData can easily be marshaled for later use. By keeping the results of glMapBuffer private, we can avoid a stall.

(We have eaten a second memcpy - one to marshall and one to actually blit into the real buffer. So this isn't great for huge amounts of data.)

Anyway, from what I can tell, the latest shipping drivers from NVidia, AMD and Intel all do this - there is no penalty for doing a full glBufferSubData, and in the case of NVidia, it goes significantly faster than orphan+map.

A glBufferSubData update like this is sometimes referred to as "in-band" - it can happen either by the driver queuing a DMA to get the data into place just in time (in-band in the commands stream) or by simply renaming the resource (that is, using separate memory for each version of it).

#### Using glBufferSubData on Uniforms

The test case I was looking at was with uniform buffer objects. Streaming uniforms are a brutal case:- A very small amount of data is going to get updated nearly every draw call - the speed at which we update our uniforms basically
*determines*our draw call rate, once we avoid knuckle-headed stuff like changing shaders a lot. - Loose uniforms perform quite well on Windows - but it's still a lot of API traffic to update uniforms a few bytes at a time.
- glMapBuffer is almost certainly too expensive for this case.

- glBufferSubData does appear to be viable. In very very limited test cases it looks the same or slightly faster than loose uniforms for small numbers of uniforms. I don't have a really industrial test case yet. (This is streaming - we'd expect a real win when we can identify static uniforms and not stream them at all.)
- If we can afford to pre-build our UBO to cover multiple draw calls, this is potentially a big win, because we don't have to worry about small-batch updates. But this also implies a second pass in app-land or queuing OpenGL work.**
- Another option is to stash the data in attributes instead of uniforms. Is this any better than loose uniforms? It depends on the driver. On OS X attributes beat loose uniforms by about 2x.

I'm working on a comprehensive test engine now to assess performance on every driver stack I have access to. When I have complete data, I'll write up a post.

* The one case that is pathological is the AMD Catalyst 13-9 drivers - the last ones that support pre-DX11 cards. In those cards, there is no caching of buffer mappings, so using map buffer at high frequency is unshipable. The current AMD glMapBuffer implementation for DX11 cards appears to have similar overhead to NVidia's.

* This is a case we can avoid in the next-gen APIs; since command buffers are explicitly enqueued, we can leave our UBO open and stream data into it as we write the command buffer, and know that we won't get flushed early. OpenGL's implicit flush makes this impossible.

What I'm missing in the post is any reference to GL_MAP_PERSISTENT_BIT. Have you tried that?

ReplyDeleteI haven't tried that yet - it's on my todo list for the next factor of the code - trying persistent mapping, map buffer range, pre-filling, and in-band buffer subdata. I am hopeful that map-persistent will be a top performer while having good flexibility. I'll post the results when I get them.

ReplyDeleteindeed glMapBuffer is not so cool... unless persistent.





ReplyDeletehad pretty good results with persistent for vertex data streaming. N buffers recycled every N frames. Make sure to omit the MAP_READ and COHERENT bits, as they may trigger slower type of memory on NVIDIA.

subdata is quite optimized for UBOs see http://on-demand.gputechconf.com/siggraph/2014/presentation/SG4117-OpenGL-Scene-Rendering-Techniques.pdf

there is also some core principles of next-gen apis already available in GL http://on-demand.gputechconf.com/gtc/2015/presentation/S5135-Christoph-Kubisch-Pierre-Boudier.pdf

First, thanks for the links. It does look like you can cobble together pretty good perf on modern GPUs via a mix of map-persistent and other extensions.






DeleteI'm not sure how much it will matter - from what I can tell, the hardware capable of providing persistent VBO mappings is also the hardware that will run Vulkan.

A year ago, OpenGL modernization was on my radar - let's get to 4.0, take advantage of persistent buffers, sparse memory, be AZDO-ish, etc.

At this point my thinking is much more "let's replace the back-end with Vulkan and Metal." The problem is that these kinds of extensions can spot-fix particular bugs (like map buffer causing chaos with a threaded driver) but can't fix the fundamental problem that GL's threading model is extremely hostile to multi-core.

At this point multi-core affects us twice:

- We'd really like to be able to use multiple cores to enqueue command buffers in parallel - and we have lots of good use cases for that.

- The unpredictability of core scheduling with driver threads is biting us. I have users turning off multi-threaded drivers (which is sad since they do boost perf for real) because we end up over-committed on cores.

Back when I was an OGL driver engineer, we'd have debates between using MapBuffer[Range] and Buffer[Sub]Data. For our implementation, we definitely preferred Buffer[Sub]Data, because of our multi-threaded driver. However, our DevTech wanted us to promote MapBuffer[Range], because it followed along with the D3D way of doing things for porting reasons (as D3D promoted using Map). But D3D had the advantage of the D3D10_MAP_FLAG_DO_NOT_WAIT bit, which is functionality that OGL did not expose.


ReplyDeleteOn top of that, we had the fun of developers conflating D3D10_MAP_FLAG_DO_NOT_WAIT with GL_MAP_UNSYNCHRONIZED_BIT, which was...awesome.

Right - theoretically in a threaded world, buffer-sub-data could do some kind of in-band scheduled update or at least copy the data until a map will no longer sync the driver and app thread. The problem is, of coarse, the $1,000,000 problem with the GL eco-system...app developers have no guarantees that there are (or are not) driver threads, or that buffer-sub-data is in-band (or out-of-band).


DeleteSuffice it to say, while it's not public to the little people (like me) how Vulkan will handle this, just having a clear spec on what is blocking vs unsynchronized, etc. will be a huge win.

I think cycles spent on checking out DX12 would be cycles well spent ;) ! Right now, DX12 has the concept of an "upload" heap, which would be GPU memory mapped for CPU write. Then you'd use this heap to upload buffer/texture updates to GPU-only memory. In some of the samples, they do keep some chunks of memory in this Update heap (index buffers, some constant buffer), but the documentation doesn't really cover what is best practice in these areas. Well, at least their samples don't totally jive with it.




Deletehttps://msdn.microsoft.com/en-us/library/windows/desktop/dn770374(v=vs.85).aspx

I've read the Mantle programming guide maybe twice now, and what they have is similar: they expose the idea that your textures are going to have to go through the command processor (maybe on a DMA queue for new hw that has that) so that the hardware can do tile twizzling on the image format. You can never directly map the image since it's not linear, etc. etc.








ReplyDeleteThe mantle stuff is vague on constant buffers too - it appears that there is:

1. A slow path when you have to update your descriptor table - the rules for mapping and unmapping descriptor tables are strict so they're only going to be fast if you can write out one giant descriptor table and use it for a big chunk of the frame.

2. A fast path for changing -one- memory descriptor - you apparently get to edit one memory descriptor on the fly - this could be a fast path for changing the window for constants that are streaming per-draw.

For DX12, you can update the root signature quickly per draw call, in theory...I've read a bunch of IHV recommendations and they're totally all over the map. :-)

I looked at the GCN docs and it looks like you can get 16 D-words loaded directly into a vertex shader from the command processor (the SH user regs) and vary their contents per-draw call cheaply. So I'm guessing that:

- Mantle uses two of them as a base pointer to the dynamic descriptor and

- DX12 maps the first 16 d-words of the root signature there.

Anyway, my assumption is that we'll definitely be able to:

1. Write high-frequency-update uniforms directly to a persistently mapped buffer, and

2. cheaply move the base pointer per draw call.

My guess is that it will not be practical to push per-draw call info "in-band" due to pressure on the very small amount of data the hardware can manage per draw call.

- 16 d-words doesn't go very far as attributes on AMD hw.

- It looks like the Intel hw has to window the whole root signature and therefore making it bigger gets expensive.

- I don't know what the green team has under the hood.

Speaking of register pressure, will instanced attributes act any differently? I tried placing 24 floats in 6 instanced attributes, and it was faster than fetching from an array within a uniform buffer by gl_InstanceID.

ReplyDeleteThat doesn't surprise me a ton. While theoretically on some hardware an instance-based lookup and an instanced attribute are doing 'the same work', they're sort of different in implementation.







DeleteWhen you use shader code in gl_InstanceID, you're implementing the lookup yourself.

When you use vertex-array-divisor, you're telling the driver what your -intent- is and letting the driver guys write the shader code (if needed) using special instructions (if they exist) and/or using dedicated fetch hardware.

My expectation is that any time I get in a speed contest with the driver team for a bit of implementation, they are going to kick my ass unless I can seriously cheat (e.g. solve a simpler problem that they can't special case for).

In terms of what is actually going on, who knows...this kind of thing can be very sensitive to hardware and driver stack. Some possibilities:

- The memory space of your vertex data may not be the same as your UBO - e.g. the driver might have a policy of DMAing VBOs into VRAM ahead of time using an async DMA controller, while reading the UBO might be reading over the PCIe bus.

- The caching of the UBO vs the vertex data might be different - hardware is moving more toward a unified cache, but there are still often fast paths and slow paths, which can vary by instruction.

If it would be more useful to use gl_InstanceID indexing, try a texture buffer object - from what I can tell, they were basically invented to let you use that fast, highly cached texture-sampling hardware to pull arbitrary read-only data into your shader with good caching. :-)

Or just stick with vertex-array-divisor...since it's a not-crazily-written part of the core spec, I would expect it to function well in a lot of places. We use it very heavily in X-plane and at this point it works well on both red and green hardware.

(I hope you don't mind me commenting on this old Blogpost)



ReplyDeleteThe pseudocode for the more aggressive version of glBufferSubData() made me wonder if there is a (semantical and practical, from common implementations) difference between glBufferSubData(target, 0, fullsize, data) and glBufferData(target, data, fullsize, last_buffer_usage)?

Related: Does doing glBufferData() with data=NULL and then glMapBuffer() + memcpy() (like you did) have any advantage over just calling glBufferData() with the actual data directly? (I'd imagine the libGL doing the same thing internally in both cases, but I'm quite new to OpenGL and graphics programming in general so my mental model of the whole thing is probably pretty flawed)

You're better off using glBufferSubData if you know at the app level that it's okay. The _best case_ of using glBufferData is that the driver spends its time figuring out that you should have used glBufferSubData and you get the same 'faster path' after spending more CPU cycles. The worst case is the driver doesn't figure it out and just does a full reallocation of the VBO.




DeleteIn cases like this where one set of functionality is a strict subset, if you have app knowledge to save the driver time, use it.

To rephrase the second question, orphan + map vs glBufferSubData, I think it's going to vary by driver stack - my suggestion is to set your code up to do both - if your code can use glBufferSubData then you can also do a orphan/map/memcpy/unmap in place of it - and see how it runs.

On Windows turn the threaded driver on and off in the NV control panel and compare both cases. Unfortunately GL perf tends to be write once, test everywhere.

Thanks for the (quick) reply!


Deletehttp://docs.gl/gl3/glBufferSubData says "Consider using multiple buffer objects to avoid stalling the rendering pipeline during data store updates." - is this (still) true? I guess glBufferData() would not call stalls, but just allocate a new buffer (unless there's an internal optimization for using the old one if its contents are not needed anymore).

Yep, setting my code up to support all the different ways should be easy enough, testing is a bit harder as I don't have that much different hardware and operating system for testing.. or experience with the corresponding profilers. But I guess I'll have to learn using those anyway :)

To avoid stalls you either need to:




Delete1. buffer data with NULL to orphan the buffer or

2. use map-buffer-range and do an unsynchronized map and use disparate ranges of your VBO or

3. use multiple VBOs.

If you map the same buffer without orphaning you'll stall until the GPU has finished consuming the old data - the GL has to because it's not allowed to let your (later in time) rewrites to the buffer) to alter the (already issued) draw calls display.

My experience with orphaning is that AMD drivers can have limited capacity for orphaning a huge number of small VBOs - frankly it's a bad thing to do anyway. Assume the real memory of your VBO is at least the VM page size no matter what you ask for.

In our case we're shipping using client arrays for ultra-small draws, but on my todo list is to try map-persistent-coherent and then just writing to sub-ranges of the VBO. In that model, you have to make sure to not reuse a range of the VBO while the draw call is issued but not completed by the GPU.

I did some small tests with updating UBOs with glBufferData() vs glBufferSubData().



DeleteOn OSX (Intel Core i5-4570R with Iris Pro), glBufferData() was a lot faster, got like twice the overall performance in my test case (my Quake2 GL3 renderer).

On Linux with open source radeon drivers on a R3 370, glBufferData() brought about 15% performance increase.

Open source intel (on ivy bridge integrated GPU) didn't care much, /maybe/ glBufferSubData() had slightly better performance, like 3%, but my measuring wasn't that sophisticated so maybe it doesn't matter at all.

On Linux with nvidia 375.39 on 770GTX I couldn't notice a difference either.

So for a simple solution it seems like glBufferData() is best, at least for frequently updated small UBOs.

I haven't tried unsynchronized map access with disperate ranges and orphaning yet.

Daniel, that actually matches X-Plane. I went back and looked at our code - we have one "test sight" where we're pushing UBOs just to get the code path in and catch sketchy old drivers. The original beta implementation (glMapBuffer with orphaning) was show-stoppingly bad.





DeleteIt turns out I swapped in a glBufferSubData and we went final, and no one's complained since, so it is at least "not eye-bleedingly bad".

It's not a stress test though, so all we can conclude is that the update is always in-band and doesn't block.

(By comparison, we recently discovered that too many oprhan-map buffers seems to sometimes cause red-team drivers to pause for a few ms...we were orphaning a lot of tiny buffers though, so I consider that to be "stupid app behavior".)

I have on my TODO list to try a persistent coherent buffer, so we can just memory write, bind the UBO and go.

This comment has been removed by a blog administrator.

ReplyDelete