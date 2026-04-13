---
title: 'OpenGL Notes #2: Texture bind performance'
url: https://outerra.blogspot.com/2012/11/opengl-notes-2-texture-bind-performance.html
author: Laco Hrabcak
published: '2012-11-15'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Some time ago we encountered a strange performance slowdown in our object renderer on NVIDIA hardware. I didn't have mesh sorting by material id implemented yet; I knew that this could be issue but I thought it could take 1ms top. But the actual slowdown was way bigger. Later I found out that it was indeed caused by glBindMultiTextureEXT. So I ran a couple of tests, first using one big texture


TABLE 1: Objects in the test scene had about 400k tris, ~250 meshes and 42 textures

all textures had the same format, diffuse DXT1, normal 3DC/ATI2 etc.

NVIDIA DRV: 306.97, 306.94 (Nsight) and 310.33, AMD DRV: 12.10



Those numbers are pretty bad for NVIDIA. But the weird thing is that we have no such issue in the terrain renderer, which uses unique textures for every terrain tile, making about ~200 meshes/textures per frame, but the performance there is great. There is no difference in the render states, object renderer follows immediately after the terrain renderer without any changes to the render states. I have tried a lot of tests - a simple shader, non-DSA functions for texture binding, render without terrain etc., without luck - every time I started to change the textures per mesh I hit the wall.


I moved to NVIDIA Nsight to find out where exactly is this slowdown, and I found out that every time glBindMultiTextureEXT is called, the following draw call


The idea that came to me was to bind as many textures as I can at once


TABLE 2: The same scene, NVIDIA DRV: 306.97, 306.94 (Nsight) and 310.33, AMD DRV: 12.10




I was curious how this will work on AMD, but the limit is 32 image units there. I created so called


I would be still interested to learn what is causing such a big slowdown on NVIDIA architecture.

*(**2048x2048**)*for all meshes, then adding the sorting by material id. You can see the times for the final object pass in the Table 1.TABLE 1: Objects in the test scene had about 400k tris, ~250 meshes and 42 textures

all textures had the same format, diffuse DXT1, normal 3DC/ATI2 etc.

NVIDIA DRV: 306.97, 306.94 (Nsight) and 310.33, AMD DRV: 12.10

| NVIDIA 460 1GB (ms) | AMD 6850 (ms) | |
without sorting |
15.0 |
5.0 |
| one texture | 3.3 | 4.0 |
| sort by mesh/material | 6.8 | 4.3 |

Those numbers are pretty bad for NVIDIA. But the weird thing is that we have no such issue in the terrain renderer, which uses unique textures for every terrain tile, making about ~200 meshes/textures per frame, but the performance there is great. There is no difference in the render states, object renderer follows immediately after the terrain renderer without any changes to the render states. I have tried a lot of tests - a simple shader, non-DSA functions for texture binding, render without terrain etc., without luck - every time I started to change the textures per mesh I hit the wall.

*(**I used two textures for this test and the time was almost 15 ms).*I moved to NVIDIA Nsight to find out where exactly is this slowdown, and I found out that every time glBindMultiTextureEXT is called, the following draw call

*(in this case**glDrawRangeElements**)*is much longer both on the CPU side and the GPU side too. With debug rendering context there were no performance warnings. Full of frustration I was browsing the[glCapsViewer database](http://delphigl.de/glcapsviewer/listreports.php)and comparing with texture caps between NVIDIA and AMD. There was one interesting number that had drawn my attention: MAX_COMBINED_TEXTURE_IMAGE_UNITS on NVIDIA SM4 hardware is from 96 to 192 texture image units. On AMD only 32*(the spec tells it should be at least 48 for GL3.3, at least 16 per stage and there are three stages in GL3.3)*. This number means how many textures you can bind at once by glActiveTexture(GL_TEXTURE0+192,...). In one shader stage you can use 16-32 textures only from this budget and these textures are specified by glUniform1i calls.The idea that came to me was to bind as many textures as I can at once

*(in my case there were 160 units available on NV460, more than enough for my test scene)*and render all meshes without texture binding. Additionally per mesh I call one glUniform1iv, which tells the shader which texture unit is being used. This uniform call is a fast one*(usually i'm using*glVertexAttrib*to pass a mesh specific parameters to the vertex shader, whould be nice to know which way is faster but I think the difference is negligible)*The result was more than interesting, see Table 2.TABLE 2: The same scene, NVIDIA DRV: 306.97, 306.94 (Nsight) and 310.33, AMD DRV: 12.10

| NVIDIA 460 1GB (ms) | AMD 6850 (ms) | |
| one texture | 3.3 | 4.0 |
| sort by mesh/material | 6.8 | 4.3 |
texture bind group | 3.36 | 4.1 |

I was curious how this will work on AMD, but the limit is 32 image units there. I created so called

*"texture bind groups"*with the max size set to MAX_COMBINED_TEXTURE_IMAGE_UNITS minus the number of channels needed for other stuff*(in my case I have 26 free bindable units on AMD)*and split the meshes to these groups. The result was better than the version with sorting, so I left this implementation for both vendors.I would be still interested to learn what is causing such a big slowdown on NVIDIA architecture.

## 5 comments:

What NVIDIA driver are you using?

I did not realize that it's now possible to bind that many textures...



If you wanted to really optimize, you could still sort meshes by texture in order to minimize the number of calls to glUniform1i.

If your scene has more than 192 texture, then you still need to bind textures every frame. In that context, you can try to find an algorithm that minimizes both the number of texture bindings and the number of uniform bindings. As I'm not sure that it's possible to optimize both at the same time, you may need to find the best tradeoff. Sounds fun!

@Timothy Lottes I have updated the tables with driver versions. I was mainly working on the version 306.97 and 306.94 from Nsight package, I didn't test the old/slow version on the latest beta, I will try it today.


@David Roger The meshes are still sorted by textures, the binding groups come atop of that. Besides, glUniform is not a problem, the performance hit shows up in the draw call following the texture bind. Binding the textures in groups and then passing the id in uniforms minimizes that hit.

Try posting to the nVidia developer forum and see if anyone has more info.


https://devtalk.nvidia.com

Post a Comment