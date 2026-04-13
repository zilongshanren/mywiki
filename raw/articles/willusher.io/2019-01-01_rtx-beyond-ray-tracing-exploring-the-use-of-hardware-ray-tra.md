---
title: 'RTX Beyond Ray Tracing: Exploring the Use of Hardware Ray Tracing Cores for
  Tet-Mesh Point Location'
url: https://www.willusher.io/publications/rtx-points/
published: '2019-01-01'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# RTX Beyond Ray Tracing: Exploring the Use of Hardware Ray Tracing Cores for Tet-Mesh Point Location

#### Ingo Wald, Will Usher, Nate Morrical, Laura Lediaev, and Valerio Pascucci

In *High Performance Graphics Short Papers*, 2019.

![](https://cdn.willusher.io/img/clMvtsl.webp)

**Fig. 1:**

*a-c) Illustrations of the tetrahedral mesh point location kernels evaluated in this paper. a) Our reference method builds a BVH over the tets and performs both BVH traversal and point-in-tet tests in software (black) using CUDA. b)*

`rtx-bvh`

uses an RTX-accelerated BVH over tets and triggers hardware BVH traversal (green) by tracing infinitesimal rays at the sample points, while still performing point-tet tests in software (black). c) `rtx-rep-faces`

and `rtx-shrd-faces`

use both hardware BVH traversal and triangle intersection (green) by tracing rays against the tetrahedras’ faces. d) An image from the unstructured-data volume ray marcher used to evaluate our point location kernels, showing the 35.7M tet Agulhas Current data set rendered interactively on an NVIDIA TITAN RTX (34FPS at 1024^2 pixels).## Abstract

We explore a first proof-of-concept example of creatively using the Turing generation’s hardware ray tracing cores to solve a problem other than classical ray tracing, specifically, point location in unstructured tetrahedral meshes. Starting with a CUDA reference method, we describe and evaluate three different approaches to reformulate this problem in a manner that allows it to be mapped to these new hardware units. Each variant replaces the simpler problem of point queries with the more complex one of ray queries; however, thanks to hardware acceleration, these approaches are actually faster than the reference method.

`@inproceedings{wald_rtx_2019, title = {{RTX} {Beyond} {Ray} {Tracing:} {Exploring} the {Use} of {Hardware} {Ray} {Tracing} {Cores} for {Tet}-{Mesh} {Point} {Location}}, booktitle = {High-Performance Graphics - Short Papers}, author = {Wald, Ingo and Usher, Will and Morrical, Nate and Lediaev, Laura and Pascucci, Valerio}, year = {2019}, DOI = {10.2312/hpg.20191189} }`