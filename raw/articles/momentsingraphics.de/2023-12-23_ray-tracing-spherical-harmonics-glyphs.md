---
title: Ray Tracing Spherical Harmonics Glyphs
url: http://momentsingraphics.de/VMV2023.html
published: '2023-12-23'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Ray Tracing Spherical Harmonics Glyphs

Christoph Peters, Tark Patel, Will Usher, Chris R. Johnson.

2023–09 in *Vision, Modeling, and Visualization*. The Eurographics Association.

[Official version](https://doi.org/10.2312/vmv.20231223)

## Abstract

Spherical harmonics glyphs are an established way to visualize high angular resolution diffusion imaging data. Starting from a unit sphere, each point on the surface is scaled according to the value of a linear combination of spherical harmonics basis functions. The resulting glyph visualizes an orientation distribution function. We present an efficient method to render these glyphs using ray tracing. Our method constructs a polynomial whose roots correspond to ray-glyph intersections. This polynomial has degree 2k+2 for spherical harmonics bands 0,2,...,k. We then find all intersections in an efficient and numerically stable fashion through polynomial root finding. Our formulation also gives rise to a simple formula for normal vectors of the glyph. Additionally, we compute a nearly exact axis-aligned bounding box to make ray tracing of these glyphs even more efficient. Since our method finds all intersections for arbitrary rays, it lets us perform sophisticated shading and uncertainty visualization. Compared to prior work, it is faster, more flexible and more accurate.

## Images

![glyph](../../assets/8bdf53b053de2bf7.webp)


![glyph](../../assets/8bdf53b053de2bf7.webp)

## Notes

This work has been presented orally at VMV 2023 on September 27th 2023. It won an honorable mention award, i.e. a jury judged it to be among the best three papers (out of 26) at VMV 2023. The paper has been published on September 26th 2023.