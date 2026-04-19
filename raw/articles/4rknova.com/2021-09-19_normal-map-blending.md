---
title: Normal Map Blending
url: https://www.4rknova.com/blog/2021/09/19/normal-blending
author: Nikolaos Papadopoulos
published: '2021-09-19'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

Blending of normal maps has been used extensively in computer graphics to break repetition patterns, add granularity to surfaces, and achieve a more realistic look. Examples of that are:

- Adding micro detail when rendering sea waves
- Simulating skin wrinkles
- Transitioning smoothly between different materials

When creating game assets, it’s common practice to use layer blending in image editing tools such as Photoshop to achieve this effect, however the issue with this approach is that the result is skewed towards the (0, 0, 1) vector, resulting in surfaces that look flat [2].

# Techniques

Many different techniques have been used in the past to blend normal maps. Some of the most popular ones are:

- Linear blending
- Overlay blending
- Partial derivative blending
- Whiteout blending
[[3]](https://www.4rknova.com#REF-3) - UDN method
- Unity’s method
[[5]](https://www.4rknova.com#REF-5) - Reoriented Normal Mapping (RNM)
[[1]](https://www.4rknova.com#REF-1) - RNM PD approximation
[[4]](https://www.4rknova.com#REF-4)

Stephen Hill wrote an excellent [blog post](https://blog.selfshadow.com/publications/blending-in-detail/) on this topic, with a detailed breakdown of multiple techniques. In this blog post, he also introduces a novel approach called *Reoriented Normal Mapping* which addresses the issue described above.

# Reoriented Normal Mapping (RNM)

RNM essentially reorients the secondary “detail” normal to follow the orientation of the base normal, which is an intuitive way to combine the two vectors. Stephen Hill’s technique achieves this transform using the shortest arc quaternion. Please visit his [blog post](https://blog.selfshadow.com/publications/blending-in-detail/) for a more detailed description of the math behind this.

Here’s an implementation of RNM for unpacked normals n1, n2 [1].

```
float3 RNM(float3 n1, float3 n2)
{
n1 += float3( 0, 0, 1);
n2 *= float3(-1, -1, 1);
return n1 * dot(n1, n2) / n1.z - n2;
}
```