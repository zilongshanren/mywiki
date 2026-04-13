---
title: Order and types of depth testing
url: https://interplayoflight.wordpress.com/2013/01/17/depth_testing/
author: Kostas Anagnostou
published: '2013-01-17'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Some time ago I did a bit of research to gather some info about the state of depth testing in D3D11 and what new features are supported. I am summarising my findings here as well in case someone finds them useful.

Depth testing by default happens after pixel shading. The aim of the depth testing was originally just to do correct z-sorting while blending the shaded pixel colour with the backbuffer. The Direct3D and OpenGL specifications dictate this even to this day. With the fixed function pipeline the cost of shading a pixel was small and no one cared to avoid it, even if that meant discarding it later.

Later on, with the programmable pixel shaders, the cost of shading a pixel went up and we wanted to avoid it if possible. The original (Z-sorting) depth test still happens after the pixel shader though! Enter “Early-Z” and “Hierarchical Z”.

These two methods take place before the pixel shader is executed and their aim is to discard pixels that will fail the depth test before shading them. The Early-Z test is performed at pixel level while the Hierarchical Z works on blocks of pixels maintaining a coarse approximation of the depth buffer. “Early-Z” is on by default, so in reality no pixel that will fail the depth test is actually shaded. The Early-Z is deactivated though for pixel shaders that output Depth (as we do when rendering depth sprites for example), or use alpha testing and alpha to coverage. Also, it seems that “Early-Z” is deactivated for pixel shaders that write to Unordered Access Views (i.e. write to arrays and not to a rendertarget). (Note: “Early-Z” and “Hierarchical Z” exist on pre D3D11 GPUs as well, it is not a recent feature of graphics cards).

So, if we want to use Early-Z with pixel shaders that output depth there is an option called “Conservative Depth” in D3D11 (and OpenGL as well) that allows us to output depth using the SV_DepthGreater/LessEqual pixel shader outputs. If we want to use Early-Z with pixel shaders that write to UAVs, there is the [earlydepthstencil] directive (placed above the pixel shader code) that will force the GPU to use the depth test before executing the shader.

For more in-depth information on how depth testing (and the GPU in general) works I highly recommend this excellent [series of articles](http://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/).