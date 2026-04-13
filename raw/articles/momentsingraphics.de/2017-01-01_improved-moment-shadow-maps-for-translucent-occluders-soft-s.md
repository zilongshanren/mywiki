---
title: Improved Moment Shadow Maps for Translucent Occluders, Soft Shadows and Single
  Scattering
url: http://momentsingraphics.de/JCGT2017.html
published: '2017-01-01'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Improved Moment Shadow Maps for Translucent Occluders, Soft Shadows and Single Scattering

Christoph Peters, Cedrick Münstermann, Nico Wetzstein, Reinhard Klein.

2017–03 in *Journal of Computer Graphics Techniques (JCGT)* 6, 1.

[Official version](http://jcgt.org/published/0006/01/03/)

## Abstract

Like variance shadow maps, the recently proposed moment shadow maps can be filtered directly but they provide a substantially higher quality. We combine them with earlier approaches to enable three new applications. Shadows for translucent occluders are obtained by simply rendering to a moment shadow map with alpha blending. Soft shadows in the spirit of percentage-closer soft shadows are rendered using two queries to a summed-area table of a moment shadow map. Single scattering is rendered through one lookup per pixel in a prefiltered moment shadow map with six channels. As a foundation we also propose improvements to moment shadow mapping itself. All these techniques scale particularly well to high output resolutions and enable proper antialiasing of shadows through extensive filtering.

**Keywords:** filterable shadow maps, moment shadow mapping, participating media, real-time rendering, real-time shadows, single scattering, prefiltered single scattering, god rays, soft shadows, contact-hardening shadows, moment soft shadow mapping, translucent occluders, implementation, shader code

## Note

This paper is an extended version of the earlier [i3D 2016 paper](http://momentsingraphics.de/I3D2016.html) with various improvements to the techniques and a more detailed discussion of implementation details as well as additional comparisons.

## Links

All downloads related to this paper are freely available at the [Journal of Computer Graphics Techniques](http://www.jcgt.org/published/0006/01/03/). More information is available in [this blog post](http://momentsingraphics.de/JCGTAnnouncement.html).