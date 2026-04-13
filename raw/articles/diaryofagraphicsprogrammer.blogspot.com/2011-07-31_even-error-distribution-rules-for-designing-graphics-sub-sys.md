---
title: 'Even Error-Distribution: Rules for Designing Graphics Sub-Systems (Part III)'
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/07/even-error-distribution-rules-for.html
author: Wolfgang Engel
published: '2011-07-31'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[No Look-up Tables](http://altdevblogaday.com/2011/07/03/no-look-up-tables-rules-for-designing-graphics-sub-systems-part-ii/)" and "

[Screen-Space](http://altdevblogaday.com/2011/06/13/screen-space-rules-for-designing-graphics-sub-systems-part-i/)" rules, it is probably easier to agree on this principle in general. The idea is that whatever technique you implement, you face the observer always with a consistent "error" level. The word error describes here a difference between what we consider the real world experience and the visual experience in a game. Obvious examples are toon and hatch shading, where we do not even try to render anything that resembles the real world but something that is considered beautiful. More complex examples are the penumbras of shadow maps, ambient occlusion or a real-time global illumination approach that has a rather low granularity.

The idea behind this design rule is that whatever you do, do it consistently and hope that the user will adjust to the error and not recognize it after a while anymore. Because the error is evenly distributed throughout your whole game, it is tolerated easier by the user.

To look at it from a different perspective. At Confetti we target most of the available gaming platforms. We can render very similar geometry and textures on different platforms. For example iOS/Android with OpenGL ES 2.0 and then Windows with DirecX 11 or XBOX 360 with its Direct3D. For iOS / Android you want to pick different lighting and shadowing techniques than for the higher end platforms. For shadows it might be stencil shadow volumes on low-end platforms and shadow maps on high end platforms. Those two shadowing techiques have very different performance and visual characteristics. The "error" resulting from stencil shadow volumes is that the shadows are -by default- very sharp and pronounced while shadow maps on the higher end platforms can be softer and more like real life shadows.

A user that watches the same game running on those platforms, will adjust to the "even" error of each of those shadow mapping techniques as long as they do not change on the fly. If you would mix the sharp and the soft shadows, users will complain that the shadow quality changes. If you provide only one or the other shadow, there is a high chance that people will just get used to the shadow appearance.

Similar ideas apply to all the graphics programming techniques we use. Light mapping might be a viable option on low end platforms and provide pixel perfect lighting, a dynamic solution replacing those light maps might have a higher error level and not being pixel perfect. As long as the lower quality version always looks consistent, there is a high chance that users won't complain. If we would change the quality level in-game, we are probably faced with reviews that say that the quality is changing.

Following this idea, one can exclude techniques that change the error level on the fly during game play. There were certainly a lot of shadow map techniques in the past that had different quality levels based on the angle between the camera and the sun. Although in many cases they looked better than the competing techniques, users perceived the cases when their quality was lowest as a problem.

Any technique based on re-projection, were the quality of shadows, Ambient Occlusion or Global Illumination changes while the user watches a scene, would violate the "Even Error-Distribution" rule.

A game that mixes light maps that hold shadow and/or light data and dynamic light and / or regular shadow maps might have the challenge to make sure that there is no visible difference between the light and shadow quality. Quite often the light mapped data looks better than the dynamic techniques and the experience is inconsistent. Evenly distributing the error into the light map data would increase the user experience because he/she is able to adjust better to an even error distribution. The same is true for any form of megatexture approach.

A common problem of mixing light mapped and generated light and shadow data is that in many cases dynamic objects like cars or characters do not receive the light mapped data. Users seems to have adjusted to the difference in quality here because it was consistent.

## No comments:

Post a Comment