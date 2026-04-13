---
title: How To Change Your UV Map on the Fly
url: http://hacksoflife.blogspot.com/2010/02/how-to-change-your-uv-map-on-fly.html
author: Benjamin Supnik
published: '2010-02-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

- You can make your textures look less repetitive without making meshes more complex.
- Since the effect is in-shader, it can be turned off on lower end machines - scalability!

Huh?!?!

In order to understand why this is necessary, you first have to understand how the hardware selects a mipmap level, and to understand that you have to understand how OpenGL generates derivatives.

First the derivatives. Most of the video cards I know about generate derivatives of a shader variable by "cross-differencing" - that is, a 2x2 block of pixels is run using the same shader, and when the shader hardware gets to the derivative (dFdx, and dYdx) it simply subtracts the interim values from the four pixels to find how much they "change" in the box. In other words, the derivative function in GLSL works by discreet per-pixel sampling.

(BTW this is why when you screw up code that needs to treat derivatives carefully, often you'll get 2x2 pixel artifacts.)

These derivatives allow the graphics card to select a LOD. At the sight of a texture fetch, the card can do a derivative operation on the input texture coordinates and see how fast they change per pixel. The faster they change, the lower the effective texture res and the lower LOD mip-map we need. That is how the card "knows" to use the lower mip-maps even when you use expressions for your texture coordinates - the derivative is taken on the entire expression.

But...what happens when you have a discontinuity in your UV map? Take a simple case like "fract". If you "fract" a wrapping texture, you will quite possibly see an artifact at the edges. This is because, right at the edge, the rate of change of the UV map is

*much*higher than before, as it "jumps" from one edge of the texture to the other. High rate of change = low LOD - the graphics card goes and selects the lowest level LOD it has!

(If you don't know what's in your lowest mip, you might not know where the color was coming from.)

The solution is

[here](http://www.opengl.org/registry/specs/ARB/shader_texture_lod.txt): texture2DGradARB. This function lets you separately specify the texture coordinates and the derivatives. Here's a simple example. Imagine you have this:

vec2 uv_swizzled = fract(uv);That example will create a few pixels of low-mipmap texture at the discontinuity (where the texture goes from 1 back to 0). To use texture2DGradARB, you do this:

vec4 rgba = texture2D(my_tex, uv_swizzled);

vec2 uv_swizzled = fract(uv);By using the original (continuous) texture coordinates for the derivative, but the modified ones for the fetch, you can have discontinuous fetches with no LOD artifacts.

vec4 rgba = texture2DGradARB(my_tex,uv_swizzled,dFdx(uv),dFdy(uv));

NVidia and ATI cards don't respond the same way to discontinuous coordinates, but both will produce artifacts, and both are right to do so.

One last note. From the shader texture LOD extension:

Mipmap texture fetches and anisotropic texture fetchesI can tell you from experience that a number of my artifacts have come from conditional code flow. I believe that by non-uniform control flow they mean the case where the shader branches are not all taken the same way for a 2x2 block, but I am not sure.

require an implicit derivatives to calculate rho, lambda

and/or the line of anisotropy. These implicit derivatives

will be undefined for texture fetches occuring inside

non-uniform control flow or for vertex shader texture

fetches, resulting in undefined texels.

This was discussed in the OpenGL pipeline newsletter from 2006

ReplyDeletehttp://www.opengl.org/pipeline/article/vol001_5/