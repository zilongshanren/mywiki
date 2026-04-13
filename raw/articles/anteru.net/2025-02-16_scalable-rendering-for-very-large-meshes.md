---
title: Scalable rendering for very large meshes
url: https://anteru.net/research/scalable-rendering-for-very-large-meshes
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Debug view showing a mesh displayed using the technique from another view angle. The primary camera is looking from the top right onto the mesh. The rendering algorithm automatically adjust level-of-detail and removes invisible geometry.

In this paper, we present a novel approach for rendering of very large polygonal meshes consisting of several hundred million triangles. Our technique uses the rasterizer exclusively to allow for high-quality, anti-aliased rendering and takes advantage of a compact, voxel-based level-of-detail simplification. We show how our approach unifies streaming, occlusion culling, and level-of-detail into a single rasterization based pipeline. We also demonstrate how our level-of-detail simplification can be quickly computed, even for the most complex polygonal meshes.