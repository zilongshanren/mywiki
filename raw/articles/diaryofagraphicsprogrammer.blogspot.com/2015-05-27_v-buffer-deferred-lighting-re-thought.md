---
title: V Buffer - Deferred Lighting Re-Thought
url: http://diaryofagraphicsprogrammer.blogspot.com/2015/05/v-buffer-deferred-lighting-re-thought.html
author: Wolfgang Engel
published: '2015-05-27'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

After eight years I would like to go back to re-design the existing rendering systems, so that they are capable to run more efficiently on high-resolution devices and display more lights with attached shadows.


Let's first see where we are: the Light Pre-Pass was introduced in March 2008 on this blog. At this point I had it already running in one R* game for a while. It eventually shipped in a large number of games and also outside of R*. The S.T.A.L.K.E.R series and the games developed by Naughty Dog had at the time a similar approach. Since then a number of modifications were proposed.

One modification was to calculate lighting by tiling the G-Buffer, then sorting lights into those tiles and then execute each tile with its light. Johan Andersson covered a practical implementation in "DirectX 11 rendering in Battlefield 3" (

The drawback of this approach is the higher minimum run-time cost. Sorting the lights into the tiles raised the "resting" workload even when only a few lights were rendered. Compared to the older approaches it didn't break even until one rendered a few dozen lights. Additionally as soon as lights had to be drawn with shadows, the memory bandwidth savings were negligible.

Newer approaches like "Clustered Deferred and Forward Shading" (

Because transparency solutions with all the approaches mentioned above are inconsistent with the way opaque objects are handled, there was a group of people that wishes to go back to forward rendering. Takahiro Harada described and refined an approach that he called Forward+ (


Filling a G-Buffer or re-submitting geometry in case of Forward+ is expensive. For the Deferred Lighting implementations, the G-Buffer fill was the stage were also visibility of geometry was solved (there is also the option of making a Z Pre-Pass which means geometry is submitted one more time at least).

With modern 4k displays and high-res devices like Tablets and smart phones, a G-Buffer is not a feasible solution anymore. When the Light Pre-Pass was developed a 1280x720 resolution was considered state of the art. Today 1080p is considered the minimum resolution, iOS and Android devices have resolutions several times this size and even modern PC monitors can have more than 4K resolution.

MSAA increases the size and therefore cost manifold.


Instead of rendering geometry into three or four render targets with overdraw (or re-submitting after the Z prepass), we need to find a way to store visibility data separate in a much smaller buffer, in a more efficient way.

In other words, if we could capture the full-screen visibility of geometry in as small a footprint as possible, we could significantly reduce the cost of geometry submission and pixel overdraw afterwards.


A first idea on how this could be done is described in the article "The Visibility Buffer: A Cache-Friendly Approach to Deferred Shading" by Christopher A. Burns et all.. The article outlines the idea to store per triangle visibility data in a visibility buffer.











Let's first see where we are: the Light Pre-Pass was introduced in March 2008 on this blog. At this point I had it already running in one R* game for a while. It eventually shipped in a large number of games and also outside of R*. The S.T.A.L.K.E.R series and the games developed by Naughty Dog had at the time a similar approach. Since then a number of modifications were proposed.

One modification was to calculate lighting by tiling the G-Buffer, then sorting lights into those tiles and then execute each tile with its light. Johan Andersson covered a practical implementation in "DirectX 11 rendering in Battlefield 3" (

[http://www.slideshare.net/DICEStudio/directx-11-rendering-in-battlefield-3](http://www.slideshare.net/DICEStudio/directx-11-rendering-in-battlefield-3)). Before Tiled-Deferred, lights were additively blended into a buffer, consuming memory bandwidth with each blit. The Tiled-Deferred approach reduced memory bandwidth consumption substantially by resolving all the lights in one tile.The drawback of this approach is the higher minimum run-time cost. Sorting the lights into the tiles raised the "resting" workload even when only a few lights were rendered. Compared to the older approaches it didn't break even until one rendered a few dozen lights. Additionally as soon as lights had to be drawn with shadows, the memory bandwidth savings were negligible.

Newer approaches like "Clustered Deferred and Forward Shading" (

[http://www.cse.chalmers.se/~uffe/clustered_shading_preprint.pdf](http://www.cse.chalmers.se/~uffe/clustered_shading_preprint.pdf)) by Ola Olsson et all. started solving the "light overdraw" problem in even more efficient ways. A practical implementation is shown on Emil Perrson's website ([http://www.humus.name/Articles/PracticalClusteredShading.pdf](http://www.humus.name/Articles/PracticalClusteredShading.pdf)) in an example program.Because transparency solutions with all the approaches mentioned above are inconsistent with the way opaque objects are handled, there was a group of people that wishes to go back to forward rendering. Takahiro Harada described and refined an approach that he called Forward+ (

[http://www.slideshare.net/takahiroharada/forward-34779335](http://www.slideshare.net/takahiroharada/forward-34779335)). The tiled-based handling of light sources was similar to the Tiled-Deferred approach. The advantage of having a consistent way of lighting transparent and opaque objects was bought by having to re-submit all potentially visible geometry several times.Filling a G-Buffer or re-submitting geometry in case of Forward+ is expensive. For the Deferred Lighting implementations, the G-Buffer fill was the stage were also visibility of geometry was solved (there is also the option of making a Z Pre-Pass which means geometry is submitted one more time at least).

With modern 4k displays and high-res devices like Tablets and smart phones, a G-Buffer is not a feasible solution anymore. When the Light Pre-Pass was developed a 1280x720 resolution was considered state of the art. Today 1080p is considered the minimum resolution, iOS and Android devices have resolutions several times this size and even modern PC monitors can have more than 4K resolution.

MSAA increases the size and therefore cost manifold.

Instead of rendering geometry into three or four render targets with overdraw (or re-submitting after the Z prepass), we need to find a way to store visibility data separate in a much smaller buffer, in a more efficient way.

In other words, if we could capture the full-screen visibility of geometry in as small a footprint as possible, we could significantly reduce the cost of geometry submission and pixel overdraw afterwards.

A first idea on how this could be done is described in the article "The Visibility Buffer: A Cache-Friendly Approach to Deferred Shading" by Christopher A. Burns et all.. The article outlines the idea to store per triangle visibility data in a visibility buffer.

## No comments:

Post a Comment