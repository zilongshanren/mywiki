---
title: Nanite + Reyes
url: http://graphicrants.blogspot.com/2026/02/nanite-reyes.html
author: Brian Karis
published: '2026-02-06'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

That means there can be a mix of both simplification from base Nanite and amplification from tessellation simultaneously on the same mesh. Small patches collapsed away by Nanite’s LOD selection and large patches tessellated. The base LOD heuristic is still valid. It takes into account both positional error and normal error. If both are low then many patches can be represented by a few with little loss whether they are displaced or not. It isn’t simplifying the displacement function in this case, just the base geometry that is being displaced.

The error calculated is for the original surface area which could change significantly due to displacement but that is an example like many others where the displacement signal must be known to compute the correct error. Because the displacement isn’t known, its impacts are ignored.

### Pipeline

This is a high level diagram of the stages in the base Nanite rendering pipeline:

These are the new pipeline stages appended to the end to support tessellation:

The

[programmable blocks are actually multiple passes](https://www.unrealengine.com/en-US/blog/take-a-deep-dive-into-nanite-gpu-driven-materials). There was one such block before but now there are two:

**ClusterRasterize**

and **PatchRasterize**

. There are binning setup passes that I’ve omitted from those blocks but more importantly there is a Dispatch and Draw call for each material using a programmable rasterization feature. We can ignore the previously supported programmable features for the moment. What is important to understand is that displacement mapping is a programmable feature. The displacement function is shader logic expressed by a node graph and authored by an artist. Any shader that needs to evaluate the displacement function must be programmable meaning there needs to be a material shader permutation compiled for it and a `DispatchIndirect`

to launch it.Also important to realize what is not a programmable stage. Artist programmable shaders should in general be minimized to reduce the number of unique compiled shaders and dispatches but in this case there are also scheduling reasons to avoid them. Not being programmable obviously means not having access to any of the programmable logic which can be difficult. I’ll get into all of this more of this later.

## ClusterRasterize

Time to start digging into these stages. The

**ClusterRasterize**

compute shader used to do exactly what its name implies, take a visible cluster and rasterize it using our software rasterizer.Rough sketch of old

**ClusterRasterize**

:
Scalar

- Load cluster data

Thread per vertex

- Load position
- Transform position
- Store in groupshared

Thread per triangle

- Load indexes
- Load transformed positions from groupshared
-
Rasterize triangle
- If pixel inside triangle then atomic write to VisBuffer


In the triangle stage it now needs to check if a patch needs tessellation first. To do that it calculates its TessFactors. If all are <=1 it doesn’t need tessellation. Even still the vertices need to be displaced, hence why this is still a programmable stage. If all TessFactors <= MaxDiceFactor it can be added to the dice queue, otherwise it’s added to the split queue.

We’ll return later to

**ClusterRasterize**

as it is far more complex than that but this is enough for now to stand up a functional pipeline.## PatchSplit

Each thread reads 1 subpatch from the split queue and operates on it. It will bound and cull. If visible, determine TessFactors and split it.

If TessFactors <= MaxDiceFactor it is queued for dicing and

**PatchRasterize**

. Otherwise it is split into child subpatches according to the SplitFactors and the Tessellation Table. The Tessellation Table’s barycentrics for each child are now relative to the subpatch so they need to be made absolute, ie relative to the base patch. Those child subpatches are finally added back to the split queue for another round of **PatchSplit**

. I’ll skip over how to load balance the work of a variable number of children for now.### Subpatch format

I’ve been referring to reading and writing subpatches but how are they stored? Ideally the data to express a subpatch is as small as possible since recursive splitting means a lot of reading and writing of these subpatches from the split work queue. Unlike regularized topology we can’t just store an index representing which region of the original patch this subpatch covers. The Tessellation Table generates irregular topology by design. While it might be tempting to store an index into the Tessellation Table, that would only work for 1 level of recursion. Each level is relative to the last and the stack would need to be unwound to derive the actual coordinates. Instead a subpatch stores barycentric coordinates for all 3 corners.```
struct Subpatch
{
uint32 VisibleClusterIndex : 25;
uint32 TriIndex : 7;
uint32 BarycentricsUV[3]; // 16:16
};
```


### Culling

Visibility culling for subpatches works the same as clusters; their bounds are tested against the frustum, HZB for occlusion, and VSM page mask in the case of shadows. Unlike clusters, tight bounds around displaced patches aren’t known until they are displaced, classic chicken or egg problem. Since the displacement function is arbitrary shader logic there is limited ability to be clever, outside of involved interval arithmetic analysis of shader code.Instead we ask the user to specify the max range of the displacement function. This is a key source of user error and I’ve tried my best to reframe the problem as user defined mapping of a [0,1] displacement function to encourage full use of the specified range but this continues to be a commonly tripped over pitfall by artists, overly bloating bounds and destroying culling and performance.

But, even if we wanted to evaluate displacement in this shader we couldn’t.

**PatchSplit**

is a global shader and not specialized per material. I’ll explain why in a moment. This one shader is responsible for splitting patches from all materials so all logic contributing to patch splitting must be fixed function.This user provided displacement range is in the same space as the displacement function, ie it is scalar. To determine screen space bounds for testing I use the technique from [

[Niessner and Loop](https://graphics.stanford.edu/~niessner/niessner2012patch.html)]. We have since removed the normalizing of displacement vectors after interpolation so the spherical capped cone logic is unnecessary but it has yet to be adjusted. A simple union of prism corners should be slightly tighter.

### Recursive splitting

Recursive splitting is effectively recursive tree expansion of an implicit tree. This task looks just like Nanite’s hierarchical cluster culling so the same tool to solve work distribution comes to mind, a persistent threads shader with a global MPMC lockless work queue. That is exactly what I started with and was what shipped in the first version.### Multipass for recursive

As previously mentioned this is not D3D spec compliant and not guaranteed to make forward progress on all GPU architectures. It does work well on many though. On PC, where we can’t be certain, we no longer use it for cluster culling. Dealing with the support burden wasn’t worth it for the perf improvement. For fixed platforms like consoles we still use it.Likewise, instead of persistent threads,

**PatchSplit**

now is multipass on all platforms not just PC. Remember the key advantage of persistent threads was avoiding sync points with drain and spin up where the GPU isn’t filled. With **PatchSplit**

we can async overlap with non-tessellated Nanite rasterization work through smart scheduling and not worry about idling.Also worth noting that there is a known and small limit to the number of passes required. Subpatches write 16b barycentrics. The MaxSplitFactor can only divide 65534 so many times before written child subpatches will be the same as their parents. With the persistent threads approach this actually caused problems since in rare cases recursion would go past this depth and become an infinite loop. Detecting that requires a bunch of checks that a fixed recursion depth of multipass doesn’t need.

One could argue that those cases showing up in practice suggests more than 16b is needed for subpatch barycentrics but I’d argue that 1 base triangle being tessellated to a resolution of MaxDiceFactor * 64k is surely plenty. The encountered crashes only happened in unreasonable cases with cameras crashing through surfaces.

Either way, whether persistent threads or multipass, it becomes clear now why it is important this is a global shader and thus all logic needs to be fixed function, decoupled from the programmable material displacement. If there were per material dispatches of

**PatchSplit**

a persistent threads style would need to spin up enough threads to fill the machine each time, often only to immediately retire since many wouldn’t have much work. Impossible to know how much work a single starting patch might turn into due to recursion. No overlap could be used between dispatches if they used the same buffer for the queue. Multipass has a simpler reason: overhead of lots of dispatches.Being a global shader means any data about the materials that needs to be accessed, such as the displacement range needs to be in global buffers. It also means no user programmable normals, no programmable dicing rate.

## PatchRasterize

Unlike the split queue, the dice queue doesn’t contain subpatch structs since every patch in this queue already was on the split queue or is a base patch. Instead we can index them and reduce memory and traffic. What has also been done already in a prior stage is calculating the TessFactors for dicing. To avoid repeating that they are also written to the dice queue, or more accurately the Tessellation Table index that pattern corresponds to is.

Subpatches after splitting are mostly close to uniform topology and full size. By that I mean most have TessFactors near MaxDiceFactor. This is because splitting already dealt with most of the irregularity, assuming that patches reaching here were the result of splitting. That isn’t true from what I’ve explained so far but will be true by the end.

Given this,

**PatchRasterize**

can follow the same pattern as base Nanite **ClusterRasterize**

. It's fine to statically assign threads to diced vertices and triangles and not worry about empty threads since there will be few of those.Rough sketch of

**PatchRasterize**

:
Scalar

- Load cluster data
- Load patch data
- Load patch corner data
- Transform corners

Thread per diced vertex

- Load vertex barycentrics from Tessellation Table
- Lerp the corners using barycentrics
- Evaluate displacement function
- Transform position
- Store in groupshared

Thread per diced triangle

- Load indexes from Tessellation Table
- Load transformed positions from groupshared
- Rasterize triangle

### Too much scalar

While there is a decent chunk of scalar work in with base**ClusterRasterize**

in the form of per cluster work, there is much more with **PatchRasterize**

since there is also per patch work. In most cases scalar work gets hidden by vector work. If there is too much of it, too front loaded, it can start to matter. Worse yet when that group uniform work is float math. RDNA3 and earlier don’t have any scalar float ops so these ops go to the vector unit with only 1 lane utilized. Basically while the virtual “domain shader” (DS) work is vectorized the “vertex shader” (VS) work isn’t.Having all this scalar work is not well utilizing what is primarily a vector processor. To try and vectorize this while still keeping the results in registers Rune Stubbe made an optimization where both the 3x work from patch corners as well as multiple patches are spread across the threads. This means 1 wave works on multiple patches, purely to try and vectorize per patch work. First each thread works on 1 patch corner (VS). Then the shader switches to 1 patch at a time, looping over all patches this wave covers. A patch loads its data from the first phase using

`WaveReadLaneAt`

.### Don’t normalize

Another optimization Rune made was noticing that if he removed normalizing the vertex normal after interpolation, that all the rest of the transform math is linear. That means that the base patch positions and base patch normals can be transformed to clip space and shared for the whole patch. This is basically like moving work from DS to VS. The visual difference and more importantly the choice to normalize in the first place is conventional but arbitrary.### Software rasterization only

Unlike clusters, patches don’t have a hardware rasterization path. The most obvious reason is that Reyes generates micropolys by design. Even if the dicing rate is larger than 1 pixel it will still be far smaller than the threshold for switching to HW rasterization. This is convenient in that it means we don’t need an additional shader permutation for HW. We also don’t need to issue the draws for them, most of which would be empty. This presents some issues though.### Near plane clipping

The first is easy to address. Before to avoid having to deal with near plane clipping in SW we sent any clusters that intersected with the near plane down the HW path. We still don’t want to deal with it but at least this time the triangles are small. So instead of clipping I cull triangles that cross the near plane. This looks nearly indistinguishable from clipping since the triangles are so small. Initially I culled subpatches but that was too coarse and depending on their bounds which may be considerably bigger than the subpatches themselves leading to unexpected culling of subpatches nowhere near the camera.### No MaxEdgeLength test

While tessellation tries to achieve triangles that are the size of the dicing rate it only does so before displacement. Typically the difference is small but it isn’t guaranteed. Sharp discontinuities in the displacement function are the worst case. These will cause a diced triangle to stretch the distance from min to max displacement. That can be longer than is good for the SW rasterizer to handle. Instead of allowing unbounded rasterization cost there is a clamp to the screen rect a triangle covers in the rasterizer (set to max 64 pixels). This means this worse case will visually appear as the surface tearing apart under too much stretching as the camera gets close. This may force us to add HW rasterization in the future.

Holes due to SW rasterized triangles longer than 64 pixels

## DS derivatives

The last issue isn’t because of SW raster or even is particular to Nanite Tessellation. There are no automatic derivatives in domain shaders. Texture samples in the displacement function require UV derivatives for mipmapping to work. Mipmapping needs to work for band limiting the signal and reducing aliasing but more importantly it is needed for cache coherency. Using mip0 can be a serious performance loss.Traditional Reyes renderers dice into rectangular grids. Finite differences along grid UV directions are simple and can be used for shading but the Tessellation Table’s irregular meshing doesn’t provide that simple neighbor lookup. Perhaps analytic gradients could be used instead like we do for deferred materials? It still needs to be relative to a sampling rate though. For that we can use the chain rule:

\begin{equation} \frac{dUV}{dTessFactors} = \frac{dUV}{dXYZ} \frac{dXYZ}{dTessFactors} \end{equation} Pardon my lack of mathematical rigor here in terms of dimensionality. Anisotropic texture filtering isn’t important, only isotropic trilinear filtering is needed, so for simplicity assume this is projected in the direction that maximizes this derivative and the equation above can be treated as scalar.

The second term that includes TessFactors is inconvenient. It’s only defined at the edges. The interior could somehow lerp it but the corners would still remain undefined. Thankfully $\frac{dXYZ}{dTessFactors}$ is effectively $\frac{1}{DicingRate}$. That was how the TessFactors were computed in the first place. That is a perfectly smooth function in XYZ space, independent from the surface. So it is defined, continuous, and thus will always match between patches.

The problem of continuity is actually with the first term. Taken directly this is a piecewise constant function. It’s basically the tangent basis of each face before orthonormalization. Like TessFactors, edges could be made to match by only using data of the edge. Edges could exclusively use the UV difference along the edge, ignoring any component of the gradient orthogonal to the edge direction. Unlike TessFactors this doesn’t entirely solve it due to the corners. Corners won’t have just 1 neighbor. They will have an arbitrary number of them depending on the valence of the vertex. Following a similar trick would mean using only vertex data which doesn’t make sense for a rate of change since a point is zero size.

Solving this requires some form of continuous function over the mesh through preprocessing. Like how the tangent basis is typically calculated, this could be averaged and

[stored per vertex](https://www.sebastiansylvan.com/post/the-problem-with-tessellation-in-directx-11/)but at a memory cost. Worth noting we support multiple UV channels. From a workflow perspective it would mean extra heavyweight data would need to be optionally built for meshes to allow displacement on them.

## No comments:

Post a Comment