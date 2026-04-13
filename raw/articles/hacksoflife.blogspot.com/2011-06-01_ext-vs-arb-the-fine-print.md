---
title: EXT vs ARB - The Fine Print
url: http://hacksoflife.blogspot.com/2011/06/ext-vs-arb-fine-print.html
author: Benjamin Supnik
published: '2011-06-01'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I thought I had found a driver bug: my ATI card on Linux rejecting a G-Buffer with a mix of RGBA8 and RG16F surfaces. I know the rules: DX10-class cards need the same bit plane width for all MRT surfaces.


I had good reason to think driver bug: the nappy old drivers I got from Ubuntu 10.04 showed absolutely no shadows at all, weird flicker, incorrect shadow map generation - and cleaning them out and grabbing the 11-5 Catalyst drivers fixed it.


Well, when the drivers don't work, there's always another explanation: an idiot app developer who doesn't know what his own app does. In that guy's defense, maybe the app is large and complex and has distinct modules that sometimes interact in surprising ways.


In my case, the ATI drivers follow the rules: the "EXT" variant of the framebuffer extension: an incomplete format error is returned if the color attachments aren't all of the same internal type. This was relaxed in the "ARB" variant, which gives you more MRT flexibility.


What amazes me is that the driver cares! The driver actually tracks which entry point I use and changes the rules for the FBO based on how I got in. Lord knows what would happen if I mixed and matched entry points. I feel bad for the poor driver writers for having to add the complexity to their code to manage this correctness.

## No comments:

## Post a Comment