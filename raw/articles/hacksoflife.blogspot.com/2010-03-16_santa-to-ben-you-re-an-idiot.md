---
title: 'Santa to Ben: You''re An Idiot'
url: http://hacksoflife.blogspot.com/2010/03/santa-to-ben-youre-idiot.html
author: Benjamin Supnik
published: '2010-03-16'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[posted a request](http://hacksoflife.blogspot.com/2009/12/all-i-want-for-xmas-is-parallel-command.html)(to Santa) for parallel command dispatch. The idea is simple: if I am going to render several CSM shadow map levels and the scene graph contained in each does not overlap, then each one is both (1) independent in render target and (2) independent in the actual work being done. Because the stuff being rendered to each shadow map is different, using geometry shaders and multi-layer FBOs doesn't help.* My idea was: well I have 8 cores on the CPU - if the GPU could slurp down and run 8 streams, it'd be like having 8 independent GLs running at once and I'd get through my shadow prep 8x as fast.

I was talking with a CUDA developer and finally I got a clue. The question at hand was whether CUDA actually runs parallel kernels. Her comment was that while you can queue multiple kernels asynchronously, the goal of such a technique is to keep the GPU busy - that is, to keep the GPU from going idle between batches of kernel processing. The technique of multiple kernels isn't necessary to keep the GPU fully busy, because even iwth hundreds of shader units, the kernel is going to run over thousands or tens of thousands of data points. That is, CUDA is intended for wildly parallel processing, so the entire swarm of "cores" (or "shaders"?) is still smaller than the number of units of work in a batch.

If you submit a tiny batch (only 50 items to work over) there's a much bigger problem than keeping the GPU hardware busy - the overhead of talking to the GPU at all is going to be worse than the benefit of using the GPU. For small numbers of items, the CPU is a better bet - it has better locality to the rest of your program!

So I thought about that, then turned around to OpenGL and promptly went "man am I an idiot". Consider a really trivial case: we're preparing an environment map, it's small (256 x 256) and the shaders have been radically reduced in complexity because the environment map is going to be only indirectly shown to the user.

That's still at least 65,536 pixels to get worked over (assuming we don't have over-draw, which we do). Even on our insane 500-shader modern day cards, the number of shaders is still much smaller than the amount of fill we have to do. The entire card will be busy - just for a very short time. (In other words, graphics are still

*embarrassingly*parallel.)

So, at least on a one GPU card, there's really no need for parallel dispatch - serial dispatch will still keep the hardware busy.

So...parallel command dispatch? Um...never mind.

This does beg the question (which I have not been able to answer with experimentation): if I use multiple contexts to queue up multiple command queues to the GPU using multiple cores (thus "threading the driver myself") will I get faster command-buffer fill and thus help keep the card busy? This assumes that the card is going idle when it performs trivially simple batches that require a fair amount of setup.

To be determined: is the cost of a batch in driver overhead (time spent deciding

*whether*we need to change the card configuration or

*real*overhead (e.g. we have to switch programs and GPU isn't that fast at it). It can be very hard to tell from an app standpoint where the real cost of a batch lives.

Thanks to those who haunt the OpenGL forums for smacking me around^H^H^H^H^H^H^H^H^Hsetting me straight re: parallel dispatch.

* geometry shaders and multilayer FBO help, in theory, when the batches and geometry for each rendering layer are the same. But for a cube map if most of the scene is not visible from each cube face, then the work for each cube face is disjoint and we are simply running our scene graph, except now we're going through the slower geometry shader vertex path.

## No comments:

## Post a Comment