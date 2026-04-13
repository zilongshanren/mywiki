---
title: Tile-based Deferred and Forward Lighting
url: http://diaryofagraphicsprogrammer.blogspot.com/2012/04/tile-based-deferred-and-forward.html
author: Wolfgang Engel
published: '2012-04-15'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

DirectCompute opened up new abilities to apply lighting to a scene. In the last three years, dealing with many lights in screen-tiles on DirectX 11 GPUs became a popular discussion topic, following implementations in major PS3 games like "Blur" and "Uncharted".

As long as you look only at the cost of light rendering, dealing with lights per screen-tile can make a huge difference in memory bandwidth consumption. In best case, data is read from the G-Buffer once and wrote into the light or framebuffer once. This is a major improvement compared to the Deferred Lighting approaches on DirectX 9/10 GPUs.

As soon as you add shadows to the equation, the line gets more blurry. Assuming that a next-gen game that requires many dynamic lights also requires many dynamic shadows (see my blog entry below "

With old-style Deferred Lighting, the shadows are applied with each light source. That means -from a memory bandwidth standpoint- writing into the light or framebuffer happens only once for the light and the shadow and many arithmetic instructions can be shared.

Any Tiled-Based approach will want to create all the shadow data before lighting. To do this, G-Buffer data need to be read for each light that is supposed to cast a shadow. Additionally for each light that is supposed to cast a shadow, the data need to be written into the light or framebuffer.

In other words, if each light casts a shadow, any Tiled-Based approach won't offer much gain anymore when compared to Deferred Lighting on DirectX 9/10 GPUs.

Following this train of thought, it would be better to stick with old-style Deferred Lighting, because it offers a fall-back path that is consistent throughout many hardware platforms.


That being said, I consider the introduction of Tiled-Based Forward rendering a major step forward, because it offers a consistent way to deal with "alpha-blended" objects. So far everyone created a separate lighting system to deal with objects that are not in the depth buffer. This lighting system was usually simpler and not capable to render many lights.

With Tiled-Based Forward rendering, we can replace the simpler system with a lighting system that deals with many lights on "alpha-blended" objects and make it more consistent with the lighting on objects that can be captured in the depth buffer.

That is exciting. Unfortunately this will still be only available on DirectX 11 hardware but it is a huge step forward.

As long as you look only at the cost of light rendering, dealing with lights per screen-tile can make a huge difference in memory bandwidth consumption. In best case, data is read from the G-Buffer once and wrote into the light or framebuffer once. This is a major improvement compared to the Deferred Lighting approaches on DirectX 9/10 GPUs.

As soon as you add shadows to the equation, the line gets more blurry. Assuming that a next-gen game that requires many dynamic lights also requires many dynamic shadows (see my blog entry below "

[Shadows - Thoughts on Ellipsoid Light Shadow Rendering](http://diaryofagraphicsprogrammer.blogspot.com/2011/02/shadows-thoughts-on-ellipsoid-light.html)"), all the Tiled-based approaches come with a higher cost of shadow rendering compared to the Deferred Lighting approaches for lower-end hardware.With old-style Deferred Lighting, the shadows are applied with each light source. That means -from a memory bandwidth standpoint- writing into the light or framebuffer happens only once for the light and the shadow and many arithmetic instructions can be shared.

Any Tiled-Based approach will want to create all the shadow data before lighting. To do this, G-Buffer data need to be read for each light that is supposed to cast a shadow. Additionally for each light that is supposed to cast a shadow, the data need to be written into the light or framebuffer.

In other words, if each light casts a shadow, any Tiled-Based approach won't offer much gain anymore when compared to Deferred Lighting on DirectX 9/10 GPUs.

Following this train of thought, it would be better to stick with old-style Deferred Lighting, because it offers a fall-back path that is consistent throughout many hardware platforms.

That being said, I consider the introduction of Tiled-Based Forward rendering a major step forward, because it offers a consistent way to deal with "alpha-blended" objects. So far everyone created a separate lighting system to deal with objects that are not in the depth buffer. This lighting system was usually simpler and not capable to render many lights.

With Tiled-Based Forward rendering, we can replace the simpler system with a lighting system that deals with many lights on "alpha-blended" objects and make it more consistent with the lighting on objects that can be captured in the depth buffer.

That is exciting. Unfortunately this will still be only available on DirectX 11 hardware but it is a huge step forward.

## 2 comments:

Hi,



Being author of a paper which details Tiled Forward Shading, I'm curious about the assertion at the end. What do you see as the inherently DX11 part? My demo implementation uses OpenGL 3.3 (i.e. ~DX10.1), but doesn't rely on any particularly advanced features.

Cheers

.ola

Hey Ola,

you are right you can also implement it with OpenGL 3.3 ... I was thinking of DirectX 11's DirectCompute capabilties that make it easier to implement tiled-based rendering approaches.

Post a Comment