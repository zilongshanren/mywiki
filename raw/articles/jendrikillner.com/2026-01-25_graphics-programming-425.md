---
title: Graphics Programming 425
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-425/
author: Jendrik Illner
published: '2026-01-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents the Vulkan Roadmap 2026 milestone, which requires features such as variable-rate shading, shader clock queries, and higher descriptor limits
- announces the VK_EXT_descriptor_heap extension, which exposes direct access to descriptor memory while retaining compatibility with existing descriptor sets

![](../../assets/6d7d7b3cac66e355.jpg)


- explains ordered dithering using threshold maps (Bayer matrices) to convert grayscale images into black-and-white patterns
- compares threshold-map families (Bayer, cluster-dot, and void-and-cluster/blue-noise) and their characteristic visual textures
- shows how matrix size affects smoothness and previews the next part on error-diffusion dithering

![](../../assets/4a0f00f510e97467.png)


- presents a system for adding reflections in the Block Game by rendering a back-facing view and applying it via spherized matcaps
- uses reflected rays in view space instead of surface normals to correctly sample the environment map
- implements stochastic blue noise blur for roughness effects and discusses limitations

![](../../assets/75a41b98199f600e.png)


- demonstrates using the Terrain Texture Node in Unity’s Shader Graph to import terrain-system parameters for material layer settings
- shows how to adjust layer properties (color tint, opacity, etc.) and notes practical Inspector/HDRP quirks

![](../../assets/19afe534f34eea3d.png)


- covers practical challenges of using Marching Cubes at scale (performance, mesh transitions, LOD) in large games
- discusses integration strategies (e.g., Transvoxel, streaming meshes) and common pitfalls for scalability
- includes demos, time-coded chapters, and links to implementation resources for further reading

![](../../assets/0b7822c3141d0a19.png)


- presents sphere-based particle collision detection and response, with practical code examples and a demo
- explains momentum, kinetic energy, collision types, and coefficient of restitution, including a 1D→3D generalization

![](../../assets/fd95598e7bd16c50.png)

Thanks to [Nathan Reed](https://www.reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.