---
title: Double-Buffering Part 2 - Why AGP Might Be Your Friend
url: http://hacksoflife.blogspot.com/2010/02/double-buffering-part-2-why-agp-might.html
author: Benjamin Supnik
published: '2010-02-28'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[In my previous post](http://hacksoflife.blogspot.com/2010/02/double-buffering-vbos.html)I suggested that to get high VBO vertex performance in OpenGL, it's important to decouple pushing the next set of vertices from the GPU processing the existing ones. A naively written program will block when sending the next set of vertices until the last one goes down the pipe, but if we're clever and either orphan the buffer or use the right flags, we can avoid the block.

(My understanding is that orphaning actually gets you a second buffer, in the case where you want to double the entire buffer. With manual synchronization we can simply be very careful and use half the buffer each frame.

*Very careful.*)

Now I'm normally a big fan of geometry in VRAM because it is, to put it the Boston way, "wicked fast". And perhaps it's my multimedia background popping up, but to me a nice GPU-driven DMA seems like the best way to get data to the card. So I've been trying to wrap my head around the question: why not double-buffer into VRAM? This analysis is going to get into the highly speculative - the true answer I think is "the devil is in the details, and the details are in the driver", but at least we'll see that the issue is very complex, double-buffering into VRAM has a lot of things that could go wrong, so we should not be surprised if when we tell OpenGL that we intend to stream our data it gives us AGP memory instead.*

Before we look at the timing properties of an application using AGP memory or VRAM, let's consider how modern OpenGL implementations work: they "run behind". By this I mean: you ask OpenGL to draw something, and some time later OpenGL actually gets around to doing it. How much behind? Quite possibly a lot. The card can run behind at least an entire frame, depending on implementation, maybe two. You can keep telling the GPU to do more stuff until:

- You hit some implementation defined limit (e.g. you get 2 full frames ahead and the GPU says "enough!"). Your app blocks in the swap-backbuffer windowing system call.
- You run out of memory to build up that outstanding "todo" list. (Your app blocks inside the GL driver waiting for command buffers - the memory used to build the todo list.)
- You ask the OpenGL about something it did, but it hasn't done it. (E.g. you try to read an occlusion query that hasn't finished and block in the "get' call.)
- You ask to take a lock on a resource that is still pending for draw. (E.g. you do a glMapBuffer on a non-orphaned VBO with outstanding draws, and you haven't disabled sync with one of the previously mentioned extensions.)

Having OpenGL "run behind" is a good thing for your application's performance. You can think of your application and the GPU as a reader-writer problem. In multimedia, our top concern would be underruns - if we don't "feed the beast" enough audio by a deadline, the user hears the audio stop and calls tech support to complain that their expensive ProTools rig is a piece of junk. With an OpenGL app, underruns (the GPU got bored) and overruns (the app can't submit more data) aren't fatal, but they do mean that one of your two resources (GPU and CPU) are not being fully used. The

*longer*the length of the FIFO (that is, the more OpenGL can run behind without an overrun) the more flexibility we have to have the speed of the CPU (requesting commands) and the GPU (running the commands) be mismatched for short periods of time.

An example: the first thing you do is draw a planet - it's one VBO, the app can issue the command in just one call. Very fast! But the planet has an expensive shader, users a ton of texture memory, and fills the entire screen. That command is going to take a little time for the GPU to finish. The GPU is now "behind." Next you go to draw the houses. The houses sit in a data structure that has to be traversed to figure out which houses are actually in view. This takes some CPU time, and thus it takes a while to push those commands to the GPU. If the GPU is still working on the planet, then by the time the GPU finishes the planet, the draw-house commands are ready, and the GPU moves seamlessly from one task to the other without ever going idle.

So we know we want the GPU to be able to run behind and we don't want to wait for it to be done. How well does this work with the previous posts double-buffer scheme? It works pretty well. Each draw has two parts: a "fill" operation done on the CPU (map orphaned buffer, write into AGP memory, unmap) and a later "draw" operation on the GPU. Each one requires a lock on the buffer actually being used. If we can have two buffers underneath our VBO (some implementations may allow more - I don't know) then:

- The fill operation on frame 3 will wait for the draw operation on frame 1.
- The fill operation on frame 4 will wait for the draw operation on frame 2.
- The draw operation on frame N always waits for the fill operation (of course).

*still*not finished) only then might we block. That's good enough for me.

If the buffer is going to be drawn from VRAM, things get trickier. We now have three steps:

- "fill" the system RAM copy. Fill 2 waits on DMA 1.
- "DMA" the copy from system RAM to VRAM. DMA 2 waits on fill 2 and draw 1.
- "draw" the copy from VRAM. Draw 1 waits on DMA 1.

Consider the case where the DMA happens right after we finish filling the buffer. In this case, the DMA is going to block on the last draw not completing - we can't specify frame 2 until frame 1 draw is mostly done. That's bad.

What about the case where the DMA happens really late, right before the draw really happens. Filling buffer 2 is going to block taking a lock until the previous frame 1 DMA completes. That's bad too!

I believe that there is a timing that isn't as bad as these cases though: if the OpenGL driver can schedule the DMA as early as possible once the card is done with the last draw, the DMA ends up with timing somewhere in between these two cases, moving around depending on the actual relationship between GPU and CPU speed.

At a minimum I'd summarize the problem like this: since the DMA requires both of our buffers (VRAM and system) to be available at the same time, the DMA has to be timed just right to keep from blocking the CPU. By comparison, a double-buffered AGP strategy simply requires locking the buffers.

To complete this very drawn out discussion: why would we even want to stream out of VRAM? As was correctly pointed out on the OpenGL list, this strategy requires an extra copy of the data - our app writes it, the DMA engine copies it, then the GPU reads it. (With AGP, the GPU reads what we write.) The most compelling case that I could think of, the one that got me thinking about this, is the case where the streaming ratio isn't 1:1. We specify our data per frame, but we make multiple rendering passes per frame. Thus we draw our VBO perhaps 2 or 3 times for each rewrite of the vertices, and we'd like to only use bus up once. A number of common algorithms (environment mapping, shadow mapping, early Z-fill) all run over the scene graph multiple times, often with the assumption that geometry is cheap (which mostly it is).

But this whole post has been pretty much entirely speculative. All we can do is clearly signal our intentions to the driver (are we a static, stream, or dynamic draw VBO) and orphan our buffers and hope the driver can find a way to keep giving us buffers rapidly without blocking, while getting our geometry up as fast as possible.

* We might want to assume this and then be careful about how we write our buffer-fill code so that it is efficient in uncached write-combined memory: we want to fill the buffer linearly in big writes and not read or muck around with it.

## No comments:

## Post a Comment