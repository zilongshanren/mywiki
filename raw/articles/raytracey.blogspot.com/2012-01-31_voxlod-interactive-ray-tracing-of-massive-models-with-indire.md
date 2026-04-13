---
title: 'VoxLOD: Interactive ray tracing of massive models with indirect lighting using
  voxels'
url: http://raytracey.blogspot.com/2012/01/voxlod-interactive-ray-tracing-of.html
author: Sam Lapere
published: '2012-01-31'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just encountered an impressive video of a technology named VoxLOD on Youtube today:

As the name aptly implies, VoxLOD uses a voxel-based LOD scheme to smoothly stream in and visualize the geometry of the massive model. The first part of the video shows direct lighting only (primary and shadow rays), while the second half is much more interesting and demonstrates real-time one bounce diffuse indirect lighting (filtered Monte Carlo GI). From the

[paper "Interactive ray tracing of large models using voxel hierarchies":](http://voxelium.wordpress.com/2012/01/31/interactive-ray-tracing-of-large-models-using-voxel-hierarchies/)"We cast one shadow ray per primary or diffuse ray, and two random diffuse rays per primary ray. The diffuse rays are used to compute both one bounce of indirect irradiance and environment irradiance, which are processed with a bilateral ﬁlter [TM98] to eliminate noise."


"There are two light sources: a point light (the Sun) and a hemispherical one (the sky). I use Monte Carlo integration to compute the GI with one bounce of indirect lighting. Nothing is precomputed (except the massive model data structure of course).

I trace only two GI rays per pixel, and therefore, the resulting image must be heavily filtered in order to eliminate the extreme noise. While all the ray tracing is done on the CPU, the noise filter runs on the GPU and is implemented in CUDA. Since diffuse indirect lighting is quite low frequency, it is adequate to use low LODs for the GI rays."

Another interesting tidbit from the paper:



The quality of the indirect lighting looks pretty amazing for just 2 (filtered) random samples per pixel and is completely noise-free, as can be seen in this picture from the paper

"By using LOD voxels, signiﬁcantly higher frame rates can be achieved, with minimal loss of image quality, because ray traversals are less deep, memory accesses are more coherent, and intersections with voxels are free, contrary to triangles (the voxel ﬁlls its parent node, therefore, the intersection is equal to the already computed intersection with the node). Furthermore, the LOD framework can also reduce the amount of aliasing artifacts, especially in case of highly tessellated models"

The quality of the indirect lighting looks pretty amazing for just 2 (filtered) random samples per pixel and is completely noise-free, as can be seen in this picture from the paper

All the ray tracing is currently CPU based (the GI algorithm runs at 1-2 fps on a quad core cpu), but it would probably run in real-time at much higher framerates when implemented entirely on the GPU.

## 2 comments:

The one big question about running this on a GPU is memory pressure. For a 300 million poly model, there's a rather large difference between 3GB as seen on a high end GPU and 24GB, as seen on a high end CPU.


Napkin calculations indicate that the model should take somewhere in the vicinity of 18.6GB (float3 position, uchar4 normal, uchar4 color, uint index. Since there are 300 million faces, then assuming a more or less watertight mesh, we can apply Eular's formula, x = V - E + F, where x is fairly small (perhaps around 10000 in this case). We know that each triangle has three edges, and each edge is shared by two triangles, so (3/2)*E=F. This gives us x = V - (5/2)*E for a general triangular mesh. Plugging in the numbers, we have something near to 0 = V - (5/2)*300 million, so V = 750 million. Thus, memory consumption for the mesh is 20 bytes/vertex * 750 million vertices + 4 bytes/index * 300 million faces * 3 indices/face = 18.6 GB). This means that the model will fit into the CPUs memory, but badly overflow the GPUs memory.

That's a pretty big napkin!



I agree with you that it is tricky to pull off out-of-core rendering of massive models on the GPU, but the CentiLeo video (youtube.com/watch?v=mxx9dyPO0js) shows it is possible.

I actually meant that the GI technique used in the VoxLOD video could be easily implemented on the GPU (the filtering algorithm already runs in CUDA) and it would run at high framerates because it only computes 2 random diffuse rays per pixel per frame.

Post a Comment