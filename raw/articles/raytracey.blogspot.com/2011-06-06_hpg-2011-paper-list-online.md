---
title: HPG 2011 paper list online
url: http://raytracey.blogspot.com/2011/06/hpg-2011-paper-list-online.html
author: Sam Lapere
published: '2011-06-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The


These are some of the more juicy titles on the subject of ray tracing and path tracing that immediately catch the attention:


[Real-Time Rendering blog](http://www.realtimerendering.com/blog/)just blogged that Kesen Huang has put the list of papers for the High Performance Graphics 2011 symposium online at[http://kesen.realtimerendering.com/hpg2011Papers.htm](http://kesen.realtimerendering.com/hpg2011Papers.htm). HPG 2011 takes place in Vancouver (home of the Canucks ;) on Aug 5-7.These are some of the more juicy titles on the subject of ray tracing and path tracing that immediately catch the attention:

**Simpler and Faster HLBVH with Work Queues**(Kirill Garanzha, Jacopo Pantaleoni, David McAllister) I've been waiting an eternity for Pantaleoni's[HLBVH code](http://code.google.com/p/hlbvh/)to be open sourced, so I hope the code from this new paper will get published eventually.

**Improving SIMD Efficiency for Parallel Monte Carlo Light Transport on the GPU**(Dietger van Antwerpen) This paper is from the co-developer of the real-time path tracer called Brigade, who also implemented Metropolis light transport and ERPT on the GPU, so it should be really interesting.

**Active Thread Compaction for GPU Path Tracing**(Ingo Wald) From the guy that pioneered real-time CPU ray tracing.

Some other attention-grabbing titles:


**Real-Time Diffuse Global Illumination Using Radiance Hints**(Georgios Papaioannou)

**VoxelPipe: A Programmable Pipeline for 3D Voxelization**(Jacopo Pantaleoni)

**High-Performance Software Rasterization on GPUs**(Samuli Laine, Tero Karras)

**MSBVH: An Efficient Acceleration Data Structure for Ray Traced Motion Blur**(Leonhard, Gruenschloss, Martin Stich, Sehera Nawaz, Alexander Keller)

The program looks very promising so far, especially for real-time and interactive ray tracing and path tracing.


UPDATE:


The paper by McGuire et al. on the






UPDATE:

The paper by McGuire et al. on the

[Alchemy Screen Space Ambient Obscurance Algorithm](http://graphics.cs.williams.edu/papers/AlchemyHPG11/VV11AlchemyAO.pdf)contains a pretty neat idea, which could prove to be very useful for real-time path tracing. The idea is to adapt the number of samples per pixel with distance from the camera, essentially some kind of LOD scheme for the spp number as shown in this picture (taken from the

[paper](http://graphics.cs.williams.edu/papers/AlchemyHPG11/VV11AlchemyAO.pdf)):

![](../../assets/cec91b6bba3f0fbe.png)

![](../../assets/cec91b6bba3f0fbe.png)

## No comments:

Post a Comment