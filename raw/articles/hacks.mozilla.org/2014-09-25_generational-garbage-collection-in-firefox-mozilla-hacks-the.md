---
title: Generational Garbage Collection in Firefox – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/09/generational-garbage-collection-in-firefox/
author: Steve Fink
published: '2014-09-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Generational garbage collection (GGC) has now been enabled in the SpiderMonkey JavaScript engine in Firefox 32. GGC is a performance optimization only, and should have no observable effects on script behavior.

So what is it? What does it do?

GGC is a way for the JavaScript engine to collect short-lived objects faster. Say you have code similar to:

```
function add(point1, point2) {
return [ point1[0] + point2[0], point1[1] + point2[1] ];
}
```

Without GGC, you will have high overhead for garbage collection (from here on, just “GC”). Each call to `add()`

creates a new `Array`

, and it is likely that the old arrays that you passed in are now garbage. Before too long, enough garbage will pile up that the GC will need to kick in. That means the entire JavaScript heap (the set of all objects ever created) needs to be scanned to find the stuff that is still needed (“live”) so that everything else can be thrown away and the space reused for new objects.

If your script does not keep very many total objects live, this is totally fine. Sure, you’ll be creating tons of garbage and collecting it constantly, but the scan of the live objects will be fast (since not much is live). However, if your script **does** create a large number of objects and keep them alive, then the full GC scans will be slow, and the performance of your script will be largely determined by the rate at which it produces temporary objects — even when the older objects aren’t changing, and you’re just re-scanning them over and over again to discover what you already knew. (“Are you dead?” “No.” “Are you dead?” “No.” “Are you dead?”…)

## Generational collector, Nursery & Tenured

With a generational collector, the penalty for temporary objects is much lower. Most objects will be allocated into a separate memory region called the Nursery. When the Nursery fills up, only the Nursery will be scanned for live objects. The majority of the short-lived temporary objects will be dead, so this scan will be fast. The survivors will be promoted to the Tenured region.

The Tenured heap will also accumulate garbage, but usually at a far lower rate than the Nursery. It will take much longer to fill up. Eventually, we will still need to do a full GC, but under typical allocation patterns these should be much less common than Nursery GCs. To distinguish the two cases, we refer to Nursery collections as *minor GCs* and full heap scans as *major GCs*. Thus, with a generational collector, we split our GCs into two types: mostly fast minor GCs, and fewer slower major GCs.

## GGC Overhead

While it might seem like we should have always been doing this, it turns out to require quite a bit of [infrastructure that we previously did not have](http://blog.mozilla.org/javascript/2013/07/18/clawing-our-way-back-to-precision/), and it also incurs some overhead during normal operation. Consider the question of how to figure out whether some Nursery object is live. It might be pointed to by a live Tenured object — for example, if you create an object and store it into a property of a live Tenured object.

How do you know which Nursery objects are being kept alive by Tenured objects? One alternative would be to scan the entire Tenured heap to find pointers into the Nursery, but this would defeat the whole point of GGC. So we need a way of answering the question more cheaply.

Note that these Tenured ⇒ Nursery edges in the heap graph won’t last very long, because the next minor GC will promote all survivors in the Nursery to the Tenured heap. So we only care about the Tenured objects that have been modified since the last minor (or major) GC. That won’t be a huge number of objects, so we make the code that writes into Tenured objects check whether it is writing any Nursery pointers, and if so, record the cross-generational edges in a *store buffer*.

In technical terms, this is known as a *write barrier*. Then, at minor GC time, we walk through the store buffer and mark every target Nursery object as being live. (We actually use the source of the edge at the same time, since we relocate the Nursery object into the Tenured area while marking it live, and thus the Tenured pointer into the Nursery needs to be updated.)

With a store buffer, the time for a minor GC is dependent on the number of newly-created edges from the Tenured area to the Nursery, not just the number of live objects in the Nursery. Also, keeping track of the store buffer records (or even just the checks to see whether a store buffer record needs to be created) does slow down normal heap access a little, so some code patterns may actually run slower with GGC.

## Allocation Performance

On the flip side, GGC can speed up object allocation. The pre-GGC heap needs to be fully general. It must track in-use and free areas and avoid fragmentation. The GC needs to be able to iterate over everything in the heap to find live objects. Allocating an object in a general heap like this is surprisingly complex. (GGC’s Tenured heap has pretty much the same set of constraints, and in fact reuses the pre-GGC heap implementation.)

The Nursery, on the other hand, just grows until it is full. You never need to delete anything, at least until you free up the whole Nursery during a minor GC, so there is no need to track free regions. Consequently, the Nursery is perfect for *bump allocation*: to allocate *N* bytes you just check whether there is space available, then increment the current end-of-heap pointer by *N* bytes and return the previous pointer.

There are even tricks to optimize away the “space available” check in many cases. As a result, objects with a short lifespan never go through the slower Tenured heap allocation code at all.

## Timings

I wrote a simple benchmark to demonstrate the various possible gains of GGC. The benchmark is sort of a “vector Fibonacci” calculation, where it computes a Fibonacci sequence for both the *x* and *y* components of a two dimensional vector. The script allocates a temporary object on every iteration. It first times the loop with the (Tenured) heap nearly empty, then it constructs a large object graph, intended to be placed into the Tenured portion of the heap, and times the loop again.

On my laptop, the benchmark shows huge wins from GGC. The average time for an iteration through the loop drops from 15 nanoseconds (ns) to 6ns with an empty heap, demonstrating the faster Nursery allocation. It also shows the independence from the Tenured heap size: without GGC, populating the long-lived heap slows down the mean time from 15ns to 27ns. With GGC, the speed stays flat at 6ns per iteration; the Tenured heap simply doesn’t matter.

Note that this benchmark is intended to highlight the improvements possible with GGC. The actual benefit depends heavily on the details of a given script. In some scripts, the time to initialize an object is significant and may exceed the time required to allocate the memory. A higher percentage of Nursery objects may get tenured. When running inside the browser, we force enough major GCs (eg, after a redraw) that the benefits of GGC are less noticeable.

Also, the description above implies that we will pause long enough to collect the entire heap, which is not the case — our [incremental garbage collector](http://blog.mozilla.org/javascript/2012/08/28/incremental-gc-in-firefox-16/) dramatically reduces pause times on many Web workloads already. (The incremental and generational collectors complement each other — each attacks a different part of the problem.)


## Benchmark Code

```
function bigHeap(N) {
var result = [];
for (var i = 0; i < N; i++)
result.push({ 'number': i, 'prev': result[-1] });
return result;
}
function add(a, b) {
return [a[0] + b[0], a[1] + b[1]];
}
function vecfib(n) {
var v1 = [0, 0];
var v2 = [1, 1];
for (var i = 0; i < n; i++) {
var v = add(v1, v2);
v1 = v2;
v2 = v;
}
return v1;
}
var t = {};
var iters = 10000000;
t.smallheap_start = Date.now();
var dummy1 = vecfib(iters);
t.smallheap_end = Date.now();
H = bigHeap(10000000);
t.bigheap_start = Date.now();
var dummy2 = vecfib(iters);
t.bigheap_end = Date.now();
print("Small heap: " + ((t.smallheap_end - t.smallheap_start) / iters) * 1000000 + " ns/iter");
print("Big heap: " + ((t.bigheap_end - t.bigheap_start) / iters) * 1000000 + " ns/iter");
```

## About
[
Steve Fink ](https://blog.mozilla.org/sfink/)

SpiderMonkey JavaScript engine developer, working mainly on the garbage collector and static analysis. Also moonlights working on release engineering, mercurial customization, and generally making a nuisance of himself. Author of the 'mrgiggles' bot on IRC.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 14 comments

StyMaarSeptember 26th, 2014 at 05:52Robert Nyman [Editor]September 26th, 2014 at 07:49Ed MurphySeptember 29th, 2014 at 09:07ThorstenSeptember 30th, 2014 at 06:12Dawson LoudonOctober 1st, 2014 at 07:38Robert Nyman [Editor]October 1st, 2014 at 08:01eaglgenes101October 5th, 2014 at 15:54Steve FinkOctober 6th, 2014 at 09:50Naman PatelOctober 12th, 2014 at 03:45Steve FinkOctober 13th, 2014 at 09:13Naman PatelOctober 13th, 2014 at 10:44Terrence ColeOctober 17th, 2014 at 11:21Steve FinkOctober 17th, 2014 at 11:43Naman PatelOctober 21st, 2014 at 05:22