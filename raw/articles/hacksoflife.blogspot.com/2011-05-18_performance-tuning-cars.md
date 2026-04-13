---
title: Performance Tuning Cars
url: http://hacksoflife.blogspot.com/2011/05/performance-tuning-cars.html
author: Benjamin Supnik
published: '2011-05-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Initial Tests

I ran a few initial tests to understand the performance problems:

- Cars on max, vis distance on max, other parts of the sim "dumbed down" to isolate car costs.
- True framerate measured, including < 19 fps.
- Looked at 10.5.8 and 10.6.7 to make sure analysis on 10.5.8 wasn't biased by driver performance (which is way better on 10.6.7).
- Looked at paused forward view, which isolates car drawing (no car AI when paused), and no-pause down view, which isolates car AI (no drawing when the world is culled).
- Sharked both configs, time profile, all thread states, focused on the main thread.

Initial Findings

The sim was somewhat limited based on car AI (about 20 ms per frame), and heavily bounded on car headlights (we were pushing 500,000+ headlights at about 7-8 fs). The actual 3-d physical cars were a non-issue: very few due to limited visibility distance, and they all hit the instancing path (which has a huge budget on DX11 hardware).

The major performance hits were:

- AI: time to edit the quad tree when cars are moved. Since there is already a cache on this, that means that what's left of this op must be really slow.
- The quad tree editing requires access to some per-object properties that aren't inlined.
- Drawing: the transform time for car headlights.

The sim transforms and builds deferred "spill" lights even in the forward renderer. This is hugely wasteful, as these lights are just thrown out. And getting rid of it nearly doubles draw performance. (There's another bit of dumb work - the car headlights are fully running during the day. I'll wait on that one; the problem is that X-Plane's lighting abstraction leaves "on/off during the day" totally to the GPU during v10, so we don't eliminate a ton of work. I'll leave it to later to decide how much to "expose" the implementation to cull out lights that are off during the day.)

Another "wasted work" note: the spill lights are still transformed in HDR mode, but when we actually need them, things are really bad - about 5 fps. CPU use is only 70%, which is to say, 500,000 deferred lights is a lot of lights, even for a deferred renderer. (It may also be that the 2 million vertices pushed down to make this happen is starting to use up bus bandwidth.) So we can consider a few more optimizations later:

- Provide a cutoff distance for spawning deferred lights from dynamic scenery elements. Since we've measured the distance on these elements anyway (to decide if we want the 3-d car) we could choose to strip out deferred lights.
- We may want to migrate the deferred lights into geometry shaders and/or instancing to cut down on-CPU transform time and bus bandwidth.
- We may want to "prep" streamed light VBOs on a worker thread.

Similarly, threading the build-out of VBOs is going to be dependent on driver capability. If the driver can't accept mapping a buff on a worker and unmapping on a main thread, then we're going to have problems keeping the worker thread independent without pre-allocating a lot of VBO memory.

Cutting down the LOD distance of deferred lights from 20 km to 5 km takes us from 2.1 million deferred light vertices at 5 fps to 128k vertices at 10 fps. We can even go down to 2 km for 12 fps.

Inlining

Another thing that the Shark profiles showed was that the cars effectively generated some hot loops that had to call non-inlined accessor functions. I had a note to examine inlining at some point, but in this case a few specific accessors "popped". Inlining is a trade-off between keeping code clean and encapsulated and letting the compiler boil everything down.

In this case, I chose to use macros to control whether an inline code file is included from header or translation unit. X-Code still sees the inlines as a dependency, but we get faster compile and better GDB behavior in debug mode, plus a clean public header.

Inlining didn't change the performance of drawing car headlights (whose code path was mostly inline already) but it made a significant difference in the car AI (that is, the code that decides where the cars will drive to) - that code had to update the quadtree using non-inline accessors; with 44k cars navigating we went from 41 fps. (Also notable: the sim will run at 73 fps in the exact "AI" stress case but with cars off - that's 13 ms for basic drawing and the flight model and 11 ms for cars. There's still a lot to be had here.)

When the inlining dust settles, we have on-CPU headlight transform taking a lot of time at the low level, and reculling the scene graph when moving cars still showing up prominently.

More Scrubbing

At this point we have to look at the low level headlight transformer in x86 assembly. Wow, that's not pretty - it looks like someone took a scrabble set, emptied it on the floor, and then hit it repeatedly with a hammer. We can pull some conditional logic out of the tight loop for a small win (about 5%) but even better: the sim is trying to "modulate" the phase of headlights per headlight. This is a clever technique to authors, but totally stupid for headlights because they don't flash. Pull that out and we are getting 695k headlights at 14.5 fps. There's no subtitute for simply not doing things.

The assembly is spending a surprising amount of its time in the matrix transform. It's a rare case where SSE can be a win - in this case, we can squeeze another 15% out of it. Note that before I spent any time on SSE, I did an L2 profile - this shows the code's time by who is missing the L2 cache. The hot loop for transform didn't show up at all, indicating that the time was not being spent waiting for memory. This surprised me a little bit, but if the memory subsystem is keeping up, trying to cram more instructions through the CPU can be a win.

Now you might think: why not just push the work onto another core, or better yet the GPU? The answer is that the particular problem doesn't play well with the more performant APIs. We do have half a million transforms to do, but:

- Since the transform is going straight into AGP memory, filling the buffers with multiple threads would require OpenGL sync code - we may get there some day, but that kind of code requires a lot of in-field validation to prove that the entire set of drivers we run on (on three operating systems) handles the case both correctly and without performance penalties.
- The vertex data is generated off an irregular structure, making it difficult to put on the GPU. (This is definitely possible now with the most programmable cards, but it wouldn't run on our entire set of required hardware.)

One last note on the scrubbing: it really demonstrated the limits of GCC's optimizer. In particular, if a call tree is passing param values that always branch one way, but the call sight at which the constant is passed is not inlined with the actual if statement, I can get a win by "specializing" the functions myself. From what I can tell, GCC can't "see" that far through the function tree. This is with GCC 4.0 and no guided profiling, so it may be there are better tools. I also haven't tried LLVM as a back-end yet; LLVM supposedly is quite clever with inference.

Multi-Core = Free?

There's one last trick we can pull: we can move the per-frame car AIs off onto another thread that runs parallel to the flight model. On a multi-core machine this is "free" processing if the worker threads are not saturated. When looking "down" (so the AI is the only cost) this takes us from 65 to 80 fps. In a forward view with 20 km visibility, we are (after all of our work on CPU) possibly limited by bus bandwidth - CPU use is "only" 85%. This is important because in this configuration, removing the AI work won't show up as a fps change. If we reduce the car distance from 20km t0 10km for drawing (we still pay for AI all the time) we still get a few fps back.

**Follow-Up: Final SSE Numbers**

I wrote the rest of this post about a week and a half ago. Today I cleaned up some of my SSE code, the result being that I can turn SSE on and off for the same matrix primitives.

Putting the sim into a "car-heavy" state causes 23% of frame-time to be spent on car headlights; using SSE improves overall frametime by 6% (that is, we get a 6% net boost in fps). This implies that the actual car headlights (currently the only SSE-capable code) becomes 26% faster. Since the headlights are only partly math ops, the actual matrix transforms are

*significantly*faster. (Note the baseline still uses non-SIMD single-float SSE as the math ABI.)

So what can we conclude:

- Using SSE for our matrix ops is a big win for actual time spent doing matrices.
- X-Plane doesn't have a lot of CPU time in this category.

*potential*to be useful if we can find other sites to deploy the same tricks to. See also

[this post](http://hacksoflife.blogspot.com/2010/11/is-1-lot.html).)

## No comments:

## Post a Comment