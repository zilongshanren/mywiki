---
title: 'Deferred Depth: 3 Ways'
url: http://hacksoflife.blogspot.com/2012/07/deferred-depth-3-ways.html
author: Benjamin Supnik
published: '2012-07-24'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I have been updating X-Plane 10's deferred pipeline; when 10.10 is in a later beta and we're sure that the new pipeline is going to hold, I'll write it up in more detail. But for now, a few notes on deferred depth.


Our art guys need more properties in the G-Buffer, so I went looking to see if I could recycle the depth buffer, rather than waste a G-Buffer channel on depth.




This saves us the copy and extra VRAM, but assumes that our various post-processing effects don't need to write Z, an assumption that is usually true.Our art guys need more properties in the G-Buffer, so I went looking to see if I could recycle the depth buffer, rather than waste a G-Buffer channel on depth.

#### The Problem

The problem is this: a deferred renderer typically wants to read depth to reconstruct eye-space position in the lighting pass; position is needed for lighting attenuation and shadows.

But the lighting pass almost certainly also needs the depth buffer to be bound for depth rejection. There are a number of cute G-Buffer tricks that require this

- Any kind of depth-based light rejection (whether with a full stencil volume or just based on the bounding volume being occluded) requires the depth buffer of the scene as a real Z buffer.
- Soft particles require rejecting Z and sampling (to soften). We really want the hardware Z buffer to cut fill rate!

#### Copying the Depth Buffer

One simple approach is to copy the depth buffer to a depth texture. In my case, I tried copying the current depth buffer (which is D24/S8) to a GL_depth_component24 texture using glCopyTexSubImage. This worked well and didn't cause performance problems; I guess after a number of years ripping the depth buffer to a texture has finally been ironed out.

With this technique the eye space layer of the G-buffer is another texture, but it comes from a single full-screen copy rather than from an additional MRT color attachment.

#### Read And Use

A second approach is to simply bind the depth buffer and use it at the same time. This scheme requires GL_NV_texture_barrier (an extension I didn't know about until smarter people clued me in recently) and thus is only available on Windows. In this scheme you:

- Set up your D24/S8 depth buffer as a texture attached to depth in your main G-Buffer FBO, rather than a render-buffer. Non-POTS textures is a given for DX10 hardware.
- Share this depth buffer with your HDR texture that you "accumulate" light into.
- After completing the g-buffer fill pass, call glTextureBarrierNV() to ensure that all write-outs to the depth buffer have completed before the next thing happens.
- Turn off depth writing and Z-test and read from the depth buffer at the same time (something that is allowed by the relaxed semantics of the extension).

I have not tried this technique; see below for why sharing Z isn't for X-Plane.

#### Eye-Space Float Z

One simple way to solve the problem (the one X-Plane originally used, and one that is sometimes used on older platforms that won't let you read and sample Z at the same time) is to simply write eye-space Z to part of the G-Buffer. This wastes G-Buffer space, but...

...it is unfortunately necessary for X-Plane. X-Plane draws in two depth domains, one for the world and one for the 3-d cockpit. Thus no one Z buffer contains full position information for the entire screen. In order to avoid two full mix-downs of the G-Buffer, we simply write out eye-space position in floating point, which gives us adequate precision over the entire world.*

If I could find a depth encoding that clips properly, doesn't inhibit early Z, and can span the entire depth range we need, we could use one of the techniques above, but I don't think such a Z technique exists, as X-Plane needs a near clip plane of around 1-5 cm in the cockpit and at least 100k meters to the far clip plane. With D24S8 we're off by quite a few bits.

(I have not had a chance to experiment with keeping the stencil buffer separate yet.)

*Currently the code uses 16-bit float eye space depth, which is apparently faster to fill than 32F on ATI hardware according to some presentation I found. Is it enough precision? I am not sure because I will have to fix other shadow bugs first. But it should be noted that we care a lot about near precision but really not much about far depth, which is only used for fog. If a later post says we use a 32F eye-space Z and not 16F, you'll know what happened.

Hi,



ReplyDeleteYou might be interested by the way Outerra deals with depth issues:

http://outerra.blogspot.fr/2012/06/couple-of-opengl-notes.html

I tried what they do but it has a serious draw-back: because the log depth function isn't defined for negative values, you can't output log depth in a vertex shader; geometry that is partly behind and partly in front of the camera will contain NaNs.



ReplyDeleteI tried offsetting the depth values but the linear interp of clipped values wasn't the same as the original log function, which produced all sorts of weird artifacts.

I believe their approach was to use a new depth function in the fragment shader; I didn't want to do that because changing the depth write-out in the fragment shader disables early-Z optimization.