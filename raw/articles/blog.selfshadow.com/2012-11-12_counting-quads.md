---
title: Counting Quads
url: https://blog.selfshadow.com/2012/11/12/counting-quads/
author: Stephen Hill
published: '2012-11-12'
source_blog: Self Shadow
source_site: https://blog.selfshadow.com/
category: graphics
fetched: '2026-04-13'
---

*This is a DX11 followup to an earlier article on quad ‘overshading’. If you’ve already read that, then feel free to skip to the meat of this post.*

## Recount

As you likely know, modern GPUs shade triangles in blocks of 2x2 pixels, or *quads*. Consequently, redundant processing can happen along the edges where there’s partial coverage, since only some of the pixels will end up contributing to the final image. Normally this isn’t a problem, but – depending on the complexity of the pixel shader – it can significantly increase, or even dominate, the cost of rendering meshes with lots of very small or thin triangles.

![Figure 1: Quad overshading, the silent performance killer.](../../assets/b6ac2ab717dff4ce.png)

Figure 1: Quad overshading, the silent performance killer.

*For more information, see Fabian Giesen’s post, plus his excellent series in general.*

It’s hardly surprising, then, that IHVs have been advising for years to avoid triangles smaller than a certain size, but that’s somewhat at odds with game developers – artists in particular – wanting to increase visual fidelity and believability, through greater surface detail, smoother silhouettes, more complex shading, etc. (As a 3D programmer, part of my job involves the thrill of being stuck in the middle of these kinds of arguments!)

Traditionally, mesh LODs have helped to keep triangle density in check. More recently, deferred rendering methods have sidestepped a large chunk of the redundant shading work, by writing out surface attributes and then processing lighting more coherently via volumes or tiles. However, these are by no means definitive solutions, and nascent techniques such as DX11 tessellation and [ tile-based forward shading](http://aras-p.info/blog/2012/03/27/tiled-forward-shading-links/) not only challenge the status quo, but also bring new relevancy to the problem of quad shading overhead.

Knowing about this issue is one thing, but, as they say: *seeing is believing*. In a [previous article](https://blog.selfshadow.com/publications/overdraw-in-overdrive/), I showed how to display hi-z and quad overshading on Xbox 360, via some plaform-specific tricks. That’s all well and good, but it would be great to have the same sort of visualisation on PC, built into the game editor. It would also be helpful to have some overall stats on shading efficiency, without having to link against a library ([GPUPerfAPI](http://developer.amd.com/tools/gpu/GPUPerfAPI/Pages/default.aspx), [PerfKit](https://developer.nvidia.com/nvidia-perfkit)) or run a separate tool.

There are several ways of reaching these modest goals, which I’ll cover next. What I’ve settled on so far is admittedly a hack: a compromise between efficiency, memory usage, correctness and simplicity. Still, it fulfils my needs so far and I hope you find it useful as well.

## Going To Eleven

First, let’s restate the problem: what we want, essentially, is to count up the number of times we shade a given *screen* quad. The trick is to only count each *shading* quad once.

The way I achieved this on Xbox 360 hinged on knowing whether a given pixel was ‘alive’ or not, and then only accumulating overdraw for the first live pixel in each shading quad. As far as I’m aware, there’s no official way of detemining this on PC through standard graphics APIs, but some features of DX11 – namely *Unordered Access Views* (UAVs) and atomic operations – will allow us to arrive at the same result via a different route.

#### The right way

What I was after was an implementation that was as simple as before, involving three steps:

- Render depth pre-pass (optional; do whatever the regular rendering path does for this)
- Render scene (material/lighting passes) with special overdraw shader
- Display results

A straightforward, safe option is to gather a list of triangles per screen quad, filtering by ID (a combination of `SV_PrimitiveID`

and object ID). This filtering can be performed during the overdraw pass or as a post-process.

What’s unsatisfying with this approach is that it involves budgeting memory for the worst case, or accepting an upper bound on displayable overdraw. Whilst I can imagine that a multi-pass variation is doable, that just adds unwanted complexity to what ought to be a simple debug rendering mode.

#### The wrong way

So, in order to overcome these limitations, I started toying around with something a lot simpler:

```
1RWTexture2D<uint> primIDUAV : register(u0);
2RWTexture2D<uint> overdrawUAV : register(u1);
3
4[earlydepthstencil]
5void OverdrawPS(float4 vpos : SV_Position, uint id : SV_PrimitiveID)
6{
7 uint2 quad = vpos.xy*0.5;
8 uint prevID;
9
10 InterlockedExchange(primIDUAV[quad], id, prevID);
11
12 if (prevID != id)
13 InterlockedAdd(overdrawUAV[quad], 1);
14}
```


The intent here is to use a UAV to keep track of the current triangle per screen quad. Through `InterlockedExchange`

, we both update the ID and use the previous state to determine if we’re the first pixel to write this ID (`prevID != id`

). If so, we increment an overdraw counter in a second UAV. This is similar in the spirit to the Xbox 360 version, in that we’re selecting one of the live pixels in a shading quad to update the overdraw count. Finally, we can display the results in a fullscreen pass:

```
1Texture2D<uint> overdrawSRV;
2
3float4 DisplayPS(float4 vpos : SV_Position) : SV_Target
4{
5 uint2 quad = vpos.xy*0.5;
6 return ToColour(overdrawSRV[quad]);
7}
```


On paper, this appears to elegantly avoid the storage and complexity of the previous approach. Alas, it relies on one major, dubious assumption: that quads are shaded sequentially! In reality, GPUs process pixels in larger batches of *warps/wavefronts* and there’s no guarantee that UAV operations are ordered between quads – hence the name: *unordered*. So, during the shading of pixels in a quad for one triangle, it’s perfectly possible for another unruly triangle to stomp over the quad ID and break the whole process!

#### The cheat’s way

Fortunately, we can get around this issue with a few modifications. The basic idea here is to loop and use `InterlockedCompareExchange`

to attempt to *lock* the screen quad:

```
1RWTexture2D<uint> lockUAV : register(u0);
2RWTexture2D<uint> overdrawUAV : register(u1);
3
4[earlydepthstencil]
5void OverdrawPS(float4 vpos : SV_Position, uint id : SV_PrimitiveID)
6{
7 uint2 quad = vpos.xy*0.5;
8 uint prevId;
9
10 uint unlockedID = 0xffffffff;
11 bool processed = false;
12 int lockCount = 0;
13
14 for (int i = 0; i < 16; i++)
15 {
16 if (!processed)
17 InterlockedCompareExchange(lockUAV[quad], unlockedID, id, prevID);
18
19 [branch]
20 if (prevID == unlockedID)
21 {
22 // Wait a bit, then unlock for other quads
23 if (++lockCount == 2)
24 InterlockedExchange(lockUAV[quad], unlockedID, prevID);
25 processed = true;
26 }
27
28 if (prevID == id)
29 processed = true;
30 }
31
32 if (lockCount)
33 InterlockedAdd(overdrawUAV[quad], 1);
34}
```


This leads to three outcomes for unprocessed pixels:

- If
`prevID == unlockedID`

, then the pixel holds the lock for its shading quad - If
`prevID == id`

, another pixel in the shading quad holds the lock - Otherwise, no pixel in the shading quad holds the lock

In the first case we mark the pixel as processed and increment a lock counter. After an additional iteration, we release the lock. This ensures that pixels with the same ID see the state of the lock (second case), so that they can be filtered out. Finally, pixels that held the lock update the quad overdraw.

Ideally we’d loop until the pixel has been tagged as processed, but I haven’t had success with current NVIDIA drivers and UAV-dependent flow control, i.e.:

```
1[allow_uav_condition]
2while (1)
3{
4 // ...
5
6 if (++lockCount == 2)
7 {
8 InterlockedExchange(lockUAV[quad], unlockedID, prevID);
9 break;
10 }
11
12 // ...
13
14 if (prevID == id)
15 break;
16}
```


As a workaround, I’ve simply set the iteration count to a number that works well in practice across NVIDIA and AMD GPUs (those that I’ve had a chance to test, anyway).

## Four, Three, Two, One

Now that we have a working system in place, it’s easy to gather other stats. For instance, although we can’t determine directly if a pixel is alive, we can count the number of live pixels in each shading quad, since `Interlocked*`

operations are masked out for dead pixels. With this, we can tally up the number of quads with 1 to 4 live pixels in yet another UAV:

```
1RWTexture2D<uint> lockUAV : register(u0);
2RWTexture2D<uint> overdrawUAV : register(u1);
3RWTexture2D<uint> liveCountUAV : register(u2);
4RWTexture1D<uint> liveStatsUAV : register(u3);
5
6[earlydepthstencil]
7void OverdrawPS(float4 vpos : SV_Position, uint id : SV_PrimitiveID)
8{
9 uint2 quad = vpos.xy*0.5;
10 uint prevID;
11
12 uint unlockedID = 0xffffffff;
13 bool processed = false;
14 int lockCount = 0;
15 int pixelCount = 0;
16
17 for (int i = 0; i < 64; i++)
18 {
19 if (!processed)
20 InterlockedCompareExchange(lockUAV[quad], unlockedID, id, prevID);
21
22 [branch]
23 if (prevID == unlockedID)
24 {
25 if (++lockCount == 4)
26 {
27 // Retrieve live pixel count (minus 1) in quad
28 InterlockedAnd(liveCountUAV[quad], 0, pixelCount);
29
30 // Unlock for other quads
31 InterlockedExchange(lockUAV[quad], unlockedID, prevID);
32 }
33 processed = true;
34 }
35
36 if (prevID == id && !processed)
37 {
38 InterlockedAdd(liveCountUAV[quad], 1);
39 processed = true;
40 }
41 }
42
43 if (lockCount)
44 {
45 InterlockedAdd(overdrawUAV[quad], 1);
46 InterlockedAdd(liveStatsUAV[pixelCount], 1);
47 }
48}
```


To my surprise, incrementing a 4-wide UAV didn’t lead to a massive slowdown here. That said, one can certainly use a number of buckets for intermediate results (indexed by the lower bits of the screen position, for instance), if this proves to be a problem.

With these numbers, it’s trivial to add a pie chart to the final pass:

![](../../assets/fd867925fea32680.png)

*Figure 2: Quad overdraw (dark blue = 1x, to green = 4x),and proportion of live pixels per quad (yellow = 4, to dark red = 1).*

## Demolition

For your convenience, I’ve packaged things up into a [simple demo](https://blog.selfshadow.com/code/QuadShading.zip). Please let me know if you hit any compatibility issues, or come up with any enhancements.