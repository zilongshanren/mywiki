---
title: Hybrid raytraced shadows and reflections
url: https://interplayoflight.wordpress.com/2018/07/04/hybrid-raytraced-shadows-and-reflections/
author: Kostas Anagnostou
published: '2018-07-04'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Unless you’ve been hidden in a cave the past few months, doing your rendering with finger painting, you might have noticed that raytracing is in fashion again with both Microsoft and Apple providing official [DirectX (DXR)](https://blogs.msdn.microsoft.com/directx/2018/03/19/announcing-microsoft-directx-raytracing/) and [Metal](https://developer.apple.com/videos/play/wwdc2018/606/) support for it.

Of course, I was curious to try it but not having access to a DXR capable machine, I decided to extend my toy engine to add support for it using plain computer shaders instead.

I opted for a [hybrid approach](https://www.imgtec.com/blog/hybrid-rendering-for-real-time-lighting/) that combines rasterisation, for first-hit determination, with raytracing for secondary rays, for shadows/reflection/ambient occlusion etc. This approach is quite flexible as it allows us to mix and match techniques as needed, for example we can perform classic deferred shading adding raytraced ambient occlusion on top or combine raytraced reflections will screen space ambient occlusion, based on our rendering budget. Imagination has already done [a lot of work](https://www.imgtec.com/blog/tag/powervr-ray-tracing/) on hybrid rendering, presenting a [GPU](https://www.imgtec.com/blog/powervr-gr6500-ray-tracing/) which supports it in 2014.

Realtime rendering without rasterisation is nothing new and it is already being used in games, like the excellent [Dreams](http://advances.realtimerendering.com/s2015/AlexEvans_SIGGRAPH-2015-sml.pdf) and [Claybook](https://twvideo01.ubm-us.net/o1/vault/gdc2018/presentations/Aaltonen_Sebastian_GPU_Based_Clay.pdf). Both those games are based on raymarching signed distance fields to speed up/determine ray collisions though and do not deal with polygons directly.

Like DXR, in this demo we will processing mesh polygons to determine if/where a ray collides with a prop analytically solving ray-triangle intersections. This is a time consuming task if you brute force it, as you can imagine, as it would require us to test NxM intersections, for N rays and M scene polygons, and that is for just one ray per pixel. So, to speed things up, we typically calculate a spatial subdivision hierarchy for our scene. [Bounding Volume Hierarchies](https://en.wikipedia.org/wiki/Bounding_volume_hierarchy) (BVH) are pretty common as a raytracing acceleration technique and this is what I implemented in the demo.

To create a BVH we start by determining the axis aligned bounding box (aabb) that contains all props in the scene, subdivide it by an axis and continue the process. In 2D, this looks like this (image from [Wikipedia](https://en.wikipedia.org/wiki/Bounding_volume_hierarchy)).

![500px-Example_of_bounding_volume_hierarchy.svg](../../assets/025ce686c3c8cf07.png)


There are various approaches to determine which axis to subdivide across and where, for example [@Peter_shirley](https://twitter.com/Peter_shirley) in his great Raytracing books chooses the axis [randomly](https://github.com/petershirley/raytracingthenextweek/blob/master/bvh.h), sorts the leaf bounding boxes, divides the list in half and recursively processes the two halves. An alternative would be a [Surface Area Heuristic](https://medium.com/@bromanz/how-to-create-awesome-accelerators-the-surface-area-heuristic-e14b5dec6160) (SAH) which tries to balance area size and number of polygons. SAH produces better subdivision results especially when the scene is non uniform in terms of prop density, size and polycount (as would be, I expect, a real game level). You can find an implementation of this technique [here](https://github.com/kayru/RayTracedShadows).

In my case the prop distribution (200 prop instances in total) is uniform and the sizes are similar.

So I went for a similar to Shirley’s approach, only I chose to subdivide across the maximum axis at every step and didn’t pick it randomly, since my demo level has a much shorter Y axis and subdividing across it would give very short and wide aaboxes.

WordPress won’t format the skeleton BVH creation code correctly so I pasted it [here](https://pastebin.com/wCDbFnGt), you can also find the full implementation in the attached code at the end of the post.

Something worth noticing is that I process bounding boxes and not polygons, meaning that the BVH tree leaves will contain individual prop bounding boxes and “pointers” to the actual geometry. This is not ideal in terms of performance since it means that when I reach a leaf while traversing the tree, I will have to then iterate over all prop triangles to find ray intersections. Adding the triangles to the BVH should speedup collision detection at the expense of a deeper tree. I kept it like that for the moment though for simplicity.

All geometry in the scene is stored in a number of global buffers (one for position, one for normals, one for per instance data etc) and also we use an arguments buffer for indirect rendering, similarly to the [GPU driven rendering post](https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/) (I suggest to take a quick look for more on the data layout).

The most intuitive way to traverse a BVH is recursion, calling the same method on each of a node’s children. As recursion is not supported by shading languages, we can resort to other methods like maintaining [a stack in the shader](https://devblogs.nvidia.com/thinking-parallel-part-ii-tree-traversal-gpu/) to push and pop nodes to or we can simply linearise the BVH getting every “Left” node to store an offset to its “Right” sibling. The BVH is stored in a “depth-first” ordering, following the left nodes until we reach a leaf and then backtracking.

In the above image, on the left is a typical BVH tree and on the right how the tree is actually stored. The shader, when traversing the tree, always follows the Left node first and is only skipping to the Right when the ray-aabb test fails.

Each node of the BVH is represented by a simple structure which contains the node aabb, an offset to the node sibling and a prop instance index. A node offset of -1 means that the BVH traversal must stop. Also an instance index of -1 signifies an intermediate node (not a leaf node):

struct BVHNode { D3DXVECTOR3 m_minBounds; int m_instanceIndex; D3DXVECTOR3 m_maxBounds; int m_nodeOffset; };

This all happens on the CPU which calculates the BVH and produces an simple Structured Buffer with the BVHNode data.

Given a ray the compute shader starts at the root of the BVH tree, checking for an intersection against its aabb. Actually, as we are only tracing secondary rays we can skip the root node as the ray origin will always be in its aabb. Then it checks the left child’s aabb for collision and if there is a collision it continues down its left node until it reaches a node that the intersection test fails. Then it uses the nodeOffset to skip to the right node of the failed sibling and continue the same process all over again. When it reaches a leaf node, this means that the ray potentially intersects the corresponding prop instance and it stores the instanceIndex in an array of potential collisions. Unfortunately, determining ray-aabb intersection for a leaf node is not enough to terminate the traversal. A simple example, consider an aabb that contains a sphere prop. The ray can pass through and collide with its corner but never touch the sphere. This is why we need to traverse all of the BVH tree and store all the potential intersections.

In case you’re wondering if we could, once we’ve reached a leaf node, pull in the prop instance’s mesh data and perform the ray intersection test against all of its triangles there and then before continuing the traversal: I’ve tried that and apparently it is significantly slower than storing all the potential intersections and doing fine-grain ray intersection tests later. A reason for that is that the shader code in such a case becomes very branchy with large branches. The compiler will conservatively allocate the amount of registers needed for the largest branch, even if it is not followed very often, reducing the opportunity to have many warps in flight to hide memory latency. There is also another reason why storing all potential collisions is necessary which I will explain later.

We are going to calculate 2 types of intersections, a ray-box one and a ray-triangle one. For the ray-box intersection I adapted the technique described [here](https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-box-intersection):

bool RayIntersectsBox(float3 origin, float3 rayDirInv, float3 BboxMin, float3 BboxMax) { const float3 t0 = (BboxMin - origin) * rayDirInv; const float3 t1 = (BboxMax - origin) * rayDirInv; const float3 tmax = max(t0, t1); const float3 tmin = min(t0, t1); const float a1 = min(tmax.x, min(tmax.y, tmax.z)); const float a0 = max( max(tmin.x,tmin.y), max(tmin.z, 0.0f) ); return a1 >= a0; }

For the ray-triangle intersection I used [Möller-Trumbore’s algorithm, ](https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/moller-trumbore-ray-triangle-intersection)adapted from [@YuriyODonnell](https://twitter.com/YuriyODonnell)‘s [implementation](https://github.com/kayru/RayTracedShadows/blob/master/Source/Shaders/RayTracedShadows.comp):

bool RayTriangleIntersect( const float3 orig, const float3 dir, float3 v0, float3 e0, float3 e1, inout float t, inout float2 bCoord) { const float3 s1 = cross(dir.xyz, e1); const float invd = 1.0 / (dot(s1, e0)); const float3 d = orig.xyz - v0; bCoord.x = dot(d, s1) * invd; const float3 s2 = cross(d, e0); bCoord.y = dot(dir.xyz, s2) * invd; t = dot(e1, s2) * invd; if ( #if BACKFACE_CULLING dot(s1, e0) < -kEpsilon || #endif bCoord.x 1.0 || bCoord.y 1.0 || t 1e9) { return false; } else { return true; } }

The algorithm can support back face culling, and also returns a collision point's distance from the ray origin and the barycentric coordinates which we will use later to interpolate attributes on the surface of the triangle.

### Raytracing Shadows

Having a way to accelerate ray-aabb intersections (the BVH) and the tools to test for ray-box and ray-triangle intersections, it is time to put them to use to calculate raytraced shadows for the directional light. The “hybrid” part of the approach refers to first performing a regular g-buffer pass, which is similar to finding the first ray intersection with the scene props although it is done with rasterisation and it is very fast. Then, in the compute shader, we reconstruct world space position from the depth buffer and use that as the ray origin. The ray direction is simply the light direction for the directional light, same for all rays.

We start by traversing the BVH to find potential collisions:

InstanceDataIn instance; do { //try collision against this node's bounding box instance = instanceDataLDS[index]; collision = RayIntersectsBox(worldPos, rayDirInv, instance.BboxMin.xyz, instance.BboxMax.xyz); if (collision && (noofCollisions = 0) ) { instanceIndices[startIndex][noofCollisions++] = instance.BboxMin.w; } //if there is collision, skip to the next node (left) or skip over the whole branch index += collision ? 1 : instance.BboxMax.w; } while (instance.BboxMax.w > 0);

We store up to 5 potential collisions (the instance indices that corresponds to the aabb intersected by the ray).

Once this is done, we iterate over the potential collisions array and using the instance index we pull the world matrix and DrawcallID from the per-instance data buffer. The DrawcallID is used to index into the arguments buffer array to retrieve the number of indices for this prop and the vertex/index buffer offsets (I suggest you refer to [this blog post](https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/) which describes that data layout in great detail).

for (int j = 0; j < noofLeaves && !collision; j++) { int instanceID = instanceIndices[startIndex][j]; int drawcallID = instancePropData[instanceID].DrawcallID; //number of indices uint noofIndices = drawcallData[drawcallID * 5 + 0]; //offset into the index buffer uint indexBufferOffset = drawcallData[drawcallID * 5 + 2]; //offset into the vertex buffer uint vertexBufferOffset = drawcallData[drawcallID * 5 + 3]; //get world matrix for this instance float4x4 world = ConvertVectorsToMatrix( instancePropData[instanceID].World_Row1, instancePropData[instanceID].World_Row2, instancePropData[instanceID].World_Row3 ); [loop] for (int i = 0; i < noofIndices && !collision; i += 3) { float index0 = vertexBufferOffset + IndexBuffer[indexBufferOffset + i + 0]; float index1 = vertexBufferOffset + IndexBuffer[indexBufferOffset + i + 1]; float index2 = vertexBufferOffset + IndexBuffer[indexBufferOffset + i + 2]; float3 v0 = mul(float4(Positions[index0].xyz, 1), world); float3 v1 = mul(float4(Positions[index1].xyz, 1), world); float3 v2 = mul(float4(Positions[index2].xyz, 1), world); collision = RayTriangleIntersect( worldPos, rayDir, v0, v1 - v0, v2 - v0 ); } }

All we are looking for is something that blocks the ray towards the light, so stopping the iteration when we find the first ray-triangle collision is enough. Also to speed things up we do not use the backface culling feature of the ray-triangle intersection algorithm I mentioned above. Any triangle collision will do.

The shadows are calculated at a quarter resolution screen-space buffer to speed things up.

The main bottleneck in this shader is memory bandwidth, which depends on the number of polygons of the prop. In this example I am using the lowest mesh lod to calculate intersections (which does not mean much in this context as most of the props are cubes), but in a real game environment it could be a couple of lods lower that you’d use to render the main pass at this distance, or lower if you can afford it visually.

Things I have tried and their impact on performance:

- Storing the potential collisions list in shared memory instead of a “register array”. The reasoning behind this is that since registers are not indexable and since the GPU will potentially store them in Local Memory, which is cached in L2 on Maxwell, it should be faster to keep them closer to the SM (
[Streaming Multiprocessor](http://international.download.nvidia.com/geforce-com/international/pdfs/GeForce_GTX_980_Whitepaper_FINAL.PDF)) in shared memory. In practice it didn’t make a measurable difference, probably because of the small size of the array. - Caching the BVH buffer in shared memory. Since it is used by all the threads in the thread group it makes sense to keep it locally in shared memory. In practice it didn’t help as it required me to increase the thread group size a lot to allow reuse of the buffer among more threads and this didn’t help with the already low occupancy (the ratio of active warps on an SM to the maximum number of active warps supported by the SM). Also in this demo the BVH buffer is small enough (802 float4s) to be cached in the texture cache of the SM and it is used by all thread groups (so less opportunities to get evicted).
- Decreasing the thread group size. Initially I started with a 256 thread group size. Dropping it to 64 reduced the shadow pass cost a bit, increasing the occupancy.
- Changing the data format for vertex data. This had the largest impact, initially I had the vertex position stored using a R32G32B32_FLOAT format. This might be ok when you render the mesh once or twice, but in the case of raytracing, where you might have to touch the vertex many times it can cripple performance. Since collision detection was my aim, precision was not of utmost importance so I went ahead and tried a R8G8B8A8_SNORM format to store my vertex position. In my case the (object space) vertex positions range at most between -1.0..1.0 so the range is correct and the precision for that range for shadows is good enough. This was the biggest win in this context and brought down the shader cost significantly. Considering that vertex positions are in object space (so their range is relatively small especially if your unit is a metre), then it might be worth considering a normalised, non floating point data format (such as R16G16B16A16_SNORM), even if that means having to normalise the vertex position ranges, to win from the increased precision and size reduction.

Other issues:

- There is no vertex caching at all, we have to transform the vertex every time we need to use it, wasting both memory bandwidth for the transform, registers for the calculations and ALUs. Storing the transformed vertex back to global memory might be an option which I didn’t try.

Hard raytraced shadows are good but at quarter resolution they look a bit aliased. I wondered if some [temporal antialiasing](https://github.com/playdeadgames/temporal) might help at all in this case, so I implemented a bare bones system to give it a try. Essentially, since I don’t have a projection transform to jitter, during depth buffer quarter-size downsampling I cycle through all 4 hi-res samples and use those to calculate world position and ray origin. Then in a separate, again quarter resolution, pass I use a history buffer to accumulate the “jittered” samples. This is equivalent to supersampling the raytraced shadows in time, and improves the shadow quality noticeably, at a minimal extra cost.

Of course, like any temporal AA technique, it suffers from ghosting when the camera moves. Nothing a bit of [neighbourhood clamping](http://advances.realtimerendering.com/s2016/Filmic%20SMAA%20v7.pptx) can’t improve though.

### Raytracing Reflections

Having a basic system that traces secondary rays to calculate hard shadows, it is relatively straightforward to use it in other contexts like mirror reflections. Following the above example we will need to load the normal from the normal buffer (gbuffer), calculate the reflected ray direction and start traversing the BVH to produce the list of potential collisions like previously.

The next step, that of actually determining mesh collision, is a bit more involved and more expensive. Firstly, testing ray-triangle intersection is not enough, we will need to locate the exact position of on the triangle the collision happened at. This is needed to interpolate uv coordinates and normals on the surface of the triangle.

Fortunately, the ray-triangle intersection code we used for the shadows already supports this in the form of barycentric coordinates. As an added bonus, the algorithm supports back face culling which, unlike the shadow raycasting pass, we would like to use to exclude back faces from the ray-intersection test.

The core loop looks similar to the shadow raycasting one:

for (int i = 0; i <noofIndices && !collision; i += 3) { float index0 = vertexBufferOffset + IndexBuffer[indexBufferOffset + i + 0]; float index1 = vertexBufferOffset + IndexBuffer[indexBufferOffset + i + 1]; float index2 = vertexBufferOffset + IndexBuffer[indexBufferOffset + i + 2]; float3 v0 = mul(float4(Positions[index0].xyz, 1), world); float3 v1 = mul(float4(Positions[index1].xyz, 1), world); float3 v2 = mul(float4(Positions[index2].xyz, 1), world); collision = RayTriangleIntersect( worldPos, rayDir, v0, v1 - v0, v2 - v0, t, barycentricCoords ); collisionPoint.materialIndex = materialIndex; collisionPoint.coord = barycentricCoords; collisionPoint.triangleIndex = i; collisionPoint.vertexOffset = vertexBufferOffset; collisionPoint.indexOffset = indexBufferOffset; }

Once we’ve determined the collision we will need to interpolate and calculate uv coordinates and normal at the collision point something that needs accessing the normal and uv vertex streams:

if (collision) { bcoords = collisionPoint.coord; MaterialInfo material = MaterialData[collisionPoint.materialIndex]; float3 colour = material.Colour.rgb; int index0 = collisionPoint.vertexOffset + IndexBuffer[collisionPoint.indexOffset + collisionPoint.triangleIndex + 0]; int index1 = collisionPoint.vertexOffset + IndexBuffer[collisionPoint.indexOffset + collisionPoint.triangleIndex + 1]; int index2 = collisionPoint.vertexOffset + IndexBuffer[collisionPoint.indexOffset + collisionPoint.triangleIndex + 2]; float3 n0 = Normals[index0].xyz; float3 n1 = Normals[index1].xyz; float3 n2 = Normals[index2].xyz; float3 n = n0 * (1 - bcoords.x - bcoords.y) + n1 * bcoords.x + n2 * bcoords.y; if (material.AlbedoTexArrayID < 255) { float2 uv0 = UVs[index0].xy; float2 uv1 = UVs[index1].xy; float2 uv2 = UVs[index2].xy; float2 uvCoord = uv0 * (1 - bcoords.x - bcoords.y) + uv1 * bcoords.x + uv2 * bcoords.y; colour *= AlbedoTextureAtlas.SampleLevel(samplerLinear, float3(uvCoord, material.AlbedoTexArrayID), 0).rgb; } outputColour = ((1 - roughness) * (2.5 * saturate(dot(n, DirLightDirection)) + 0.25)) * colour; }

We first interpolate the normals to do some lighting and if the material support textures we interpolate the uvs as well and sample the texture atlas (as I describe in [a previous post](https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/), I batch all textures in a texture atlas to reduce the number of drawcalls and the amount of DX state setting). Then I botch some diffuse lighting for the reflected surface and make the intensity of the reflection depend on the roughness of the reflector.

The result is pretty good, apart from two issues: first, the reflected surfaces are not shadowed properly. This would require casting another ray from the reflected surface point towards the light, something that would increase the shader complexity (let alone the memory requirements) a lot. The second issue is that the ordering of the reflections looks a bit wrong. This is because, unlike the shadow pass, determining a mesh collision is not enough, we need to determine collision with the mesh **closest **to the ray origin. This we can fix, the ray-triangle intersection test returns the distance of the collision point along the ray. What we need to do is iterate over all instances in the potential collisions list and keep the one with the smallest distance t:

collision = RayTriangleIntersect( worldPos, rayDir, v0, v1 - v0, v2 - v0, t, bcoords ); if (collision && t < minDist) { minDist = t; collisionPoint.materialIndex = materialIndex; collisionPoint.coord = bcoords; collisionPoint.triangleIndex = i; collisionPoint.vertexOffset = vertexBufferOffset; collisionPoint.indexOffset = indexBufferOffset; }

The reflections still don’t look properly lit but now at least the ordering is correct!

Like in the shadow pass, I lowered the precision and range of the vertex positions, normals and UV streams data formats to R8G8B8A8_SNORM and R8G8_UNORM. This again had a measurable (positive) impact on performance, due to memory bandwidth requirement reduction.

To drive the importance of selecting the proper data format and layout of your shader data home, this is the NSight capture of the reflection pass, before and after the data format modifications:

The shader is mostly TEX bound which relates to reading data from the memory through shader resource views/unordered access views.

Changing the data formats reduces the amount of data read in the shader and improves things noticeably, bringing the TEX bottleneck down and increasing the SM utilisation, reducing the number of warps that are waiting on memory fetches (Warp Stall Long Scoreboard value).

The numbers are still not ideal though and the shader clearly needs another optimisation pass.

The performance of both shadows and reflections was not bad in overall on the GTX 970, **2.4ms** for the reflections and **1.5 ms** for the shadows (varying according to the view position/orientation of course), processing 200 prop instances, it was also pretty decent (as in, interactive) on the IntelHD 4000 laptop after some optimisations. Unlike rendering approaches that decouple shading from geometry though, such as deferred shading and screen space techniques, raytracing cost is linked to both the geometric complexity and the shading/lighting model complexity, and mesh and material lodding becomes even more important. In this demo I conveniently chose the lowest LOD for the meshes and did no texture/material lodding (mainly because my textures did not have mips), but in a more representative environment you would like to select lod levels in the compute shader, based on the prop instance distance/size on screen. Shader lodding might be a bit more complicated though, as it would have to be in the form of an ubershader with dynamic branches to skip over code that shouldn’t be executed in the distance. This might cause problems with divergent rays as I will explain next.

Admittedly, I chose to handle possibly the easiest raycasting problem, hard shadows and mirror reflections. I only used a ray per pixel/thread and since the rays are mostly parallel, it is very likely that all the threads in a warp will follow exactly the same path in the compute shader, reducing divergence to a minimum and keeping memory and cache access predictable and well defined. Once you start widening the raytracing area and adding more rays the divergent shader paths will kick in, performance will become less predictable and performance will deteriorate significantly.

Even adding something as simple as refraction might have a large performance impact. To illustrate this I added a normal map to the terrain mesh (ok, the large cuboid at the bottom) which immediately adds more than half a ms to the reflections pass cost (up to 3 ms from 2.4 ms for that particular view)

Doubling the intensity of normal perturbation increases the reflections cost significantly (up to 3.9ms from 2.4ms without the normalmap):

This is happening because now each ray (direction) in each thread is different and follows a different path through the shader, it can potentially fetch data from a different location, introducing cache misses and increasing the raytracing cost. Perturbation does produce nicer reflections though. :-)

A video demonstrating raytraced shadows and reflections in action:

To summarise the key takeaways from the whole experiment:

- Raytracing is fun!
- The raytracing shader is memory bandwidth limited. Use
[Structure of Arrays](https://en.wikipedia.org/wiki/AOS_and_SOA)(SoA) data layouts to only pull in the data that you need and consider lower precision/bit size formats specifically for the raytracing pass. This might introduce some memory allocation overhead but it is worth it, memory is cheap but accessing it in the shader is not. - Smaller thread groups might help the GPU hide latencies a bit better (at least in this case, on Maxwell) and increase occupancy.
- Don’t introduce many and very large branches in the shader code. The compiler will allocate registers based on the needs of the largest branch, even if not taken that often, and this will reduce the GPU’s capability to have many threads in flight to hide memory latency. Also divergence (many potential paths through a series of if-statements) in the shader is in general a bad thing as it can increase shader execution time.
- Study the target GPU and understand how it works.

What’s next? I suppose some deeper performance profiling and analysis are in order, the raytracing shader has low occupancy (~30%) still, significantly lower than the theoretical occupancy afforded by the number of registers allocated (48 which corresponds to 60% occupancy). Also the Scoreboard % is still quite high meaning that a significant % of warps are stalling on memory fetches.

The demo’s [code and executable](https://1drv.ms/u/s!AmOPA68QU4JIiNdbmHiF4nd2KQeAow) are available if anyone would like to take a peek. It uses some textures from the Sponza model.

Raytracing shadows and reflections was great fun and can produce more plausible results than screen-space solutions. I am not convinced yet that raytracing will fully replace rasterisation any time soon but I believe that it will complement it nicely.

A few more good articles on BVH and raytracing worth studying:

[Primitives And Intersection Acceleration](http://www.pbrt.org/chapters/pbrt-2ed-chap4.pdf)from Physically Based Rendering 2nd edition[Introduction to Acceleration Structures](https://www.scratchapixel.com/lessons/advanced-rendering/introduction-acceleration-structure/bounding-volume-hierarchy-BVH-part1)[Thinking Parallel, Collision Detection on the GPU](https://devblogs.nvidia.com/thinking-parallel-part-i-collision-detection-gpu/)[GPU path tracing tutorial 3: GPU-friendly Acceleration Structures](http://raytracey.blogspot.com/2016/01/gpu-path-tracing-tutorial-3-take-your.html)[Shiny Pixels And Beyond: Real-Time Raytracing At Seed](https://www.ea.com/seed/news/seed-gdc-2018-presentation-slides-shiny-pixels)[D3D12 Raytracing Samples](https://github.com/Microsoft/DirectX-Graphics-Samples/tree/master/Samples/Desktop/D3D12Raytracing)


[…] Hybrid raytraced shadows and reflections […]