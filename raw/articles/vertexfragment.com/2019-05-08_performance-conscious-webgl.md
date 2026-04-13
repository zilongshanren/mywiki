---
title: Performance Conscious WebGL
url: https://www.vertexfragment.com/ramblings/performance-conscious-webgl/
author: Steven Sell
published: '2019-05-08'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

*Disclaimer: I am not a JavaScript developer. I just happen to find myself using it more than expected.*

Recently, I began to [dabble in WebGL](https://github.com/ssell/webgl-experiments). This is not unexpected as I have a history of both hobbyist and professional work in graphics programming, as you may tell from the name of this website. And though my journey began with OpenGL, much of my most recent work has been in Direct3D.

As there is no WebD3D, and I am not entirely sure I would want to venture down that path if it existed, I found myself back more-or-less to my roots. However in my recent experimentations I have come across a number of performance critical surprises which are documented in this article.

And as my collection of experiments and demos grow, assuredly so will this list of interesting, and at times perplexing, performance gotchas. Hopefully some of these will help out others who find themselves in the wild and typeless world of JavaScript-based graphics programming.

A [ Float32Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Float32Array) is often used as the source buffer for calls to

[, though other](https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/bufferData)

`bufferData`

[implementations can be used (and they likely suffer the same performance penalty as described below).](https://developer.mozilla.org/en-US/docs/Web/API/ArrayBufferView)

`ArrayBufferView`

In my instanced rendering pipeline, I store material property data for a large number of objects in a single `Float32Array`

. The exact amount of data varies, based on the underlying type (`vec3`

vs `mat4`

, etc.) and the upper limit of objects in a single instance. The important part to note is that subsets of these arrays are regularly updated.

Initially these updates were being performed using the provided [ Float32Array.set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/set) method, such as:

|
|

However according to [these performance results](https://jsperf.com/float32array-performance-set/2), this is **40% slower** than manually setting the values yourself.

|
|

Alternatively, using a `while`

instead of a `for`

is marginally even faster:

|
|

Using a [ Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map) with a string key is really nice as it is a simple way to store relational data that is easy to understand. Especially so when initially setting up a framework and you just want to get things working ASAP.

As an example, as part of my instanced rendering pipeline I organize objects based on their material and mesh. Objects that use the same material and mesh combination are rendered in the same instance. A simple way to describe this relationship is a string such as `"<material_id>:<mesh_id>"`

. Easy right? And of course using a string as a key is slow and not optimal, but it can’t be *that* slow can it?

Well, it is.

When rendering 50,000 objects, my `addRenderObject`

method which constructed the above string and inserted the object into a `Map`

took **17ms** according to the Chrome profiler. So much for doing the entire frame in 16.67ms and hitting 60 FPS.

After putting in the little bit of effort required to generate integer IDs for my materials and meshes, and using those to create a Cantor Pair as the key into the `Map`

instead, the time spent in `addRenderObject`

over the same 50,000 objects dropped down to **1ms, a 94% improvement**.

And if you don’t believe me you can check the [performance results](https://jsperf.com/map-set-string-vs-index/1) of ~35 million ops/sec for string-based IDs vs ~110 million ops/sec for cantor pair integer-based IDs.

This was the most perplexing performance penalty during my initial tune-up effort.

While profiling the code, I noticed that a good chunk of time was spent in the `update`

method for my flashing quads. This led to a lot of optimizations in how material properties were structured and handled. But even after those efforts I was still seeing 15ms or more spent in `update`

over 150,000 objects. The method looked similar to this:

|
|

That is barely anything, even for 150,000 objects. Incrementing one variable through the `super`

call, and then another three through `translate`

. So what is taking so long?

After a little bit of tinkering I began suspecting the `super`

itself. After changing that to the equivalent, but a bit more verbose, call of `SceneObject.prototype.update.call(this, delta)`

there was a **reduction of 8ms**. Then when I decided that calling into the parent wasn’t even necessary, and instead updating `timeElapsed`

inside of `FlashingQuad`

itself, there was an additional improvement of **5ms**, for a total of **13ms**.

Yes, that is right. Simply invoking `super`

over those 150,000 objects hit me for a **13ms penalty, each frame.**

Looking at the [performance results](https://jsperf.com/super-is-super-expensive/1) we see the same thing:

- super: 13.7 million ops/sec
- prototype: 121.6 million ops/sec
- self: 125.8 million ops/sec

Though these results speak more favorably to [ Function.prototype.call](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/call) than my personal experience, they agree on the fact that super is super slow.