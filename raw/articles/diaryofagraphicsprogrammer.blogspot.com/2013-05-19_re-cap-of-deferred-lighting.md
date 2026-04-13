---
title: Re-cap of Deferred Lighting
url: http://diaryofagraphicsprogrammer.blogspot.com/2013/05/re-cap-of-deferred-lighting.html
author: Wolfgang Engel
published: '2013-05-19'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is part of a response in a discussion forum I did recently and it summarizes a lot of the things I did a few years ago with renderer design on XBOX 360 / PS3 (more details in the articles below). So I thought I share it here as well:


----------------------------------------------------

Before I start talking about memory bandwidth, let me first outline my favorite renderer design that shipped now in a couple of games: from a high-level view, you want to end up with mainly three stages:


Geometry -> Light / Shadow data -> Materials


Geometry

In this stage you render your objects into a G-Buffer. It might be the most expensive or one of the more expensive parts of your rendering pipeline. You want your G-Buffer to be as small as possible. When we moved from Deferred Shading to Deferred Lighting, one of the motivations was to decrease the size of the G-Buffer. In a typical Deferred Lighting scenario you have three render targets in the G-Buffer: the depth buffer, a color buffer and a normal buffer (those might hold specular information and a material index as well). There are all kinds of ways to compress data like using two channel color formats, two channel normal data etc..

One reason why the G-Buffer needs to be small is what I mentioned above. Every mesh you render in there will be expensive. Obviously I am leaving out a lot of stuff here like pre-Z pass etc..

The other reason why the G-Buffer needed to be small was the fact that you have to read it for each light. On XBOX 360 and PS3 that was a major memory bandwidth challenge and the ultimate reason to move from Deferred Shading to Deferred Lighting. You were able to render now much more lights with the smaller G-Buffer.


Lighting / Shadow Stage

Rendering lights into the light / shadow buffer had the advantage of just using two render targets out of the three in the G-Buffer. The depth buffer and the normal buffer with the specular information. With that setup you could increase the number of lights substantially compared to Deferred Shading.

The light / shadow buffer holds the data for all lights and shadows, in other words: brightness data separated for diffuse and specular together with the light color. Please note the third render target in the G-Buffer that holds color is not used here.


Material Stage

Splitting up the high-level view into Geometry -> Light / Shadows -> Materials is done because you want to apply expensive materials like skin, hair, cloth, leather, car paint etc.. and you can't store much data in the G-Buffer to describe those materials. So you apply them in screen or image space like a PostFX.

One of the reasons to move to Deferred Lighting was the increased material variety it offers. In a Deferred Shading setup you have to apply the material terms while you do the lighting calculations which sometimes made those really expensive and with the overlapping lights, you did those too often.

----------------------------------------------------


A lot of the recent work is about materials in screen-space. In the last few years my focus moved away from renderer design to global illumination and re-thinking the current Post-Processing pipelines; while solving other challenges for our customers. I hope I have something to share in those areas very soon ...




----------------------------------------------------

Before I start talking about memory bandwidth, let me first outline my favorite renderer design that shipped now in a couple of games: from a high-level view, you want to end up with mainly three stages:

Geometry -> Light / Shadow data -> Materials

Geometry

In this stage you render your objects into a G-Buffer. It might be the most expensive or one of the more expensive parts of your rendering pipeline. You want your G-Buffer to be as small as possible. When we moved from Deferred Shading to Deferred Lighting, one of the motivations was to decrease the size of the G-Buffer. In a typical Deferred Lighting scenario you have three render targets in the G-Buffer: the depth buffer, a color buffer and a normal buffer (those might hold specular information and a material index as well). There are all kinds of ways to compress data like using two channel color formats, two channel normal data etc..

One reason why the G-Buffer needs to be small is what I mentioned above. Every mesh you render in there will be expensive. Obviously I am leaving out a lot of stuff here like pre-Z pass etc..

The other reason why the G-Buffer needed to be small was the fact that you have to read it for each light. On XBOX 360 and PS3 that was a major memory bandwidth challenge and the ultimate reason to move from Deferred Shading to Deferred Lighting. You were able to render now much more lights with the smaller G-Buffer.

Lighting / Shadow Stage

Rendering lights into the light / shadow buffer had the advantage of just using two render targets out of the three in the G-Buffer. The depth buffer and the normal buffer with the specular information. With that setup you could increase the number of lights substantially compared to Deferred Shading.

The light / shadow buffer holds the data for all lights and shadows, in other words: brightness data separated for diffuse and specular together with the light color. Please note the third render target in the G-Buffer that holds color is not used here.

Material Stage

Splitting up the high-level view into Geometry -> Light / Shadows -> Materials is done because you want to apply expensive materials like skin, hair, cloth, leather, car paint etc.. and you can't store much data in the G-Buffer to describe those materials. So you apply them in screen or image space like a PostFX.

One of the reasons to move to Deferred Lighting was the increased material variety it offers. In a Deferred Shading setup you have to apply the material terms while you do the lighting calculations which sometimes made those really expensive and with the overlapping lights, you did those too often.

----------------------------------------------------

A lot of the recent work is about materials in screen-space. In the last few years my focus moved away from renderer design to global illumination and re-thinking the current Post-Processing pipelines; while solving other challenges for our customers. I hope I have something to share in those areas very soon ...

## No comments:

Post a Comment