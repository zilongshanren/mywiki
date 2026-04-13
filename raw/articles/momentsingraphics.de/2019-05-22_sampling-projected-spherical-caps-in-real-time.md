---
title: Sampling Projected Spherical Caps in Real Time
url: http://momentsingraphics.de/I3D2019.html
published: '2019-05-22'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Sampling Projected Spherical Caps in Real Time

Christoph Peters, Carsten Dachsbacher.

2019–06 in *Proceedings of the ACM on Computer Graphics and Interactive Techniques (Proc. i3D)* 2, 1.

[Official version](https://doi.org/10.1145/3320282)

## Abstract

Stochastic shading with area lights requires methods to sample the light sources. For diffuse materials, the best strategy is to sample proportionally to projected solid angle. Recent work in offline rendering has addressed this problem for spherical light sources, but the solution is unsuitable for a GPU implementation. We present a far more efficient solution. It offers results without noteworthy noise for diffuse surfaces lit by an unoccluded spherical light source while being only two to three times more costly than simple sampling of the solid angle. The core insight of the technique is that a projected spherical cap can be decomposed into, or at least approximated by, cut disks. We present an efficient method to sample cut disks and show how to use it to sample projected spherical caps. In some cases, our method does not sample exactly proportionally to projected solid angle but the deviation is provably bounded.

**Keywords:** sampling, projected spherical caps, spherical light sources, area lights, diffuse shading, real-time shadows, ray traced soft shadows

## Images

![MagnifiedProjectedSolidAngleSampling1Sample](../../assets/8a8bcfbdf30e83a9.png)


![MagnifiedProjectedSolidAngleSampling1Sample](../../assets/8a8bcfbdf30e83a9.png)

![MagnifiedProjected1spp](../../assets/4e760daefc64cf8b.png)


![MagnifiedProjected1spp](../../assets/4e760daefc64cf8b.png)

![ProjectedSolidAngleOurs0.1](../../assets/6b17f04412cdfb9b.png)


![ProjectedSolidAngleOurs0.1](../../assets/6b17f04412cdfb9b.png)

## Notes

This work has been presented at the ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games 2019 on 22nd of May 2019. The author's version has been published on 28th of April 2019.

## Erratum

An error made its way into the pseudocode in the paper (both the official version and the author's version available here). The supplementary source code is (and has always been) correct.

- In Algorithms 2, 3 and 4, \(\frac{\pi}{2}\) should be subtracted from whatever is passed as first argument to
`SampleCutUnitDisk()`

.