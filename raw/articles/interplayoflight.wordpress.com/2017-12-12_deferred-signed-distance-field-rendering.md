---
title: Deferred Signed Distance Field rendering
url: https://interplayoflight.wordpress.com/2017/12/12/deferred-signed-distance-field-rendering/
author: Kostas Anagnostou
published: '2017-12-12'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Inspired by some awesome-looking games that have based their rendering pipeline on [signed distance fields](http://jamie-wong.com/2016/07/15/ray-marching-signed-distance-functions/) (SDFs), such as [Claybook](http://www.claybookgame.com/) and [Dreams](http://dreams.mediamolecule.com/), I decided to try some SDF rendering myself, for the first time.

Having seen some impressive [shadertoy ](https://www.shadertoy.com/view/Xds3zN)[demos](https://www.shadertoy.com/view/ld3Gz2), I wanted to try SDFs in the context of an actual rendering engine, so I fired Unity up and modified the standard shader so that it renders SDFs to the g-buffer. The SDF implementations came mainly from these two [excellent](http://jamie-wong.com/2016/07/15/ray-marching-signed-distance-functions/) [posts](http://www.iquilezles.org/www/articles/distfunctions/distfunctions.htm).


To render the SDFs I added a script that produces a full-screen triangle and renders it during the g-prepass using a modified “standard” shader.

The vertex shader in this case becomes pass-through:

VertexOutputDeferred vertSDFDeferred(VertexInput v) { VertexOutputDeferred o = (VertexOutputDeferred)0; o.pos = v.vertex; o.tex = TexCoords(v); return o; }

To produce the ray that will be used during raymarching we calculate the clip position at each pixel using the far plane depth (1.0) and transform it to world space.

float3 eye = _WorldSpaceCameraPos; //transform clip pos to world space float4 clipPos = float4(i.tex.xy * 2.0 - 1.0, 1.0, 1.0); clipPos.y = -clipPos.y; float4 worldPos = mul(InverseViewProjectionMatrix, clipPos); worldPos.xyz = worldPos.xyz / worldPos.w; float3 worldDir = normalize(worldPos.xyz - eye);

This makes raymarching use the main camera, like all polygonal geometry in the scene.

In order to allow the SDFs to correctly sort against other polygonal geometry in the scene, the shader outputs depth as well, by projecting the hit position to NDC.

clipPos = mul(UNITY_MATRIX_VP, float4(hitPos,1)); outDepth = clipPos.z / clipPos.w;

The result on a scene with a mixture of polygonal meshes and SDFs, and 2 point lights (green and red) is this:

![rough](../../assets/679bfc71c95147e7.png)


In the above image the white sphere at the centre is polygonal and it sorts correctly with the box SDF.

Using Unity’s material system allows for some nice effects as well, such as modifying the roughness of the SDFs making them more or less glossy:

![smooth](../../assets/b11927e244226a27.png)


As well as adding emissive to them:

![emissive2](../../assets/006997c36b085a15.png)


Of course these settings will apply to all SDFs that are rendered with that material and it is not very useful if you need finer grained control, so in all probability we’d need to add a custom material system in the shader.

Finally, since we are rendering the SDFs’ depth to the z-buffer we can get all sorts of [postprocessing effects](https://github.com/Unity-Technologies/PostProcessing), such as screen space reflections, ambient occlusion and bloom:

![scene_larger](../../assets/790f1b580014e1c0.png)


Decoupling lighting from SDF rendering removes the ability to produce high quality reflections and shadows but on the other hand might help reduce the cost of the shader and the register pressure with all those loops and branches.

It should be possible to modify the shadowmap pass to render the SDFs into the shadowmap as well, although I expect the shadow cost will go up measurably.

Although not very useful yet, this was a fun exercise! Here’s the (hacky) [Unity 2017.2 project](https://1drv.ms/u/s!AmOPA68QU4JIiNYen570tJJ-QqhurQ) if anyone is interested in the specifics.