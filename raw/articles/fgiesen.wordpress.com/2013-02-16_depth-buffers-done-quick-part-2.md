---
title: Depth buffers done quick, part 2
url: https://fgiesen.wordpress.com/2013/02/16/depth-buffers-done-quick-part-2/
published: '2013-02-16'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Depth buffers done quick, part 2

*This post is part of a series – go here for the index.*

Welcome back! At the end of the [last post](https://fgiesen.wordpress.com/2013/02/11/depth-buffers-done-quick-part/), we had just finished doing a first pass over the depth buffer rendering loops. Unfortunately, the first version of that post listed a final rendering time that was an outlier; more details in the post (which also has been updated to display the timing results in tables).

### Notation matters

However, while writing that post, it became clear to me that I needed to do something about those damn over-long Intel SSE intrinsic names. Having them in regular source code is one thing, but it really sucks for presentation when performing two bitwise operations barely fits inside a single line of source code. So I whipped up two helper classes `VecS32`

(32-bit signed integer) and `VecF32`

(32-bit float) that are actual C++ implementations of the pseudo-code `Vec4i`

I used in [“Optimizing the basic rasterizer”](https://fgiesen.wordpress.com/2013/02/10/optimizing-the-basic-rasterizer/). I then converted a lot of the SIMD code in the project to use those classes instead of dealing with `__m128`

and `__m128i`

directly.

I’ve used this kind of approach in the past to provide a useful common subset of SIMD operations for cross-platform code; in this case, the main point was to get some basic operator overloads and more convenient notation, but as a happy side effect it’s now much easier to make the code use SSE2 instructions only. The original code uses SSE4.1, but with the everything nicely in one place, it’s easy to use `MOVMSKPS / CMP`

instead of `PTEST`

for the mask tests and `PSRAD / ANDPS / ANDNOTPS / ORPS`

instead of `BLENDVPS`

; you just have to do the substitution in one place. I haven’t done that in the code on Github, but I wanted to point out that it’s an option.

Anyway, I won’t go over the details of either the helper classes (it’s fairly basic stuff) or the modifications to the code (just glorified search and replace), but I will show you one before-after example to illustrate why I did it:

col = _mm_add_epi32(colOffset, _mm_set1_epi32(startXx)); __m128i aa0Col = _mm_mullo_epi32(aa0, col); __m128i aa1Col = _mm_mullo_epi32(aa1, col); __m128i aa2Col = _mm_mullo_epi32(aa2, col); row = _mm_add_epi32(rowOffset, _mm_set1_epi32(startYy)); __m128i bb0Row = _mm_add_epi32(_mm_mullo_epi32(bb0, row), cc0); __m128i bb1Row = _mm_add_epi32(_mm_mullo_epi32(bb1, row), cc1); __m128i bb2Row = _mm_add_epi32(_mm_mullo_epi32(bb2, row), cc2); __m128i sum0Row = _mm_add_epi32(aa0Col, bb0Row); __m128i sum1Row = _mm_add_epi32(aa1Col, bb1Row); __m128i sum2Row = _mm_add_epi32(aa2Col, bb2Row);

turns into:

VecS32 col = colOffset + VecS32(startXx); VecS32 aa0Col = aa0 * col; VecS32 aa1Col = aa1 * col; VecS32 aa2Col = aa2 * col; VecS32 row = rowOffset + VecS32(startYy); VecS32 bb0Row = bb0 * row + cc0; VecS32 bb1Row = bb1 * row + cc1; VecS32 bb2Row = bb2 * row + cc2; VecS32 sum0Row = aa0Col + bb0Row; VecS32 sum1Row = aa1Col + bb1Row; VecS32 sum2Row = aa2Col + bb2Row;

I don’t know about you, but I already find this *much* easier to parse visually, and the generated code is the same. And as soon as I had this, I just got rid of most of the explicit temporaries since they’re never referenced again anyway:

VecS32 col = VecS32(startXx) + colOffset; VecS32 row = VecS32(startYy) + rowOffset; VecS32 sum0Row = aa0 * col + bb0 * row + cc0; VecS32 sum1Row = aa1 * col + bb1 * row + cc1; VecS32 sum2Row = aa2 * col + bb2 * row + cc2;

And suddenly, with the ratio of syntactic noise to actual content back to a reasonable range, it’s actually possible to see what’s really going on here in one glance. Even if this *was* slower – and as I just told you, it’s not – it would still be totally worthwhile for development. You can’t always do it this easily; in particular, with integer SIMD instructions (particularly when dealing with pixels), I often find myself frequently switching between the interpretation of values (“typecasting”), and adding explicit types adds more syntactic noise than it eliminates. But in this case, we actually have several relatively long functions that only deal with either 32-bit ints or 32-bit floats, so it works beautifully.

And just to prove that it really didn’t change the performance:

**Change**: VecS32/VecF32

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.367 | 3.420 | 3.432 | 3.445 | 3.512 | 3.433 | 0.021 |
| End of part 1 | 3.020 | 3.081 | 3.095 | 3.106 | 3.149 | 3.093 | 0.020 |
| Vec[SF]32 | 3.022 | 3.056 | 3.067 | 3.081 | 3.153 | 3.069 | 0.018 |

### A bit more work on setup

With that out of the way, let’s spiral further outwards and have a look at our triangle setup code. Most of it sets up edge equations etc. for 4 triangles at a time; we only drop down to individual triangles once we’re about to actually rasterize them. Most of this code works exactly as we saw in [“Optimizing the basic rasterizer”](https://fgiesen.wordpress.com/2013/02/10/optimizing-the-basic-rasterizer/), but there’s one bit that performs a bit more work than necessary:

// Compute triangle area VecS32 triArea = A0 * xFormedFxPtPos[0].X; triArea += B0 * xFormedFxPtPos[0].Y; triArea += C0; VecF32 oneOverTriArea = VecF32(1.0f) / itof(triArea);

Contrary to what the comment says :), this actually computes twice the (signed) triangle area and is used to normalize the barycentric coordinates. That’s also why there’s a divide to compute its reciprocal. However, the computation of the area itself is more complicated than necessary and depends on `C0`

. A better way is to just use the direct determinant expression. Since the area is computed in integers, this gives exactly the same results with one operations less, and without the dependency on `C0`

:

VecS32 triArea = B2 * A1 - B1 * A2; VecF32 oneOverTriArea = VecF32(1.0f) / itof(triArea);

And talking about the barycentric coordinates, there’s also this part of the setup that is performed per triangle, not across 4 triangles:

VecF32 zz[3], oneOverW[3]; for(int vv = 0; vv < 3; vv++) { zz[vv] = VecF32(xformedvPos[vv].Z.lane[lane]); oneOverW[vv] = VecF32(xformedvPos[vv].W.lane[lane]); } VecF32 oneOverTotalArea(oneOverTriArea.lane[lane]); zz[1] = (zz[1] - zz[0]) * oneOverTotalArea; zz[2] = (zz[2] - zz[0]) * oneOverTotalArea;

The latter two lines perform the half-barycentric interpolation setup; the original code multiplied the `zz[i]`

by `oneOverTotalArea`

here (this is the normalization for the barycentric terms). But note that all the quantities involved here are vectors of four broadcast values; these are really scalar computations, and we can perform them while we’re still dealing with 4 triangles at a time! So right after the triangle area computation, we now do this:

// Z setup VecF32 Z[3]; Z[0] = xformedvPos[0].Z; Z[1] = (xformedvPos[1].Z - Z[0]) * oneOverTriArea; Z[2] = (xformedvPos[2].Z - Z[0]) * oneOverTriArea;

Which allows us to get rid of the second half of the earlier block – all we have to do is load `zz`

from `Z[vv]`

rather than `xformedvPos[vv].Z`

. Finally, the original code sets up `oneOverW`

but never uses it, and it turns out that in this case, VC++’s data flow analysis was *not* smart enough to figure out that the computation is unnecessary. No matter – just delete that code as well.

So this batch is just a bunch of small, simple, local improvements: getting rid of a little unnecessary work in several places, or just grouping computations more effectively. It’s small fry, but it’s also very low-effort, so why not.

**Change**: Various minor setup improvements

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.367 | 3.420 | 3.432 | 3.445 | 3.512 | 3.433 | 0.021 |
| End of part 1 | 3.020 | 3.081 | 3.095 | 3.106 | 3.149 | 3.093 | 0.020 |
| Vec[SF]32 | 3.022 | 3.056 | 3.067 | 3.081 | 3.153 | 3.069 | 0.018 |
| Setup cleanups | 2.977 | 3.032 | 3.046 | 3.058 | 3.101 | 3.045 | 0.020 |

As said, it’s minor, but a small win nonetheless.

### Garbage in the bins

When I was originally performing the experiments that led to this series, I discovered something funny when I had the code at roughly this stage: occasionally, I would get triangles that had `endXx < startXx`

(or `endYy < startYy`

). I only noticed this because I changed the loop in a way that should have been equivalent, but turned out not to be: I was computing `endXx - startXx`

as an unsigned integer, and it wrapped around, causing the code to start stomping over memory and eventually crash. At the time, I just made note to investigate this later and just added an `if`

to detect the case early for the time being, but when I later came back to figure out what was going on, the explanation turned out to be quite interesting.

So, where do these triangles with empty bounding boxes come from? The actual per-triangle assignments

int startXx = startX.lane[lane]; int endXx = endX.lane[lane];

just get their values from these vectors:

// Use bounding box traversal strategy to determine which // pixels to rasterize VecS32 startX = vmax( vmin( vmin(xFormedFxPtPos[0].X, xFormedFxPtPos[1].X), xFormedFxPtPos[2].X), VecS32(tileStartX)) & VecS32(~1); VecS32 endX = vmin( vmax( vmax(xFormedFxPtPos[0].X, xFormedFxPtPos[1].X), xFormedFxPtPos[2].X) + VecS32(1), VecS32(tileEndX));

Horrible line-breaking aside (I just need to switch to a wider layout), this is fairly straightforward: `startX`

is determined as the minimum of all vertex X coordinates, then clipped against the left tile boundary and finally rounded down to be a multiple of 2 (to align with the 2×2 tiling grid). Similarly, `endX`

is the maximum of vertex X coordinates, clipped against the right boundary of the tile. Since we use an inclusive fill convention but exclusive loop bounds on the right side (the test is for `< endXx`

not `<= endXx`

), there’s an extra +1 in there.

Other than the clip to the tile bounds, this really just computes an axis-aligned bounding rectangle for the triangle and then potentially makes it a little bigger. So really, the only way to get `endXx < startXx`

from this is for the triangle to have an empty intersection with the active tile’s bounding box. But if that’s the case, why was the triangle added to the bin for this tile to begin with? Time to look at the binner code.

The relevant piece of code is [here](https://github.com/rygorous/intel_occlusion_cull/blob/2d1282e5/SoftwareOcclusionCulling/TransformedMeshSSE.cpp#L127). The bounding box determination for the whole triangle looks as follows:

VecS32 vStartX = vmax( vmin( vmin(xFormedFxPtPos[0].X, xFormedFxPtPos[1].X), xFormedFxPtPos[2].X), VecS32(0)); VecS32 vEndX = vmin( vmax( vmax(xFormedFxPtPos[0].X, xFormedFxPtPos[1].X), xFormedFxPtPos[2].X) + VecS32(1), VecS32(SCREENW));

Okay, that’s basically the same we saw before, only we’re clipping against the screen bounds not the tile bounds. And the same happens with Y. Nothing to see here so far, move along. But then, what does the code do with these bounds? Let’s have a look:

// Convert bounding box in terms of pixels to bounding box // in terms of tiles int startX = max(vStartX.lane[i]/TILE_WIDTH_IN_PIXELS, 0); int endX = min(vEndX.lane[i]/TILE_WIDTH_IN_PIXELS, SCREENW_IN_TILES-1); int startY = max(vStartY.lane[i]/TILE_HEIGHT_IN_PIXELS, 0); int endY = min(vEndY.lane[i]/TILE_HEIGHT_IN_PIXELS, SCREENH_IN_TILES-1); // Add triangle to the tiles or bins that the bounding box covers int row, col; for(row = startY; row <= endY; row++) { int offset1 = YOFFSET1_MT * row; int offset2 = YOFFSET2_MT * row; for(col = startX; col <= endX; col++) { // ... } }

And in this loop, the triangles get added to the corresponding bins. So the bug must be somewhere in here. Can you figure out what’s going on?

Okay, I’ll spill. The problem is triangles that are completely outside the top or left screen edges, but not too far outside, and it’s caused by the division at the top. Being regular C division, it’s truncating – that is, it always rounds towards zero (Note: In C99/C++11, it’s actually defined that way; C89 and C++98 leave it up to the compiler, but on x86 all compilers I’m aware of use truncation, since that’s what the hardware does). Say that our tiles measure 100×100 pixels (they don’t, but that doesn’t matter here). What happens if we get a triangle whose bounding box goes from, say, `minX=-75`

to `maxX=-38`

? First, we compute `vStartX`

to be 0 in that lane (`vStartX`

is clipped against the left edge) and `vEndX`

as -37 (it gets incremented by 1, but not clipped). This looks weird, but is completely fine – that’s an empty rectangle. However, in the computation of `startX`

and `endX`

, we divide both these values by 100, and get zero both times. And since the tile start and end coordinates are inclusive not exclusive (look at the loop conditions!), this is *not* fine – the leftmost column of tiles goes from x=0 to x=99 (inclusive), and our triangle doesn’t overlap that! Which is why we then get an empty bounding box in the actual rasterizer.

There’s two ways to fix this problem. The first is to use “floor division”, i.e. division that always rounds down, no matter the sign. This will again generate an empty rectangle in this case, and everything works fine. However, C/C++ don’t have a floor division operator, so this is somewhat awkward to express in code, and I went for the simpler option: just check whether the bounding rectangle is empty before we even do the divide.

if(vEndX.lane[i] < vStartX.lane[i] || vEndY.lane[i] < vStartY.lane[i]) continue;

And there’s another problem with the code as-is: There’s an off-by-one error. Suppose we have a triangle with `maxX=99`

. Then we’ll compute `vEndX`

as 100 and end up inserting the triangle into the bin for x=100 to x=199, which again it doesn’t overlap. The solution is simple: stop adding 1 to `vEndX`

and clamp it to `SCREENW - 1`

instead of `SCREENW`

! And with these two issues fixed, we now have a binner that really only bins triangles into tiles intersected by their bounding boxes. Which, in a nice turn of events, also means that our depth rasterizer sees slightly fewer triangles! Does it help?

**Change**: Fix a few binning bugs

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.367 | 3.420 | 3.432 | 3.445 | 3.512 | 3.433 | 0.021 |
| End of part 1 | 3.020 | 3.081 | 3.095 | 3.106 | 3.149 | 3.093 | 0.020 |
| Vec[SF]32 | 3.022 | 3.056 | 3.067 | 3.081 | 3.153 | 3.069 | 0.018 |
| Setup cleanups | 2.977 | 3.032 | 3.046 | 3.058 | 3.101 | 3.045 | 0.020 |
| Binning fixes | 2.972 | 3.008 | 3.022 | 3.035 | 3.079 | 3.022 | 0.020 |

Not a big improvement, but then again, this wasn’t even for performance, it was just a regular bug fix! Always nice when they pay off this way.

### One more setup tweak

With that out of the way, there’s one bit of unnecessary work left in our triangle setup: If you look at the [current triangle setup code](https://github.com/rygorous/intel_occlusion_cull/blob/db909a37/SoftwareOcclusionCulling/DepthBufferRasterizerSSEMT.cpp#L294), you’ll notice that we convert all four of X, Y, Z and W to integer (fixed-point), but we only actually look at the integer versions for X and Y. So we can stop converting Z and W. I also renamed the variables to have shorter names, simply to make the code more readable. So [this change] ends up affecting lots of lines, but the details are trivial, so I’m just going to give you the results:

**Change**: Don’t convert Z/W to fixed point

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.367 | 3.420 | 3.432 | 3.445 | 3.512 | 3.433 | 0.021 |
| End of part 1 | 3.020 | 3.081 | 3.095 | 3.106 | 3.149 | 3.093 | 0.020 |
| Vec[SF]32 | 3.022 | 3.056 | 3.067 | 3.081 | 3.153 | 3.069 | 0.018 |
| Setup cleanups | 2.977 | 3.032 | 3.046 | 3.058 | 3.101 | 3.045 | 0.020 |
| Binning fixes | 2.972 | 3.008 | 3.022 | 3.035 | 3.079 | 3.022 | 0.020 |
| No fixed-pt. Z/W | 2.958 | 2.985 | 2.991 | 2.999 | 3.048 | 2.992 | 0.012 |

And with that, we are – finally! – down about 0.1ms from where we ended the previous post.

### Time to profile

Evidently, progress is slowing down. This is entirely expected; we’re running out of easy targets. But while we’ve been starting intensely at code, we haven’t really done any more in-depth profiling than just looking at overall timings in quite a while. Time to bring out VTune again and check if the situation’s changed since our last detailed profiling run, way back at the start of [“Frustum culling: turning the crank”](https://fgiesen.wordpress.com/2013/02/02/frustum-culling-turning-the-crank/).

Here’s the results:

Unlike our previous profiling runs, there’s really no smoking guns here. At a CPI rate of 0.459 (so we’re averaging about 2.18 instructions executed per cycle over the whole function!) we’re doing pretty well: in “Frustum culling: turning the crank”, we were still at 0.588 clocks per instruction. There’s a lot of L1 and L2 cache line replacements (i.e. cache lines getting cycled in and out), but that is to be expected – at 320×90 pixels times one float each, our tiles come out at about 112kb, which is larger than our L1 data cache and takes up a significant amount of the L2 cache for each core. But for all that, we don’t seem to be terribly bottlenecked by it; if we were seriously harmed by cache effects, we wouldn’t be running nearly as fast as we do.

Pretty much the only thing we do see is that we seem to be getting a lot of branch mispredictions. Now, if you were to drill into them, you would notice that most of these related to the row/column loops, so they’re purely a function of the triangle size. However, we do still perform the early-out check for each quad. With the initial version of the code, that’s a slight win (I checked, even though I didn’t bother telling you about it), but that a version of the code that had more code in the inner loop, and of course the test itself has some execution cost too. Is it still worthwhile? Let’s try removing it.

**Change**: Remove “quad not covered” early-out

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.367 | 3.420 | 3.432 | 3.445 | 3.512 | 3.433 | 0.021 |
| End of part 1 | 3.020 | 3.081 | 3.095 | 3.106 | 3.149 | 3.093 | 0.020 |
| Vec[SF]32 | 3.022 | 3.056 | 3.067 | 3.081 | 3.153 | 3.069 | 0.018 |
| Setup cleanups | 2.977 | 3.032 | 3.046 | 3.058 | 3.101 | 3.045 | 0.020 |
| Binning fixes | 2.972 | 3.008 | 3.022 | 3.035 | 3.079 | 3.022 | 0.020 |
| No fixed-pt. Z/W | 2.958 | 2.985 | 2.991 | 2.999 | 3.048 | 2.992 | 0.012 |
| No quad early-out | 2.778 | 2.809 | 2.826 | 2.842 | 2.908 | 2.827 | 0.025 |

And just like that, another 0.17ms evaporate. I could do this all day. Let’s run the profiler again just to see what changed:

Yes, branch mispredicts are down by about half, and cycles spent by about 10%. And we weren’t even that badly bottlenecked on branches to begin with, at least according to VTune! Just goes to show – CPUs really do like their code straight-line.

### Bonus: per-pixel increments

There’s a few more minor modifications in the most recent set of changes that I won’t bother talking about, but there’s one more that I want to mention, and that several comments brought up last time: stepping the interpolated depth from pixel to pixel rather than recomputing it from the barycentric coordinates every time. I wanted to do this one last, because unlike our other changes, this one does change the resulting depth buffer noticeably. It’s not a huge difference, but changing the results is something I’ve intentionally avoided doing so far, so I wanted to do this change towards the end of the depth rasterizer modifications so it’s easier to “opt out” from.

That said, the change itself is really easy to make now: only do our current computation

VecF32 depth = zz[0] + itof(beta) * zz[1] + itof(gama) * zz[2];

once per line, and update `depth`

incrementally per pixel (note that doing this properly requires changing the code a little bit, because the original code overwrites `depth`

with the value we store to the depth buffer, but that’s easily changed):

depth += zx;

just like the edge equations themselves, where `zx`

can be computed at setup time as

VecF32 zx = itof(aa1Inc) * zz[1] + itof(aa2Inc) * zz[2];

It should be easy to see why this produces the same results in exact arithmetic; but of course, in reality, there’s floating-point round-off error introduced in the computation of `zx`

and by the repeated additions, so it’s not quite exact. That said, for our purposes (computing a depth buffer for occlusion culling), it’s probably fine. This gets rid of a lot of instructions in the loop, so it should come as no surprise that it’s faster, but let’s see by how much:

**Change**: Per-pixel depth increments

| Version | min | 25th | med | 75th | max | mean | sdev |
|---|---|---|---|---|---|---|---|
| Initial | 3.367 | 3.420 | 3.432 | 3.445 | 3.512 | 3.433 | 0.021 |
| End of part 1 | 3.020 | 3.081 | 3.095 | 3.106 | 3.149 | 3.093 | 0.020 |
| Vec[SF]32 | 3.022 | 3.056 | 3.067 | 3.081 | 3.153 | 3.069 | 0.018 |
| Setup cleanups | 2.977 | 3.032 | 3.046 | 3.058 | 3.101 | 3.045 | 0.020 |
| Binning fixes | 2.972 | 3.008 | 3.022 | 3.035 | 3.079 | 3.022 | 0.020 |
| No fixed-pt. Z/W | 2.958 | 2.985 | 2.991 | 2.999 | 3.048 | 2.992 | 0.012 |
| No quad early-out | 2.778 | 2.809 | 2.826 | 2.842 | 2.908 | 2.827 | 0.025 |
| Incremental depth | 2.676 | 2.699 | 2.709 | 2.721 | 2.760 | 2.711 | 0.016 |

Down by about another 0.1ms per frame – which might be less than you expected considering how many instructions we just got rid of. What can I say – we’re starting to bump into other issues again.

Now, there’s more things we could try (isn’t there always?), but I think with five in-depth posts on rasterization and a 21% reduction in median run-time on what already started out as fairly optimized code, it’s time to close this chapter and start looking at other things. Which I will do in the next post. Until then, code for the new batch of changes is, as always, on [Github](https://github.com/rygorous/intel_occlusion_cull/tree/blog).

If you keep going like this, eventually the rasterizer will end up taking -0.5ms :-D

I like this series

You can of course do floor division with shift (if tiles are power of two).

Yep, but the tile size in this case is 320×90, so no dice. (I think I mention that a bit later in the post)

Just a minor nitpick: While introducing to the series index is a great thing, please don’t use those annoying “here” links. (see also the W3C recommendation: http://www.w3.org/QA/Tips/noClickHere)

So I propose to change to following text:

This post is part of a series – go here for the index.

to:

This post is part of the Optimizing Software Occlusion Culling series.

(where “Optimizing Software Occlusion Culling” links to the series index)

I don’t habitually link like this, but I do reserve the right to do so when I feel like it, and I don’t much care what the W3’s recommendation is either way. :)

My argument was not that you should do whatever W3C say. ;-)

My argument was that “here” links are annoying to read and it’s hard to tell where they link to at a first glance (which is important for navigation on every website).

Here links don’t play nice with browsers like Android’s, where there is no status bar nor does hovering the cursor (if using mouse) over the link show a tooltip. That is, you don’t know where the link is taking you until you open it by clicking or pop up the context menu with a long press.

Anyhow, thank you for excellent series of posts! Keep up the great work!

Hi Fabian,

Thanks for a very interesting article series. I liked the idea of using operator overloads for SSE intrinsics, but one thing piqued my interest about your unions: They don’t seem to explictly care about alignment.

1) Not applicable? (Possibly stack only objects?)

2) Somehow implicitly handled?

3) Other?

Best,

Ralph

Implicitly handled. __m128 / __m128i require 16-byte alignment, and unions always satisfy the alignment requirements of whatever their most “demanding” member is. (C/C++ guarantee this)

This being VC++ on Windows, you still need to be careful with stuff that’s allocated on the heap/free store because the default allocator only guarantees 8-byte alignment. Most other systems these days do guarantee that malloc returns a pointer sufficiently aligned for *all* basic types, including vector types, so on these platforms it will just work.

Ok – that what I was getting at in the parens in point 1. Thanks for clearing it up!