---
title: Towards Practical Meshlet Compression
url: https://anteru.net/research/towards-practical-meshlet-compression
published: '2025-02-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

We propose a codec specifically designed for meshlet compression, optimized for rapid data-parallel GPU decompression within
a mesh shader. Our compression strategy orders triangles in optimal generalized triangle strips (GTSs), which we generate by
formulating the creation as a mixed integer linear program (MILP). Our method achieves index buffer compression rates of
16:1 compared to the vertex pipeline and crack-free vertex attribute quantization based on user preference. The 15.5 million
triangles of our teaser image decompress and render in 0.59 ms on an AMD Radeon RX 7900 XTX