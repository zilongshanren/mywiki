---
title: Permutation Coding for Vertex-Blend Attribute Compression
url: http://momentsingraphics.de/I3D2022.html
published: '2022-05-03'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Permutation Coding for Vertex-Blend Attribute Compression

Christoph Peters, Bastian Kuth, Quirin Meyer.

2022–05 in *Proceedings of the ACM on Computer Graphics and Interactive Techniques (Proc. i3D)* 5, 1.

[Official version](https://doi.org/10.1145/3522607)

## Abstract

Compression of vertex attributes is crucial to keep bandwidth requirements in real-time rendering low. We present a method that encodes any given number of blend attributes for skinning at a fixed bit rate while keeping the worst-case error small. Our method exploits that the blend weights are sorted. With this knowledge, no information is lost when the weights get shuffled. Our permutation coding thus encodes additional data, e.g. about bone indices, into the order of the weights. We also transform the weights linearly to ensure full coverage of the representable domain. Through a thorough error analysis, we arrive at a nearly optimal quantization scheme. Our method is fast enough to decode blend attributes in a vertex shader and also to encode them at runtime, e.g. in a compute shader. Our open source implementation supports up to 13 weights in up to 64 bits.

**Keywords:** skinning, linear vertex blend animation, vertex buffer compression, vertex blend attribute compression, permutation coding, bone weights, bone indices, simplex, tetrahedron

## Images

![shuffled](../../assets/7e02719e8136f743.png)


![shuffled](../../assets/7e02719e8136f743.png)

![benchmark_scene](../../assets/c409cf904760e127.png)


![benchmark_scene](../../assets/c409cf904760e127.png)

## Notes

This work has been presented at the ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games 2022 on May 3 2022. The author's version has been published on April 15 2022. It won the best paper award (tied with one other paper).