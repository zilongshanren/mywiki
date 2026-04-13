---
title: 'VoxLOD: interactive ray tracing of massive polygon models with voxel based
  LOD + Monte Carlo global illumination!'
url: http://raytracey.blogspot.com/2010/09/voxlod-interactive-ray-tracing-of.html
author: Sam Lapere
published: '2010-09-08'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/4bdbe9487c72c4e7.png)


![](../../assets/4bdbe9487c72c4e7.png)

This is really amazing technology:


Video:


Some quotes from the author's blog:


[http://voxelium.wordpress.com/2010/07/25/shadows-and-global-illumination/](http://voxelium.wordpress.com/2010/07/25/shadows-and-global-illumination/)Video:

[http://www.youtube.com/watch?v=RZ48J48b3J8](http://www.youtube.com/watch?v=RZ48J48b3J8)Some quotes from the author's blog:

"a real-time massive model visualization engine called VoxLOD, which can handle data sets consisting of hundreds of millions of triangles.The author of this engine has also written a paper entitled: "

It is based on ray casting/tracing and employs a voxel-based LOD framework. The original triangles and the voxels are stored in a compressed out-of-core data structure, so it’s possible to explore huge models that cannot be completely loaded into the system memory. Data is fetched asynchronously to hide the I/O latency. Currently, the renderer runs entirely on the CPU.

...

I’ve implemented shadows in VoxLOD, which has thus become a ray tracer. Of course, level-of-detail is applied to the shadow rays too.

While shadows make the rendered image a lot more realistic, the parts in shadow are completely flat, devoid of any details, thanks to the constant ambient light. One possible solution is ambient occlusion, but I wanted to go further: global illumination in real-time.

GI in VoxLOD is very experimental and unoptimized for now. It’s barely interactive: it runs at only 1-2 fps at 640×480 on my dual-core Core i7 notebook. Fortunately, there are lots of optimization opportunities. Now let’s see an example image:

Note that most of the scene is not directly lit, and color bleeding caused by indirect lighting is clearly visible. There are two light sources: a point light (the Sun) and a hemispherical one (the sky). I use Monte Carlo integration to compute the GI with one bounce of indirect lighting. Nothing is precomputed (except the massive model data structure of course).

I trace only two GI rays per pixel, and therefore, the resulting image must be heavily filtered in order to eliminate the extreme noise. While all the ray tracing is done on the CPU, the noise filter runs on the GPU and is implemented in CUDA. Since diffuse indirect lighting is quite low frequency, it is adequate to use low LODs for the GI rays."

[Interactive Out-of-Core Ray Casting of Massive Triangular Models with Voxel-Based LODs](http://voxelium.files.wordpress.com/2010/03/voxlod_paper.pdf)"

There is a very interesting graph in this paper, which shows that when using LOD, the cost of ray casting remains constant once a certain number of triangles (0.5M) is reached:

![](../../assets/0f95312e850df5b6.jpg)


![](../../assets/0f95312e850df5b6.jpg)

Quoting the paper,

"by using LODs, significantly higher frame rates can be achieved with minimal loss of image quality, because ray traversals are less deep, intersections with voxels are implicit, and memory accesses are more coherent. Furthermore, the LOD framework can also reduce the amount of aliasing artifacts, especially in case of highly tesselated models."

"Our LOD metric could be also used for several types of secondary rays, including shadow, ambient occlusion, and planar reflection rays. One drawback of this kind of metric is that it works only with secondary rays expressible as linear transformations. Because of this, refraction and non-planar reflection rays are not supported."

- it makes heavy use of LOD for primary, shadow and GI rays which greatly reduces their tracing cost

- LOD is generated automatically by the voxel data structure

- nearby geometry is represented by triangles, so there isn't any voxel blockiness on close inspection

- characters and other dynamic geometry can still be represented as triangles and as such avoid the difficulties with animating voxels

- huge immensely detailed levels are possible thanks to the out-of-core streaming of the voxels and triangles

- it uses Monte Carlo GI, which scales very easily (number of bounces + number of samples per pixel) and can be filtered, while still giving accurate results

This is certainly something to keep an eye on!

## 2 comments:

http://voxelium.files.wordpress.com/2010/03/voxlod_paper.pdf


404 — File not found

look here: http://voxelium.tumblr.com/


simple google search

Post a Comment