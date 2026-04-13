---
title: This is Why ASAN Makes The Big Bucks
url: http://hacksoflife.blogspot.com/2016/07/this-is-why-asan-makes-big-bucks.html
author: Benjamin Supnik
published: '2016-07-06'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/d4ceb0bd6305592e.png)


![](../../assets/d4ceb0bd6305592e.png)

I've been meaning to post this: this is ASAN (Address Sanitizer) in X-Code 7 catching a memory scribble in an X-Plane beta.

I don't usually drink the Kool-Aid when it comes to Apple development tools. If you say "Swift Playground" my eyes roll all the way into the back of my head like in the exorcist.

My skepticism with Apple tools comes from X-Plane being a big heavy app that aims to use 100% of a gamer-class PC; when run with developer tools on the Mac, the results sometimes aren't pretty. Instruments took several versions to reach a point where we could trace X-Plane without the tool blowing up.

ASAN is something else. It's so fast that it can run X-Plane (fully unoptimized debug build) with

*real*settings, like what users use, at 7-10 fps with full address checking. That's not even on the same planet as Valgrind. (When we tried Valgrind on Linux, we didn't have the patience to find the fps - it never finished auditing the load sequence.)

In this crash ASAN has not only shown me where I have utterly stomped on memory, but it has also provided a full backtrace to where I relinquished the memory that I am now stopping on

*and*where I first allocated it. That's a huge amount of information to get in a real-time run.

In this case the underlying bug issue was: we have a geometry accumulator that takes a big pile of geometry and stuffs it in a VBO when done. (What makes the class interesting is that it takes input geometry from multiple sources and sequences them into one big VBO for efficiency.)

A participating client can't delete their chunk of the VBO until after accumulation is finished, but there was no assert protecting us from this programming mistake. When code does delete its geometry "too early", the removed reference isn't properly tracked and stale pointers are used during the VBO build-up process, trashing memory.

Suffice it to say, ASAN's view of this is about the best you can hope for in this kind of scribble situation.

clang's AddressSanitizer isn't an Apple tool. It's cross platform and It has even better support on Linux.

ReplyDeleteSorry, I didn't mean to imply that it was "Apple's" tool - like tsan, it's part of the Clang-LLVM-industrial-complex. My point was that in this case I was using ASAN "as integrated" into X-Code.


ReplyDelete