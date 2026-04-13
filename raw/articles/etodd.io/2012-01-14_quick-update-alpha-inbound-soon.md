---
title: Quick update - Alpha inbound soon!
url: https://etodd.io/2012/01/14/quick-update-alpha-inbound-soon/
published: '2012-01-14'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Quick update - Alpha inbound soon!

This week was a lot of under the hood improvements. The voxel engine got a TON of performance optimizations, which allow my Nvidia GTX 260 to render my test scene at 100-200 FPS.

**Screenshots:**
![](../../assets/414a2fc5dcecbe74.jpg)


![](../../assets/60af4c78d475646f.jpg)


![](../../assets/3c0d294868537f6f.jpg)


![](../../assets/3ee49d834a26f0a6.jpg)


**New features:**

- Rough-draft tutorial level with instructions and whatnot.
- Fullscreen toggling on-the-fly by hitting F11
- Rudimentary fog effect

**Performance optimizations:**

- Voxels are now rendered as surfaces, rather than complete cubes. This lets me cull a lot of unnecessary geometry.
- Voxels are now split into chunks. This lets me easily implement frustum culling and view distance, which helps tremendously with shadow map rendering as well.
- I fixed some bugs in the voxel modification code, making voxel modifications of up to 100-150 cells practically instantaneous.
- Shadow maps and reflections are now rendered every other frame. It's a hack, but the important thing is that the gameplay is responsive.

My biggest development challenge was my battle with fullscreen toggling and graphics resource management. Switching from fullscreen to windowed mode, the entire XNA GraphicsDevice is invalidated, along with every vertex buffer, texture, shader, everything. So that was interesting.

Just a quick update this time. Expect a playable alpha soon! Very soon!