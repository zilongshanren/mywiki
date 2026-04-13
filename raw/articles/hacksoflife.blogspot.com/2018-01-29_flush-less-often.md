---
title: Flush Less Often
url: http://hacksoflife.blogspot.com/2018/01/flush-less-often.html
author: Benjamin Supnik
published: '2018-01-29'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Here's a riddle:




Until that buffer of commands goes to the GPU, from the GPU's perspective, you haven't actually asked it to do anything - your command buffer is just sitting there, collecting dust, while the GPU is idle.


In modern APIs like Vulkan, Metal, and DX12, the command buffer is an object you build, and then you explicitly send it to the GPU with an API call.


With OpenGL, the command buffer is implicit - you never see it, it just gets generated as you make API calls. The command buffer is sent to the GPU ("flushed") under a few circumstances:




But with modern OpenGL, calling the API is only a small fraction of the work we do; most of the work of drawing involves filling buffers with numbers. This is where your meshes and hopefully constant state are all coming from.


The flushing problem comes to haunt us when we want to draw a large number of small drawing batches. It's easy to end up with code like this:


// write some data to memory

glDrawElements.

// write some data to memory






* My two-year old has figured out how to flush the toilet and thinks it's fascinating. What he hasn't figured out how to do is listen^H^H^H^H^Hwait until I'm done peeing. (And yes, non-parents, of coarse


"Okay Ezra, wait until Daddy's done. No, not yet. It's too soon. Don't flush. Ezra?! Sigh. Wait, this is exactly like @#$@#$ glDrawElements!"

Q: What does a two year old and OpenGL have in common?

A: You never know when either of them is going to flush.*In the case of a two-year old, you can wait a few years and he'll find different ways to not listen to you; unfortunately in the case of OpenGL, this is a problem of API design; therefore we have to use a fairly big hammer to fix it.

#### What IS the Flushing Problem?

Modern GPUs work by writing a command buffer (a list of binary encoded drawing instructions) to memory (using the CPU) and then "sending" that buffer to the GPU for execution, either by changing ownership of the shared memory or by a DMA copy.Until that buffer of commands goes to the GPU, from the GPU's perspective, you haven't actually asked it to do anything - your command buffer is just sitting there, collecting dust, while the GPU is idle.

In modern APIs like Vulkan, Metal, and DX12, the command buffer is an object you build, and then you explicitly send it to the GPU with an API call.

With OpenGL, the command buffer is implicit - you never see it, it just gets generated as you make API calls. The command buffer is sent to the GPU ("flushed") under a few circumstances:

- If you ask GL to do so via glFlush.
- If you make a call that does an automatic flush (glFinish, glSwapBuffer, waiting on a sync with the flush bit).
- If the command buffer fills up due to you doing a lot of stuff.

#### Why Do We Care?

Back in the day, we didn't care - you'd write commands and buffers would go out when they were full (ensuring a "goodly amount of work" gets sent to the GPU) and the last command buffer was sent when you swapped your back buffer.But with modern OpenGL, calling the API is only a small fraction of the work we do; most of the work of drawing involves filling buffers with numbers. This is where your meshes and hopefully constant state are all coming from.

The flushing problem comes to haunt us when we want to draw a large number of small drawing batches. It's easy to end up with code like this:

// write some data to memory

glDrawElements.

// write some data to memory

glDrawElements.

Expanding this out, the code actually looks more like:

// map a buffer

// write to the buffer

// flush and unmap the buffer

glDrawElements.

// map a buffer

// write to the buffer

// flush and unmap the buffer

glDrawElements.

The problem is: even with glMapBufferRange and "unsynchronized" buffers, you still have to issue some kind of flush to

*your*data before each drawing call.
The reason this is necessary is: glDrawElements might cause your command buffer to be sent to the GPU at any time! Therefore you have to have your data buffer completely flushed and ready to go after every drawing call.




This second technique is a double-edged sword.





#### How Do We Fix It?

You basically have two choices to make code like the above fast:- If your are on a modern GL, use persistent coherent buffers. They don't
*need*to be flushed - you can write data, call draw, and if the GL happens to send the command buffer down, your data is already visible. This is a great solution for UBOs on Windows. - If you can't get persistent coherent buffers,
[defer all of your actual state and draw calls](http://hacksoflife.blogspot.com/2015/03/accumulation-to-improve-small-batch.html)until every buffer has been built.

This second technique is a double-edged sword.

- Win: it works every-where, even on the oldest OpenGL.
- Win: as long as you're accumulating your state change, you can optimize out stupid stuff - handy when client code tends to produce crap OpenGL call-streams.
- Lose: it does require you to marshal the entire API, so it's only good for code that sits on a fairly narrow foot-print.

*not*to use UBOs when persistent-coherent buffers are not also available. It turns out the cost of flushing per draw call is really bad, and our fallback path (loose uniforms) is actually surprisingly fast, because the driver guys have tuned the bejeezus out of that code path.* My two-year old has figured out how to flush the toilet and thinks it's fascinating. What he hasn't figured out how to do is listen^H^H^H^H^Hwait until I'm done peeing. (And yes, non-parents, of coarse

[peeing is a group activity](https://www.youtube.com/watch?v=dtWWKM-5tLE). Duh.) The monologue went something like:"Okay Ezra, wait until Daddy's done. No, not yet. It's too soon. Don't flush. Ezra?! Sigh. Wait, this is exactly like @#$@#$ glDrawElements!"

## No comments:

## Post a Comment