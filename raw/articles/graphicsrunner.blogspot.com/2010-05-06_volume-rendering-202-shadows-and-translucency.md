---
title: 'Volume Rendering 202: Shadows and Translucency'
url: http://graphicsrunner.blogspot.com/2010/05/volume-rendering-202-shadows-and.html
author: Kyle Hayward
published: '2010-05-06'
source_blog: Graphics Runner
source_site: http://graphicsrunner.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Last time I left you with some basic optimizations, one being a pseudo-empty space skipping. But as I noted, the volumes needed to be sorted in order for it to work completely. We sort the sub-volumes back to front with respect to distance to the camera. This insures that we have a smooth framerate no matter what angle the camera is at. A speedup we can do here is to only sort the volumes if the camera has moved 45 degrees since we last sorted.

So now our subvolumes are sorted w.r.t. the camera. But we have alpha blending artifacts because depending on the view, the pixels of the subvolumes are not drawn in the correct order. What we can do to fix this is to draw a depth only pass, and ensure that we only draw pixels that will contribute to the final image.

![alpha_errors alpha_errors](../../assets/afbd70e9b2d5344a.img)


![no_alpha_errors no_alpha_errors](../../assets/c978916facb3a61a.img)


Left: no depth prepass. Right: depth prepass

**Translucency**

The first sample includes an approximated translucency. It is far from realistic, but it gives fairly good results. The idea is very similar to depth mapping, compare the current pixels depth to that of the depth map, and either use this value to look up into a texture or perform an exponential falloff in the shader (the sample does the latter).

![translucency translucency](../../assets/8d1db7f297300cba.img)


**Shadows**

There isn’t much to say here. The sample below uses variance shadow mapping.


![shadow0 shadow0](../../assets/111656e1b6448b75.img)

![shadow1 shadow1](../../assets/c730de768908bee2.img)


Well, there it is. Anticlimactic wasn't it?

## 6 comments:

Hey, this is great stuff! Thanks for putting it up!

Really cool tutorials.


They`re a bit tricky to get running on ATI hardware, though :(

Hi there!



I hope you don't mind a few very basic questions.. I'm not a programmer, I'm a theoretical physicist with game development as a hobby :)

Anyway, here goes: I've read the usual real time algorithms for atmosphere simulation (rayleigh scattering and all) and was curious to know whether these volume rendering techniques could be useful to have a more flexible atmosphere rendering, even if it has to be very low resolution to be rendered in real time. By 'more flexible' I mean it could be used to generate different atmospheres, with varying densities etc.

Yes you could certainly use volume rendering to simulate non-uniform atmospheric densities. I could see a 32^3 or 64^3 density volume being able to ray-casted at high frame rates in conjunction with a atmospheric model.

Cool, thanks for the insight :) I feel motivated enough to learn how to make a simple Optix application! (or try to)

Hi,


Very

veryinteresting stuff, your ray casting blogs! Having difficulties running 202 with Visual Studio 2012 though (I'm a DirectX and C++ Builder guy). Any chance for a Studio 2012 compatible project?Post a Comment