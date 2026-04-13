---
title: Meshlets and Mesh Shaders
url: https://interplayoflight.wordpress.com/2025/05/05/meshlets-and-mesh-shaders/
author: Kostas Anagnostou
published: '2025-05-05'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Mesh shaders, introduced back in 2018 as an NVidia Turing and later as an AMD RDNA2 feature, is an evolution of the geometry pipeline which removes a number of fixed function units like the Input Assembler and Tessellator as well as the Vertex shader/Domain Shader/Geometry Shader stages and replaces them with a simpler, programmable pipeline consisting of an Amplification (aka Task) and a Mesh shader.

Ever since programmable shader GPUs were introduced a couple of decades ago, as I was just starting my graphics programming career, geometry and pixel processing, although becoming much more flexible using shaders, was supported by a number of fixed function units and caches that fetched and held data passed between the various stages of the pipeline. In the following high level view of the pipeline, the Input Assembler is responsible for setting up the vertices to feed to the vertex shader while the Primitive Assembler/Rasteriser are responsible for gathering the shaded vertices into triangles, performing out of screen, backface and small primitive culling and rasterising them to feed the pixel shader (green boxes are the fixed function units).

While the GPUs have become increasingly “wider” since, capable of many, many more shader calculations, the fixed function units remained and can become a bottleneck in some cases, especially with the increasing geometry complexity of the scenes in games.

Things changed with the introduction of mesh shaders, that shader (optionally combined with the amplification shader) is now responsible for reading and processing the geometry data and feeding it to the Primitive Assembler/Rasteriser stages, bypassing the Input Assembler:

Mesh shaders are like compute shaders in many ways, they spawn and work on threadgroups, using the DispatchMesh() API, and can use groupshared memory for intermediate data storing and sharing. Additionally, unlike the vertex shader pipeline that processes vertices in isolation, a mesh shader (as well as the amplification shader) has primitive awareness, individually and in clusters which offers the opportunity for finer grained primitive/cluster culling. Given the increasing complexity of game worlds, any opportunity to remove or reduce pressure on fixed function bottlenecks as well as for more efficient culling to avoid wasted work is very appealing.

Long overdue, I recently started tinkering with mesh shaders in my toy engine to get a feel for what is involved in adding support and any performance improvement opportunities. In this post I won’t go deep into mesh shader implementation, there are already a lot of good articles out there, I will focus more on the performance characteristics.

Let’s take a step back first and talk a bit about the importance of culling. In most cases, the expensive part of the rendering pipeline is pixel shading and the GPU is making a lot of effort not to shade pixels that are not visible. For that, it culls all out of screen (frustum), back-facing or small triangles that won’t contribute to the rendered image. This work is done through fixed function units, such as the Primitive Assembler (conceptually, individual GPUs vendors have different names for the fixed function units), which can become a bottleneck in some cases, especially when the pixel shader work is light, as in the case of a shadowmap rendering pass, or a z-prepass. All vertex shader work performed for vertices belonging to triangles that will eventually be culled is effectively wasted. For this reason, it is standard practice in games to test each model/mesh against the camera frustum and not render ones fully out of frustum ([frustum culling](https://learnopengl.com/Guest-Articles/2021/Scene/Frustum-Culling)). There is also the option to cull based on projected size on screen and even to cull occluded meshes (meshes behind other meshes) using [a CPU-side solution](https://www.intel.com/content/www/us/en/developer/articles/technical/masked-software-occlusion-culling.html). An additional benefit of culling a mesh, on the CPU, is that there is no need to submit it for rendering, avoiding all the overhead.

Culling can improve the rendering cost measurably, depending on the content and view, for eg this view from St Miguel scene

![](../../assets/35fc2a901a98d738.png)


![](../../assets/35fc2a901a98d738.png)

simple, per mesh, frustum culling alone drops the gbuffer pass cost from 3.11ms to 2.86ms, an 8% decrease. All the performance numbers quoted in this post refer to a RTX 3080 mobile GPU rendering at a 1080p resolution.

Culling at the mesh/model level on the CPU can be tricky though, developers try to adjust mesh sizes for culling efficiency (frustum/occlusion), splitting and batching meshes based on spatial proximity but even if a good balance is achieved for the main view between culling efficiency and rendering overhead, there could be other use-cases for example point light shadowmap rendering where the smaller frustum can lead to inefficient mesh culling.

Meshlets are another level of mesh subdivision, smaller chunks of the original geometry, usually ranging from 32 to 128 vertices, that can offer finer grained culling and can work well in different contexts. A quick showcase of this, the original scene rendered using a different colour per mesh

![](../../assets/a5eca6a38c9ed360.png)


![](../../assets/a5eca6a38c9ed360.png)

The same scene rendered using a different colour per meshlet (64 vertices per meshlet).

![](../../assets/2caf41030541c73f.png)


![](../../assets/2caf41030541c73f.png)

In the second view there are more opportunities for culling geometry, focus for example on the tree where in the original scene is a single mesh while on the meshlet scene is much more subdivided. Moving the camera closer and freezing visibility

![](../../assets/54a474f6eb78a010.png)


![](../../assets/54a474f6eb78a010.png)

with per mesh frustum culling we manage to cull little from the canopies

![](../../assets/4c9588d03a1f9ad6.png)


![](../../assets/4c9588d03a1f9ad6.png)

while with per meshlet culling most of the out of frustum canopy is culled.

![](../../assets/5f0ea66927795ff3.png)


![](../../assets/5f0ea66927795ff3.png)

This is all very convenient as meshlets is what mesh shaders process, which brings us to the topic of this post.

Adding mesh shader support is relatively straightforward, in its most basic form is an almost direct replacement of the vertex shader (the pixel shader remains the same). One of the ways the classic vertex shader pipeline differs to the mesh shader one is in the amount of work the fixed function units, the Input Assembler in particular, do in the background to deduplicate indices and prepare the data for consumption (I suggest reading [this post](https://gpuopen.com/learn/mesh_shaders/mesh_shaders-from_vertex_shader_to_mesh_shader/) for a discussion of this work in the context of the RDNA GPU architecture). None of this happens with the mesh shader pipeline which means that we need to do that work offline to convert the geometry data into meshlets, so that can be processed by the mesh shader.

To achieve this I used the [meshoptimizer](https://github.com/zeux/meshoptimizer) library that can both optimise the original meshes and create the meshlets needed by the mesh shader pipeline. The first thing I noticed after I added support for it to the toy engine is that meshoptimizer can improve the original meshes and can speed up the vertex shader pipeline as well. For example, testing with the St Miguel scene and view discussed above,

![](../../assets/65f7bbef30ec18c8.png)


![](../../assets/65f7bbef30ec18c8.png)

the original, unoptimised version costs 3.28ms, while the meshoptimizer optimised version costs 2.87ms (measuring gbuffer pass).

The improvement is content dependent, performing the same test with the Bistro scene

![](../../assets/144c2bffecfda447.png)


![](../../assets/144c2bffecfda447.png)

doesn’t really improve the cost, dropping it from 1.08ms to 1.05ms for the gbuffer pass, so as always it is worth profiling your specific use case.

Going back to mesh shaders, the meshlet related buffers the meshoptimizer produces, per mesh, are the following:

- a “mesh_vertices” buffer, which contains the deduplicated (unique) indices of the mesh vertices
- a “mesh_triangles” buffer, which contains the (triangle) indices to the mesh_vertices buffer
- a “meshlets” buffer which contains the vertex and triangle counts as well as the offsets to the mesh_vertices and mesh_triangles buffers.

and this is all that is needed to render the mesh using a mesh shader. The actual vertex data streams, eg positions, normals etc can be exactly the same as in the vertex shader pipeline. Worth noticing that there is an indirection here, mesh_vertices contains indices to the original vertex buffer and mesh_triangles contains indices to the indices in mesh_vertices. This may or may not be an issue and can be addressed by creating local vertex buffers for each meshlet at the expense of some vertex data duplication. It is also worth calling out that the original index buffer is no longer needed.

To get an idea of the overhead of a mesh shader pipeline, compared to the vertex shader one, when rendering the same content and the same, CPU side frustum culling, I started by trying a few meshlet/threadgroup size configurations in a “pass through” mode (no GPU side culling). This is the mesh shader I put together, for reference:

```
[NumThreads(MESH_SHADER_GROUPSIZE, 1, 1)]
[OutputTopology("triangle")]
void MSMain(
uint gtid : SV_GroupThreadID,
uint gid : SV_GroupID,
out indices uint3 tris[MESHLET_MAX_TRIS],
out vertices PSInput verts[MESHLET_MAX_VERTS]
)
{
PSInput result = (PSInput) 0;
uint meshletIndex = gid;
uint meshletCount = MaterialID >> 16;
if (meshletIndex >= meshletCount)
return;
Meshlet meshlet = Meshlets[meshletIndex];
//declare how many vertices and primitives we will be writing out
SetMeshOutputCounts(meshlet.VertCount, meshlet.PrimCount);
//prepare and write out vertex data (AKA "vertex phase")
int VertLoopCount = (MESHLET_MAX_VERTS + MESH_SHADER_GROUPSIZE - 1) / MESH_SHADER_GROUPSIZE;
for (int i = 0; i < VertLoopCount; i++)
{
int index = gtid * VertLoopCount + i;
// clamp index to the maximum number of vertices exported
index = min(index, meshlet.VertCount - 1);
uint vertexIndex = MeshletVertices[meshlet.VertOffset + index];
Vertex vertex = Vertices[vertexIndex];
result.position = mul(World, float4(vertex.position.xyz, 1));
result.worldPos = result.position.xyz;
result.position = mul(ViewProjection, result.position);
result.normal.xyz = mul((float3x3) WorldNormal, vertex.normal.xyz);
result.normal.w = result.position.z;
result.uv = vertex.texcoord;
verts[index] = result;
}
// write out triangle indices (AKA "triangle phase")
int PrimLoopCount = (MESHLET_MAX_TRIS + MESH_SHADER_GROUPSIZE - 1) / MESH_SHADER_GROUPSIZE;
for (int i = 0; i < PrimLoopCount; i++)
{
int index = gtid * PrimLoopCount + i;
//clamp index to maximum of primitives exported
index = min(index, meshlet.PrimCount - 1);
tris[index] = uint3(
MeshletTriangles[meshlet.PrimOffset + index * 3],
MeshletTriangles[meshlet.PrimOffset + index * 3 + 1],
MeshletTriangles[meshlet.PrimOffset + index * 3 + 2]
);
}
}
```

The above mesh shader is pretty standard: based on the maximum number of triangles, vertices and threadgroup size it decides whether to perform a loop in the shader to process input vertices and triangles. It is important to call SetMeshOutputCounts() at the start of the shader to declare the number of vertices and triangles to be written out. Writing out more vertices or triangles than those declared is undefined behaviour, the GPU is not required to clamp the numbers, so we need to protect against it in the shader. In many mesh shader examples online the usual way to achieve this is with a branch, eg

```
if (index < meshlet.VertCount)
{
// process vertex
}
```

In my tests I found this to have a large overhead though due to divergence, so I ended up clamping the indices to the number of output vertices and triangles which was much faster although it could end up processing the same vertex/triangle multiple times (performance difference example below).

When setting up a mesh shader pipeline, 2 parameters are important and the trickiest to get right aspect of it, in than they may have dependencies on the content and the targeted GPU: the meshlet size and the mesh shader threadgroup size. According to the [specification](https://microsoft.github.io/DirectX-Specs/d3d/MeshShader.html#mesh-shader-output-size-limits), a mesh shader can output a maximum of 256 vertices, a maximum of 256 triangles and have a maximum threadgroup size of 128.

There are a couple of things to consider when selecting the meshlet size an threadgroup size:

- The larger the meshlet (in terms of vertex count) the larger the vertex reuse (less need to shade a vertex multiple times)
- The smaller the meshlet the easier it is to cull
- Vertex shading the most expensive operation in the mesh shader, it might be preferable to make threadgroup size match meshlet vertex count to avoid wasted threads during the vertex phase.

In the following table I summarise the results of 2 experiments, trying different configurations of max number of vertices and max number of triangles per meshlet and mesh shader threadgroup size with and without a pixel shader bound, for the St Miguel scene, reporting the cost of the gbuffer and depth prepass.

Number of vertices | Number of triangles | Threadgroup size | Cost (ms) | Cost no PS (ms) |
| 32 | 64 | 32 | 2.83 | 2.53 |
| 64 | 124 | 32 | 2.83 | 2.46 |
| 64 | 124 | 64 | 2.78 | 2.46 |
| 128 | 256 | 32 | 3.59 | 2.58 |
| 128 | 256 | 64 | 3.46 | 2.59 |
| 128 | 256 | 128 | 3.43 | 2.53 |

A reminder that the vertex shader pipeline cost for the same view is 2.87 ms and with no pixel shader bound it is 2.42 ms.

In the above experiment I tried going as low as 32 vertices and 64 triangles per meshlet and as high as 128 vertices and 256 triangles. [NVidia suggests](https://developer.nvidia.com/blog/introduction-turing-mesh-shaders/) using a max meshlet vertex count of 64 and a max triangle count of 126 (the number above is capped to 124 because meshoptimizer requires triangle counts multiples of 4). [AMD recommends](https://gpuopen.com/learn/mesh_shaders/mesh_shaders-optimization_and_best_practices/) 128 vertices and 256 triangles. Also, I have tuned the threadgroup size based on the meshlet vertex count, as discussed above.

A first observation we can make is that for that specific scene and GPU, a mesh shader can match and maybe perform a bit better than the vertex shader pipeline for smaller meshlets. As the meshlet size increases we notice an increased overhead. It appears that 64 vertices/124 triangles/64 threads is the best configuration for this usecase. Interestingly, when no pixel shader is bound, in which case the vertex/mesh shader just outputs a position, the meshlet and threadgroup size don’t appear to matter as much and the vertex shader pipeline is faster than the mesh shader in all cases.

Quickly cycling back the the vertex/primitive index clamping discussed above, if we use a branch instead of the min(), the cost for the 124/64/64 case jumps from 2.78ms to 3.36ms.

To dig a bit deeper into what is happening under the hood, let’s compare 2 GPU Traces with (top) and without mesh shaders (bottom)

![](../../assets/05812157acb4e5de.png)


![](../../assets/05812157acb4e5de.png)

It is apparent that, not limited by the [Primitive Distributor](https://pixeljetstream.blogspot.com/2015/02/life-of-triangle-nvidias-logical.html) (PD, NVidia’s Input Assembler equivalent), the mesh shader version has noticeably higher “Geometry” warps (blue graph).

Comparing the 2 traces side by side (1st trace mesh shaders, 2nd trace vertex shaders), we can confirm that PD throughput is minimal compared the vertex shader pipeline and the Vertex Attribute Fetch (VAF, the unit that brings vertex data to the vertex shader) is not utilised at all, so those 2 units can’t bottleneck the mesh shader pipeline.

Inspecting the Vertex-Tessellation-Geometry (VGT), the stages related to vertex processing and shading, related counters we can confirm that the active warps per cycle have increased noticeably when using a mesh shader, about x6 the number.

This seems to also increase the pressure to the Inter-Stage Buffer Entry (ISBE) memory. This is where vertex data that flow through the VGT stages are stored. This in turn appears cause the mesh shader warp launch to be stalled more, compared to the vertex shader pipeline warps.

In overall, it appears that the mesh shader pipeline avoids the PD bottlenecks, utilises the geometry units better and has higher shader occupancy than the vertex shader pipeline.

Now that we’ve established that a mesh shader pipeline can have no overhead, or even slightly improve performance over a vertex shader pipeline in some scenarios, it is time to investigate the true potential of mesh shaders, visibility culling. Doing per triangle visibility calculations in the mesh shader is certainly possible but it is usually better to start at a coarser level to quickly cull geometry in batches and we already have the geometry is cullable batches, the meshlets. To process the meshlets we will need to add an amplification shader to the pipeline.

```
struct Payload
{
uint MeshletIndices[AMPLIFICATION_SHADER_GROUP_SIZE];
};
groupshared Payload g_Payload;
[NumThreads(AMPLIFICATION_SHADER_GROUP_SIZE, 1, 1)]
void ASMain(
uint gtid : SV_GroupThreadID,
uint dtid : SV_DispatchThreadID,
uint gid : SV_GroupID
)
{
bool visible = false;
if (dtid < MeshletCount)
{
// Do visibility testing for this meshlet
visible = IsVisible(MeshletCullData[dtid]);
}
// Compact visible meshlets
if (visible)
{
uint index = WavePrefixCountBits(visible);
g_Payload.MeshletIndices[index] = dtid;
}
// Dispatch the required number of threadgroups to render the visible meshlets
uint visibleCount = WaveActiveCountBits(visible);
DispatchMesh(visibleCount, 1, 1, g_Payload);
}
```

Quite similar to a mesh shader, or a compute shader for that matter, the amplification shader will process one whole meshlet per thread, determine visibility and if visible, store the meshlet index to the Payload, which is just some common to the whole threadgroup memory that will be passed down to the mesh shader. In this instance I used a threadgroup size of 32.

Meshoptimiser can also produce the culling data required for this, using meshlet_computeMeshletBounds(), in the form of bounding spheres for each meshlet, or cones for fast back face culling. In this instance I only used the bounding spheres for culling. In the first instance I tried some simple frustum culling, using the planes to determine visibility of the bound sphere:

```
bool IsVisible(CullData cullData)
{
// Do a cull test of the bounding sphere against the view frustum planes.
float4 centre = mul(World, float4(cullData.BoundingSphere.xyz, 1) );
float radius = WorldScale * cullData.BoundingSphere.w;
for (int i = 0; i < 6; ++i)
{
if (dot(centre, Planes[i]) > radius)
{
return false;
}
}
return true;
}
```

For the reference St Miguel view, meshlet frustum culling makes a noticeable difference, dropping the g-buffer pass from 2.75ms (with CPU only, per mesh frustum culling) to 2.43ms. It is worth mentioning that this scene is made up of large triangles which cause some meshlets and bounding spheres to be very large, making them less effective during culling. More subdivision, or using bounding boxes instead of spheres might lead to improved culling.

To try a different culling method, I also dropped a quick and dirty occlusion culling implementation, based on an earlier experiment I described in [this post](https://interplayoflight.wordpress.com/2017/11/15/experiments-in-gpu-based-occlusion-culling/). For a hierarchical z-buffer I used the one produced by FidelityFX SSSR I had already integrated to the toy engine. The occlusion culling code was used mostly verbatim from that post so I won’t be pasting it here, only the results.

Red pixels in the following screenshot represent meshlets that are occlusion pass in the amplification shader culled.

![](../../assets/8f565f19c1fefbd2.png)


![](../../assets/8f565f19c1fefbd2.png)

In terms of performance, meshlet occlusion culling makes a much bigger difference dropping the gbuffer pass cost (for that view) from 2.75ms (with CPU per mesh frustum culling) to 1.86 ms. Adding per meshlet frustum culling on top, drops it even further, to 1.64ms, offering in total a very respectable 40% cost decrease for that pass, view and content.

The culling numbers presented are using a meshlet size of 124 triangles and 64 vertices (and a threadgroup size of 64), which as discussed earlier seems to be the optimal meshlet size for this GPU and scene. We discussed above the meshlet size may have an impact on visibility calculations. To showcase this, I re-run the experiment using meshlets of 64 triangles, 32 vertices and a threadgroup size of 32. Although without an amplification shader and meshlet occlusion this meshlet size is not the best in terms of performance, things change when meshlet occlusion is factored in. In this case, the smaller meshlet has the advantage, dropping the overall cost of the mesh shader path further, to 1.59ms.

Comparing occlusion for both meshlet sizes (left 64 vertices, right 32) reveals noticeably increased occlusion when using the smaller meshlet.

![](../../assets/8b0e2e1ffbf15238.png)

![](../../assets/c2c21287b366059c.png)

If we compare this final cost to the original, vertex shader pipeline cost of 2.85ms, the mesh shader pipeline, with per meshlet frustum and occlusion culling, dropped the gbuffer pass cost by 44% for that scene and view.

Using the Bistro scene with the view showcased earlier, the same mesh shader configuration drops the g-buffer pass cost from 1.06ms to 0.74ms a 30% decrease, which speaks to the content dependent effectiveness of the new pipeline.

Let’s do another GPU trace comparison between the vertex shader pipeline and the mesh shaders pipeline implementing the occlusion culling techniques discussed to see where the improvements are, for the St Miguel view. Remember that one of the goals of this work was to reduce the pressure on the Primitive Assembler/Rasteriser units by “software” culling as much geometry as possible. We can see that, indeed, we managed to do so (1st trace is mesh shaders, 2nd trace is vertex shaders):

The VPC unit responsible for clipping and culling triangles before rasterisation processes many less using the mesh shader pipeline.

The ZCULL unit, responsible for coarse z-culling of pixels, now culls many less due to the occlusion culling in the amplification shader:

During geometry processing (VTG units), the mesh shader manages to spawn many more warps compared to the vertex shader pipeline, more pixel warps and improves utilisation of the Streaming Multiprocessor (SM, the unit executing the shaders) reducing the amount of unallocated warps, meaning that in overall the GPU manages to do more actual work.

There is one last thing to test, we discussed earlier that a “pass-through” mesh shader pipeline (no AS), was a bit more expensive than the original vertex shader one for all meshlet configurations for a depth only pass (eg shadowpass, z-prepass). Factoring in occlusion and re-running the z-prepass in St Miguel showcases a big drop in the cost from 2.41ms with vertex shaders to 1.24ms with an amplification shader and occlusion, around 48%, even larger than the g-buffer pass improvement.

Worth mentioning that meshlet, even triangle, culling is certainly possible using a traditional pipeline, Frostbite demonstrated a few years ago a [compute shader pipeline](https://ubm-twvideo01.s3.amazonaws.com/o1/vault/gdc2016/Presentations/Wihlidal_Graham_OptimizingTheGraphics.pdf), using execute indirect, that processed meshlets and performed a similar job. Mesh shaders is a more flexible pipeline though, easier to set up, no compaction needed to remove empty drawcalls, and culling is done “inline” without the need for a memory roundtrip to store the data and for barriers to correctly synchronise the work.

To summarise the findings, with the small sample of scenes I tried, mesh shaders appear have the potential to speed up rendering measurably. Their efficiency depends a lot on the rendered content though and it takes some experimentation to find what configuration (meshlet size/threadgroup size) will work best in each case. Removing the Input Assembler (IA) from the pipeline can allow the GPU to go wider when processing vertices in those passes where IA is the bottleneck and while it doesn’t remove the Primitive Assembler, it can reduce the pressure on it by culling meshlets and triangles that don’t contribute to the scene.

There are aspects of mesh shading like how to support instancing, lodding and how to compress the data output from the mesh shader that I haven’t talked about but this will likely be a topic for a future post.

**Further readings on Meshlets and Mesh Shaders**

[Reinventing the Geometry Pipeline: Mesh Shaders in DirectX 12](https://www.youtube.com/watch?v=CFXKTXtil34)[Advanced Mesh Shaders](https://www.youtube.com/watch?v=0sJ_g-aWriQ)[Introduction to Turing Mesh Shaders](https://developer.nvidia.com/blog/introduction-turing-mesh-shaders/)[Mesh and task shaders intro and basics](https://timur.hu/blog/2022/mesh-and-task-shaders)[Mesh Shaders in AMD RDNA 3 architecture](https://gpuopen.com/gdc-presentations/2024/GDC2024_Mesh_Shaders_in_AMD_RDNA_3_Architecture.pdf)[Mesh shaders on AMD RDNA graphics cards](https://gpuopen.com/learn/mesh_shaders/mesh_shaders-index/)[Meshlet size tradeoffs](https://zeux.io/2023/01/16/meshlet-size-tradeoffs/)[Using Mesh Shaders for Professional Graphics](https://developer.nvidia.com/blog/using-mesh-shaders-for-professional-graphics/)[Mesh Shader DirectX specification](https://microsoft.github.io/DirectX-Specs/d3d/MeshShader.html)

Love mesh shaders! Such an elegant API. Glad to see it was straightforward to get some significant wins. Look forward to seeing more experiments in this area…