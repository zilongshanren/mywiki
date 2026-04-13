---
title: Guessing the Fine Print
url: http://hacksoflife.blogspot.com/2011/06/guessing-fine-print.html
author: Benjamin Supnik
published: '2011-06-01'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One of the great things about OpenGL is that it's really flexible.

But is it fast and flexible? No. There are "fast paths"; ask the GL to do something adequately byzantine and it's going to get the job done by a correct but not particularly optimized driver path.

I have had one or two occasions to peer over the shoulder of driver writers and see what a production driver looks like. Here's a taste. (Note: this is made up for illustration...no NDAs were harmed in the creation of this example.)

`/* Figure out if we can push vertices through the fast path. */`


#if X2913_GPU

#if USE_FAST_PATHS

if (

vbo->internal.struct_align % STRUCT_ALIGN_MOD == 0 &&

(vbo->source_mode == SOURCE_AGP || !vbo->resident) &&

#if FIX_STALL_BUG

vbo->current_day != AGP_YES_IT_IS_TUESDAY &&

#endif

vbo->internal.size > MIN_SIZE_FOR_FAST_PATH &&

vbo->internal.size < MAX_SIZE_FOR_FAST_PATH &&

IS_SIZE_WE_LIKE(vbo->internal.size) &&

#endif

FREE_SPACE(CMD_PACKET_BUF(OUR_CONTEXT)) > CMD_PACKET_ACCEL_SIZE)

{

/* do accelerated case *

} else

/* another 50,000 conditions have to be met. */

#endif

#if NEXT_GPU_THAT_IS_TOTALLY_DIFFERENT

...


What we have here might qualify as a

[leaky abstraction](http://www.joelonsoftware.com/articles/LeakyAbstractions.html)(at least with respect to performance): the fast path isn't obvious from the OpenGL API, but it matters.

Well, every now and then, you get to see yourself fall off the fast path. Ouch!

![](../../assets/0cdb479dddaae662.png)


![](../../assets/0cdb479dddaae662.png)

This is is a screenshot of an instruments 2.x trace (with the time profiler - 1.x won't give you this kind of info) of X-Plane with a fast path failure. In this case, we do a glCopyTexSubImage2D and...bad things happen! It's taking 67% of our frame time! In this case, we can sort of guess what the driver might be doing.

- 57% of the time goes into a gldFinish - I speculate that that's Apple asking nVidia to finish filling pixels on a surface. This of course goes through into Kernel space and spends a lot of time doing things that have "wait" in them.
- Another 8.2% is in glgProcessPixelsWithProcessor - that sounds a lot like Apple using the host to do some kind of pixel op.

Driver monitor confirms this - with non-zero "time spent waiting in user code" (meaning a call that might not block is blocking) and a non-zero texture page off bytes (meaning something in VRAM had to be copied back to the host). This is not what we want out of glCopyTexImage2D. Generally we never want to copy anything off of the GPU and we never want to wait in host.

What did it turn out to be? Well, the first surprise was that we were using glCopyTexImage2D at all (and not using an FBO). It turns out that we were reading back from an RGBA16F surface into an RGBA8 texture in a misguided attempt to cope with mismatching gamma. Of course, the driver could in theory build a custom shader to make that transformation, but it's very reasonable to expect a punt. Getting the two surfaces to the same format and using an FBO fixed the problem.

## No comments:

## Post a Comment