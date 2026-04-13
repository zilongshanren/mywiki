---
title: Alpha Blending, Back To Front, Front To Back
url: http://hacksoflife.blogspot.com/2010/02/alpha-blending-back-to-front-front-to.html
author: Benjamin Supnik
published: '2010-02-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[smoke particles](http://developer.download.nvidia.com/compute/cuda/sdk/website/projects/smokeParticles/doc/smokeParticles.pdf)and came across the notion of front-to-back blending. The idea is to change OpenGL's blend equation so that you can start at the front and blend in behind translucent geometry.

To blend front to back, you must have a destination surface that has an alpha channel, because the surface alpha channel remembers how much the next layer "shows through' the closer layer already put down.

To render front to back, we need to do three unusual things:

- Init our background to all black, all translucent (0,0,0,0).
- We set a blend function of GL_ONE_MINUS_DST_ALPHA, GL_ONE. This means that the new layer is dimmed to be the remainder of the opacity already put down.
- We need to pre-multiply our fragment's RGB by its alpha, because this isn't being done by the alpha blender anymore.

One down side of front to back is that we can't use it on top of an existing scene unless the existing scene has an alpha channel that is set to clear. (This is usually not what you'd find after rendering.)

**Compositing**

If you then want to put the front-to-back mixed layers on top of another layer, you need to use a blend function of GL_ONE, GL_ONE_MINUS_SRC_ALPHA. Why? Well, since we rendered over black, our mix is "pre-multiplied" by its alpha value - that is, more transparent areas are darker. So we disable the alpha multiply.

**Back To Front Revisited**

If we render back to front, we can use GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, and not premultiply in shader. There's just one problem: alpha poke-through. Basically if you layer four polygons on top of each other, each with 50% opacity, the end result will be very close to 50% opacity, but the correct result should be 1-0.5^4, or 93.75% opaque. So with "standard" back-to-front opacity we can't later blit our accumulated texture.

It turns out we can work around this with some GL voodoo:

- Init the background to black opaque (0,0,0,1).
- Set the blend function to GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA for color but use GL_ZERO, GL_ONE_MINUS_SRC_ALPHA for the alpha coefficients. This requires glBlendFunctionSeparate and GL 1.4.
- When it comes time to mix down, use GL_ONE, GL_SRC_ALPHA

Here's what's going on: we need to use multiplication to "accumulate" opacity. But since multiplication tends to move colors toward zero, and zero is transparent, multiplying our fragments alpha together tends to make things more transparent. So this scheme is based on treating 1.0 as transparent and 0.0 as opaque. Let's review those steps:

- Since 1 is now transparent, we init our buffer to alpha=1 for transparency.
- By using alpha coefficients of GL_ZERO, GL_ONE_MINUS_SRC_ALPHA, we are multiplying the destination alpha by the source alpha. So here we have our "multiplying" to build up opacity. By using GL_ONE_MINUS_SRC_ALPHA we invert our alpha - the fragment outputs 0 = transparent and this converts it to 1 = transparent. The existing alpha in the framebuffer is already inverted.
- When we go to actually composite, we use GL_SRC_ALPHA instead of GL_ONE_MINUS_SRC_ALPHA because our source alpha is already inverted. (The source factor is GL_ONE because, like all pre-made blend mixes, we are pre-multiplied.)

## No comments:

## Post a Comment