---
title: Ray Tracing Spherical Harmonics Glyphs
url: https://www.willusher.io/publications/rt-sph-glyphs/
published: '2023-12-23'
source_blog: Will Usher's Blog
source_site: https://www.willusher.io/
category: game programming
fetched: '2026-04-13'
---

# Ray Tracing Spherical Harmonics Glyphs

#### Christoph Peters, Tark Patel, Will Usher, and Chris R. Johnson

In *International Symposium on Vision, Modeling and Visualization (VMV)*, 2023.
*Honorable Mention*

![](https://cdn.willusher.io/img/peters-2023-glyphs-teaser.webp)

**Fig. 1:**

*Left: We render spherical harmonics glyphs using an efficient and accurate method based on polynomial root finding. A second glyph visualizes uncertainty and we trace secondary rays to render soft shadows. Right: Our method renders large HARDI datasets in real time on a single GPU.*

## Abstract

Spherical harmonics glyphs are an established way to visualize high angular resolution diffusion imaging data. Starting from a unit sphere, each point on the surface is scaled according to the value of a linear combination of spherical harmonics basis functions. The resulting glyph visualizes an orientation distribution function. We present an efficient method to render these glyphs using ray tracing. Our method constructs a polynomial whose roots correspond to ray-glyph intersections. This polynomial has degree 2k+2 for spherical harmonics bands 0,2,…,k. We then find all intersections in an efficient and numerically stable fashion through polynomial root finding. Our formulation also gives rise to a simple formula for normal vectors of the glyph. Additionally, we compute a nearly exact axis-aligned bounding box to make ray tracing of these glyphs even more efficient. Since our method finds all intersections for arbitrary rays, it lets us perform sophisticated shading and uncertainty visualization. Compared to prior work, it is faster, more flexible and more accurate.

`@inproceedings{peters_rtglyphs_23, booktitle = {International Symposium on Vision, Modeling, and Visualization (VMV)}, title = {{Ray} {Tracing} {Spherical} {Harmonics} {Glyphs}}, author = {Peters, Christoph and Patel, Tark and Usher, Will and Johnson, Chris R.}, year = {2023}, doi = {10.2312/vmv.20231223}, }`