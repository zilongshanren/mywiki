---
title: Creating a 3D Game Engine (Part 21)
url: https://cybereality.com/creating-a-3d-game-engine-part-21/
author: Cybereality
published: '2014-06-08'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

After a few days of hacking away at the code, I’ve got a new video up. In this update I have added normal mapping and specular lighting. I did have a few set-backs while working on the shaders, and it was made even more difficult since I was basically “flying blind” without a debugger. It seems that the Express version of Visual Studio does not support shader debugging, and neither does Nvidia’s debugger tool. Very sad, and I may (at some point) have to upgrade to the Pro version. I’ll probably hold out for a little bit, and I did end up figuring the problems out this time.

With the specular lighting shader, the issue I had was doing the matrix multiply and output on a float4 instead of a float3. To be honest, I am not quite sure why it didn’t work, but switching things around seemed to help. The change I made was also follows.

output.normal = normalize(mul((float3x3)worldMatrix, normal.xyz));

Instead of:

output.normal = normalize(mul(worldMatrix, normal));

Again, not sure why that works, but I’m happy it does. With the normal mapping, there was a lot of math and changes involved, and it became difficult to find which piece was broken. As it turns out, all the math was (mostly) correct, but the values I was sending to the constant buffer were not being updated. From what I can tell, the pixel shader cannot read the constant buffer (cbuffer) but the vertex shader can. Strange, and I’m not sure why this must be the case. So instead of trying to read the cbuffer values directly from the pixel shader, I passed them in as output values from the vertex shader. In addition, trying to pass bool or int values to the pixel shader would not work. So, as a hack, I added the same int value to all parameters of a float3 and passed that instead. I bet I can figure this one out eventually, but I’ve already spent all day on this and I’m happy just to see something working on the screen.

Next up I will probably try to model something more substantial than a cube so I have something better to look at.