---
title: 'Sparse voxel octree and path tracing: a perfect combination?'
url: http://raytracey.blogspot.com/2010/07/sparse-voxel-octree-and-path-tracing.html
author: Sam Lapere
published: '2010-07-12'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I have been wondering for some time if SVO and path tracing would be a perfect solution for realtime GI in games. Cyril Crassin has shown in his paper


I think that this LOD "trick" could work with all kinds of secondary ray effects, not just shadows. Particularly ambient occlusion and indirect lighting could be efficiently calculated in this manner, even on glossy materials. One limitation could be high frequency content, because every voxel is an average of the eight smaller voxels that it's constituted of, but in such a case the voxels could be adaptively subdivided to a higher res (same for perfectly specular reflections). For diffuse materials, the cost of computing indirect lighting could be drastically reduced.


Another idea is to compute primary rays and first bounce secondary rays at full resolution, and all subsequent bounces at lower voxel LODs with some edge-adaptive sampling, since the 2nd, 3rd, 4th, ... indirect bounces contribute relatively little to the final pixel color compared to direct + 1st indirect bounce. Not sure if this idea is possible or how to make it work.


Voxelstein3d has already implemented the idea of pathtracing SVOs for global illumination (


UPDATE: VoxLOD actually has done this for diffuse global illumination and it seems to work nicely:



["Beyond triangles: Gigavoxels effects in videogames"](http://artis.imag.fr/Publications/2009/CNLSE09/gigavoxels_siggraph09_talk.pdf)that secondary ray effects such as shadows can be computed very inexpensively by tracing a coarse voxel resolution mipmap without tracing all the way down to the finest voxel resolution, something that is a magic intrinsic property of SVO's and which is to my knowledge not possible when tracing triangles (unless there are multiple LOD levels), where all rays have to be traced to the final leaf containing the triangle, which is of course very expensive. A great example of different SVO resolution levels can be seen in the video "Efficient sparse voxel octrees" by Samuli Laine and Tero Karras (on[http://code.google.com/p/efficient-sparse-voxel-octrees/](http://code.google.com/p/efficient-sparse-voxel-octrees/), video link at the right, a demo and source code for CUDA cards is also available).I think that this LOD "trick" could work with all kinds of secondary ray effects, not just shadows. Particularly ambient occlusion and indirect lighting could be efficiently calculated in this manner, even on glossy materials. One limitation could be high frequency content, because every voxel is an average of the eight smaller voxels that it's constituted of, but in such a case the voxels could be adaptively subdivided to a higher res (same for perfectly specular reflections). For diffuse materials, the cost of computing indirect lighting could be drastically reduced.

Another idea is to compute primary rays and first bounce secondary rays at full resolution, and all subsequent bounces at lower voxel LODs with some edge-adaptive sampling, since the 2nd, 3rd, 4th, ... indirect bounces contribute relatively little to the final pixel color compared to direct + 1st indirect bounce. Not sure if this idea is possible or how to make it work.

Voxelstein3d has already implemented the idea of pathtracing SVOs for global illumination (

[http://raytracey.blogspot.com/2010/03/svo-and-path-tracing-update.html](http://raytracey.blogspot.com/2010/03/svo-and-path-tracing-update.html)) with some nice results. Once a demo is released, it's going to be interesting to see if the above is true and doesn't break down with non-diffuse materials in the scene.UPDATE: VoxLOD actually has done this for diffuse global illumination and it seems to work nicely:

## No comments:

Post a Comment