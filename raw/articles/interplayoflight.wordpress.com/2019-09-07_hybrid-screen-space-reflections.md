---
title: Hybrid screen-space reflections
url: https://interplayoflight.wordpress.com/2019/09/07/hybrid-screen-space-reflections/
author: Kostas Anagnostou
published: '2019-09-07'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

As realtime raytracing is slowly, but steadily, gaining traction, a range of opportunities to mix rasteration-based rendering systems with raytracing are starting to become available: [hybrid raytracing](https://media.contentapi.ea.com/content/dam/ea/seed/presentations/gdc2018-seed-shiny-pixels-and-beyond-real-time-raytracing-at-seed.pdf) where rasterisation is used to provide the hit points for the primary rays, hybrid shadows where shadowmaps are combined with raytracing to achieve smooth or higher detail shadows, [hybrid antialiasing](https://news.developer.nvidia.com/understanding-the-need-for-adaptive-temporal-antialiasing/) where raytracing is used to antialias the edges only, hybrid reflections, where raytracing is used to fill-in the areas that screenspace reflections can’t resolve due to lack of information.

Of these, I found the last one particularly interesting: how well can a limited information lighting technique like SSR be combined with a full-scene aware one like raytracing, so I set about exploring this further.

I have experimented with raytracing in the past, I refer you to [previous](https://interplayoflight.wordpress.com/2018/07/04/hybrid-raytraced-shadows-and-reflections/) [blogposts](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/) for implementations of hybrid raytracing in the context of shadows and reflections. Since my main developing is done on a lowly HD 4000-GPU laptop, I don’t have the luxury of using raytracing APIs so I resort to traditional, compute shader-based raytracing, based on a bounding volume hierarchy, created on the CPU.

For screen space reflections I relied on the commonly used DDA line algorithm as implemented by [McGuire and Mara](http://casual-effects.blogspot.com/2014/08/screen-space-ray-tracing.html), using the hlsl port described [here](http://roar11.com/2015/07/screen-space-glossy-reflections/). Integrating the technique to my toy engine was pretty straightforward and I got it up and running with some good results.

![SSR](../../assets/996c7f02e3539228.png)


![SSR](../../assets/996c7f02e3539228.png)

Worth mentioning is that the floor material has a normal map which perturbs the reflection rays, so some visible discontinuities are not actually artifacts.

Visualising the reflections only, we can see the shortcoming of the screen-space technique, namely that it works with what it can find on screen. If a reflected ray can’t find a collision it fails and that can lead to large areas being black.

![SSR_only](../../assets/64d1d8c5792f3e8e.png)


![SSR_only](../../assets/64d1d8c5792f3e8e.png)

The following image marks in red the screen areas where geometric collision actually exists which SSR didn’t manage to resolve due to lack of information.

![](../../assets/a806f5c88f7f48ae.png)


![](../../assets/a806f5c88f7f48ae.png)

In such a case games typically resort to a local or global cubemap to fill-in the missing areas but this often leads to obvious transitions as the two sources of lighting can differ significantly, especially for global cubemaps.

With raytracing we can do better than that. We already know the pixels (and corresponding world positions) for which collision can’t be determined, so we can just cast reflection rays for those pixels only.

![SSRwithRaytracing](../../assets/931e72873a851081.png)


![SSRwithRaytracing](../../assets/931e72873a851081.png)

Much better! Raytracing manages to fill-in the missing areas, such as the bottom of the teapots, nicely as well as extending the reflections to the edges of the screen.

An interlude to briefly talk about the raytraced reflections, I am using a BVH of the scene geometry as described in an [older blogpost](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/). The BVH tree uses a [surface area heuristic](https://medium.com/@bromanz/how-to-create-awesome-accelerators-the-surface-area-heuristic-e14b5dec6160) to decrease traversal time and stores triangles in the leaves. In contrast to shadow raytracing, reflections require texture mapping and lighting, meaning access to normals, uvs and some material information. To avoid bloating the BVH tree with the extra information I am creating extra 2 buffers, one for normals and one for uvs and also a buffer for material information. I also pack a vertex index, to access normals/uvs, and a per triangle index, to access the material information, in the BVH leaf nodes.

//leaf node, write triangle vertices BVHLeafBBoxGPU* bbox = (BVHLeafBBoxGPU*)(bboxData + dataOffset); bbox->Vertex0 = ToFloat4(node->BoundingBox.Vertex0); bbox->Vertex1MinusVertex0 = ToFloat4(XMFloat3Sub(node->BoundingBox.Vertex1, node->BoundingBox.Vertex0)); bbox->Vertex2MinusVertex0 = ToFloat4(XMFloat3Sub(node->BoundingBox.Vertex2, node->BoundingBox.Vertex0)); //when on the left branch, how many float4 elements we need to skip to reach the right branch? bbox->Vertex0.w = sizeof(BVHLeafBBoxGPU) / sizeof(XMFLOAT4); // store the triangle index, we need it to access normals and uvs bbox->Vertex1MinusVertex0.w = node->TriangleIndex; // store material ID for this triangle bbox->Vertex2MinusVertex0.w = m_materialIDList[node->TriangleIndex];

The [Möller-Trumbore](https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/moller-trumbore-ray-triangle-intersection) ray-triangle intersection algorithm I am using, as [adapted](https://github.com/kayru/RayTracedShadows/blob/master/Source/Shaders/RayTracedShadows.comp) by [@YuriyODonnell](https://twitter.com/YuriyODonnell) returns the barycentric coordinates of the hit point which I use to interpolate normals and uvs.

//interpolate normal float3 n0 = BVHNormals[hitdata.TriangleIndex * 3].xyz; float3 n1 = BVHNormals[hitdata.TriangleIndex * 3 + 1].xyz; float3 n2 = BVHNormals[hitdata.TriangleIndex * 3 + 2].xyz; float3 n = n0 * (1 - hitdata.BarycentricCoords.x - hitdata.BarycentricCoords.y) + n1 * hitdata.BarycentricCoords.x + n2 * hitdata.BarycentricCoords.y; n = normalize(n); //interpolate uvs float2 uv0 = BVHUVs[hitdata.TriangleIndex * 3].xy; float2 uv1 = BVHUVs[hitdata.TriangleIndex * 3 + 1].xy; float2 uv2 = BVHUVs[hitdata.TriangleIndex * 3 + 2].xy; float2 uvCoord = uv0 * (1 - hitdata.BarycentricCoords.x - hitdata.BarycentricCoords.y) + uv1 * hitdata.BarycentricCoords.x + uv2 * hitdata.BarycentricCoords.y;

With the normal and uv coordinates at hand I can do texturing and lighting at the hitpoint getting the result showcased above. In the current implementation only texture mip 0 is sampled, performing mipmapping without screen space derivates (as in the case of raytracing) requires special handling as discussed in the Raytracing Gems [book chapter](https://media.contentapi.ea.com/content/dam/ea/seed/presentations/2019-ray-tracing-gems-chapter-20-akenine-moller-et-al.pdf).

Having implemented both techniques side by side gives us a prime opportunity to compare them directly, in the same context, to identify potential differences/discontinuities.

Before we start the comparison, it is worth keeping this image in mind, this is conceptually how reflections work, it is as if we mirror the camera under the reflection plane.

![](../../assets/726357fa6880d0cc.png)

The new camera position will not affect view direction invariant lighting such as diffuse lighting. Comparing SSR and fully raytraced reflections confirm this, the diffuse light intensity is the same in both images (Top is SSR, bottom is fully RT reflections):

![](../../assets/24e9ca180ea637b2.png)


![](../../assets/24e9ca180ea637b2.png)

![](../../assets/70aad3b89df5a804.png)


![](../../assets/70aad3b89df5a804.png)

In terms of specular highlights in the reflected image, which actually depend on the camera direction, there are can be significant differences. Focus for example on the specular highlight on the red teapot (top SSR, bottom RT):

![](../../assets/cd58a37a059acc5d.png)


![](../../assets/cd58a37a059acc5d.png)

![](../../assets/abfbe98e0ce4648c.png)


![](../../assets/abfbe98e0ce4648c.png)

SSR just copies the specular from the top of the teapot and places it at the wrong place while raytracing correctly places the specular reflection according to the mirrored camera position.

This also showcases a major difference between SSR and raytraced reflections: SSR produces the reflection of a photo of the scene while raytracing produces the reflection of the scene, with a pair of images which demonstrate this nicely (top SSR, bottom RT)

![](../../assets/768c257cb1851d19.png)


![](../../assets/768c257cb1851d19.png)

![](../../assets/0e7bd71dabe10c85.png)


![](../../assets/0e7bd71dabe10c85.png)

Raytracing also solves a screen space reflections pet peeve of mine, which is specular highlights in the reflected image that do not exist in the main image (top SSR, bottom RT)

![](../../assets/1246855d66b0f348.png)


![](../../assets/1246855d66b0f348.png)

![](../../assets/7bd2ca8bcbf4a364.png)


![](../../assets/7bd2ca8bcbf4a364.png)

Raytracing does not win in all areas though. For example with SSR we automatically have access to shadows in the reflected image, something that does not come for free with RT (top SSR, bottom RT)

![](../../assets/b6a8e40c6aaa413f.png)


![](../../assets/b6a8e40c6aaa413f.png)

![](../../assets/989f029c1ec8e8d7.png)


![](../../assets/989f029c1ec8e8d7.png)

This is particularly noticeable on the reflections of the walls bottom left and top right in the above images, and on the statue. It is possible to calculate shadows in reflected image with raytracing of course by casting additional rays from the hit points to the light, something I actually did in the following image.

![](../../assets/f547f438838637ce.png)


![](../../assets/f547f438838637ce.png)

In such a case though, the extra rays add to the cost of the raytraced reflections and even then it is unlikely that we can achieve the quality of the main scene shadows. This also extends to other types of (expensive) lighting that we calculate during the main scene rendering such as global illumination, ambient occlusion etc. These will come for free with SSR.

There is one last difference but to see it I had to remove the floor material normal map (to avoid distortion) in the hybrid SSR/RT reflections image: the texture quality with raytracing is better than with SSR. For example, in the area marked in red, the transition between SSR and RT is clearly visible.

![](../../assets/1ebbd6db66b71e6b.png)


![](../../assets/1ebbd6db66b71e6b.png)

How much all the above will affect the use of raytracing to augment an SSR image depends on one’s use case of course. With mirror reflections the differences may be visible, normal map distortion can hide some of them and glossy reflection may hide even more.

I didn’t mention performance so far, only focused on the visual differences, and this is because both reflection techniques, as implemented, are out of reach of the HD 4000, making profiling them hard. Also, the typed buffer I use to store the BVH is not the best choice for this particular GPU making the any comparison unfair. For a discussion on the impact of buffer types to store the BVH I refer you to [my previous post](https://interplayoflight.wordpress.com/2018/09/04/hybrid-raytraced-shadows-part-2-performance-improvements/) on raytracing. In general the cost of SSR is relatively bound and does not depend on the geometric complexity of the scene, something raytracing is very sensitive of. In the low-polygon scene I used, it is quite likely that fully raytraced reflections will be faster than high quality screen space reflections.

I have made my new [DX12 toy engine](https://github.com/KostasAAA/FeaxRenderer) available on github if you are interested in the implementation of the above, I must warn you that it is very much work in progress and quite messy at the moment. :-)

Also, the textures I am using in the above examples are from [cc0textures.com](https://cc0textures.com/)

Glad to see you still got this going.

I have an idea on how to improve the performance of RT shadows. Rather than performing ray tracing every pixel you can take advantage of the fact that shadow maps only show aliasing at the edge of shadows and perform shadow RT only on pixels that are at the border of the shadow where aliasing occurs.