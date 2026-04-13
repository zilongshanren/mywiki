---
title: 'Gamma and Lighting Part 3: Errata'
url: http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-3-errata.html
author: Benjamin Supnik
published: '2010-11-22'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[linear space](http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-2-working-in.html)...

Light Accumulation

In order to get correct lighting, lights need to be accumulated (that is, the contribution of each light to any given pixel) in linear space. There are three ways to do this safely:

Accumulate all lights in a single pass. The sum happens in your shader (which must calculate each light's contribution and add them). This is typical of a traditional one-pass forward renderer, and is straight forward to convert to linear space. The lighting calculation is done linearly in shader, converted to something with gamma, then written to an 8-bit framebuffer.

Clamping and exposure control are up to you and can happen in-shader while you are in floating point.

Multi-pass with sRGB_framebuffer. If you want to accumulate lights by blending (e.g. using blending to add more "light" into the framebuffer and your framebuffer is 24-bit RGB, you'll need the sRGB_framebuffer extension. This will cause OpenGL to not only accept linear fragments from you, but the blending addition will happen in linear space too.

In this case, exposure control is tricky; you don't want to saturate your framebuffer, but no one lighting pass knows the total exposure. You'll have to set your exposure so that the conversion to sRGB doesn't "clip".

Multi-pass with an HDR framebuffer. The other option for accumulating light by blending is to use a floating point framebuffer. This configuration (like mutli-pass with sRGB) might be typical of a deferred renderer (or a stencil-shadow-volume solution).

Unlike sRGB into a 24-bit framebuffer, this case doesn't have a clipping problem, because you can write linear vlaues into the floating point framebuffer. You do need to "mix down" the floating point framebuffer back to sRGB later.


What Color Space Is The Mac Framebuffer?

On OS X 10.5 and older, your framebuffer will have the color profile of the device, at least as far as I can tell. This probably means that the effective gamma is 1.8 (since the OS's color management should adjust the LUT enough to achieve this net result).

On OS X 10.6 every window has its own color profile, and the window manager color-converts as needed to get correct output on multiple devices. Edit: By default you get the monitor's default color profile, but you can use HIWindowSetColorSpace to change what color profile you work in.

## No comments:

## Post a Comment