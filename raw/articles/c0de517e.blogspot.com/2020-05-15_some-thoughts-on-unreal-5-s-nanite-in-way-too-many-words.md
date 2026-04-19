---
title: Some thoughts on Unreal 5's Nanite - in way too many words
url: https://c0de517e.blogspot.com/2020/05/some-thoughts-on-unreal-5s-nanite-in.html
published: '2020-05-15'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Preface**

For the past decade or two, improvements in videogame real-time rendering fidelity have always been going in locksteps with console releases, as these provide a large install base of relatively powerful (and power-efficient) GPUs that provide the anchoring for rendering technology and asset authoring.

Thus, now that the next next-generation is knocking at the door, we should start seeing more and more interesting, applied R&D coming out, after the relative slump of the last year or two. Exciting times!

Of course, though I'm not writing this because we're eager in general about tinkering with new next-gen toys, but because in the last two days we've been going through lots of excitement as we've seen a few great demos, starting a week ago with Sebastien Hillaire's new atmospheric sky simulation, then the Unreal 5 announcement showcasing Nanite's geometry and Lumen's GI, and finally NVidia releasing a new demo of their vision for RTX raytracing and cloud (as in datacenters) rendering.

Of all these, it's undeniable that Nanite is the one that got the most attention, at least from rendering professionals. Why is that? I don't think this is just because of visual appeal, albeit Brian is undeniably in the exclusive pantheon of most handsome rendering engineers (in my heart, only challenged by Drobot), we always expect beauty from Unreal demos.

I think the real difference here between this and many other incredibly smart developments, is that rendering development has been incredibly unbalanced. While we know that we don't know anything about almost anything, when we look at the big picture, it's also undeniable that we spent a lot more effort in certain areas than others.

Shading, since we started this idea of PBR, has seen a ton of attention, ostensibly way past the point where innovation in that realm actually translates to benefits for artists and visual quality for end-users (remember, PBR started as an idea to reduce the amount of weird, ad-hoc controls and shaders we were asking artists to tune!). I would even venture that we know exact solutions for certain specific problems in the shading equation, while never having proved that these were the

[most significant source of error](https://c0de517e.blogspot.com/2019/05/seeing-whole-physically-based-picture.html)when looking at the end-to-end pipeline...

Light transport is arguably a much bigger problem, both algorithmically and in its influence in the end quality, and it's far from being solved... But we were not slacking. Most rendering innovation is light transport in real-time rendering: shadows, various ideas on occlusion and indirect illumination, area lighting and environment lighting, and so on and so forth. Important, yes. Definitely not "solved" yet. But an area where we applied the brunt force of hundreds of genius minds for the last decade, arriving now at solutions that are undeniably quite amazing.

[Art production on the other hand](https://c0de517e.blogspot.com/2019/06/the-value-of-pixels-presentation-slides.html)... We started with objects made of triangles and uv-mapped textures, and we largely are at objects made of triangles and uv-mapped textures. There has been some effort here and there to break free, from Lionhead's "mega meshes" to Carmack's "megatextures", but nothing that ultimately took hold in the industry.

Sure, we did, on the art side, started working in material layers (Substance et al), and with acquired data (photogrammetry, BRDF scanning), but that has been going mostly at a tooling level, with relatively "low tech" ideas (relatively!).

Yet, every time that we see something new (hello Dreams!) in the asset authoring domain, we get excited. We know that this matters, we agree. But we were perhaps still riding on the growth of big games being able to pay for sheer art grunt - even if we should know that saving on the human capital does not mean scaling down our production (necessarily), it means that people can focus their creativity on things that matter more.

Arguably it "had" to come from a third party engine. Games sell to users. Middleware sells to developers. Developer productivity is an end-product feature for an engine. Almost none of the successful gaming middleware was so due to being the most efficient implementation of a given concept, but because they understood (or outright created) the needs of their audience. Engineering excellence is not measured in instructions per cycle but in the ability to deliver amazing value to your customers. Sometimes this implies optimizing for IPC, sometimes it doesn't.

It's painfully obvious, I know, but I feel like it's worth reiterating when many professionals in our line of business used to deride the inefficiencies of Unity, notoriously, and even of course of Unreal itself which was never (and I think could never be) the absolute champion of rendering efficiency. Now both, of course, are hubs of excellence in rendering research.

So. Is this going to "be it"? Way too early to say. But any new piece of R&D in this area is amazing to see.

**How does this thing work?**

Who knows!

Who cares!

Ok, seriously. I know that we stand on the shoulders of the giants, and this is how progress is made, you don't need to tell me. And we're all eager to lean on Brian's and Graham's and all the rest of Epic's gang, (handsome) shoulders. But let's allow ourselves to be silly and wrong and imagine how this could be made. Puzzles are fun, and having everybody explore a single direction in R&D is a very dangerous thing.

So, let's start.

I think pixel-peeping the UE5 video is not particularly interesting. For what it's worth, I am not entirely sure that such a demo / vertical slice would not just run on a powerful enough GPU with semi-conventional techniques and just eating the memory footprint and killing the rasterizer. Desktop GPUs are so powerful that you can be very dumb and use a fraction of their power, still creating great results (and that's part of why consoles can "bridge the gap" or rather, most PC GPUs end up being not utilized as efficiently, in relative terms).

So, let's start from the basic principles. I'd imagine that this technology is made with the explicit intent of being able to ingest any content (photogrammetry, movie assets, etc), that's to say, arbitrary triangle meshes, of whatever complexity and topology. I also would imagine that it would be ok to have some error when rendering them, as long as it's kept around the pixel/sub-pixel level.

A few things seem to be a hard problem in crafting such technology:

1) How to compress the data, so that we can hopefully still fit in the constraints of physical media (bluray) and we can push it through our vertex pipelines.

2) How to LOD.

2b) How to antialias, as we are effectively side-stepping normalmaps under our assumptions (baking detail from highpoly to intermediate cages).

3) How to render pixel-sized geometric details efficiently.

3b) How to do culling.

Of these problems, I would say the one it's hardest to talk about is the compression aspects. This is both a very well researched topic and something that interacts really with the specifics of the whole system in ways that, at least for me, make it impossible to use it as a starting point.

In fact, I'd say that the best approach for this is to start from rendering and work our way up.

**Why can't we just use the hardware as is?**

Now, why is it hard to render pixel-sized or subpixel triangles?

Well, it isn't of course, a GPU just does it. But for the longest times GPUs with an almost universal assumption that there is a given pixel-to-triangle ratio (around an average of ten or so pixels per triangle), triangles do work-expansion. And this is really one of these cardinal ideas around which GPUs are balanced, we "expect" a given ratio between vertices and triangles, triangles to non-culled triangles, and finally triangles to pixels.

Many people, including myself, have been suggesting (to various vendors) the idea that such ratios should change (quite like other did, for example, ALU to TEX), but so far, unsuccessfully, and it's not hard to imagine why. We all know that gradients, and thus mipmaps et al, require 2x2 quads of course, so small triangles need to generate lots of partial quads wasting efficiency. Any GPU rendering pixel-size triangles would literally run at 1/4th of the compute efficiency.

Well, what if we don't need the gradients you ask? And I asked! But hardware people can be lazy. Once you know that you need quads then you can build your texture units to compute addressing in groups of 2x2, all the way down the memory lane. And you can build your work setup to create waves that in the very worst case will have wave_size/4 different triangles, and so on and so forth going "up" the pipeline.

Killing quads seems easy enough, making all the units up and downstream work with 4x more work isn't. In fact one could fundamentally argue that it would never be a good idea, because the raster is there (among other things) to -create- pixel work.

If you have to have one-to-one raster to compute thread ratio, then one can argue that you wouldn't have a fixed function raster but rather some more instructions that do raster-like things for the compute pipeline... Perhaps near the texture units? I wonder how hardware raytracing works... :)

Ok, so the hardware rasterizer is out of the window. What next? Here is where we start Dreaming...

**Look, ma, no (hardware) raster!**

Especially after Dreams, I think we all want non-orthodox rendering methods to be the answer. Volumes? SDF? Raymarching? Points? Perhaps we could even create crude shells around the geometry, raster them with the hardware, and leverage hardware raytracing (which ought to be "wider" and leveraging compute more than the fixed-function raster) for visibility inside the shell? I love it!

But as I start thinking of this a bit more, I don't think I would be able to make it work.

Volumes and SDFs are immensely powerful, but for this specific use-case, they would not guarantee that the original geometry is always preserved accurately, which I think is an important constraint. In general, I am always scared of leveraging data structures that require lots of iterations per pixel, but I'm probably wrong.

I really would like people to think more in that direction, but I failed. And the few "debug draw" frames from the Unreal presentation clearly show "arbitrary" triangles.

It is true though that, at least without pixel peeping every single frame, I could not notice any LOD switch / topology change, which with just triangle data sounds somewhat tricky even if triangles are that small.

The thing that "killed" the shell idea for me really though is that I don't think the hardware raster will help, because you'd need to output the depth of the fine geometry from a pixel shader, slowing down, if not killing outright, early depth rejection, which would be the only reason to leverage the hardware path anyways.

And we already know we can do all the culling work in software! We have games already shipped that move object culling, draw culling, triangle cluster, and even individual triangle culling to compute, pre-raster. We know we can already do better than the conventional hardware path when we dealing with complex geometry, and of course, all the CPU-side culling techniques still apply as well.

What's next? Another "obvious" source of inspiration is REYES, and Karis himself referenced to

[geometry images](http://www.cs.harvard.edu/~sjg/papers/gim.pdf), that, if seen through the right distortion lens could remind of micropolygon grids.

Also, there are in the literature REYES implementations

[on the GPU](https://markussteinberger.net/papers/GPUReyes.pdf), and other experiments with software rasterization, including ideas of "

[quad-merging](http://graphics.stanford.edu/papers/fragmerging/shade_sig10.pdf)" and so on.

So, what does REYES do? Well, the idea there is to create regular grids of vertices, with the squares of the grid roughly pixel-sized. This allowed to then compute all shading on the grid in world space, which literally means shading and geometry detail are one-to-one (sort-of, actual implementations are more complex), while not needing all the topology information of arbitrary meshes (the connectivity is implicit, it's a grid).

It also means we compute shading pre-visibility (works even with path tracing! see Weta's

[Manuka](https://www.wetafx.co.nz/research-and-tech/technology/manuka/)), and the grid itself will provide a way to compute gradients and it serves as the unit of SIMD work.

Essentially, REYES maps the concepts that we know and love from HW raster (SIMD, gradients) to a different space (world/object instead of screen).

The question is now, do we need all that? I don't think we'd want to do shading this way, in fact, I doubt we want to do shading -at all- in our software solution, as it would be a million times harder than just resolving visibility.

And at the end we still have to rasterize the grid's triangle, the only thing that this provides in our case would be a compression format, essentially, mini-geometry images, and we don't care about that right now.

From Karis on DigitalFoundry already spelled it out I think clearly. "The vast majority of triangles are software rasterized using hyper-optimized compute shaders specifically designed for the advantages we can exploit [...]".

Would it be hard to imagine that we can extend

[Graham's ideas](https://www.gdcvault.com/play/1023109/Optimizing-the-Graphics-Pipeline-With)of GPU culling pipelines to distribute chunks of triangles to a software raster? Say that we removed the hard cases, we don't need to do shading, we don't even want to write gbuffers, just visibility (and some triangle IDs).

Chunks of triangles are small enough that one can send them to specialized shaders even bucketed for size or the need for clipping etc.

In the "simplest" case of unclipped, pixel-ish sizes triangles, it's not hard to beat the hardware raster with a "simple" shader that computes one triangle per thread.

In fact, this is certainly true for depth-only rendering, and I know that different people experimented with the idea for shadowmaps at the very least, not sure if it ever shipped in an era where these are often cached or the wasted raster work can be overlapped with other compute via async, but it's definitely possible.

So, moving culling to compute and doing software rasterization in compute is definitely possible, and for small triangles, ought to be fast. One could even dream that some GPUs might have instructions to help visibility computation nowadays... But to be fair, I don't think that's the way here, with what we have right now.

Now comes the real tricky things though. The software raster is easy to imagine, but how to do shading is not. I'm rather sure you do not want to write gbuffers or worse, do shading directly from the SW raster. You need to write a "visibility buffer".

As far as I know, here you have two options, you either

[write draw-IDs, UVs, gradients, and tangent-spaces](http://cg.ivd.kit.edu/publications/2015/dais/DAIS.pdf), or you just

[write triangle/draw-IDs and barycentrics](http://jcgt.org/published/0002/02/04/), then go back to the triangle data to compute UVs.

The

[first approach](https://mynameismjp.wordpress.com/2016/03/25/bindless-texturing-for-deferred-rendering-and-decals/)limits you to only one set of UVs (realistically) - that might not be a problem in many cases or if say, we had virtual texturing as well. It requires more bandwidth, but you do not need to access the geometric data "twice".

The second decouples visibility from attribute fetching, and thus the vertex attributes can be arbitrary, but in general is more complex and I'd imagine you really don't want to have "fat" attributes when the geometry is this dense anyways, you really have to be careful with your inputs, so I guess it's overall less attractive.

Note that they both impose some limit on the number of draws you can do before you run out of IDs, but that's not a huge issue as one could find ways to "flush" the visibility buffer by resolving the shading (kind of what a mobile GPU does).

With deferred rendering, we already moved roughly half of the shading out of the raster and into compute tiles. It was never a stretch of the imagination to think that we could move pieces out, and keep just visibility. I guess it's the natural next step to try to entirely get rid of the hardware raster (at least, when dealing with pixel-sized triangles)...

Compute-based culling, plus visibility buffers, plus compute-based raster. I guess what I'm saying is that the future is to implement mobile GPUs in software, huh?

Seriously though,

[this has been in my mind for a while](https://c0de517e.blogspot.com/2017/08/tiled-hardware-speculations.html), and I know too little about GPU hardware to have a real opinion.

I wonder if the fact that we seem to be moving more and more towards concepts that exist in mobile GPU a proof that their design is smart, or a proof that such systems should not fundamentally be part of the hardware, because they can be efficiently implemented in software (and perhaps GPUs could help by providing some specialized instructions and data paths).

Also, would this imply not leveraging two of new cool GPU features we have now? Mesh shaders, and raytracing? Who knows.

All of this, if it's even in the ballpark of something that can be realistically imagined, is still incredibly hard to actually make it work (I mean, even just on paper or in a demo, much less in a production system, complete with streaming and so on).

On mobile hardware, there is a lot of (secret, magical) compression going on behind the scenes on the geometrical data, and this is without pushing pixel-sized triangles...

Of course, all this also implies throwing away quad-based gradients, but I guess that's not a huge stretch if the rest of the shading is mostly about fetching a single texture from an UV, directly. And with raytracing (and honestly even some things in conventional deferred) we threw away quads already.

Or maybe one can take a page from REYES and bake everything into vertex data. One can even imagine that with so much geometrical detail, prefiltering becomes a lost war anyways and one really has to double-down on

[temporal antialiasing](https://research.activision.com/publications/2020-03/dynamic-temporal-antialiasing-and-upsampling-in-call-of-duty).

Compression and LODs are the hard part in this scheme. Is it possible to extract chunks of regular topology, REYES-style, from arbitrary meshes? Sort of triangle-strips on steroids. Perhaps. Or maybe that doesn't matter as much, as long as you can stream really fast a lot of geometry.

If one managed to compress really well, one could argue that LODs are actually not that hard, especially if it's "just" about changing topology and reusing the vertex data, which for such dense meshes, and with triangles always being almost pixel-sized, it should be possible...

I guess that would be an decent use-case for cloud streaming, where a game could have terabytes of read-only data because they would not need to be delivered to the user's devices, and shared among many instances on the same hardware (bandwidth notwithstanding...).

I hope none of (the rather boring) things I wrote makes sense anyways, and they really likelt do not, as it's hard to even know what would really be hard, without starting to implement. And I like to dream of what the next Dreams will look like... Maybe we don't need triangles at all! Render it on!

## 1 comment:

Pretty interesting. I've also been thinking about the magic behind this. If the triangles are really pixel-sized, we no longer have to care about textures. It can be useful to help create patches at variable resolutions like you pointed out, but then it's more of a geometry compression thing.

Also, maybe we could ditch triangles altogether. We could render as point clouds or voxels.

A bonus for voxels is that you can directly reuse it for cone-traced GI. Then there's the whole thing about animations: you either bake triangles on the fly or need tons of pre-baked frames that can't blend together, or do ragdoll.

Anyway, their thing is probably much more boring in reality as it's supposed to be able to scale down all the way to mobile.

Post a Comment