---
title: A trip through the Graphics Pipeline 2011, part 6
url: https://fgiesen.wordpress.com/2011/07/06/a-trip-through-the-graphics-pipeline-2011-part-6/
published: '2011-07-06'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# A trip through the Graphics Pipeline 2011, part 6

*This post is part of the series “A trip through the Graphics Pipeline 2011”.*

Welcome back. This time we’re actually gonna see triangles being rasterized – finally! But before we can rasterize triangles, we need to do triangle setup, and before I can discuss triangle setup, I need to explain what we’re setting things up *for*; in other words, let’s talk hardware-friendly triangle rasterization algorithms.

### How *not* to render a triangle

First, a little heads-up to people who’ve been at this game long enough to have written their own optimized software texture mappers: First, you’re probably used to thinking of triangle rasterizers as this amalgamated blob that does a bunch of things at once: trace the triangle shape, interpolate u and v coordinates (or, for perspective correct mapping, u/z, v/z and 1/z), do the Z-buffer test (and for perspective correct mapping, you probably used a 1/z buffer instead), and then do the actual texturing (plus shading), all in one big loop that’s meticulously scheduled and probably uses all available registers. You know the kind of thing I’m talking about, right? Yeah, forget about that here. This is hardware. In hardware, you package things up into nice tidy little modules that are easy to design and test in isolation. In hardware, the “triangle rasterizer” is a block that tells you what (sub-)pixels a triangle covers; in some cases, it’ll also give you barycentric coordinates of those pixels inside the triangle. But that’s it. No u’s or v’s – not even 1/z’s. And certainly no texturing and shading, through with the dedicated texture and shader units that should hardly come as a surprise.

Second, if you’ve written your own triangle mappers “back in the day”, you probably used an incremental scanline rasterizer of the kind described in Chris Hecker’s [series on Perspective Texture Mapping](http://chrishecker.com/Miscellaneous_Technical_Articles). That happens to be a great way to do it in sofware on processors without SIMD units, but it doesn’t map well to modern processors with fast SIMD units, and even worse to hardware – not that it’s stopped people from trying. In particular, there’s a certain dated game console standing in the corner trying very hard to look nonchalant right now. The one with that triangle rasterizer that had *really* fast guard-band clipping on the bottom and right edges of the screen, and not so fast guard-band clipping for the top and left edges (that, my friends, is what we call a “tell”). Just saying.

So, what’s bad about that algorithm for hardware? First, it really rasterizes triangles scan-line by scan-line. For reasons that will become obvious once I get to Pixel Shading, we want our rasterizer to output in groups of 2×2 pixels (so-called “quads” – not to be confused with the “quad” primitive that’s been decomposed into a pair of triangles at this stage in the pipeline). This is all kinds of awkward with the scan-line algorithm because not only do we now need to run two “instances” of it in parallel, they also each start at the first pixel covered by the triangle in their respective scan lines, which may be pretty far apart and doesn’t nicely lead to generating the 2×2 quads we’d like to get. It’s also hard to parallelize efficiently, not symmetrical in the x and y directions – which means a triangle that’s 8 pixels wide and 100 pixels stresses very different parts of the rasterizer than a triangle that’s 100 pixels wide and 8 pixels high. Really annoying because now you have to make the “x” and “y” stepping “loops” equally fast in order to avoid bottlenecks – but we do all our work on the “y” steps, the loop in “x” is trivial! As said, it’s a mess.

### A better way

A much simpler (and more hardware-friendly) way to rasterize triangles was presented in a 1988 [paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.157.4621&rep=rep1&type=pdf) by Pineda. The general approach can be summarized in 2 sentences: the signed distance to a line can be computed with a 2D dot product (plus an add) – just as a signed distance to a plane can be compute with a 3D dot product (plus add). And the interior of a triangle can be defined as the set of all points that are on the correct side of all three edges. So… just loop over all candidate pixels and test whether they’re actually inside the triangle. That’s it. That’s the basic algorithm.

Note that when we move e.g. one pixel to the right, we add one to X and leave Y the same. Our edge equations have the form , with a, b, c being per-triangle constants, so for X+1 it will be

. In other words, once you have the values of the edge equations at a given point, the values of the edge equations for adjacent pixels are just a few adds away. Also note that this is absolutely trivial to parallelize: say you want to rasterize 8×8 = 64 pixels at once, as AMD hardware likes to do (or at least the Xbox 360 does, according to the 3rd edition of

[Real-time Rendering](http://realtimerendering.com/book.html)). Well, you just compute for

once for each triangle (and edge) and keep that in registers; then, to rasterize a 8×8 block of pixels, you just compute the 3 edge equation for the top-left corner, fire off 8×8 parallel adds of the constants we’ve just computed, and then test the resulting sign bits to see whether each of the 8×8 pixels is inside or outside that edge. Do that for 3 edges, and presto, one 8×8 block of a triangle rasterized in a truly embarrassingly parallel fashion, and with nothing more complicated than a bunch of integer adders! And by the way, this is why there’s snapping to a fixed-point grid in the previous part – so we can use integer math here. Integer adders are much,

*much* simpler than any floating-point math unit. And of course we can choose the width of the adders just right to support the viewport sizes we want, with sufficient subpixel precision, and probably a 2x-4x factor on top of that so we get a decently-sized guard band.

By the way, there’s another thorny bit here, which is fill rules; you need to have tie-breaking rules to ensure that for any pair of triangles sharing an edge, no pixel near that edge will ever be skipped or rasterized twice. D3D and OpenGL both use the so-called “top-left” fill rule; the details are explained in the respective manuals. I won’t talk about it here except to note that with this kind of integer rasterizer, it boils down to subtracting 1 from the constant term on some edges during triangle setup. That makes it guaranteed watertight, no fuss at all – compare with the kind of contortions Chris has to go through in his article to make this work properly! Sometimes things just come together beautifully.

We have a problem though: How do we find out which 8×8 blocks of pixels to test against? Pineda mentions two strategies: 1) just scanning over the whole bounding box of the triangle, or 2) a smarter scheme that stops to “turn around” once it notices that it didn’t hit any triangle samples anymore. Well, that’s just fine if you’re testing one pixel at a time. But we’re doing 8×8 pixels now! Doing 64 parallel adds only to find out at the very end that exactly none of them hit any pixels whatsoever is a *lot* of wasted work. So… don’t do that!

### What we need around here is more hierarchy

What I’ve just described is what the “fine” rasterizer does (the one that actually outputs sample coverage). Now, to avoid wasted work at the pixel level, what we do is add another rasterizer in front of it that doesn’t rasterize the triangle into pixels, but “tiles” – our 8×8 blocks ([This](http://people.csail.mit.edu/ericchan/bib/pdf/p15-mccormack.pdf) paper by McCormack and McNamara has some details, as does Greene’s [“Hierarchical Polygon Tiling with Coverage Masks”](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.115.1646&rep=rep1&type=pdf) that takes the idea to its logical conclusion). Rasterizing edge equations into covered tiles works very similarly to rasterizing pixels; what we do is compute lower and upper bounds for the edge equations over full tiles; since the edge equations are linear, such extrema occur on the boundary of the tile – in fact, it’s enough to loop at the 4 corner points, and from the signs of the ‘a’ and ‘b’ terms in the edge equation, we can determine which corner. Bottom line, it’s really not much more expensive than what we already discussed, and needs exactly the same machinery – a few parallel integer adders. As a bonus, if we evaluate the edge equations at one corner of the tile anyway, we might as well just pass that through to the fine rasterizer: it needs one reference value per 8×8 block, remember? Very nice.

So what we do now is run a “coarse” rasterizer first that tells us which tiles might be covered by the triangle. This rasterizer can be made smaller (8×8 at this level really seems like overkill!), and it doesn’t need to be as fast (because it’s only run for each 8×8 block). In other words, at this level, the cost of discovering empty blocks is correspondingly lower.

We can think this idea further, as in Greene’s paper or Mike Abrash’s description of [Rasterization on Larrabee](http://drdobbs.com/architecture-and-design/217200602), and do a full hierarchical rasterizer. But with a hardware rasterizer, there’s little to no point: it actually *increases* the amount of work done for small triangles (unless you can skip levels of the hierarchy, but that’s not how you design HW dataflows!), and if you have a triangle that’s large enough to actually produce significant rasterization work, the architecture I describe should already be fast enough to generate pixel locations faster than the shader units can consume them.

In fact, the actual problem here isn’t big triangles in the first place; they are easy to deal with efficiently for pretty much any algorithm (certainly including scan-line rasterizers). The problem is small triangles! Even if you have a bunch of tiny triangles that generate 0 or 1 visible pixels, you still need to go through triangle setup (that I *still* haven’t described, but we’re getting close), at least one step of coarse rasterization, and then at least one fine rasterization step for an 8×8 block. With tiny triangles, it’s easy to get either triangle setup or coarse rasterization bound.

One thing to note is that with this kind of algorithm, slivers (long, very thin triangles) are seriously bad news – you need to traverse tons of tiles and only get very few covered pixels for each of them. So, well, they’re slow. Avoid them when you can.

### So what does triangle setup do?

Well, now that I’ve described what the rasterization algorithm is, we just need to look what per-edge constants we used throughout; that’s exactly what we need to set up during triangle setup.

In our case, the list is this:

- The edge equations – a, b, c for all 3 triangle edges.
- Some of the derived values, like the
for

that I mentioned; note that you wouldn’t actually store a full 8×8 matrix of these in hardware, certainly not if you’re gonna add another value to it anyway. The best way to do this is in HW probably to just compute the

and

, use a

[Carry-save adder](http://en.wikipedia.org/wiki/Carry-save_adder)(aka 3:2 reducer, I wrote about them[before](https://fgiesen.wordpress.com/2010/08/23/carry-save-adders-and-averaging-bit-packed-values/)) to reduce theexpression to a single sum, and then finish that off with a regular adder. Or something similar, anyway.

- Which reference corner of the tiles to use to get the upper/lower bounds of the edge equations for coarse rasterizer.
- The initial value of the edge equations at the first reference point for the coarse rasterizer (adjusted for fill rule).

…so that’s what triangle setup computes. It boils down to several large integer multiplies for the edge equations and their initial values, a few smaller multiplies for the step values, and some cheap combinatorial logic for the rest.

### Other rasterization issues and pixel output

One thing I didn’t mention so far is the scissor rect. That’s just a screen-aligned rectangle that masks pixels; no pixel outside that rect will be generated by the rasterizer. This is fairly easy to implement – the coarse rasterizer can just reject tiles that don’t overlap the scissor rect outright, and the fine rasterizer ANDs all generated coverage masks with the “rasterized” scissor rectangle (where “rasterization” here boils down to a one integer compare per row and column and some bitwise ANDs). Simple stuff, moving on.

Another issue is multisample antialiasing. What changes is now you have to test more samples per pixel – as of DX11, HW needs to support at least 8x MSAA. Note that the sample locations inside each pixel aren’t on a regular grid (which is badly behaved for near-horizontal or near-vertical edges), but dispersed to give good results across a wide range of multiple edge orientations. These irregular sample locations are a total pain to deal with in a scanline rasterizer (another reason not to use them!) but very easy to support in a Pineda-style algorithm: it boils down to computing a few more per-edge offsets in triangle setup and multiple additions/sign tests per pixel instead of just one.

For, say 4x MSAA, you can do two things in an 8×8 rasterizer: you can treat each sample as a distinct “pixel”, which means your effective tile size is now 4×4 actual screen pixels after the MSAA resolve and each block of 2×2 locations in the fine rast grid now corresponds to one pixel after resolve, or you can stick with 8×8 actual pixels and just run through it four times. 8×8 seems a bit large to me, so I’m assuming that AMD does the former. Other MSAA levels work analogously.

Anyway, we now have a fine rasterizer that gives us locations of 8×8 blocks plus a coverage mask in each block. Great, but it’s just half of the story – current hardware also does early Z and hierarchical Z testing (if possible) before running pixel shaders, and the Z processing is interwoven with actual rasterization. But for didactic reasons it seemed better to split this up; so in the next part, I’ll be talking about the various types of Z processing, Z compression, and some more triangle setup – so far we’ve just covered setup for rasterization, but there’s also various interpolated quantities we want for Z and pixel shading, and they need to be set up too! Until then.

### Caveats

I’ve linked to a few rasterization algorithms that I think are representative of various approaches (they also happen to be all on the Web). There’s a lot more. I didn’t even try to give you a comprehensive introduction into the subject here; that would be a (lengthy!) serious of posts on its own – and rather dull after a fashion, I fear.

Another implicit assumption in this article (I’ve stated this multiple times, but this is one of the places to remind you) is that we’re on high-end PC hardware; a lot of parts, particularly in the mobile/embedded range, are so-called *tile renderers*, which partition the screen into tiles and render each of them individually. These are *not* the same as the 8×8 tiles for rasterization I used throughout this article. Tiled renderes need at least another “ultra-coarse” rasterization stage that runs early and finds out which of the (large) tiles are covered by each triangle; this stage is usually called “binning”. Tiled renderers work differently and have different design parameters than the “sort-last” architectures (that’s the official name) I describe here. When I’m done with the D3D11 pipeline (and that’s still a ways off!) I might throw in a post or two on tiled renderers (if there’s interest), but right now I’m just ignoring them, so be advised that e.g. the PowerVR chips you so often find in smartphones handle some of this differently.

The 8×8 blocking (other block sizes have the same problem) means that triangles smaller than a certain size, or with inconvenient aspect ratios, take a lot more rasterization work than you would think, and get crappy utilization during the process. I’d love to be able to tell you that there’s a magic algorithm that’s easy to parallelize *and* good with slivers and the like, but if there is I don’t know it, and since there’s still regular reminders by the HW vendors that slivers are bad, apparently neither do they. So for the time being, this just seems to be a fact of life with HW rasterization. Maybe someone will come up with a great solution for this eventually.

The “edge function lower bound” thing I described for coarse rast works fine, but generates false positives in certain cases (false positives in the sense that it asks for fine rasterization in blocks that don’t actually cover any pixels). There’s tricks to reduce this, but again, detecting some of the rarer cases is trickier / more expensive than just rasterizing the occasional fine block that doesn’t have any pixels lit. Another trade-off.

Finally the blocks used during rasterization are often snapped on a grid (why that would help will become clearer in the next part). If that’s the case, even a triangle that just covers 2 pixels might straddle 2 tiles and make you rasterize two 8×8 blocks. More inefficiency.

The point is this: Yes, all this is fairly simple and elegant, but it’s not perfect, and actual rasterization for actual triangles is nowhere near theoretical peak rasterization rates (which always assume that all of the fine blocks are completely filled). Keep that in mind.

Your E() equations look like expectations of random processes.

As with all mathematical notation, there’s just not enough letters to pick unique non-overlapping ones for everything. I try to make the notation within the series internally consistent and sufficiently mnemonic, no promises beyond that.

You said:

“D3D and OpenGL both use the so-called “top-left” fill rule; the details are explained in the respective manuals.”

While this is true for D3D, I can’t find anything this specific in the OpenGL spec. The closest thing I can find is this (from the current 4.1 spec, pp. 169):

“The rule for determining which fragments are produced by polygon rasterization is called point sampling. The two-dimensional projection obtained by taking the x and y window coordinates of the polygon’s vertices is formed. Fragment centers that lie inside of this polygon are produced by rasterization. Special treatment is given to a fragment whose center lies on a polygon edge. In such a case we require that if two polygons lie on either side of a common edge (with identical endpoints) on which a fragment center lies, then exactly one of the polygons results in the production of the fragment during rasterization.”

This reads as “no gaps and no double-draws allowed, but the specific fill convention is implementation defined” to me. Is there something else more specific elsewhere in the spec that I’m missing?

Great article series; keep it up!

Good point. No, I believe you’re right, OpenGL does not require any specific fill rule, just internally consistent tie-breaking in general.

However, D3D does specifically require the top-left rule, and has done so for quite some time – at the very least D3D9 and upwards explicitly require top-left. I think it’s explicitly been mentioned earlier too (probably DX8, maybe DX7 and even earlier too) but I don’t have the old docs anymore to check :)

“With tiny triangles, it’s easy to get either triangle setup or coarse rasterization bound.”

This piqued my curiosity since if we want to draw a lot of hair strands, which means lots and lots of triangles, by using tessellation and see those hair strands from afar, then we may have this bottleneck, although one solution to address this problem might be to adjust the size of the triangles and reduce the number of triangles according to the viewer distance.

But I’m just wondering if it is possible to see this triangle setup or coarse rasterization bound visually by using NSight, or perhaps other tools ?

Not on the PC (at least not that I’m aware of). But some game consoles can give you that kind of analysis.

Small triangles have tons of other problems too. Other problem factors are per-vertex work (if you only have a few pixels covered by each triangle, you do a

lotof vertex shading, and can easily end up spending more time reading vertex data than shading pixels) and quad over-shading (GPUs always shade “quads” of 2×2 pixels at a time, no matter if all 4 pixels are inside the triangle or only one of them).There are sparse resources on the topic online. msdn guidelines seem to to affirm that D3D has no flexibility in rasterization implementation. it’s one mode, it renders minimal numbers of pixels, and the result is that graphics cards simply can’t accurately calculate adjoined triangles in D3D. as the camera rotates, the triangle angles rotate through every degree of decimal complexity.

And in so doing, missed pixels at the seams flash on and off as the graphics card FP is outdone by the triangles. That is at world space XYZ = (0,0,0) at 10,000 or 50,000 distance from origin, inaccuracies increase.

Every time you take away a point of decimal precision from the graphics, the seams have 10 times more errors, until 50k away from origin, in D3D, seams flash constantly with seam errors. Errors are never more than a single pixel wide, so, slightly lenient rasterization rules, that dont exist in d3d, and maybe not in gl, could allow robust display of seam pixels. I’m interested for more info and developments in raster pipeline configuration for programmers.

This is completely wrong.

In both D3D and OpenGL, triangle vertex positions (in pixels) are quantized to a fixed-resolution integer subpixel grid as part of triangle setup. Everything after that is *exact* – it computes the exact set of pixels covered (as per the fill convention used) by that quantized-coordinate triangle.

The quantization depends only on the screen-space position of the vertices. If you have two adjoining triangle that share *the same* edge (e.g. triangles ABC, DBA), the positions of the vertices A and B are *the same* (bit-identical) for both triangles, as are the quantized screen-space positions. Rasterizing these two triangles will thus never produce a gap. This is required by both OpenGL and D3D (“watertight rasterization”).

The only way you get flashing pixels at seams is by either not using the same positions for the vertices of a shared edge (which is a bug in your code, and would produce gaps even if rasterized with arbitrary-precision arithmetic!) or by having a triangle edge end in the middle of another triangle edge, instead of ending at a vertex (a so-called “T-junction”). T-junctions cause problems with *all* types of finite-precision calculations, and in particular, are very likely to have caused cracking before rasterization even starts (floating point rounding is almost sure to cause this). This happens with *any* algorithm that processes triangles with less than arbitrary-precision arithmetic (which is completely impractical for real-time applications), for what it’s worth. The solution is to not use T-junctions; whenever one edge e1 ends at another edge e2, you need to split e2 into two halves at that point, and connect things up accordingly. Once you do this, you’re back to having properly shared vertices, which guarantees watertight rasterization.

The “errors away from the origin” you mention are indeed intrinsic in floating-point computation. They can cause triangles to “wobble” if you’re far from the origin, but they do not ever cause seam errors unless your meshes have T-junctions.

I see. That is what i was told, so i have tested the d3d game engine thoroughly, to see if in reality i have the same observation. The test returns seam errors. please explain what could be going wrong?

For the test, i rounded all the mesh vertices to 3 decimal places, and printed them, to check they are the same on both meshes. the print readouts displays all vertices are the same i.e.:

v1= (-6875,0000000, 566,0000000, 3100,0000000)

v2= (-6875,0000000, 566,0000000, 3100,0000000)

So, that is what the code thinks that it is sending to the graphics card.

I took every precaution to ensure that the vertices are the same.

However, the graphics card has many many errors at the seams. my friend’s graphics card has the same. The further away from the world origin, the missing pixels appear.

Is it certain from the test that the vertices are the same? can the same number with just 3 decimal places always produce a different binary figure? I think we can say the vertices are the same. how could the vertices be different, when they are the same simple integer numbers on x, y and z?

Either the game engine is unreliable, it’s Unity3d, or the d3d is wrong.

Please Please help me find some explanations for the problem.

D3D is not a game engine.

3D APIs use binary not decimal floating point. Rounding to a set number of decimal places doesn’t mean anything; the way to check whether floats are equal is to test them for equality, not print them and eyeball the numbers to check whether they look similar.

What matters for rasterization is the vertices sent to the rasterizer (after all pre-rasterization shader stages are finished), not what you send to the graphics API. The same source vertex data can result in completely different vertex positions depending what the shaders do. Even seemingly minor variations of the same shader source code can produce different results depending on what the shader compilers do. If you do not want seams, you have to either make sure that you use the exact same vertex/geometry/hull/domain shaders for all affected vertices, or if you’re using different shaders make sure that they’re all computing positions in the

exact sameway (i.e. same computations in the same order from the same data and using the HLSL precise keyword in all shaders to prevent the drivers from reorganizing computations or optimizing them in unsafe ways).Thank you that is very helpful. yes sorry I know that Direct3d is a graphics framework within directx.

There are many times the same question on the unity forums, and with many millions of users, I would have thought that one of the threads would have had a solution, thankfully, due to your assurance and some thorough research, I have understood why unity, and other game engines, can cause this kind of error,and I first started trying to figure out one year ago!

another solution-round the vertices to for example one hundredth of world space in geometry function of the shader. thanks a lot! using CG, I am not sure if CG implements precise keyword! Thanks.

The top-left rule actually works really well for scanline renderers. The critical bit is that top-left is vertical-horizontal, just like the typical rasterization order (four out of eight fill rules of this kind work like this; the other four work for column renderers). That means you can hardcode your loops without considering slopes and the like. Of course you still need to understand what you’re doing, but it’s very straightforward if you do.

Nice series.

“When I’m done with the D3D11 pipeline (and that’s still a ways off!) I might throw in a post or two on tiled renderers (if there’s interest)”

Did you end up doing this? I assume not since it’s not in the index. It would be awesome if you did a post on tiled renderers sometime!

Nicolas

I did talk about tiled renderer differences in a few places, but not as a separate post.