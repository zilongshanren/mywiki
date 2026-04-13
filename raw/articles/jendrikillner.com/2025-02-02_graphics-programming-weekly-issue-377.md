---
title: Graphics Programming Weekly - Issue 377
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-377/
author: Jendrik Illner
published: '2025-02-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the detailed article provides an overview of the implementation of the Goo-like in “The Gunk”
- explains the underlying voxel-based implementation, how it’s represented and interacts with gameplay
- describes how it’s authored and rendered integrated into UE
- additionally presents how the effect is rendered using a ray-marching-based approach

![](../../assets/7d99b7c21c5c3f5f.png)


- the sample is part of Nvidia RTX Mega Geometry and presents how to use a continuous Level of detail through mesh clustering
- presents how to rasterize using mesh shaders and use the new VK_NV_cluster_acceleration_structure for raytracing
- provided documentation provides a detailed walkthrough of the sample code and the underlying implementation

![](../../assets/567a9eda72fe1ab0.jpg)


- the blog post provides an overview of the latest released features in the D3D12 Agility SDK update
- the SDK introduces Shader hash bypass, reduced alignment requirements for buffers, as well as the recreation of resources at specific virtual addresses
- as well as shared links to updates to the d3d12 video encoding functionality

![](../../assets/5927062cfe69a41c.png)


- continuation of custom lighting model using Unreal and Unity
- this part covers Phong, Blinn formula, as well as Half Lambert, diffuse
- implementation is shown using visual shader language

![](../../assets/30d2751c30bd5fa2.png)


- the blog post presents new features for D3D12 video encoding
- allows developers to provide additional hints (such as motion vectors or dirty rectangles) to speed up the encoder processing
- also now allows frames to be split into sub-regions with individual progress tracking and data access control

![](../../assets/9ee52bf8f4eb317b.png)


- first, experimental support for Cooperative vectors has been added to Slang
- the blog post explains the features and presents two examples of how to use it
- additionally provides a link to the SPIR-V extension

![](../../assets/1a28098a6ccce436.png)


- Nvidia open-sourced a mesh processing library that allows meshes to be split into meshlets and calculate LOD cluster that allows for continues LODs
- documentation explains the API, how the implementation approaches the decimation and split steps
- additionally, explain the limitations (there are a number of them at this time)

![](../../assets/e7c82afeb33ae773.jpg)

Thanks to [Angel Ortiz](https://x.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.