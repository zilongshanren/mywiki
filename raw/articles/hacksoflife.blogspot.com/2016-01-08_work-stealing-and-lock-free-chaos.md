---
title: Work Stealing and Lock Free Chaos
url: http://hacksoflife.blogspot.com/2016/01/work-stealing-and-lock-free-chaos.html
author: Benjamin Supnik
published: '2016-01-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Pablo Halpern explains



A good introduction to more advanced parallel task scheduling strategies.


X-Plane's task scheduler for multi-core work is a central work-pool, similar to libdispatch and pretty much any basic worker-pool design that isn't trying to get too clever with continuations. Our assumption is that the amount of background work is (hopefully) relatively large; typically the work is "cold" when it's scheduled and is going to a core other than the one running the main rendering lop.



And Fedor Pikus on lock-free programming. There's some mind-bending stuff in here. For example, is your concurrent FIFO really a FIFO when used with multiple threads? No one knows, because the only way to test it (from a correct race free program) disallows testing concurrent ordering.


(I view that as a win - one more thing I don't have to code...)



One good point from the talk:



Instead, look for chances to simplify the problem in the application space.


An example from X-Plane: the APIs around our art assets are not lock-free. But the API to


But once you have a reference count and pointer to an art asset, you can


This isn't a "fair" design, and it's not lock-free or wait-free, but it's unfair in exactly the way we need it to be and it's faster on the path that actually matters.


(It also has a subtle race condition due to an implementation error...but that's for another post.)

[work stealing](https://en.wikipedia.org/wiki/Work_stealing)at[cppcon](http://cppcon.org/)2015:A good introduction to more advanced parallel task scheduling strategies.

X-Plane's task scheduler for multi-core work is a central work-pool, similar to libdispatch and pretty much any basic worker-pool design that isn't trying to get too clever with continuations. Our assumption is that the amount of background work is (hopefully) relatively large; typically the work is "cold" when it's scheduled and is going to a core other than the one running the main rendering lop.

And Fedor Pikus on lock-free programming. There's some mind-bending stuff in here. For example, is your concurrent FIFO really a FIFO when used with multiple threads? No one knows, because the only way to test it (from a correct race free program) disallows testing concurrent ordering.

(I view that as a win - one more thing I don't have to code...)

Design only what you need, avoid generic designs.

Avoid writing generic lock-free code.In other words, making a fully general lock free thingie with no fine print and no strings attached is really, really hard. After you spend more time engineering your super-data-structure than you should have, you will end up with something that has subtle concurrency bugs.

Instead, look for chances to simplify the problem in the application space.

An example from X-Plane: the APIs around our art assets are not lock-free. But the API to

*use*them is lock-free, and that's actually all we care about. Loading/unloading happens in the background on worker threads and is always asynchronous. It has to be, because the actual work of loading/unloading the art assets is often non-trivial.But once you have a reference count and pointer to an art asset, you can

*use*it with no further checks; the reference count guarantees it isn't going anywhere. This means the rendering loop can proceed and never gets locked out by loading threads, which is what we care about.This isn't a "fair" design, and it's not lock-free or wait-free, but it's unfair in exactly the way we need it to be and it's faster on the path that actually matters.

(It also has a subtle race condition due to an implementation error...but that's for another post.)

## No comments:

## Post a Comment