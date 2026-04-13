---
title: glNext is Neither OpenGL nor Next, Discuss
url: http://hacksoflife.blogspot.com/2015/03/glnext-is-neither-opengl-nor-next.html
author: Benjamin Supnik
published: '2015-03-14'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The title is a stretch at best, but as I have said before, good punditry has to take precedence over correctness. Khronos posted a ~~glNext~~Vulkan + SPIR-V talk with good audio and slices. I'll see you in an hour and a half.










But how the hell does anyone ever


OpenGL doesn't just have a huge API, it has a combinatorially huge API - you can combine just about anything with anything else; documenting the fast path (even if all driver providers could agree) is mathematically impossible.


Vulkan fixes this by making performance explicit. These functions are fast, these are slow. Don't call the slow calls when you want to go fast. It gives app developers a huge insight into what is expensive for the driver/hardware and what is not.




When we had to port X-Plane 9 for iPhone from GLES 1.1 to GLES 2.0, I wrote a shim that emulated the stuff we needed in GLES 1.1 Some of this is now core to our engine (e.g. the transform stack) and some still exists because it is only used in crufty non-critical path code and it's not worth it to rip it out (e.g. glBegin).


The shimming exercise was not that hard, but it was made more complicated by the fact that half of the GL API is actually implemented in


Because Vulkan isn't gl at all, one option is to simply implement OpenGL using...Vulkan. I will be curious if a portable open source gl layer emerges; if it does, it would be a useful way for very large legacy code bases to move to Vulkan. There'd be two wins:






Resource management is the one area where what we know now is way too fuzzy. You can look at Apple's Metal API (fully public, shipping, code samples) and see what a world with non-mutable objects, command queues and command buffers looks like. But resource management in Metal is super simple because it only runs on a shared memory device: a buffer object is a ptr to memory, full stop. (Would if it were that easy on all GPUs.)


It's too soon to tell what the "boiler plate" will look like for handling resource management in Vulkan. There's a huge difference in the quality of resource management between different driver stacks; writing a resource manager that does as well as AMD or NVidia's is going to be a real challenge for small development teams.





[second version](https://www.youtube.com/watch?v=qKbtrVEhaw8)of the
That answered all of our questions, right! Ha ha, I kid. Seriously though, at least a little bit is now known:

- Vulkan is
**not**an incremental extension to OpenGL - there's no API compatibility. This is a replacement. - Vulkan sits a lot lower in the graphics stack than OpenGL did; this is an explicit low level API that exposes a lot of the hard things drivers did that you didn't know existed.

*less work*in the driver than they used to! And this is a good thing; the surface area of the OpenGL API (particularly when you combine ARB_compatibility with all of the latest extensions) is kafkaesque. If someone showed you the full API and said "go code that" you'd surely offer to cut off a finger as a less painful alternative.

My biases as a developer are in favor of not throwing out things that work, not assuming that things need a from scratch rewrite just because they annoy you, and not getting excited just because it's shiny and new. So I am surprised with myself that at this point, I'd much rather have a Vulkan-like API than all of the latest OpenGL extensions, even though it's more work for me. (Remember that work the driver guys aren't going to do? It goes into the engine layer.)

### What's Good/Why Do We Need This?

While there's a lot of good things for game engines in Vulkan, there are a few that got my attention because they are not possible with further extension/upgrade to OpenGL:

**Threading:**A new API is needed because OpenGL is thread-unfriendly, and it's unfriendly at the core of how the API is written; you can't fix this by adding more stuff. Some things OpenGL does:

- OpenGL sets up a 1:1 correspondence between queues, command buffers, and threads. If you want something else, you're screwed, because you get one thing ("the context") and it has damned strict threading rules.
- OpenGL does the thread synchronization for you, even if you don't want that. There are locks inside the driver, and you can't get rid of them.*

This is definitely a win for game engines. For example, with X-Plane we will load a scenery tile "in the background". We know during loading that every object involved in the scenery tile is "thread local" to us, because they have not been shared. There is no common data between the rendering thread and the loader.

Therefore both can run completely lock free. There is a one-time synchronization when the fully finished tile is inserted into the active world; this insert happens only after the load is complete (via message Q) and is done between frames by the rendering thread. Again, no locks. This code can run lock free at pretty much all points.

There's no way for the GL driver to know that. Every time I go to shovel data into a VBO in OpenGL, the driver has to go "I wonder if anyone is using this? Is this call going to blow up the world?" Under Vulkan, the answer is "I'm the app, trust me." That's going to go a lot faster. We're getting rid of "safety checks" in the driver that

*are not needed*.**Explicit Performance:**one of the hardest things about developing realtime graphics with OpenGL is knowing where the "fast path" is. The GL API lets you do about a gajillion different things, and only a few call paths are going to go fast. Sometimes I see threads like this on OpenGL mailing lists:

Newb: hey AMD, when I set the refrigerator state to GL_FROZEN_CUSTARD and then issue a glDrawGizmo(GL_ICECREAM, 10); I see a massive performance slow-down. Your driver sucks!I'm sitting in front of my computer going "Oh noooooes!!! You can't use ice cream with frozen custard - that's a

*crazy*thing to do." Maybe I even write a blog post about it.But how the hell does anyone ever

*know*? OpenGL becomes a game of "write-once performance tune everywhere" (or "write once, harass the driver guys to run your app through vtune and tell you you're an idiot everywhere") - sometimes it's not possible to tell why something is slow (NVidia, I'm looking at you and your stripped driver :-) and sometimes you just don't have time to look at every driver case (cough cough, Intel, cough).OpenGL doesn't just have a huge API, it has a combinatorially huge API - you can combine just about anything with anything else; documenting the fast path (even if all driver providers could agree) is mathematically impossible.

Vulkan fixes this by making performance explicit. These functions are fast, these are slow. Don't call the slow calls when you want to go fast. It gives app developers a huge insight into what is expensive for the driver/hardware and what is not.

**Shim It:**I may do a 180 on this when I have to code it, but I think it may be*easier*to move legacy OpenGL apps to Vulkan specifically*because*it is not the OpenGL API.When we had to port X-Plane 9 for iPhone from GLES 1.1 to GLES 2.0, I wrote a shim that emulated the stuff we needed in GLES 1.1 Some of this is now core to our engine (e.g. the transform stack) and some still exists because it is only used in crufty non-critical path code and it's not worth it to rip it out (e.g. glBegin).

The shimming exercise was not that hard, but it was made more complicated by the fact that half of the GL API is actually implemented in

*both*versions of the spec. I ended up doing some evil macro trickery: glDrawElements gets #defined over to our internal call, which updates the lazily changed transform stack and*then*calls the real glDrawElements. Doing this level of shim with the full desktop GL API would have been quite scary I think.Because Vulkan isn't gl at all, one option is to simply implement OpenGL using...Vulkan. I will be curious if a portable open source gl layer emerges; if it does, it would be a useful way for very large legacy code bases to move to Vulkan. There'd be two wins:

- Reliability. That's a lot less code that comes from the driver; whether your gl layer works right or is buggy as a bed in New York, it's going to be the
*same*bugs everywhere - if you've ever tried to ship a complicated cross-platform OpenGL app, having the same bugs everywhere is like Christmas (or so I'm told). - Incremental move to Vulkan. Once you are running on a GL shim, poke a hole through it when you need to get to the metal for only performance-critical stuff. (This is what we did with GLES 1.1/2.0: the entire UI ran in GLES 1.1 emulation and the rendering engine went in and bound its own custom shaders.)

### Vulkan is Not For Everyone

When "

[OpenGL is Borked](http://aras-p.info/blog/2014/05/31/rant-about-rants-about-opengl/)" went around the blogs last year one thing that struck me was how many different constituencies were grumpy about OpenGL, often wanting fixes that could not co-exist. Vulkan resolves this tension: it's low level, it's explicit, it's not backward compatible, and therefore it's only for developers who want to do more work to get more perf and don't need to run on everything or can shim their old code.
I think this is a good thing: at least Vulkan can do the limited task it tries to do well. But it's clearly not for beginners, not for teaching an introduction to 3-d graphics, and if you were grumpy about how much work it was to use GLES 2.0 for your mobile game, Vulkan's not going to make you very happy. And if you're sitting on 100,000,000 lines of CAD code that's all written in OpenGL, Vulkan doesn't do you as much good as that one extension you really really really need.

For developers like me (full time, professional, small company, proprietary engine) there's definitely going to be a cost in moving to Vulkan in development time. Whenever the driver guys talk about resource management they often say something like:

The app has to do explicit resource management, which it's probably already doing on console.for the big game engines this is totally true, so being able to re-use their resource management code is a win. For smaller games, OpenGL

*is*their resouce management code. It's not necessarily very good resource management (in that the GL driver is basically guessing about you want, and sometimes guessing wrong) but if you have a three-person development team, having[Graham Sellers](http://www.openglsuperbible.com/)write your resource management code for you for free is sort of an epic win.Resource management is the one area where what we know now is way too fuzzy. You can look at Apple's Metal API (fully public, shipping, code samples) and see what a world with non-mutable objects, command queues and command buffers looks like. But resource management in Metal is super simple because it only runs on a shared memory device: a buffer object is a ptr to memory, full stop. (Would if it were that easy on all GPUs.)

It's too soon to tell what the "boiler plate" will look like for handling resource management in Vulkan. There's a huge difference in the quality of resource management between different driver stacks; writing a resource manager that does as well as AMD or NVidia's is going to be a real challenge for small development teams.

* My understanding is that if you create only one GL context (and thus you are not using threads) the driver will actually run in a lock-free mode to avoid over-head. The fact that the driver bothers to detect that and special case it gives you some idea how crazy a GL driver is. If that doesn't,

## No comments:

## Post a Comment