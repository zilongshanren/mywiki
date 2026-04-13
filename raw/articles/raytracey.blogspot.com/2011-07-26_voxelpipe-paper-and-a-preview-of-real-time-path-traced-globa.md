---
title: VoxelPipe paper and a preview of real-time path traced global illumination
url: http://raytracey.blogspot.com/2011/07/voxelpipe-paper-and-preview-of-real.html
author: Sam Lapere
published: '2011-07-26'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just read Nvidia's HPG 2011 paper

["VoxelPipe: A Programmable Pipeline for 3D Voxelization"](http://research.nvidia.com/publication/voxelpipe-programmable-pipeline-3d-voxelization)by Jacopo Pantaleoni. One thing that immediately caught attention was the preview of a real-time global illumination system, in which primary rays are traced against the regular triangle version of the scene, but secondary incoherent rays are traced against a voxelized version of the scene which is much more efficient intersection-wise. Scene voxelization is performed every frame (it takes only a few milliseconds even for multi-million triangle scenes), so this allows for completely dynamic scenes with (path traced) global illumination in real-time. From the paper:"Finally, in Figure 5 we show a proof of concept of a real-time global illumination system that we plan to disclose in the near future. The system relies on our voxelization pipeline to create a proxy of the scene geometry that is used to trace incoherent rays. The proxy is rebuilt every frame, allowing support of fully dynamic geometry, materials and lighting."

Combined with previous work from Pantaleoni on

## No comments:

Post a Comment