---
title: How to tessellate
url: http://graphicrants.blogspot.com/2026/02/how-to-tessellate.html
author: Brian Karis
published: '2026-02-01'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

### TessFactors

The approach[Moreton](https://dl.acm.org/doi/10.1145/383507.383520)and

[D3D’s](https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm#Tessellator)

[hardware tessellation stage](https://microsoft.github.io/DirectX-Specs/d3d/archive/images/d3d11/tessellator.cpp)take is a simple solution to this problem and the one I use. So long as the only data about a patch that affects the placement of vertices on an edge is data about the edge itself, those vertices will match between different patches. Each edge computes a tessellation factor, ie the number of segments they wish to be subdivided into. I will refer to these 3 edge factors as TessFactors. D3D also has an inner tessellation factor but in practice that is derived from the edge factors and mostly is just an artifact of the tessellation pattern D3D uses.

That doesn’t explain how these TessFactors are calculated. There are various approaches to that as well. Calculating the length of the undisplaced edge in screen space doesn’t work since that might be zero but displacement causes the patch to face towards the camera. Other approaches suggest the opposite, only densely tessellate at silhouettes and reduce tessellation where the displacement direction faces the camera and displacing would only change depth. Depth matters for object intersections and shadows though.

[Diagsplit](https://graphics.stanford.edu/papers/diagsplit/diagSplitPaper.pdf)samples the displacement function at a few points to estimate its screen space length. Not only is that too expensive, it requires every shader that needs to calculate TessFactors to have access to the displacement function, ie be programmable, which isn’t practical. Also ruled out are artist provided density hints expressed by the material graph for the same reason.

The approach I take is simple, common, and similar to what Nanite already uses to project object space error to screen space. TessFactor for an edge is based solely on its world space undisplaced length which is projected to pixels as if the edge was perpendicular to the view vector. This length in pixels is divided by a global DiceRate setting to convert it to TessFactor. Often DiceRate >1 pixel can save cost with little visual difference. The UE default is 2 pixels.

# Uniform density dicing

We have these TessFactors for a patch we want to dice. They represent roughly the length of each edge of the patch. We want to dice that triangular patch into uniformly sized triangles. What is typically called a uniform tessellation is one where a shape is tessellated into many smaller identical shapes similar to the original. The angles are congruent. This is topologically uniform. That is not helpful. What we need is uniform density.

I’ll define an optimal uniform density tessellation as one with the minimum number of triangles possible where all edges are <= to a chosen length. The length of the longest edge dictates the worst case sampling rate of the displacement function and thus the signal resolution. Achieving this target edge length with any more triangles wouldn’t be optimal. It isn’t important to achieve a perfectly optimal tessellation but it is useful to understand the target and its properties to understand how to approach it.

### Remeshing

Thankfully generating meshes like these, isotropic meshes made of roughly equal length edges forming equilateral triangles with vertices close to valence 6, is a common operation called remeshing and there are many published approaches to do so. Perhaps the most popular is [[Botsch and Kobbelt 2004](https://dl.acm.org/doi/10.1145/1057432.1057457)].

The algorithm goes as follows:

For N iterations

-
For all edges
- If edge is too long then split it
- If edge is too short then collapse it
- If edge could be shorter if it was flipped then flip it

-
For all vertices
- Move position to the average of its neighbors


After many iterations the result will approach an isotropic mesh matching the desired properties. There are more considerations when this is meant to express a particular surface but we are only concerned with remeshing a flat triangular patch. For this case the only consideration needed is to constrain boundary vertices to the patch edge they started on.

## Tessellation Table

This remeshing process is far too expensive to do in real-time though. Thankfully since we are working with just the patches themselves and there is a limit on the maximum TessFactor for dicing, every permutation of TessFactors can be[precomputed and placed in a lookup table](https://www.researchgate.net/publication/221337741_Optimized_Pattern-Based_Adaptive_Mesh_Refinement_Using_GPU)which I will call the Tessellation Table. The TessFactors index into the Tessellation Table. I will call an entry in this table a Tessellation Pattern.

### Tessellation Table redundancy

There is a lot of redundancy in this indexing though. The Tessellation Pattern for (3,4,2), (3,2,4), (4,3,2) for example are all the same. They are just rotated or mirrored versions of the same pattern. Instead a unique index into the table is defined as an ordering of the TessFactors from largest to smallest.This reduces the number of patterns stored from $N^3$ to $\binom{N+2}{3}$ or $\frac{N(N+1)(N+2)}{6}$, where $N$ is the max TessFactor the Tessellation Table covers. For N=16 this is the difference between 4096 and 816 or <20% the patterns needing to be stored. Size reduction also reduces cache pollution.

To correctly alias patterns the reordering must also be undone when the pattern is used. First, if the winding flips it needs to be reversed so backface culling is preserved. Second, the barycentrics stored in the table need to be unswizzled so they correctly index the corners of the patch. Alternatively, the patch corners themselves can be swizzled which is often cheaper since it happens at lower frequency.

### Tessellation Pattern building

The remeshing algorithm previously explained was written for meshes with Cartesian coordinates but Tessellation Patterns only store barycentric coordinates. Another way to describe this issue is to say the original algorithm assumes extrinsic geometry but Tessellation Patterns are intrinsic geometry. An extrinsic triangle is defined by the position of its corners. It is embedded in a space. An intrinsic triangle is defined by its edge lengths. It doesn’t have any specific position or orientation. A Tessellation Pattern is intrinsic. A pattern exists for each combination of TessFactors. TessFactors are treated as patch edge lengths so the goal for a pattern is to tessellate the patch into triangles with roughly unit length edges.Intrinsic isn’t a problem for the relaxation step. The average of Cartesian and barycentric coordinates will result in equivalent positions since the math is linear. What extrinsic appears to be needed for is the edge length calculations. Thankfully that is not the case. A good number of geometry calculations can be

[done with only barycentrics and edge lengths](https://web.evanchen.cc/handouts/bary/bary-full.pdf).

For a pair of barycentric points P and Q there is a vector between them $\mathbf{PQ} = Q - P$. Unlike normalized barycentric points where $u+v+w=1$, for normalized barycentric vectors $u+v+w=0$, since $1-1=0$. The squared length of a barycentric vector $\mathbf{PQ}(u,v,w)$ in a triangle with edge lengths $(a,b,c)$ is:

\begin{equation} \lVert \mathbf{PQ} \rVert^2 = -a^2 v w -b^2 w u -c^2 u v \end{equation} Thankfully this also implicitly handles a nonobvious issue. While treating TessFactors as edge lengths is sensible and expresses what we are optimizing for, they aren’t exactly lengths. There are rare cases where TessFactors interpreted as edge lengths express a non-Euclidean triangle, specifically $a>b+c$. If extrinsic geometry was required to calculate edge lengths it wouldn’t be possible for these patterns. Deriving the extrinsic coordinates would result in divide by zeros and negative sqrts. Working as intrinsic instead, using the formula above, no special handling is needed. While the distances lose geometric meaning in these cases it degrades gracefully

### Barycentric quantization

The last thing to take care of is to make sure boundary vertices bitwise match along an edge with all other patterns with the same TessFactor. If they don’t there will be cracks. That can be left for when the barycentrics are quantized to 16bit. It is important though that this quantization is symmetric.The most obvious way to quantize to 16b fixed point would be to represent the range [0.0, 1.0] as [0, 65535]. With that all float values can be made to match a reversed counterpart at the boundaries except one: 0.5, the midpoint. This is a point that will be used by any pattern that has an even TessFactor. 0.5 can’t round in the opposite direction as 0.5. It needs to be stored exactly. The easiest fix is to use an even max value, so map 1.0 to 65534.

If each coordinate is quantized separately they might not still sum to 1. To fix this for interior vertices any coordinate could be chosen to be rederived, so we can say it's always w=1-u-v. But boundary vertices need to be symmetric. To do that I quantize the median barycentric and rederive the max barycentric given they are normalized (the min is always zero on the boundary).

## Uniform density splitting

The Tessellation Table can be used for splitting as well. Typically binary splitting is used. There are advantages to using a wider branching factor though. Wider means a shallower tree, less recursion, and thus less traffic to and from a work queue. Perhaps more importantly though it has the potential to generate more uniformly shaped subpatches for the same reason we were interested in a uniformly dense final tessellation. This can reduce the number of subpatches and make each subpatch more likely to be uniform in dimensions and closer to having max DiceFactors, which we'll see matters later.

Diagsplit longest edge splitting vs Uniform splitting

### SplitFactors

How to best take advantage of this flexibility? Simplifying this question down to 1D and just looking at a single edge. If an edge has a TessFactor of 32, which is larger than the max TessFactor of 16, what SplitFactor should be used in this step? 32 is a multiple of 16 but it isn’t a power of 16 so there is a choice. Clamping to 16 means it will split into 16 subedges which each will then have a DiceFactor of 2. For reasons I will get into later it is important to have DiceFactors be as large as possible, or in other words do as much of the tessellation in the dicing phase as possible. So the other option in this example is SplitFactor of 2 and DiceFactor of 16.The same question can be asked at every step of recursive splitting. Is it better to do the smaller factors early? Does the ordering matter besides for the final dicing step I mentioned already? Predicting too far ahead won’t work well since the desired TessFactor in an early step may not be what is chosen by the end because the projection on screen refines with smaller edges. How about the aspect ratio? Would it be better to address aspect ratio early and generate uniform sized subpatches as soon as possible? Unfortunately that isn't possible while still conforming to the limit of TessFactors being determined purely from that edge’s data.

In my tests the best calculation for turning desired TessFactor into the SplitFactor is the following:

`SplitFactor = min( TessFactor / MaxDiceFactor, MaxSplitFactor )`

This tries to emit subpatches from splitting with maximized DiceFactors but nothing else. Other choices were slower.

### Results

Uniform dicing using the Tessellation Table results in 69% the diced triangles compared to D3D style uniform topology. Uniform splitting using the Tessellation Table results in 68% of the split patches compared to binary splitting. More uniformly sized triangles also benefit the rasterizer.I believe this Tessellation Table approach could have wide applicability due to its more optimal density. The first such use has already been out for a while. The Tessellation Table UE builds has already been used with permission outside of UE in

[https://github.com/nvpro-samples/vk_tessellated_clusters](https://github.com/nvpro-samples/vk_tessellated_clusters).

## No comments:

Post a Comment