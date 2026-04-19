---
title: Tiled hardware (speculations)
url: https://c0de517e.blogspot.com/2017/08/tiled-hardware-speculations.html
published: '2017-08-07'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Over at Siggraph I had a discussion with some mobile GPU engineers about the pros and cons of tiled deferred rasterization. I prompted some discussion over Twitter (and privately) as well, and this is how I understand the matter of tiled versus immediate/"forward" hardware rasterization so far...



**Thanks for all who participated in said discussions!**




**Disclaimer!**I know (almost) nothing of hardware and electronics, so everything that follows is likely to be wrong. I write this just so that people who really know hardware can laugh at the naivity of mere mortals...




**Tiled-Based Deferred Rendering.**

My understanding of TBDR is that it works by dividing into tiles all the incoming dispatches aimed at a given rendertarget.

For this to happen, you'll have at the very least to invoke the part of the vertex shader that computes the output screen position of the triangles, for all dispatches, figure out which tile(s) a given triangle belongs to, and memorize in a per-tile storage the vertex positions and indices.




*Note: Considering the number of triangles nowadays in games, the per-tile storage has to be in main memory, and not on an on-chip cache. In fact, as you can't predict up-front how much memory you'll need, you will have to allocate generously and then have some way to generate interrupts in case you end up needing even more memory...*
Indices would be rather coherent, so I imagine that they are stored with some sort of compression (probably patented) and also I imagine that you would want to try to already start rejecting invisible triangles as they enter the various tiles (e.g. backface culling).

Then visibility of all triangles per tile can be figured out (by sorting and testing against the z-buffer), the remaining portion of the vertex shader can be executed and pixel shaders can be invoked.

*Note: while this separation of vertex shading in two passes makes sense, I am not sure that the current architectures do not just emit all vertex outputs in a per-tile buffer in a single pass instead.*

From here on you have the same pipeline as a forward renderer, but with perfect culling (no overdraw, other than, possibly, helper threads in a quad - and we really should have quad-merging rasters everywhere, don't care about ddx/ddy rules!).



Vertex and pixel work overlap does not happen on single dispatches, but across different output buffers, so balancing is different than an immediate-mode renderer.




*Fabian Giesen also noted that wave sizes and scheduling might differ, because it can be hard to fill large waves with fragments in a tile, you might have only few pixels that touch a given tile with a given shader/state and more partial waves wasting time (not energy).***Pros.**



Let's start with the benefits. Clearly the idea behind all this is to have perfect culling in hardware, avoiding to waste (texture and target) bandwidth for invisible samples. As accessing memory takes a lot of power (moving things around is costly), by culling so aggressively you save energy.

The other benefit is that all your rendertargets can be stored in a small per-tile on-chip memory, which can be made to be extremely fast and low-latency.

This is

__extremely interesting__, because you can see this memory as effectively a scratch buffer for multi-pass rendering techniques, allowing for example to implement deferred shading without feeling too guilty about the bandwidth costs.
Also, as the hardware always splits things in tiles, you have strong guarantees of what areas of the screen a pixel-shader wave could access, thus allowing to turn certain vector operations (wave-wide) into scalar ones, if things are constant in a given tile (which would be very useful for example for "forward+" methods).

As the tile memory is quite fast, programmable blending becomes feasible as well.

Lastly, once the tile memory that holds triangle data is primed, in theory one could execute multiple shaders recycling the same vertex data, allowing further ways to split computation between passes.



**Cons.**

So why do we still have immediate-mode hardware out there? Well, the (probably wrong) way I see this is that TBDR is really "just" a hardware solution to zero overdraw, so it's amenable to the same trade-offs one always have when thinking of what should be done in hardware and what should be programmable.

You have to dedicate a bunch of hardware, and thus area, for this functionality. Area that could be used for something else, more raw computational units.


*Note though that even if immediate renderers do not need the sophistication of tiling and sorting, they still need space for rendertarget compression which is less needed on a deferred hardware.*
Immediate-mode rasterizers do not have to overdraw necessarily. If we do a full depth-prepass for example then the early-z test should cull away all invisible geometry exactly like TBDR.

We could even predicate the geometry pass after the prepass using the visibility data obtained with it, for example using hardware visibility queries or a compute shader. We could even go down to per-triangle culling granularity!

Also, if one looks at the bandwidth needed for the two solutions, it's not clear where the tipping point is. In both cases one has to go through all the vertex data, but in one case we emit triangle data per tile, in the other we write a compressed z-buffer/early-z-buffer.

Clearly as triangles get denser and denser, there is a point where using the z-buffer will result in less bandwidth use!

Moreover, as this is a software implementation, we could always decide for different trade-offs, and avoid doing a full depth pass but just heuristically selecting a few occluders, or reprojecting previous-frame Z and so on.

Lastly I imagine that there are some trade-offs between area, power and wall-time.

If you care about optimizing for power and are not limited much by the chip area, then building in the chip some smarts to avoid accessing memory looks very interesting.

If you only care about doing things as fast as possible then you might want to dedicate all the area to processing power and even if you waste some bandwidth that might be ok if you are good at latency hiding...

If you care about optimizing for power and are not limited much by the chip area, then building in the chip some smarts to avoid accessing memory looks very interesting.

If you only care about doing things as fast as possible then you might want to dedicate all the area to processing power and even if you waste some bandwidth that might be ok if you are good at latency hiding...

Of course that wasted bandwitdh will cost power (and heat) but you might not see the performance implications if you had other work for your compute units to do while waiting for memory.



**Conclusions.**

I don't quite know enough about this to say anything too intelligent. I guess that as we're seeing tiled hardware in mobiles but not on the high-end, and vice-versa, tiled might excel at saving power but not at pure wall-clock performance versus simpler architectures that use all the area for computational units and latency hiding.


Round-tripping geometry to main RAM seems to be outrageously wasteful, but if you want perfect culling you have to compare with a full-z prepass which reads geometry data twice, and things start looking a bit more even.


Moreover, even with immediate rendering, it's not that you can really pump a lot of vertex attributes and not suffer, these want to stay on chip (and are sometimes even redistributed in tile-like patterns) so practically you are quite limited before you start stalling your pixel-shaders because you're running out of parameter space...


Amplification, via tessellation or instancing though can save lots of data for an immediate renderer, and the second pass as noted before can be quite aggressively culled and in an immediate renderer allows to balance in software how much one wants to pay for culling quality, so doing the math is not easy at all.


The truth is that for almost any rendering algorithm and rendering hardware, there are ways to reach great utilization, and I doubt that if one looked at that the two architectures were very far apart when fed appropriate workloads.

Often it's not a matter of what can be done as there are always ways to make things work, but how easily is to achieve a given result.



Round-tripping geometry to main RAM seems to be outrageously wasteful, but if you want perfect culling you have to compare with a full-z prepass which reads geometry data twice, and things start looking a bit more even.

Moreover, even with immediate rendering, it's not that you can really pump a lot of vertex attributes and not suffer, these want to stay on chip (and are sometimes even redistributed in tile-like patterns) so practically you are quite limited before you start stalling your pixel-shaders because you're running out of parameter space...

Amplification, via tessellation or instancing though can save lots of data for an immediate renderer, and the second pass as noted before can be quite aggressively culled and in an immediate renderer allows to balance in software how much one wants to pay for culling quality, so doing the math is not easy at all.

The truth is that for almost any rendering algorithm and rendering hardware, there are ways to reach great utilization, and I doubt that if one looked at that the two architectures were very far apart when fed appropriate workloads.

Often it's not a matter of what can be done as there are always ways to make things work, but how easily is to achieve a given result.

And in the end it might even be that things are they way they are because of the expertise and legacy designs of the companies involved, rather than objective data. Or that things are hard to change due to myriads of patents, or likely a bit of all these reasons...



But it's interesting to think of how TBDR could change the software side of the equation. Perfect culling and per-tile fast memory would allow some cute tricks, especially in a console where we could have full exposure of the underlying hardware... Could be fun.

What do you think?

**Post Scriptum.**

**Many are mentioning**


[NVidia's tiled solution](https://www.techpowerup.com/231129/on-nvidias-tile-based-rendering), and AMD has

[something similar as well now](http://radeon.com/_downloads/vega-whitepaper-11.6.17.pdf). I didn't talk about these because they seem to be in the end "just" another way to save rendertarget bandwidth.

I don't know if they even help with culling (I think not for NVidia, while AMD mentions they can do pixel-shading after a whole tile batch has been processed) but certainly they don't allow to split rendering passes more efficiently via an on-chip scratch, which to me (on the software side of things...) is the most interesting delta of TBDR.

Of course you could argue that tiles-as-a-cache instead of tiles-as-a-scratch might still save enough BW, and latency-hide the rest, that in practice it allows to do deferred for "free". Hard to say, and in general blending units always had some degree of caching...

Lastly, with these hybrid rasters, if they clip triangles/waves at tile boundaries (if), one could still in theory get some improvements in e.g. F+ methods, but it's questionable because the tile sizes used seem too big to allow for the light/attribute screenspace structures of a F+ renderer to match the hardware tile size.


*External Links.*[Apple's "GPU family 4"](https://developer.apple.com/documentation/metal/about_gpu_family_4)- notice the "imageblocks" section

## 5 comments:

The vertex positions+indices don't generally go into a per-tile storage; it's basically a unified scratch buffer (allocated in chunks or similar). These can get fairly big so they're generally streamed to memory. Even so you can run out and then might need to do a partial flush (render everything queued so far to free up memory). These are expensive and you really want to not do that. And yes, everything you write into the bin buffers is compressed.








The vertex shader split is a thing you can do (we did in Omatic, at least in certain cases). It helps a lot sometimes. The trade-off here is that any vertex shading you do late (per-tile) gets re-run for every tile that a vertex is referenced in; vertex shading you do up-front needs to store its results in mem (which gets big quickly!) but is only done once.

Vertex shading invoked that way hurts somewhat more than "regular" vertex shading since the effect of running post-cull and post-Z-test (!) is that the index sequence is more random, so the memory read patterns are worse.

Programmable blending doesn't really have that much to do with the speed of memory; the key issue is the need to schedule the final blending stage of fragment shaders in-order. This is easier to coordinate in a fixed-size tile than for a full render target; e.g. for a 32x32 pixel tile, a 16x16 quad single-bit scoreboard of "write pending for this quad" is sufficient to identify conflicts, which is quite cheap, and doesn't need to coordinate with other tiles. This part is harder in an IM renderer because you don't necessarily know which other pending warps to synchronize *with*; they could be anywhere! (In practice, there's some sort of binning anyway, which simplifies things, but I digress.)

In terms of HW cost, I don't think the specific-to-TBDR hardware ends up taking any more area than what IM renderers spend on schemes like Z and color compression or early-Z/early stencil that TBDRs don't have much need (or use) for.

Triangle count is absolutely a big issue, because vertex data can get a lot bigger than what you usually store per pixel. If you have dense meshes with tris averaging ~5 pixels, then their diameter is ~2.24 pixels, and (assuming the mesh is like a quad grid) a 32x32 tile will contains a ~14x14 grid of quads = 225 verts. If each vert has 32 bytes of attribute payloads (post-shading! This is 8 scalar floats), that's 7.2k bytes per 1k pixels, so ~7 bytes (=56 bits)/pixel. That's still OK (well, with PC memory bandwidths; with mobile this is already worrisome), but if you have slightly denser meshes or more attributes, this gets ugly quick. (You can do some re-shading instead, which needs less memory for shaded verts, but more for attr fetch, and comes with scheduling issues).

With IM, you want to compress depth, color buffers, etc. to save mem bandwidth, but those are fairly regular data structures with a fixed format, and you don't spend mem BW on shaded vertex data (you do need internal interconnects and buffers to get the shaded verts to where they're needed, and that part is gnarly as hell). With a TBDR you want compressed vertex data (post pre- and post-shading) and that's messier since it's more configurable and less regular than pixel formats are.

A final issue you don't mention is warp/wavefront size. Tilers want them a bit smaller (or else you want bigger tiles). The problem is that if you have say a 32x16 tile, there's only 512 pixels in there = 8 full GCN wavefronts if everything in that tile is one shader. More likely, if a tile is touched by 2-3 shaders, then each of them will run maybe 3 or 4 wavefronts, one of which is half-full. You get more wasted utilization from partially-filled waves and your shader cores are switching shaders a lot more often. (Which means they need to be designed so they're efficient at switching shaders every handful of waves, which they aren't necessarily right now).

In case of shading only vertices and detecting overdraw "perfectly", how does it handle alpha tested geometry? Any traingle could have arbitrary holes in it... Unless there is "only" sorting of triangles (imperfect)?

Anything alpha-tested, with true blending, writing output Z etc. doesn't get deferred and does not get perfect overdraw elimination in TBDRs.


You're *strongly* encouraged to draw all opaque geometry first and anything with alpha test/transparencies second because of this.

This is anecdotal but I'm impressed with what's possible at 60fps on mobile at 2048x1536, as long as you do all the work on each tile without round tripping to memory. For example it can deal with a lot of full screen particle overdraw -- fragment shaders do more work but no extra memory bandwidth is used. I remember previous gen consoles getting destroyed by that kind of thing at much lower resolutions.


One pet peeve is that you can read the framebuffer color in the fragment shader in GLES 2.0 (iOS) but not the depth, even both values are right there on-chip. Maybe this is fixed in more recent APIs, haven't checked.

I'll reword the post a bit. Fabian: when I wrote "per tile storage" referring to the indices I didn't mean on-chip, but off-chip (ram) logically organized in tile bins.

Post a Comment