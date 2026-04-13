---
title: Vroom, Vroom! I'm Going To Win This Race Condition!
url: http://hacksoflife.blogspot.com/2017/02/vroom-vroom-im-going-to-win-this-race.html
author: Benjamin Supnik
published: '2017-02-17'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Here's a riddle:








This is a back-trace of the first race condition I hit when starting X-Plane: our main thread is reading preferences and has just inited the texture resolution setting in memory.


As it turns out, background threads are






Item three is a tall order and


With that in mind, some of the first few race conditions I hit were, perhaps, benign:




That "bouncing" idiom is simple, it works great, we use it everywhere. Except...


...it turns out that all of the airport extruding tasks (and there are a bunch of them, 64 per scenery tile divided spatially) share a single vector of layers.


And while one task is not doing async work while the layer list is being mutated on the same thread, another one might be! (The "bounce between threads" idiom


Every now and then, the vector gets resized and the memory recycled fast enough that the stale use of the vector blows up on the worker thread. This was visible in our automatic crash reporting as the airport extruder just randomly exploding on a worker thread for no reason.


Sure enough, tsan caught this, pointing to the vector resize on the main thread and the mutation on the worker thread. Because tsan catches races when they are unsynchronized and not just when that failure to synchronize results in Really Bad Data™, this race condition hit every time I booted the product, rather than every now and then. (While we have crash reports to know this happens in field, I never saw this race condition on my own machine, ever.)




Because tsan looks for race conditions between synchronization points, it is great for finding race conditions without depending on the actual order of execution. That's huge. But there


Our weather engine uses a double-buffering scheme to mutate the weather while background threads are producing particle systems for the clouds. The main thread, per frame, adjusts weather, then the buffer is switched.


As it turns out, this idiom is totally wrong, because we don't guarantee that worker threads finish their work and synchronize with the main thread


The problem is:


The result was that I had to let tsan run for almost 30 minutes before it caught a race condition so totally brain damaged that it should have been immediate.


Even if a clean short run with tsan doesn't guarantee your threading code is perfect, it's still a fantastic tool that moves a series of bugs from "nearly impossible to find" to "possible to find easily a lot of the time."


Q: Santa Clause, the Easter Bunny, a Benign Race Condition and Bjarne Stroustrup each stand 100 feet away from a $100 bill. They all run to the bill at the same time. Who gets the bill?Okay, now that we have established that (1) I am a nerd and (2) race conditions are bad, we can talk about


A: Bjarne Stroustrup, because the other threedon't exist.

**(tsan), or as I call it, "the tool that reminds you that you're not nearly as clever as you thought you were when you wrote that multi-threaded widget reduplicator."**[thread sanitizer](http://clang.llvm.org/docs/ThreadSanitizer.html)[Address Sanitizer](http://hacksoflife.blogspot.com/2016/07/this-is-why-asan-makes-big-bucks.html)(asan) is fantastic because it catches memory scribbles and other Really Bad Behavior™ and it's*fast*- fast enough that you run it in real time on your shipping product. tsan is fantastic because it finds things that*we just didn't have tools to find before.**tsan's design is quite similar to asan: a block of shadow memory records thread access to a real location, and an app's memory operations are in-place modified to work with shadow memory.*

#### Let's See Some Dumb Code

Here is an example of tsan in action:![](../../assets/598d8c13a9eb6a4d.png)

![](../../assets/598d8c13a9eb6a4d.png)

This is a back-trace of the first race condition I hit when starting X-Plane: our main thread is reading preferences and has just inited the texture resolution setting in memory.

As it turns out, background threads are

*already loading textures*. Doh! I had no idea this race condition existed.#### The Yeti of Race Conditions

A[benign race condition may not be real](https://software.intel.com/en-us/blogs/2013/01/06/benign-data-races-what-could-possibly-go-wrong), but we can still define what properties it would have if it did exist. It would have to be a case where:- All actual racing reads-writes are relaxed atomics for this particular architecture and data alignment and
- We can live with the resulting operation of the code in all possible orderings the code actually runs at and
- Clang doesn't reorganize our code into something really dangerous,
[even though it has permission to do so](http://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html).

Item three is a tall order and

[getting harder every day](http://hacksoflife.blogspot.com/2015/12/the-dangers-of-super-smart-compilers.html). While Clang is not yet[Skynet](https://en.wikipedia.org/wiki/Skynet_(Terminator)), it is still a lot smarter than I am. Five years ago a C++ programmer could know enough about compilers and code to reason about the behavior of optimized code under undefined conditions and possibly live to tell about it; at this point the possible code changes are just too astonishing. I have begrudgingly admitted that I have to follow all of the rules or Clang and LLVM will hose me in ways that it would take weeks to even understand.With that in mind, some of the first few race conditions I hit were, perhaps, benign:

- In the case above, some texture loads have a flag to indicate "always max res, don't look at prefs" - the code was written to set a local variable to the preferences-based res first, then overwrite it; restructuring this code to not touch the preferences data if it was not going to be used silenced the "benign" race condition.
- We had some unsynchronized stats counter - this is just wrong, and their data was junk, but this was a "don't care" - the stats counters weren't needed and didn't affect program operation. They could have been turned into relaxed atomics, but instead I just removed them.

#### So That's What That Was

After cleaning up texture load and some stats counters, I finally hit my first real bug, and it was a big one. The background tasks that build airports sometimes have to add shader-layers (groups of meshes drawn in the same part of the rendering pass, sharing a common shader) to the main scenery data structure; they bounce between worker thread land (where they build meshes slowly from raw data) and the main thread (where they add the shader layers into our global data structures between frames and thus don't crash us).That "bouncing" idiom is simple, it works great, we use it everywhere. Except...

...it turns out that all of the airport extruding tasks (and there are a bunch of them, 64 per scenery tile divided spatially) share a single vector of layers.

And while one task is not doing async work while the layer list is being mutated on the same thread, another one might be! (The "bounce between threads" idiom

*only works*if the thing bouncing around has exclusive access to its data structures.)Every now and then, the vector gets resized and the memory recycled fast enough that the stale use of the vector blows up on the worker thread. This was visible in our automatic crash reporting as the airport extruder just randomly exploding on a worker thread for no reason.

Sure enough, tsan caught this, pointing to the vector resize on the main thread and the mutation on the worker thread. Because tsan catches races when they are unsynchronized and not just when that failure to synchronize results in Really Bad Data™, this race condition hit every time I booted the product, rather than every now and then. (While we have crash reports to know this happens in field, I never saw this race condition on my own machine, ever.)

#### What Tsan Can Find

While tsan is about 1000x better than what we had before (E.g. staring at your code and going "is this stupid?"), it does have some limitations. Because the problem space is harder than asan, the tracking in tsan isn't perfect; scenarios with more than four threads can lead to evictions of tracking data, history can be purged, etc. I saw a number of issues in my first session with the tool, but having reviewed the docs and presentations again, I think a lot of these things can be worked around.Because tsan looks for race conditions between synchronization points, it is great for finding race conditions without depending on the actual order of execution. That's huge. But there

**are**still cases where your code's execution order will hide race conditions (and not just by not running the buggy code).Our weather engine uses a double-buffering scheme to mutate the weather while background threads are producing particle systems for the clouds. The main thread, per frame, adjusts weather, then the buffer is switched.

As it turns out, this idiom is totally wrong, because we don't guarantee that worker threads finish their work and synchronize with the main thread

*in the same frame*. In other words, the double buffer might swap twice while a worker runs, leaving the worker reading from the mutating copy of the weather.The problem is:

*if*the weather system is pretty fast (and we want it to be!!) and the particle system tasks finish within a frame, they will then synchronize with the main thread (to "check in" their finished work) before the main thread swaps the thread buffers. Since everything on a single thread is "happens before" by program order (at least, if they cross sequence points in C++, and we do here), tsan goes "yep - the thread finished, checked in, and we're all good." What it can't realize is that had the timing been different, the synchronization path would have run after the racy code.The result was that I had to let tsan run for almost 30 minutes before it caught a race condition so totally brain damaged that it should have been immediate.

Even if a clean short run with tsan doesn't guarantee your threading code is perfect, it's still a fantastic tool that moves a series of bugs from "nearly impossible to find" to "possible to find easily a lot of the time."

## No comments:

## Post a Comment