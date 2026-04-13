---
title: Running Out of Derivative Res
url: http://hacksoflife.blogspot.com/2010/02/running-out-of-derivative-res.html
author: Benjamin Supnik
published: '2010-02-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[went over the math](http://hacksoflife.blogspot.com/2009/11/per-pixel-tangent-space-normal-mapping.html)behind generating the coordinate system for normal mapping in a pixel shader, which allows you to use tangent space bump mapping without encoding coordinate axes on your vertex mesh. (In X-Plane we do this so that we can allow authors to add bump maps to "unmodified" meshes.)

One of the problems with writing shaders is that it can be write-once, debug everywhere. As it turns out, this technique has a problem that I can repro on a GF8800 but not HD4870. On the 8800, I run out of precision in my derivative (dFdx and dFdy) functions.

In the scene in question, the UV map is generated in the vertex shader via projection off the world-space input vertices and the input mesh is big - 300 x 300 km in fact. (It is of course the base terrain.)

This means that the UV coordinates are pretty big too, particularly for highly scaled up textures. And that means that the effective resolution limit of the

*texture coordinates*may be larger than one pixel.

When this happens, the result is a derivative that will be inconsistent across pixels, and the basis for the bump map will be corrupted on a per-pixel level.

Work-arounds? I can think of two:

- Modify the texture coordinate generation system to produce higher precision UV maps.
- Modify the shader to generate basis vectors from the projection parameters (rather than by "sampling" via the UV map) in the texture coordinate generation case.

## No comments:

## Post a Comment