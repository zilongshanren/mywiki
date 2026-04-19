---
title: Raytracing Myths
url: https://c0de517e.blogspot.com/2011/09/raytracing-myths.html
published: '2011-09-19'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I've already blogged about

[raytracing and rasterization](http://c0de517e.blogspot.com/2008/03/raytracing-vs-rasterization.html), a[couple of times](http://c0de517e.blogspot.com/2008/03/more-on-raytracing.html), and I guess I should stop. Still,[duty calls](http://xkcd.com/386/)when I read statements such as "[rasterization cannot be parallelized nearly as effectively as ray tracing](http://altdevblogaday.com/2011/09/19/why-i-still-think-ray-tracing-is-the-future/)".Let's go!

**Algorithms**

Let's sketch both algorithms in some sort of pseudo-accurate pseudo-code:



*Raytracing (first-hit)*

for_each pixel px on screen { for_each primitive pr in scene { intersect ray(px) with pr }}

*Rasterization*

for_each primitive pr in scene { for_each pixel px covered by pr { mark px on pr }}

Pretty similar right? The inner loops are different, one intersects a ray equation with the analytic description of a primitive, the other in some way walks on the primitive marking pixels covered by the primitive (i.e. for triangles, by scanline interpolation or by walking on the pixels of the bounding box checking the edge equations).

Visible Pixels: there is a fundamental difference here that we will disregard for the future, as it's written raytracing has to walk on all the pixels of the screen, while rasterization walks all the pixels covered by primitives, thus is only part of the screen is covered raytracing has a disadvantage. The same could be said of rasterization if primitives have large parts that off-screen. This is true but not interesting, rasterization could solve the problem by clipping (moving the complexity from pixels to objects at least) and raytracing could subdivide the screen and identify empty tiles, anyhow this does not change the problem in general and does not change the complexity.

Also, some of you might have noticed that the description I've made is overly simplistic. What I've sketched does not deal in any way with depth hiding. Both algorithms need to keep track of which primitive is the closest for every pixel. Fundamentally it's the same operation, but it has a different memory cost due to the ordering of the operations: raytracing can keep a single depth while scanning every primitive of a pixel and understand which primitive is the closest to the camera, rasterization needs to keep a value for each pixel as we will know which is the closest only when the outer loop is done (z-buffer!).

*Raytracing (first-hit)*

for_each pixel px on screen { for_each primitive pr in scene { intersect ray(px) with pr, keep nearest depth }}

*Rasterization*

zbuffer = list of depths

for_each primitive pr in scene { for_each pixel px covered by pr { mark px on pr, store nearest in zbuffer }}

**Complexity**

So memory-wise rasterization is worse than raytracing! We have to keep a z-buffer! Not so fast... Let's assume that we have a huge scene to render. Maybe we want even to stream stuff. What could we do with both algorithms? It looks like we would need to have around, in memory, the contents of the inner loop, while we could stream over what's in the outer loop. It's another interesting difference that originates from the same fundamental fact, the two loops are inverted. The z-buffer can be nifty because we can stream primitives through it, no matter how huge the scene is, we can go primitive by primitive and keeping only the z-buffer around we can render a scene. Raytracing on the other hand, has to keep primitives around.

Now we can of course imagine variants for both to be more efficient, z-buffer can be subdivided in tiles (or, for other reasons that are thought still about memory efficiency, we can use a hierarchy), primitives in raytracing can similarly partitioned and aggregated using bounding volumes and so on. It does not really change that we don't have a winner, we have the same computation expressed in a different order, which leds to different trade-offs.

What about the compute time? It's evident that from what I've sketched, it's identical. But raytracing is O(log(primitives))

[right](http://dl.acm.org/citation.cfm?id=30319)? At least using spatial subdivision structures and disregarding the complexity of building them (which is often more than linear, thus making from the beginning complexity arguments rather moot)...It might not be obvious how that is not true, so let's make a couple of examples, hopefully these will be enough to generalize to any subdivision structure.A scene with two group of primitives, one on screen, one off screen. These are bound by a box each, and the two boxes are bound with another box, thus creating a box hierarchy.

What would the raytracer do? It would for every pixel on screen check the outer box, for each pixel intersecting it it would check then inner boxes, one will fail always and not trigger the check with the inner primitives, the other will not and thus we will end up checking only one of the groups.

Rasterization? We go through all the pixels of the outer box, we see that something is on screen so we go through all the pixels of the inner boxes, one will be on screen, the other won't and we will render only one group of inner primitives.

Other than the tradeoff between "for every pixel on screen" and "for every pixel covered by primitive" - the "visible pixels" problem that I already said that we would disregard, it's the same thing.

But that is about screen coverage in two of the dimensions. What about depth complexity?

A sparial subdivision structure with a raytracer provides a way of having guarantees on the depth ordering. For each ray, if we find an intersection in a given depth of the subdivision, we don't have to proceed any further, we know that all the primitives in lower depths are hidden for that ray. Or to put it in another way, for all the nodes that are fully covered by previous node's primitives, we don't do any work.

Doesn't that happen also for rasterization? Let's persuade ourselves of this fact. Assume that we have a depth-only hierarchy, our scene is split into different "chunks" along the depth, each chunk is defined by a splitting plane and contains a primitive. Now, let's say that the primitive of the first chunk covers the entire screen. Obviously in a raytracer we would trace that and stop, considering once all the pixels of the first plane, then once over all the pixels of the primitive, and then ending. In a rasterizer, we would rasterize the plane, then the primitive, then the following plane, find it all occluded and end. A bit more work, but constant, no matter how deep the chunk with the all-covering primitive is we stop always analyzing one more plane, so it's not a concern complexity wise.

What if the primitive does not cover the entire screen though? What if it leaves exactly one pixel not covered? The raytracer would then go and check the following chunks against that single pixel only until a primitive covers it. The rasterizer would rasterize all the pixels in the planes every time it need to check, until the primitive covers it. It seems that we have a fundamental difference here, we could invoke again the "visible pixels" principle, but we would like a way to make the occlusion test resolution independent for the rasterizer to have the same cost.



To be clear, I'm not advocating the use of BVHs and z-buffer pyramids in your game engine today. I'm just saying you could, so the big algorithmic complexity argument about the doom day when rasterization will not be viable anymore are wrong. By the way, it won't even be a very impractical method good only on the paper (like the constant-time raytracing stufff), it would probably be a good idea in some heavily occluded scenes...

To be clear, I'm not advocating the use of BVHs and z-buffer pyramids in your game engine today. I'm just saying you could, so the big algorithmic complexity argument about the doom day when rasterization will not be viable anymore are wrong. By the way, it won't even be a very impractical method good only on the paper (like the constant-time raytracing stufff), it would probably be a good idea in some heavily occluded scenes...

Luckily depth complexity in practice is not even a huge deal for rasterizers, for example on a GPU. How comes? Overdraw should kill us, how do we avoid it? We can because a GPU does not need to rasterize fully covered primitives, if we have a front-to back ordering we can save most of the cost by checking our primitives against a coarse z-buffer, before shading. In a GPU shading is the big cost, and so we just do an early depth test and live with that, but in theory this works in general, we can make the occlusion cost logarithmic on the pixels by subdividing the z-buffer grid in a hierarchy and in fact if we're interested in occlusion culling and not on shading, this is a good idea (

[see HOMs](http://www.cs.unc.edu/~zhangh/hom.html)).In the real world, if we want to talk outside the theory and useless statements about big-O complexity, both techniques need to deal with primitives and occlusions and they are if not equally good, very close, with both being able to handle scenes of immense complexity and out-of-core rendering. Both can be linear, logN or whatever, it's only that some techniques make more sense in some situations, so in practice most raytracers are logN with N^2 or more subdivision structure build times, rasterizers are mostly linear, both live happily with that on equally complex scenes.



Ironically in some way, raytracing which is said to be less dependent on primitive counts, absolutely needs accelleration structures for all but the simplest scenes, no raytracer goes without one, that's because you need them not only for depth complexity, but also to deal with the screen-space one (I guess you could cull primitives, LOD and tile, but then it would be so very close to a rasterizer not to be really smart, so really no one does that).

Rasterization on the other hand performs great on a wider range of scenes and needs z-buffer hierarchies, level of detail and other complex occlusion strategies only when the shading costs are negligible and the scenes have a lot of depth complexity. Both can do amazing things.

Ironically in some way, raytracing which is said to be less dependent on primitive counts, absolutely needs accelleration structures for all but the simplest scenes, no raytracer goes without one, that's because you need them not only for depth complexity, but also to deal with the screen-space one (I guess you could cull primitives, LOD and tile, but then it would be so very close to a rasterizer not to be really smart, so really no one does that).

Rasterization on the other hand performs great on a wider range of scenes and needs z-buffer hierarchies, level of detail and other complex occlusion strategies only when the shading costs are negligible and the scenes have a lot of depth complexity. Both can do amazing things.

**Parallelism and Concurrency**

Enter the second big topic,

[parallelism and concurrency](http://blogs.oracle.com/yuanlin/entry/concurrency_vs_parallelism_concurrent_programming). Raytracing is easier to parallize says the myth - because each ray is independent. Is that true?I can honestly see where this myth comes from, it even has a bit of truth in it. I picture someone in a university, writing a raytracer for fun or for a course and finding that's easy to fork at the ray-generation lever or a parallel_for over some worker threads and it works, because the inner loop is indeed independent, does not rely on shared state. A rasterizer does, for the z-buffer, so it would require some form of syncronization. Not the end of the world, you could have a z-buffer per thread and merge, you could have some a lockless stuff per pixel, tiles or whatever, but still it requires some changes.

So is it easier? In that sense yes. But let's reason as a more experienced engineer (or scientist) and not as a freshmen. We see two nested loops, we are on a modern CPU architecture, what do we do? Instinctively (at least, I hope) we unroll and parallelize the inner (

[instruction parallel](http://en.wikipedia.org/wiki/Instruction_level_parallelism)), and try to make concurrent the outer ([data parallel](http://en.wikipedia.org/wiki/Instruction_level_parallelism)). In this respect, how do the two algorithms fare?These two, powerful forms of parallelism are absolutely fundamental to achieve great throughput on modern architectures as it provides them with a lot of coherent computation. Modern CPU execution times are dominated by latencies. Instruction latencies and dependencies and even more nowadays, memory latencies. And this won't change! Latency is hidden by unrolling, by having enough "predictable" computation (and memory access). If we have an operation A1 and a subsequent B1, with B1 dependent on A1 and A1 taking 10 cycles of latency, if we can find nine other instructions between A1 and B1 we're safe, we "hid" the latency. If we can unroll a cycle ten times over data elements 1...10, then we can trivially do A1,A2,A3,... then B1,B2... and we're done.

Now in theory, they are both good. A raytracer inner loop intersect a ray with a number of primitive, a rasterizer walks on a primitive looking for pixels. If the primitives are uniform, both are easy to unroll and play well with SIMD, we can intersect a ray with i.e. four primitives at a time, or in a similar way rasterize four pixels of a scanline (or a 2x2 block...) together.

The outer loop follows the same reasoning we did before, and indeed it's a bit easier on a raytracer. So again a win? Yes if we limit ourselves to a case that does not (as I wrote before) exist: a raytracer without a spatial acceleration structure and shading. And if we don't consider that accessing primitives in the inner loop is way more memory intensive than walking on pixels.

If we write things in "theory", or rather, with a theory based on an over-simplistic model raytracing wins... If we take a realistic renderer on the other hand, things change.

Spatial acceleration breaks uniformity. Shading of different primitives at the same time leads to incoherent memory access. Same for neighboring rays intersecting different groups of primitives. We can have a ray at level zero of the hierarchy and the neighboring one at level ten. A ray might need shading, while the next one might be still traversing. It's a mess!

And not an easy one to fight against at all, how do we deal with that? Well it turns out, it's not that simple, and not fully solved yet.

One of the first approaches was to

[collect rays into the spatial structure](http://graphics.stanford.edu/papers/coherentrt/)cells and then be parallel to all the rays in a given cell. It works if you can generate enough rays, if you have still some coherency, i.e. for a distributed raytracer, less well for a path tracer. And still it deals only with part of the problem.For a while the solution seemed to be to organize rays in "

[packets](http://software.intel.com/en-us/articles/interactive-ray-tracing/)" that could walk the structures together, hoping they won't diverge much or trying to reconstruct some coherence by splitting and merging them. Then we found out that this works again for the kind of coherent loads that (we will see) are not really _that_ interesting for a raytracer, it will give you decently fast first-hit, shadows, the sort of stuff a raytracer is still good at. You can get some perfect mirrors on a sphere or so, how[cool](http://www.geeks3d.com/20080612/ray-traced-quake-wars/)is[that](http://www.pcper.com/reviews/Graphics-Cards/Caustic-Graphics-and-CausticGL-Ray-Tracing-API).More recently, the first approach evolved in more general

[ray reordering](http://sglab.kaist.ac.kr/CORR/)strategies, while the second was turned sideways and experimented with having parallelism on a single ray by[growing the width](http://ieeexplore.ieee.org/xpl/freeabs_all.jsp?arnumber=4634618)of the__acceleration__[structures](http://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/institut/Papers/QBVH.pdf).All this while on GPUs rasterizers have been executing stuff in parallel, where it matters, over tens and hundreds of computational units, for years now (and

[Reyes](http://graphics.pixar.com/library/Reyes/)have been shading in parallel since the '82).**Ease of use**

Simple algorithms are easy to express in both, and writing a bare-bones triangle rasterizer or sphere raytracer (using the primitives that are easier to map in both) is trivial. Maybe the raytracer will take a few lines less, but hardly anything that we care about.

For more complex effects, raytracer starts to win. Adding shadows, reflections. An univeristy student can have a lot of fun with a few lines of code, feeling happy. And from here on, if we never consider resource usage, raytracing always wins. You can solve the entire

[rendering equation](http://en.wikipedia.org/wiki/Rendering_equation)(or so) with a path tracer in a[hundred lines of code](http://kevinbeason.com/smallpt/).But when we make programs, in practice and not on paper, no matter what we have to deal with resources, they enter the equation. Then it becomes a matter of performance and how much do we care about it.

When I started programming, on a commodore 64, I knew only Basic and Assembly, and that was all I knew even when I moved to the Amiga (amos) and the PC (QuickBasic, PowerBasic), until one of my older cousing started university and I grabbed his K&R book. I loved to write graphical effects, and I had to "optimize" code by either tweaking the code to suit better the (to me unknown) logic of the underlying interpreter, or add inline assembly directly via machine code. Hardly easy, even if you might argue that for some things Basic was easier to learn and use than C (and I really liked the QuickBasic PDS IDE at the time...)

I think the complexity argument is rather dumb. Raytracing is less coherent and struggles with performance. Rasterization is more coherent and struggles with algorithms that need more flexibility in the visibility queries. Raytracing needs spatial accelleration structures and complex strategies to gain ray coherency. Rasterization needs fancy algorithms and approximations when it has to deal with global effects and more general visibility queries.

**Conclusion**

In practice if you've shipped a game, you already knew this. What do GPU use to render all these incredibly complex scenes over thousands of processors? What do we do on the other hand if we have to execute random visibility queries, for example for A.I.? Sometimes there are reasons why things are the way they are. The biggest trade-off between the two is surely that raytracing starts with incoherent visibility queries and research is trying to "find" patterns in them in order to gain performance, rasterization starts with coherent primitive walking and research is trying to find algorithms to compute global, complex illumination out of these fast massive queries we can issue (this is a


I liken it to programming languages. Dynamic versus Static, Pure versus Imperative. They are all Turing-complete and in theory equally capable at expressing computation. In practice though they start from different endpoints and try to reach the other, pure languages start safe and strive to express side-effects and program order, imperative start with side effects and strive to achieve safety, and so on.

And if there is something to learn from that (and hopefully there is not :D) is that performance in computer science has been always a stronger drive in the success of a technology than other considerations (we program, unfortunately, in C++ not in Haskell), probably because it's more important to achieve a given amount of quality in practice, than having something that in theory produces something with a higher quality but in practice does not deliver.

[nice example](http://www.mpi-inf.mpg.de/resources/ImperfectShadowMaps/)).I liken it to programming languages. Dynamic versus Static, Pure versus Imperative. They are all Turing-complete and in theory equally capable at expressing computation. In practice though they start from different endpoints and try to reach the other, pure languages start safe and strive to express side-effects and program order, imperative start with side effects and strive to achieve safety, and so on.

And if there is something to learn from that (and hopefully there is not :D) is that performance in computer science has been always a stronger drive in the success of a technology than other considerations (we program, unfortunately, in C++ not in Haskell), probably because it's more important to achieve a given amount of quality in practice, than having something that in theory produces something with a higher quality but in practice does not deliver.

Going back to the

[article](http://altdevblogaday.com/2011/09/19/why-i-still-think-ray-tracing-is-the-future/)that "spawned" all this. Is raytracing the future? Sure it is, it's surely "in" the future of rendering. But not because it's easier, or because it has a lower algorithmic complexity, or because it parallelizes better. None of these big global adjectives apply, that's all bullshit. It's in the future because it's a technique which has a set of trade-offs that are orthogonal to rasterization. It's useful, having more options, techniques, points of view is always useful. There will be areas in which rasterization will always make much more sense, and areas in which raytracing will, while most else will be happy to be able to pick and choose depending on the kind of problem they're facing.I think you can always peek into the future by looking around, looking what other people in other fields with similar problems are doing... In these years, for CG, raytracing and rasterization are influencing each other more and more.

Offline renderers are mixing techniques from both realms, just see what

[Pixar's Photorealistic Renderman](http://renderman.pixar.com/)is capable of doing. It's a Reyes rasterizer, for the first hit. It's parallel, concurrent and distributed. It can do shadowmaps and raytracing. It can cache point clouds and do some sort of screen-space ambient occlusion and so on. Still we lived with rasterization for a long time even in the offline realm especially in some fields that are less concerned about absolute lighting precision.Only recently we started to see GI and raytracing as useful and productive replacements for some algorithms in the offline realm. I expect everything to be more and more hybrid. I don't think rasterization will ever die. Also, from what I know and I see of the research around raytracing I don't think that we'll see it in realtime, in games for quite some time yet.

## 22 comments:

With all due respect: I think you are wrong.




Ray tracing can be made almost insensitive to primitive count. That is why ray tracing a billion primitives is faster than rasterizing a billion primitives.

Rasterizing is O(N) in N number of primitives.

Twice as many primitives, means twice the amount of work. If you double the number of primitives for a ray tracer, the work load is nearly unaffected, and typically goes up by something like 1% or so.

This is because of the spatial data structures that allow the ray tracer to discard the bulk of the data.

Bram: You surely can think I'm wrong, but I would like you to elaborate a bit more.





Do you think that it's not possible to discard primitives in a rasterizer?

In theory or in practice?

About the theory, I tried to show why I don't think it's true, I think the same complexity arguments about spatial subdivision apply to rasterizing them too.

In practice, spatial subdivision is used in raytracers way more than in rasterizers, I agree. And it's true that many raytracers are robust in regards of scene complexity, but also rasterizers have their ways of occlusion culling, which work pretty well... HOMs, if you want to stay inside pure rasterization (as I wrote) but also other techniques (see the recent Umbra 3 stuff at Siggraph2011 for example).

Also, let me be clear about what I think when I say "in practice".






If you take even a commercial raytracer and a rasterizer, put one million subpixel triangles on the same spot, yes, the raytracer will smoke the rasterizer and that's the kind of "practice" that lazy researchers and college students writing tests do.

I imagine more for example a game engine with maybe some software occlusion culling and some rough spatial subdivision for frustum. And I expect it to throw away 80% of the scene faster than a raytracer would take just to update the acceleration structures (moving objects are still considered a reserach topic in the RT realm). Then some draw ordering, some LODs and the hardware early-z rejection do the rest, and you won't be screaming at your arstists to lower the "depth complexity" of a level.

You might object that this won't scale forever. Maybe true, I can't foresee "forever" but we're just scratching the basics of occlusion culling with rasterization, I can see that in the offline world rasterization and LODs are still working great, and even in the state of the art research for rendering massive and occluded models (which is not a common case!) raytracing holds an edge but rasterization is present as well.

To wrap it up I'm not denying that raytracing is more conductive to these sorts of optimizations and algorithms than rasterization, it is. It's easier to reason of occlusion and spatial subdivision in that setting.

I don't think thought that either in theory, on in the real world, that is a remarkable disadvantage.

Sorry,











I read your posting too hastily.

I agree with your analysis.

And yes, apples vs apples means that the rasterizer should use spatial subdiv as well.

However... I still have some doubts though.

You have to be careful with sentences like "throw away 80% of the scene" as you put it.

In big-O complexity... the 80% is a

meaninglessdetail!If culling gives the rasterizer 80% less work, or factor 5 speedup... who cares? The nr of operations will be O(N/5) which is still O(N).

Constant factor speed ups are of no relevance, if you want to render your billion triangle models.

So the question that remains for me: will the spatial subdiv for the rasterizer reduce 'the primitives seen' from N to log(N), if so, I think your whole argument may be valid.

Does spatial subdiv help the rasterizer as much as the ray tracer would? Not sure.. you gave some indications on why it would be different.

Also I concur: moving scenes is a different kettle of fish, I was referring to static scenes.

Bram

Bram: then again, in theory I do believe you can devise an algorithm with logarithmic big-O notation for both. Spatial acceleration ala raytracing on a rasterizer is not going to be as fast, but I don't think it has a different big-O complexity.



In practice, I don't care about big-O, I care about performance with current and "foreseeable future" problem sizes, as everyone should do. And we are not yet even at a stage were we do need LogN with rasterization, both the realtime and offline rasterization worlds seem to be living just fine with mostly linear algorithms. They are just that fast.

If you're in the few fields were depth complexity, massively occluded scenes, maybe out-of-core rendering is required, then things may be different even right now, but that's a very specific field where rasterization still can do something and again, I don't see the average CG scene approaching problematic depth complexities anytime soon. I don't think Pixar has any plans to kill Reyes, when that will happen then maybe I'll start worrying about raytracing in realtime.

fair enough...











Personally, I think the industry shift from rasterizing to ray tracing is really close.

Mainly because of two trends:

- historic trend of the nr of primitives in a scene

- historic trend of the nr of pixels on a screen

Did you know that for the last 20 yrs, on my desk, and probably yours as well, was a display with 10^6 pixels?

On a logarithmic scale, the nr of pixels stay the same!!!

from 800x600, to 1920x1080, both roughly 10^6.

However, if you look at poly count:

In 1991 you would have a 1000 triangle scene max.

In 2011 you typically have 1M triangle scenes.

Three orders of magnitude difference!

Will scene size double for apps in 2013? Yes!

Will nr of pixels on your screen double? No!

So.... because RT scales linearly with pixel count, it will have an easy time in the future: it's not the pixels that go up, it's the nr of primitives, which ray tracing handles with ease. If Moore's law applied to screen resolutions, ray tracing in real time would never be feasible. But it does not.

So my prediction: real time ray tracing going main stream in 2 to 4 years.

In realtime or offline? In realtime I think it's extremely optimistic, but we'll see I guess. Your considerations about the resolution and so on are true, but they can be reversed even.



The number of primitives have been growing a lot and still for realtime rasterization is easily winning on raytracing and it does not seem to want to stop.

Again, for me the offline is a good glimpse into the future. And the offline is hybrid, for the first-hit is still mostly rasterization. Usage of raytracing in movies and such is still quite limited.

I agree with most of your post, ray-tracing leaves the perfect world of absolute parallel heaven when bounding volumes and shading are implemented. However, you are absolutely wrong about one thing:




"If we write things in "theory", or rather, with a theory based on an over-simplistic model, if we are idiots, raytracing wins..."

That's like saying that a child who doesn't know something is stupid or an idiot.

People who reach a wrong conclusion based on the knowledge they currently have does not make them idiots. This is part of the learning process for EVERY SINGLE HUMAN BEING.

It really bothers me when people throw insults in their posts. I figure that if the guy who wrote the blog post about ray tracing on alt dev follows your blog he wouldn't be very happy if he feels that you are calling him an idiot.

So what's stopping the opposite argument as well? If you're using occlusion culling to throw away 80% of the scene in the rasterizer, you can do the same in the raytracer.




The occlusion culling has nothing to do with either rendering algorithm.

You argue that you can use the same acceleration structures that raytracers use in a rasterizer, so why not use the rasterizer acceleration techniques in a raytracer.

All you're describing really are heuristics to remove objects from the scene. These heuristics can be applied regardless of rendering algorithm (local illumination only). I could even apply them to a voxel engine.

Bram said…


"Will nr of pixels on your screen double? No!"

Retina displays are coming, so number of pixels onscreen may well double next year.

Excellent post! I've been making similar arguments while reviewing papers for years.




The religious side of the discussion also has interesting dynamics. Most folks start out squarely in one camp due to their early experiences, which, like religions, they often can't control (e.g. college or game dev : country & parents). As they gain experience, many become agnostic, but a minority become even more entrenched (similar to scientists with any religion?). Like with religion, hard-core devotees are typically immune to reason.

In addition to parallel performance, computing trends make it important to analyze the algorithms in terms of power usage, where coherent memory access becomes even more important than hiding latency. This tends to favor rasterization with current algorithms and architectures, as the rasterizer and texture units in a GPU provide orders of magnitude power improvements that are difficult to match with a ray intersection unit and incoherent primitive access.

The tension between performance, power, and the growing need for random visibility access for global illumination will provide fertile ground for rendering research for years to come.

viktor: I've removed that part, thanks for the suggestion




guillaume: Yes and no. RT needs spatial structures not only to deal with depth complexity but also to deal with complexity in screen space. Of course you could use a software rasterizer to do occlusion culling, then apply LODs, then maybe partition triangles in screen tiles and then sort and raytrace them.

That will probably be not too slow, but will also make your raytracer fundamentally the same with a tiled rasterizer with just the last bit of the loop inverted.

It won't probably have much sense in terms of practical application but it's fine, my whole point of the article was to show that indeed the two techniques are the same with the order you do things switched, and this leds to some different set of trade-offs but not a fundamental, general victory of one over the other.

@DEADCODE,




In regards to movies. Pixar is hybrid but ILM/Sony are mostly path tracers Sony's renderer is a unbiased path tracer.

I think WETA does 1st bounce ray tracing w/ AO.

I think the shift in offline world is to path tracing because it gives better results out of the box

For these very large scenes, you just use tricks like LOD to reduce the number of primitives so that size of primitive is roughly size of pixel. Thus in practice rasterization scales fine even to extremely detailed scenes. If number of pixels is N and you decimate meshes appropriately and depth complexity is D, then rasterization and ray tracing should both take O(ND) time with potentially some log factors in there depending on how your hierarchical data structures work (and both require linear time in number of primitives to precompute the data structures).



Also correct decimation is really beneficial for both approaches for quality reasons. If you throw a billion polygon soup into a renderer without filtering out high frequencies you'll just get horrible aliasing. For both rasterization and ray tracing you can just take more samples to get rid of the aliasing, but decimating meshes helps you by prefiltering out high frequencies.

It isn't clear that either method should have a big asymptotic advantage (beyond log factors) if implemented correctly.

David: agreed, raytracing is becoming more and more relevant in the offline world, GI started to gain momentum because it allowed artists to get better results faster (as you say) instead of having to place lights everywhere.





There could be also a discussion between power (of GI lighting) versus interactive feedback, but anyways...

Still RT it's not a clear winner _there_ where rendering times and resources mean less, and where you can buy lots of processing power.

There are also other factors to consider in the commercial success like the history of the various renderers, their robustness, their programmability and so on, so it's not really about raytracing vs rasterization.

Anyways that was not really my point, what I wanted to say is that complexity wise it's not true that RT will be needed because of the explosion in triangle counts, again, PRMan deals with these pretty well (better than any other software really), so these things do not matter.

One major advantage of unbiased renderers is that the results can be merged in an unbiased way from shared-nothing renders.



Tiling would be the equivalent for rasterizing renderers, but tiling does not improve image quality, only coverage in screen space.

My company, Fohr, has a physically-correct real-time virtual lighting and camera system for film production. Path tracing is here to stay, and has an enormous advantage in "artist time" over rasterization approaches like Renderman.

Great post.







A comment about the off-line visual effects rendering world isn't quite accurate.

The trend towards ray-tracing isn't because it's faster, it's because it's

easier. This is true in two ways:1. Given that a renderer has to have good ray-tracing for (certain) global illumination effects, then why put effort into a rasterizer which is an increasingly small part of render time.

2. It's easier for artists to work with a pure ray-tracer as they don't need to spend as much time dealing with handling all the special purpose algorithms a non-raytracer uses (shadow maps, point-based global illumination, etc).

The studios using a full ray-tracer will tell you it's SLOWER to render, but they get good results faster so do fewer iterations.

This is dramatically different than the real-time world! This may be a place where what the film studios are doing does NOT predict where the game studios will go!

Jono: I agree and I'm not very up-to-date on what most studios are doing, but it's not that black-and-white. Rasterization is still useful because even if first-hit is an increasingly small part of the rendering time, it's still the most important by far. Antialiasing, accurate derivatives, fast programmable shading, easy displacement and so on are still things which are easier on a rasterizer. Also methods that are originating from realtime GI are finding their way back to the offline world (i.e. the recent PRMan fast AO stuff), and this is pushing back the need of using RT everywhere.

Erich: I never thought that raytracing is not there to stay! I'm trying to paint a fair picture and maybe show an interesting way of looking at these two algorithms. I'm not a pro-rasterizer or such, actually I probably know more about raytracing than I know about rasterization (without probably, I SURELY do) and I used to do research in MonteCarlo GI.

eyedl"There could be also a discussion between power (of GI lighting) versus interactive feedback, but anyways..."




Actually in this case raytracing wins on both counts - a big factor in why raytracing is starting to make strong inroads in film/vfx is because it's much better for interactive feedback. Raytracers can render with progressive refinement much more easily than other techniques, which often require length shadow map/point clouds generation before you even see a single rendered pixel. It makes it very difficult to iterate quickly when you have to wait so long, just to find out that your light is in the wrong place, and move it again. With a raytracer it can easily show you a noisy/low quality result that improves over time, which is often enough for quickly tweaking lights/materials interactively. And especially if you're using something like a pathtracer, the low-quality version of what you see is qualitatively the same render as what you will get in the final frame - i.e. you don't have to disable features to get fast feedback, you get the same thing, but with less samples.

I'd also be careful using the argument along the lines of 'prman does it and it's used a lot in film, so it must be good'. prman is an excellent renderer, and it's not particularly because it's a (semi) rasteriser. It incredibly flexible, is very well battle-hardened from years of use and development, and facilities have built up huge investments in infrastructure around it. Suffice to say for better or worse, it's not going anywhere any time soon, but I'm not sure if they were to re-design it today, with the problems of today, they'd do again it the same way. It should also be noted that the latest release of prman contains a lot more functionality to replicate the sort of things (physically based materials/lighting, importance sampling) that's commonplace in raytracers today.

Anyway, just some thoughts from a someone who's currently working on an animated feature, using REYES renderers.

Ray tracing may be O(log(n)) where n is the number of primitives, but building the acceleration structure is O(n) or higher - which means that if you have to rebuild the acceleration structure every frame, which you would need to at least for animated characters in a game, that supposed advantage of raytracing simply disappears.

I appreciate your precise and abstract overview. Raytracing seems a bit like hydrogen fueled cars. If you don't have to think to an end, it's the optimal solution.

Post a Comment