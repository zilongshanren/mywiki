---
title: 'The real-time rendering continuum: a taxonomy'
url: https://c0de517e.blogspot.com/2016/08/the-real-time-rendering-continuum.html
published: '2016-08-06'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

What is forward? What is deferred? Deferred shading? Lighting? Inferred? Texture-space? Forward "+"? When to use what? The taxonomy of real-time rendering pipelines is becoming quite complex, and understanding what can be an "optimal" choice is increasingly hard.

**- Forward**

So, let's start simple. What do we need to do, in a contemporary real-time rendering system, to draw a mesh? Let's say, something along these lines:

This diagram illustrates schematically what could be going on in a "forward" rendering shader. "Forward" here really just means that most of the computation that goes from geometry to final pixel color happens in a single vertex/pixel shader pair.

We might update in separate steps some resources the shader uses, like shadow maps, reflection maps and so on, but the main steps, from attribute interpolation to texturing, to shading with analytic lights, happen in a single shader.

From there on, the various flavors of forward rendering only deal with different ways of culling and specializing computation, but the shading pipeline remains the same!

**- Culling**

Classical multi-pass forward binds lights to meshes one at a time, drawing a mesh multiple times to accumulate pixel radiance on the screen. Lights are bound to a pass as shader constants, and as you typically have only a few light types, you can generate ad-hoc shaders that efficiently deal with each. Specialization is easy, but you pay a price to the multiple passes, especially if you have a lot of overlapping lights and decals.

Single-pass forward is an improvement that foregoes the waste of multi-pass shading (bandwidth, repeated computations between passes and multiple draws) by either using a dynamic branching "uber-shader" capable of handling all the possible lights assigned to an object, or by generating static shader permutations to handle exactly what a given object needs.

The latter can easily lead to an explosion in the number of shaders needed, as now we don't need just one per light type, but per permutation of types and number of lights.

The advantage is that it can be much more efficient, especially if one is willing to split a mesh to exactly divide the triangles which need a specific technique (e.g. triangles with one light from ones that need two or more, triangles that need to blend texture layers, to perform other special effects).

![]() |

aggressive mesh splitting generating tons of draw calls

Forward+ is nothing more than a change in the way some of the data is passed to a dynamic branching style single-pass forward renderer: instead of binding lights per mesh (draw) as shader constants, they are stored in some kind of spatial subdivision structure that the shader can easily access. Typically, screen tiles or frustum voxels ("

[clustered](http://www.highperformancegraphics.org/previous/www_2012/media/Papers/HPG2012_Papers_Olsson.pdf)"), but[other structures](http://www.insomniacgames.com/siggraph-real-time-lighting-via-light-linked-list/)can be employed as well.
At first, it might sound like a terrible idea. It has all the drawbacks of a dynamic branching uber shader (lots of complexity, no ability to specialize shaders over lights, register usage bound by the most expensive path in the shader) but with the added penalty of divergent branches (as the lights are not constant in the shader). So, why would you do it?

Light culling in a conventional forward pipeline can be quite effective for static lights, or lights that follow prescribed path, as we can carve geometry influenced by each and specialize. But what if we have lots of dynamic lights? Or lots of small lights?

At a given point, carving geometry becomes either inefficient (too many small draws) or impossible. In these situations, Forward+ starts to become attractive, especially if one is able to avoid branch divergence

[by processing lights one at a time](http://advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pptx).
In the end, though, it's just culling and specialization. How to assign lights to rendering entities. How to avoid having dynamic branching, generic shaders that create inefficiencies.

Once one thinks in these terms, it's easy to see that other configurations could be possible, for example, one might think of assigning lights to mesh chunks and dynamically grouping them into draws, following the ideas of

[Ubisoft's](http://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf)and[Graham Wihlidal's](http://www.wihlidal.ca/Presentations/GDC_2016_Compute.pdf)mesh processing pipelines. Or one could assign lights to a per-object grid, or a world space BSP, and so on.**- Splitting the pipeline**

Let's look again at the diagram I drew:

Quite literally we can take this "forward shading" pipeline and cut it an arbitrary point, creating two shader passes from it. This is a

["deferred" rendering system](http://c0de517e.blogspot.ca/2011/01/mythbuster-deferred-rendering.html), some of the computation is deferred to a second pass, and albeit the most employed system (deferred shading) splits material data from lighting/BRDF evaluation, we almost have today a deferred technique for any reasonable choice of splitting point.
Of course, after we do the split, we'll need the two resulting passes to communicate. The pass that is attached to the geometry (object) needs to communicate some data to the pass that is attached to the pixel output. This data is stored by the first pass in a geometry buffer (g-buffer!) and read in the second.

Typically, we store g-buffers in screen-space, but other choices are possible.

So, why would we want to do such a split? At first, it seems very odd. Instead of having a single pass that does all computation in registers, locally and fast, we force some of the data to be written all the way out to GPU memory, uncompressed, and then read again from memory in the second pass. Why?

Well, the reasons are exactly the same as -every time- we have to decide if to split or not any GPU computation, be it a post-effect, a linear algebra routine or in our case, mesh rendering, the potential advantages are always the same:

- Specialization. We might be able to avoid a dynamic branching uber-shader by stopping the computation at a point and launching a number of specialized routines for the second part.
- Inter-thread data access. We might need to reuse the data we're writing out. Or access it in patterns that are not possible with the very limited inter-thread communication the GPU allows (and pixel shaders don't/can't give control over
[what gets packed in a wave](https://fgiesen.wordpress.com/2011/07/10/a-trip-through-the-graphics-pipeline-2011-part-8/), nor have the concept of thread groups! *) - Modifying data. We might want to inject other computation that changes some of the data before launching the second pass.
- Re-packing computation. We might want to launch the second pass using a different topology for our waves.

** Note: it would be interesting to think how a "deferred" system could take advantage of*

[hardware tile-based rendering architectures](https://en.wikipedia.org/wiki/Tiled_rendering)if one[could program passes to operate on each tile](https://developer.apple.com/library/ios/samplecode/MetalDeferredLighting/Introduction/Intro.html)... Ironically today on tile-based deferred GPUs, deferred shading is usually not employed, because the deal with tile architectures is to avoid reads/writes to a "slow" main memory, so deferred, going out to memory, would negate that. Also one of the issues that deferred can ameliorate in a traditional GPU is overshading, but on TBDR that doesn't matter because by design you don't overshade there even in forward...


**- Decision tree**

Adding a split point in our pipeline choices makes things incredibly complex, I'd say out of the reach of rendering engineers just manually doing optimal choices.

We're not dealing anymore just with dynamic versus static lights, or culling granularity, but on how to balance a GPU between ALU, memory, shader resources and different organizations of computation.

It's very hard to evaluate all these choices in parallel also because typically prototypes won't be really as optimized as possible for any given one, and optimization can change the performance landscape radically.

Also, these choices are not local, but the can change how you pack and access data in the entire rendering system. What effects you can easily support, how much material variation you can easily support, how to bake precomputed data, what space you have to inject async computation and so on.

Since we started working on "next-gen" consoles, with a heavy emphasis on compute, I've been interested in

[automatic tuning](http://www.springer.com/us/book/9781441969347), something that is quite common in scientific computing, but not at all yet for real-time rendering.
But even autotuning can only realistically be applied when the problem specification

[is quite rigid](http://groups.csail.mit.edu/commit/papers/2014/ansel-pact14-opentuner.pdf)and it's unlikely to be successful when we can change the way we structure all the data and effects in a rendering system, to fit a given choice of pipeline (which doesn't mean we can't do better in terms of our abilities to[explore pipeline choices...](http://graphics.cs.cmu.edu/projects/spire/)).**- Deferred versus Forward?**

So how can we decide what to use when? Well, some rule of thumbs are possible to devise, looking at the data, the computation we wish to operate, and making sure we don't do anything too unreasonable for a given GPU architecture.

The first bound to consider is just the data bandwidth. How much can I read and write, without being bound by reading and writing? Or to be more precise, how much computation do I have to have in order for the memory operations to not be a big bottleneck? For the latency to be well-hidden?

As an example, right now, on ps4,

[it's entirely reasonable](http://advances.realtimerendering.com/s2016/s16_ramy_final.pptx)to do a deferred shading system writing the typical attributes for GGX shading, at 1080p **, with a typical texture layer compositing system and having the g-buffer pass be mostly ALU-bound.
![]() |

*** Note: without MSAA. In my view, MSAA for geometry antialiasing is not fundamental anymore;*

[It's still a great technique for supersampling/subsampling](https://mynameismjp.wordpress.com/2015/09/13/programmable-sample-points/), but we need temporal antialiasing ([Filmic SMAA is great](http://advances.realtimerendering.com/s2016/index.html), and ideally you[could do both](https://michaldrobot.com/2014/08/13/hraa-siggraph-2014-slides-available/)) not only because it can be faster for comparable quality, but because we want to temporally filter all kind of shading effects!*I'm also not addressing in this the problem of transparencies for a deferred renderer because it's easy to deal with them in F+, sharing the same light lists and most of the shader (just by "connecting" the ends that were cut in the deferred ones)*

The second thing to consider is data access. Do you -need to- access lots of data that is parametrized on the surface (especially, vertices)?

[E.g. The Order's "fat" lightmaps?](https://readyatdawn.sharefile.com/share?cmd=d&id=s9979ff4b57c4543b#/view/s9979ff4b57c4543b)Then probably decompressing it and pushing it through screen-space buffers is not the best idea.
On the other hand, do you need to access surface data in screen-space effects? Ambient and specular occlusion, reflections (note for example that The Order doesn't do any of these screen-space effects)... Or modify surface data in screen-space, e.g. via mesh-based decals ***? Then you have to write a g-buffer anyways, the only question is when!

*** Note: Nowadays projected or "volumetric" decals are quite popular, and these can be culled in tiles/clusters just like lights, so they work in -any- rendering pipeline. They have their drawbacks though as they can't just precisely follow a surface. Maybe an idea could be to use small volume textures to map projected decals UVs and to mask their area of influence?

![]() |

foregoing any screen-space shading technique



**- Deferred splits and computation**

Often, either memory bandwidth makes the choice "easy" for a given platform, or the preference for certain rendering features do (complex lightmaps, mesh decals, screen space effects...). But if they don't then we're left with performance: how to best structure computation.

The choice of what to specialize and how many passes to for a tile is entirely non-trivial, but at least is possible and does not result in an incredible number of permutations, like in single-pass forward, both because we resolved all the material layering in the g-buffer pass, thus we don't need to specialize both over lights and material features, and because doing multiple passes over a tile is cheaper that doing them over a mesh.

Note that in F+ we can trivially specialize over material features of a given draw, but not at all over lights, and it's even best to make the various lighting paths very uniform (e.g. use the same filtering for shadows) to avoid dynamic branching issues.

In deferred shading, on the other hand, we can specialize over lights, over texture layer combiners (in the g-buffer pass) and over materials (albeit with worse culling than forward & we have to store bits in the g-buffer).

It is true that typically we're more constrained on the material model as the input data is mostly fixed via the g-buffer encoding, but one can use

[bit flags to specify what is stored into the MRTs](http://advances.realtimerendering.com/s2016/s16_ramy_final.pptx), and with[PBR rendering](http://blog.selfshadow.com/publications/s2013-shading-course/)we've seen a sharp decrease in the number of material models needed anyways.
The other advantage is of wave efficiency. In a deferred system, only the g-buffer pass uses the rasterizer, and thus is subject to rasterizer inefficiencies:

[partial quads](http://blog.selfshadow.com/2012/11/12/counting-quads/)on triangle edges, overdraw, partial waves due to small draws.
This is though very hard to quantify in practice, as there are lots of ways to balance computation on a GPU.

For example, a forward system with very heavy shaders might suffer a lot from overdraw, and require spending time in full depth pre-pass to avoid having any, but the pre-pass might overlap with some async compute, making it virtually free.

**- Cutting the pipeline "early"**

Recently there have been lots of deferred systems that cut the pipeline "high", near the geometry, before texturing, by

[writing only the data that that the vertices carry](https://community.eidosmontreal.com/blog/next-gen-dawn-engine), or even just enough to be able to[fetch the vertex data manually](http://jcgt.org/published/0002/02/04/)([e.g. triangle index and barycentric coordinates](https://onedrive.live.com/view.aspx?resid=EBE7DEDA70D06DA0!115&app=PowerPoint&authkey=!AP-pDh4IMUug6vs),[the latter can even be reconstructed from vertices and world position](http://www.confettispecialfx.com/gdce-2016-the-filtered-and-culled-visibility-buffer-2/)). These approaches create so-called "visibility buffers" instead of g-buffers.
![]() |

[Eidos R&D tested a g-buffer](https://www.youtube.com/watch?v=plFBGkAEAxE)that is used only to improve wave occupancyand avoid overdraw, not to implement deferred rendering features

These techniques are not aimed at implementing rendering techniques that are different from what maps well to forward, as they still do most of the computation in a single pass.

What they try to do instead is to minimize the work done in pixel shading, to restructure computation so most of the work is done without the constraints imposed by the rasterizer.

The aim for most of these techniques is:

- To write thin g-buffers while still supporting arbitrary material data
- To avoid partial quad, partial wave and overdraw penalties
- Some also focus
[on analyzing the geometric data](http://graphics.cs.williams.edu/papers/AggregateI3D15/)to[perform shading at sub-sampled rates](http://advances.realtimerendering.com/s2016/AGAA_UE4_SG2016_5.pptx)

In theory, nobody prevents these techniques to work with more than one split: after the geometry pass a material g-buffer could be created replacing the tile data with the data after texturing.

Compared to forward methods, the main difference is that we reorder computation in a "screen-space" centric way, all the shading is done in CS tiles instead of PS waves of quads.


It avoids partial waves, but at the cost of worse "culling": you have to shade considering all the features needed in a tile, regardless of how many pixels a feature uses, you can't specialize shaders over materials (unless you store some extra bits in the visibility buffer and summarize them per tile).

You also "get rid" of a lot of fixed-function hardware, you can't rely on optimized paths to load vertex and interpolate vertex data, compute derivatives/differentials (which become a real, hard problem! most of these systems just rely on analytic differentials, which don't work for dependent texture reads) and post-transform cache (albeit it would be possible to write from the VS back into the vertex buffer, if really needed)


Vertex and object data access becomes less coherent (as now we access based on screen-space patterns instead of over surfaces), supporting multiple vertex formats also becomes a bit harder (might not matter) and tessellation might or might not be possible (depending on what data you store).

It avoids partial waves, but at the cost of worse "culling": you have to shade considering all the features needed in a tile, regardless of how many pixels a feature uses, you can't specialize shaders over materials (unless you store some extra bits in the visibility buffer and summarize them per tile).

You also "get rid" of a lot of fixed-function hardware, you can't rely on optimized paths to load vertex and interpolate vertex data, compute derivatives/differentials (which become a real, hard problem! most of these systems just rely on analytic differentials, which don't work for dependent texture reads) and post-transform cache (albeit it would be possible to write from the VS back into the vertex buffer, if really needed)

Vertex and object data access becomes less coherent (as now we access based on screen-space patterns instead of over surfaces), supporting multiple vertex formats also becomes a bit harder (might not matter) and tessellation might or might not be possible (depending on what data you store).

Compared to deferred shading, we have similar trade-offs that we have with standard forward or foward+ versus deferred: we don't have screen-space material data for effects that need it, and we do all the shading in a single pass, thus statically specializing a shader needs to take care of more permutations, but we save on g-buffer space.


Note though that how "thin" the g-buffer is per-se is misleading in terms of bandwidth, because the shading pass uses the g-buffer only as an indirection, the real data is per vertex and per draw, these fetches still need to happen, and might be less coherent than other methods.

And we still have a bit of bandwidth "waste" in the method (similar to how g-buffers do waste reading/writing data that the PS already had) as the index buffers and vertex position data is read twice (through indirection!), and depending on the triangle to pixel ratio, that might be even not insignificant.

Note though that how "thin" the g-buffer is per-se is misleading in terms of bandwidth, because the shading pass uses the g-buffer only as an indirection, the real data is per vertex and per draw, these fetches still need to happen, and might be less coherent than other methods.

And we still have a bit of bandwidth "waste" in the method (similar to how g-buffers do waste reading/writing data that the PS already had) as the index buffers and vertex position data is read twice (through indirection!), and depending on the triangle to pixel ratio, that might be even not insignificant.



**- Beyond screen-space...**

And last, to complete our taxonomy, there has been recently some renderers that decided to split computation storing information in uv-space textures, instead of screen-space.

These ideas are similar to the early idea of

["surface caching"](https://www.bluesnews.com/abrash/chap68.shtml)employed by[Quake](http://fabiensanglard.net/quake2/quake2_software_renderer.php)and might follow quite "naturally" if one has already[a unique parametrization everywhere in the world](http://mrl.cs.vsb.cz/people/gaura/agu/05-JP_id_Tech_5_Challenges.pdf).
These systems are very attractive for subsampling computation, both spatially


If the texture layering is cached, then the scheme is similar to a g-buffer deferred system, just storing the g-buffer in texture space instead of screen space, and it can be coupled with F+ or other deferred schemes that "split early" to reduce the complexity of the shading pass (as the texture layering has already been done in specialized shaders).



[and temporally](http://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf), as the texture data is not linked to a specific frame and rasterized samples.If the texture layering is cached, then the scheme is similar to a g-buffer deferred system, just storing the g-buffer in texture space instead of screen space, and it can be coupled with F+ or other deferred schemes that "split early" to reduce the complexity of the shading pass (as the texture layering has already been done in specialized shaders).

If the final shaded results are stored, the decoupled shading rate can also be used as a mean



Decoupling visibility from shading rate.



[of improving shading stability](http://oxidegames.com/2016/03/19/object-space-lighting-following-film-rendering-2-decades-later-in-real-time/): even without supersampling aliasing doesn't produce shimmering as the samples never move, and texture sampling naturally "blurs" a bit the results.
![]() |

[A good idea.](http://graphics.pixar.com/library/Reyes/)
Caching computation is always very attractive, so these techniques are certainly promising, and the tradeoffs are easy to understand (even if they might not be easy to quantify!). How much of the cache is invalidated at any given time? At which granularity does it need to be computed (and how much waste there is due to it)? How much memory does the cache need?



![]() |

all the fine skin details come only from the specular layer.

**- Conclusions???**

As I said, it's hard to make predictions and it's hard to say that one method is absolutely better than another, even in quite specific scenarios.


But if I had to go out on a limb, I'd say that right now, for this generation of consoles the following applies:

But if I had to go out on a limb, I'd say that right now, for this generation of consoles the following applies:

- "Vanilla" deferred shading works fine and supports lots of nice rendering features.
- In theory, it's not the most efficient rendering technique, simply from the standpoint that it spends lots of energy pushing data in and out memory...
- But for now it works, and it will likely scale well to 2k and probably even 4k or near 4k resolutions, using reasonably thin buffers.
- Deferred shading executes well enough in the following important aspects, that probably need to be addressed
__by any shading technique__: - The ability to specialize shaders, even if we have architectures with good dynamic branching capabilities (and moving data from vgpr to sgpr on GCN), is quite important and saves a lot of headaches (of trying to fit every feature needed in a single, fast ubershader).
- Separating and possibly caching or precomputing (most of) texture compositing is important. Very high frequency tiled detail layers will still need to be composited in screen-space.
- Ameliorating issues with overdraw and small triangles/draws.
- On top of these, deferred supports well a number of screen-space rendering features that are popular nowadays.
- Forward+ can be made fast and it works best when lots of surface data (vertex & texture...) is needed.
- Different material models are probably not a huge concern (LODs might be more attractive, actually), and deferred shading can be specialized over materials as well, with some effort (and worse culling).
- Forward undeniably will scale better with resolution, but might have a slower "baseline" (e.g. 1080p)
- Mapping data to surfaces (e.g. lightmaps, occlusion cones...) allows for cheap and high-quality bakes, but it doesn't work on moving objects, particles and so on, so it's usually a compromise: it has better quality for static meshes, but it lacks the uniformity of volumetric bakes.
- Single pass forward, when done properly, can still very, very fast!
- Especially in games that don't have too many small triangles and don't have many small or moving lights.
- That's still a fairly large proportion of games! Lots of games are in daylight, or anyhow in settings where there aren't many overlapping lights! It is not simple to optimize though.
- Volumetric data structures are here and going to stay, we'll probably see them evolve in something more adaptive than the simple voxel grids that we use today.
- Caching is certainly interesting, especially when it comes to flattening texture layers (which is quite common, especially for terrain).
- Caching shading is a "natural" extension, the tradeoffs there are still unproven, but once one has the option of working in texture-space it's hard not to imagine that there isn't anything of the shading computations that could be meaningfully cached there...
- Visibility buffers
- If g-buffers passes are not bandwidth or ROP/export bound (writing the data), the benefit of "earlier" splits is questionable. But these techniques are -very- interesting, and might even be used in hybrid g-buffer/attribute buffer renderers.
- The general idea of using deferred methods to cluster pixels via similarity and subsample shading is very interesting...
- The same applies to trying to pack waves without resorting to predetermined screen-space tiles (e.g. via stream compaction, which the "old" stencil volume deferred methods did automatically via the early-stencil hardware). None of these have been proven in production so far.
- It would be great to see more research on hybrid renderers in general
- Shaders can be written in a "unified" fashion, the splits can be largely automatic
- Deferred shading and F+ share the same lighting representation!
- A rendering engine could draw using different techniques based on heuristics
- On the other hand, there has been recently lots of work on "GPU driven pipelines", where most of the draw dispatch work (and draw culling) is done on the GPU.
- These pipelines favor very uniform draws (no per-draw shader specialization)
- This might be though entirely a limitation of current APIs...

## 5 comments:

Great post! Two minor quibbles:



1) In "Deferred splits and computation", you linked to Ramy's SIGGRAPH presentation, referring to "the ability to dispatch specialized shaders per screen region". And later you wrote, "In F+ we can easily specialize over material features... In deferred shading, we're bound to a fairly fixed material model... but we can easily specialize over lights". However Ramy's presentation mostly talked about how the Uncharted 4 team used the "shader lookup table" to specialize over *materials* (though presumably they specialize over lights as well, using that mechanism or a different one). In any case, deferred can clearly do both.

2) You seemed to be a bit dismissive of MSAA, while later praising Reyes for "decoupling visibility from shading rate" - which is exactly what MSAA does as well, just in a different way.

Perhaps to reduce confusion, you should make it more clear that you are talking about forward/deferred and clustered/tile-based rendering 'in software', as in using specific rendering approaches targeting standard immediate rendering hardware.

As opposed to hardware that performs deferred/tile-based rendering automatically below the API-level.

So I think you should at least mention that such hardware systems exist, and make it clear that what you are discussing here does not specifically apply to this hardware.

Renderwonk:





- Regarding Uncharted's renderer, yes, you're right. Afaik it's the only public presentation that shows how to specialize tiles, but specialization is very common on tiled deferred (e.g. Black Ops 3 does it, Frostbite does it...) and usually goes towards lights, not materials. Uncharted 4 does the opposite, which yes, is doable but not as common. I've reworked a bit that section though because it's true, there's nothing fundamental that doesn't allow material specialization in a tile.

- Regarding decoupling, yes, you're right :) I do love the concept, and I just wanted to remark in the note that I don't think that the lack of MSAA for deferred is a deal breaker anymore. I've reworked that too

ScaliBQ:

- In the very first note there is mention of TBDR, but I dunno how to work that more into the text without confusing things more. I think that reading the presentation, talking about g-buffers and so on, it should be clear which "deferred" I'm talking of, but yes, it's unfortunate that the terms are overloaded that way...

FWIW, we're doing a similar to Uncharted 4 deferred specialization by material features, not lights, in our tiled deferred solution. Multiple material models are possible, and selected per tile in a similar manner to what they described (although for us it's a trivially small number of cases).


So maybe less common, but certainly not unheard of.

Actually Black Ops 3 does a material permutation in the tile specialization as well, albeit just 1-bit :-)

We distinguish between generic GGX materials and "double-sided" translucent materials (vegetation, cloth etc).

Both share a RGB color in the GBuffer, GGX interprets it as specular color, while translucent materials interpret it as translucent color and assume specular intensity of 0.04.

Post a Comment