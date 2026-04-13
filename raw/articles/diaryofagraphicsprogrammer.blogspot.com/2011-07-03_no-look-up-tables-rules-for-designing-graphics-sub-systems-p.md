---
title: 'No Look-up Tables: Rules for Designing Graphics Sub-systems (Part II)'
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/07/no-look-up-tables-rules-for-designing.html
author: Wolfgang Engel
published: '2011-07-03'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One of the design principles I apply to graphics systems nowadays is to avoid any look-up table. That means not only mathemetical look-up tables -the way we used them in the 80ieth and the 90ieth- but also cached lighting, shadow and other data, that is sometimes stored in light or radiosity maps.


This design principle follows the development of GPUs. While decent GPUs offer with each new iteration a larger number of arithetic instructions, the memory bandwidth is stagnating since several years. Additionally transporting data to the GPU might be slow due to several bottlenecks like DVD speed, PCI Express bus etc.. In many cases it might be more efficient to calculate a result with the help of arithmetic instructions, instead of doing a look-up in a texture or any other memory area. Saving streaming bandwidth throughout the hardware is also a good motivation to avoid look-up textures like this. Quite often any look-up technique doesn't allow a 24 hour game cycle, where the light and shadows have to move accordingly with time.

In many cases using pre-baked textures to store lighting, shadowing or other data also leads to a scenario where the geometry on which the texture is applied is not destructible anymore.


Typical examples are:

- Pre-calculating a lighting equation and storing results in a texture like a 2D, Cube or 3D map

- Large terrain textures, like megatextures. Texture synthesis might be more efficient here

- Light and radiosity maps and other pre-calculated data for Global illumination approaches

- Signed distance fields (if they don't allow 24 hour cycle lights and shadows)

- Voxels as long as they require a large amount of data to be re-read each frame and don't allow dynamic lighting and shadows (24 hour cycle)

- ... and more ...


Following the "No Look-up Table" design principle, one of the options to store intermediate data is to cache it in GPU memory, so that data doesn't need to be generated on the fly. This might be a good option depending on the amount of memory available on the GPU.

Depending on the underlying hardware platform or the requirements of the game, the choice between different caching schemes makes a system like this very flexible.


Here are a collection of ideas that might help to make an informed decision on when to apply a caching scheme, that keeps data around in GPU memory:

- Whenever the data is not visible to the user, it doesn't need to be generated. For example color, light and shadow data only need to be generated if the user can see them. That requires that they are on-screen with sufficient size. Projecting an object into screen-space allows to calculate its size. If it is too small or not visible any data attached to it doesn't need to be generated. This idea does not only apply to geometric objects but also light and shadows. If a shadow is too small on the screen, we do not have to re-generate it.

- Cascaded Shadow maps introduced a "level of shadowing" system that distributes shadow resolution along the view frustum in a way that the shadow resolution distribution dedicates less resolution to objects farer away, while closer up objects recieve relativly more shadow resolution. Similarly lighting quality should increase and decrease based on distance. Cascaded Reflective shadow maps extend the idea on any global illumination data, like one bounce diffuse lighting and ambient occlusion.

- If the quality requirements are rather low because the object is far away or small, screen-space techniques might allow to store data in a higher density. For example Screen-Space Global illumination approaches that are based on the G-Buffer - that is already used to apply Deferred Lights in a scene- can offer an efficient way to light far away objects.

## No comments:

Post a Comment