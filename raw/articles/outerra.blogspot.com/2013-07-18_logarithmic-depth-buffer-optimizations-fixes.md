---
title: Logarithmic depth buffer optimizations & fixes
url: https://outerra.blogspot.com/2013/07/logarithmic-depth-buffer-optimizations.html
author: Outerra
published: '2013-07-18'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

An updated

[logarithmic depth](http://outerra.blogspot.com/2009/08/logarithmic-z-buffer.html)equation (vertex shader):

//assuming gl_Position was already computed

gl_Position.z = log2(max(1e-6, 1.0 + gl_Position.w)) * Fcoef - 1.0;

Where Fcoef is a constant or uniform value computed as Fcoef = 2.0 / log2(farplane + 1.0).

Changes (compared to the

[initial version](http://outerra.blogspot.com/2009/08/logarithmic-z-buffer.html)):

**using log2 instead of log**: in shaders, log function is implemented using the log2 instruction, so it's better to use log2 directly, avoiding an extra multiply**clipping issues**: for values smaller than or equal to 0 the log function is undefined. In cases when one vertex of the triangle lies further behind the camera (≤ -1), this causes a rejection of the whole triangle even before the triangle is clipped.

Clamping the value via max(1e-6, 1.0 + gl_Position.w) solves the problem of disappearing long triangles crossing the camera plane.**no need to compute depth in camera space**: after multiplying with the modelview projection matrix, gl_Position.w component contains the positive depth into the scene, so the above equation is the only thing that has to be added after your normal modelview projection matrix multiply- Previously used "C" constant changing the precision distribution was removed, since the precision is normally much higher than necessary, and C=1 works well

To address the issue of the depth not being interpolated in perspectively-correct way, output the following interpolant from the vertex shader:

//out float flogz;

flogz = 1.0 + gl_Position.w;

and then in the fragment shader add:

gl_FragDepth = log2(flogz) * Fcoef_half;

where Fcoef_half = 0.5 * Fcoef

Note that writing fragment depth disables several depth buffer optimizations that may pose problems in scenes with high overdraw. The non-perspective interpolation isn't usually a problem when the geometry is tesselated finely enough, and in Outerra we are using the fragment depth writing only for objects, since the terrain is tesselated quite well.

## No comments:

Post a Comment