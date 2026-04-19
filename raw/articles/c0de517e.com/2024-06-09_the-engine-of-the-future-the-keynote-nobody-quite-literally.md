---
title: The engine of the future.The keynote nobody (quite literally) asked for.
url: https://c0de517e.com/014_future_engines.htm
author: Angelo Pesce
published: '2024-06-09'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

[REAC 2024](enginearchitecture.org) is over, so it seems fitting to think about the mechanics of real-time renderings and perhaps, predict the future a bit!

These kinds of exercises are, I have to admit, not something I generally favor. Humanity is chaotic. But at the same time, certain trends are pretty obvious to observe and extrapolate - so one could say at least that barring changes in the environment, there are often clear trajectories to see.

A few constraints, before we start. I won't be talking about visuals for the most part, i.e. shading, lighting et al, rendering algorithms. And I won't be talking about all the ways the industry can evolve beyond pushing "more of the same" - i.e. UGC, cloud computing/server-side rendering, massive social worlds, AR or whatever else you might consider an interesting future for the industry.

I will be speculating only about the "engine" side and how to push more content, more efficiently. Which unfortunately is the area of rendering I consider myself less of an expert, so, prepare for a wild ride :)

Real-time 3d rendering has been going in a straight line for a couple of decades now, so we can feel pretty confident. The line I'm talking about, of course, is the one that rides the exponential growth in parallel processing, the consequent increasing disparity between memory and compute, and the work-expansion needed to fill bigger and bigger chips with data-parallel threads to execute.

![You should read Fabien's writeup on the voodoo 1: https://fabiensanglard.net/3dfx_sst1/](../../assets/b86ffcf10e36a919.png)

You should read Fabien's writeup on the voodoo 1: https://fabiensanglard.net/3dfx_sst1/
One can trace this line back to the first hardware-accelerated systems for rendering. If we stay on the consumer (mass-market) side of things (videogames), say, MMX and 3dfx Voodoo? One can find different points, it doesn't matter much because the mechanics are always the same. Sidenote -

[this website](https://vintage3d.org/) is fun, contemporary reviews of old GPUs. If one wants to delve deeper, opensource drivers and PC emulators are also a nice source of knowledge.

We start handing off to hardware acceleration the innermost loops. Originally, triangle filling. Maybe even less than triangles, scanlines? If you look at the first 3d chips, they all vary in the amount of effort that they ask the CPU to perform to setup a triangle. These are small DSPs, so it doesn't take that much to fill them with work.

Eventually, chips grow. More ALUs, texture units, bottom line - we can't keep up with work generation. Enter "transform and lighting" - moving now vertex processing to the GPU.

GPUs are beasts of insatiable hunger. Driven by the ability to increase transistor count, they need more and more work to keep them fed, and more work of a specific kind - memory-friendly, data-parallel (in the SIMD sense) "wide" work, they can use to hide latencies and pack more ALUs per unit of control.

As they go wider and wider, they also move from needing to exploit some degree of instruction-level parallelism (VLIW, SIMD instructions) to being able to rely on scalar ISAs and switching between "threads" instead.

In general, we can say:

- Work amplification = great, we always want to have one unit of "control" generate exponentially more units of work.

- Data-parallel work = good

- Sorting (reordering)/Culling = careful! - can be overall a win, but requires internal buffers which can create bottlenecks!

- Small work batches = bad

- Cache misses = very bad

- Serialization, dependency chains = terrible

All progress in real-time rendering respects these rules.

Vertex shaders? Allowed to upload only small pieces of data (a draw, some constants) to initiate parallel work on the GPU (vertex processing, triangle generation, culling, pixel shading)

Pixel shaders? Yes, they gave expressive power - which is good in terms of image quality - but they were also the right way to give power. They allowed rendering techniques that previously required multi-pass rendering (memory traffic) to remain on chip.

Dynamic branching? It might seem quite anti-GPU, as it is a significant element of complexity in SIMD processing - and indeed every rendering engineer knows about the perils of "divergence", but it allowed for more work of the right kind, where the alternative would have been again to do multiple passes.

Where are we today? The state of the art lies in touching as little memory as possible to initiate work. Even with "thinner" APIs, CPU multithreading, and the like, the art of a contemporary real-time engine is in how to thin down the inevitable communication from the CPU (typically, game logic, scene updates) to the command buffer generation.

Command buffers became more expressive - first with instancing (vertex frequency divider), then parallel generation, then allowing precise control over constant resources, then provisioning for GPU-driven pipelines, bindless et al.

If we were to write an engine today, its role would be entirely around resource management, nothing else, on the CPU. Manage memory pools, swapping (streaming) resources in and out - effectively, the CPU knows about the world and its dynamics, and it constantly has to figure out what subset to expose to a GPU, in the most efficient way.

Very little of "rendering", the actual "drawing" needs to happen driven by a CPU, we can emit always the same handful of multidrawintrect(s). Not that most engines do that - for a variety of reasons, but we could, and undoubtedly, resource management is the job now.

So? If this is where we are, what's the road ahead? I would imagine a few things. Or at least, these are my hopes.

**Predictions**
1) GPUs will embrace "GPU-driven" rendering and allow for direct command buffer generation on the GPU, instead of the current awkward slew of draw commands and opaque prerecorded command lists. Perhaps we'll have "command shaders" (work graphs are clearly a step towards that direction)? On the other hand, if this becomes true, there might be less of a need of multiple command queues, albeit, that might be true only when thinking of a single app. Async will on the other hand always matter to opportunistically fill gaps, having different sources/kinds of work is a good idea, and already today the concept of a "frame" is lost, with so many tasks running at different frequencies to update data structures in a temporal-amortized way - I can't see this trend reversing itself - if anything we'd see the need of more and better way to signal GPU work. The GPU as a true OS. At the limit, will we need a command buffer, at all? Or just "tasks" that can be spawned from the CPU and can spawn themselves others?

2) As a consequence, GPUs will need to provide more options to debug the "command buffer"/currently running and queued commands. Currently, we are at the crossroads of "everything goes" - where capture tools can't predict what memory will change, and "nothing is debuggable" as stepping and even live-coding abilities have been focusing on the shader cores, not the control units.

3) Resource creation will need to move to the GPU. This means the ability to initiate asynchronous transfers from main memory, from SSDs, and the like. DirectStorage speeds up transfers, but they are still effectively CPU-initiated.

4) This also means culling might be a GPU-only affair, does the CPU need to know about the scene at all? Can the GPU communicate back visibility, for other systems? Or, as is already for the most part true today, the CPU will keep its scene approximation for gameplay (collisions, audio et al). It might be neat to truly be able to process geometry once and dispatch results to multiple "views".

5) CPUs will keep working on inputs and game logic, and the minimal updates needed to be communicated as a result of these. This, mainly because that's the part of the job that is not, by its nature, amenable to massively parallel processing (at least, not anytime soon).

6) I've always believed that triangles, derivatives (differentials/quads), barycentric setup, and the like would be a bottleneck to eventually kill. I don't think the world is made of simple surfaces densely "shaded", I think there is circa the same amount of geometric complexity as "shading", and that will end up making the vertex->pixel pass "buckle". If we end up with no work amplification there, e.g. near the one vertex-per-pixel limit, the system does not work. And we saw that resolutions won't keep climbing, if anything, the number of shaded pixels is decreasing, with temporal reconstruction techniques. I feel vindicated regarding this long-standing belief now that Nanite made that point quite strongly.

That said, I don't think the hardware raster will go away anytime soon, both because it's a small part of the GPU, and because it does such an important job in work amplification, culling, and scheduling/redistribution, in ways that are quite specific to the hardware. In fact the jury is still out re:how much deferred/tiled (and thus "complex") the raster should be. If anything, I imagine we'll have more ways to inject custom work? Not sure.

7) Memory traffic is not the only limit, if anything capacity is an even bigger issue. Compression will play a bigger role, in all its forms. Compressing assets for delivery, network streaming, for disk storage, in memory, in cache. And all the procedural generation ideas, which of course are again forms of compression (Kolmogorov...) and require the ability to generate GPU-compressed formats on the fly. Think, virtual texturing, displacement mapping, scattering of geometry et al. In the world of GaaS and big platforms that effectively are 3d content streaming systems, there is no doubt that a big part of the engines of the future is in their cloud and content distribution considerations.

8) We know that we are moving from being chip-size-limited (number of transistors) to energy and heat-limited - at least for most consumer electronics (e.g. not so much perhaps in 4090, but already true in a console, and obviously, in anything mobile). This might change the equations more, where the game might not be anymore to have all the transistors "hot" most of the time (maximizing utilization), but could allow for various areas of a GPU to stay cold, on purpose, as long as the effective-work-per-watt keeps climbing. Might mean more specialized silicon, more heterogeneous chips - not just relying on the sheer scale of generic compute, but having to target a few different units on the same chip, more than it's already true today (DMA engines etc).

9) There is something to be said about ML. I won't, though, in this article, that's... for another time.

10) Raytracing. I haven't mentioned it here so far, and in part, I could say it is because I wanted to talk more about engine-affecting ideas, versus rendering as in algorithms for lighting and shading. But the other part is that I still struggle to fully embrace an idea that in my mind is relatively anti-GPU, i.e. goes against the tenets of good, memory-coherent work. I always thought that raytracing and the like would make sense after our scenes were already at peak density, when, like in the offline world, geometric and texture detail is effectively already unlimited. But there is one angle that is worth considering, and that is again the memory one. We could see raytracing as a form of procedural generation, as it is often the substitute for large amounts of precomputed lighting data. In general, I think we will need to compute more on the fly - we are past the point where we can spare memory for computation. Cache, yes, temporal amortization, yes, but less precomputation. In that, hardware raytracing seems could play a key role in future efficiencies.

I think stopping at 10 bad predictions is perfect.

One last thing that seems interesting is how once upon a time, mobile was the realm where oldschool techniques applied, could be recycled. Nowadays, not so much, especially on the engine side of things. High-end mobile follows the same rules, in fact for some regards, spearheads them as there memory is even more of a problem, and of course, energy efficiency always has been (while only now is starting to be more of a factor on console).

Even if gaming on an M4 still looks somewhat between one and two generations behind, due to the extreme memory constraints, engine architecture should not. And low-end (a.k.a. most) mobile is a completely different ballgame, a landscape more uncharted than simply time-delayed compared to the gaming state of the art.

**Appendix:**
![](../../assets/cc5e5437a18d5c1d.png)

Isn't it interesting how we went from precise triangle culling, due to "fill-rate" being the main bottleneck, to sending over coarsely culled draws, as most engines could not cope with issuing too many of them, back to software triangle culling, but on GPU and for completely different reasons - not because fill-rate is a problem and not even necessarily because the raster is, but because shading invisibile vertices (and even simply fetching the memory) could be an issue...