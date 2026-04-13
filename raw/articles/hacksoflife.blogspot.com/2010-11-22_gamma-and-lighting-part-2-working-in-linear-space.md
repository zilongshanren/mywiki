---
title: 'Gamma and Lighting Part 2: Working in Linear Space'
url: http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-2-working-in.html
author: Benjamin Supnik
published: '2010-11-22'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[previous post](http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-1-color-sync.html)I tried to describe the process of maintaining color sync. Two important things to note:

- Most color spaces that are reasonable for 24-bit framebuffers aren't linear. Twice the RGB means a lot more than twice the luminance.
- This is good from a data-size standpoint, because 8 bits for channel isn't enough to be linear.

[perform 3-d calculations to create computer-generated images](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch24.html)of light sources. Note that this is not an issue of monitor calibration or which gamma curve (Mac or PC) you use; no color space with any gamma is going to be even remotely close to linear luminance. So this is almost a 'wrong format' issue and not a 'wrong calibration' issue.

Consider: light is additive - if we add more photons, we get more light. This is at the heart of a computer graphics lighting model, where we sum the contribution of several lights to come up with a luminance for an RGB pixel. But remember the math from the previous post: doubling the RGB value more than doubles the luminance from your monitor.

In order to correctly create lighting effects, we need to:

- Convert from sRGB to linear color.
- Do the lighting accumulation in linear color space.
- Convert back to sRGB because that's the format the framebuffer needs.

Let the GPU Do It

The OpenGL extensions

[GL_EXT_texure_sRGB](http://www.opengl.org/registry/specs/EXT/texture_sRGB.txt)and

[GL_ARB_framebuffer_sRGB](http://www.opengl.org/registry/specs/ARB/framebuffer_sRGB.txt)basically do steps 1 and 3 for you; when you set a texture's internal type to sRGB, the GPU converts from sRGB to linear space during texel fetch. When framebuffer_sRGB is enabled, the GPU converts from linear back to sRGB before writing your fragment out to the framebuffer. Thus your shader runs in linear space (which is fine because it has floating point precision) while your textures and framebuffer are sRGB like they've always been.*

The advantage of using these extensions on DirectX 10 hardware is that the conversion happens before texture filtering and after framebuffer blending - two operations you couldn't "fix" manually in your shader. So you get linear blending too, which makes the blend of colors look correct.

Of course, your internal art asset format has to be sRGB in order for this to work, because it's the only color space the GL will convert from and back to.

* The question of whether your framebuffer is sRGB or linear is really more a question of naming convention. If you go back 10 years, you know a few things: writing RGB values into the framebuffer probably produces color on the monitor that is close to what you'd expect from sRGB, but the GL does all lighting math linearly. So it's really sRGB data being pushed through a linear pipeline, which is wrong and the source of lighting artifacts.

## No comments:

## Post a Comment