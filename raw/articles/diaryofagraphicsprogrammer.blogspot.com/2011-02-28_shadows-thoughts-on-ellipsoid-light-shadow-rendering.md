---
title: Shadows - Thoughts on Ellipsoid Light Shadow Rendering
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/02/shadows-thoughts-on-ellipsoid-light.html
author: Wolfgang Engel
published: '2011-02-28'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[RawK](http://www.confettispecialfx.com/rawk%C2%AE-graphics-demo-for-sandy-bridge)].

This demo prototypes the characteristics of an open world game, when it comes to indoor shadow rendering. In an open-world game where the viewer can go inside buildings and stay outside as well, there might be shadows for

- Cloud shadows, most of the time clouds just projected down
- Self-Shadowing for the main character or more characters: those are optional shadows with their own frustum that just cover characters bodies close to the camera
- Sun shadows: Cascaded Shadow Maps
- Shadows from point, spot and other light types

Shadows from point, spot and other light types might be cached. Trading memory against the effort of updating shadow maps makes sense on some platforms. The following text will focus on shadows coming from ellipsoidal and point lights but similar thoughts apply for light types other than directional lights.

Developing a shadow system for those light types usually means facing the following challenges:

- Shadow Rendering
- Shadow Caching
- Shadow Bias value
- Softening the Penumbra

**Shadow Rendering**

For point light types and similar light types, the favorite storage method is a cube texture map. Compared to its main competitor the dual-paraboloid shadow map, it offers a more even error distribution. The hemispheric projection for dual-paraboloid shadow maps requires a high-level of tessellation that might not be common in a game where normal maps mimic the finer details.

Rendering into a cube shadow map can be done with a DirectX 10 and above capable graphics card in one draw call with the help of the geometry shader. The performance of the geometry shader on some graphics cards is not as good as one would expect. In those cases it helps to move some of the calculations from the geometry into the vertex shader. The inner loop of a typical geometry shader used to render into a cube map might look like this:

```
// Loop over cube faces
[unroll]
for (int i = 0; i < 6; i++)
{
// Translate the view projection matrix to the position of the light
float4x4 pViewProjArray = viewProjArray[i];
//
// translate
//
// access the row HLSL[row][column]
pViewProjArray[0].w += dot(pViewProjArray[0].xyz, -In[0].lightpos.xyz);
pViewProjArray[1].w += dot(pViewProjArray[1].xyz, -In[0].lightpos.xyz);
pViewProjArray[2].w += dot(pViewProjArray[2].xyz, -In[0].lightpos.xyz);
pViewProjArray[3].w += dot(pViewProjArray[3].xyz, -In[0].lightpos.xyz);
float4 pos[3];
pos[0] = mul(pViewProjArray, float4(In[0].position.xyz, 1.0));
pos[1] = mul(pViewProjArray, float4(In[1].position.xyz, 1.0));
pos[2] = mul(pViewProjArray, float4(In[2].position.xyz, 1.0));
// Use frustum culling to improve performance
float4 t0 = saturate(pos[0].xyxy * float4(-1, -1, 1, 1) - pos[0].w);
float4 t1 = saturate(pos[1].xyxy * float4(-1, -1, 1, 1) - pos[1].w);
float4 t2 = saturate(pos[2].xyxy * float4(-1, -1, 1, 1) - pos[2].w);
float4 t = t0 * t1 * t2;
[branch]
if (!any(t))
{
// Use backface culling to improve performance
float2 d0 = pos[1].xy * pos[0].w - pos[0].xy * pos[1].w;
float2 d1 = pos[2].xy * pos[0].w - pos[0].xy * pos[2].w;
[branch]
if (d1.x * d0.y > d0.x * d1.y || min(min(pos[0].w, pos[1].w), pos[2].w) < 0.0)
{
Out.face = i;
[unroll]
for (int k = 0; k < 3; k++)
{
Out.position = pos[k];
Stream.Append(Out);
}
Stream.RestartStrip();
}
}
}
```

To relieve the workload of the geometry shader the offset and transformation code was moved into the vertex shader:```
[Vertex shader]
float4x4 viewProjArray[6];
float3 LightPos;
GsIn main(VsIn In)
{
GsIn Out;
float3 position = In.position - LightPos;
[unroll]
for (int i=0; i<3; ++i)
{
Out.position[i] = mul(viewProjArray[i*2], float4(position.xyz, 1.0));
Out.extraZ[i] = mul(viewProjArray[i*2+1], float4(position.xyz, 1.0)).z;
}
return Out;
}
//------------------------------------------------------------------------------
[Geometry shader]
#define POSITIVE_X 0
#define NEGATIVE_X 1
#define POSITIVE_Y 2
#define NEGATIVE_Y 3
#define POSITIVE_Z 4
#define NEGATIVE_Z 5
float4 UnpackPositionForFace(GsIn data, int face)
{
float4 res = data.position[face/2];
[flatten]
if (face%2)
{
res.w = -res.w;
res.z = data.extraZ[face/2];
[flatten]
if (face==NEGATIVE_Y)
res.y = -res.y;
else
res.x = -res.x;
}
return res;
}
[maxvertexcount(18)]
void main(triangle GsIn In[3], inout TriangleStream<PsIn> Stream)
{
PsIn Out;
// Loop over cube faces
[unroll]
for (int i = 0; i < 6; i++)
{
float4 pos[3];
pos[0] = UnpackPositionForFace(In[0], i);
pos[1] = UnpackPositionForFace(In[1], i);
pos[2] = UnpackPositionForFace(In[2], i);
// Use frustum culling to improve performance
float4 t0 = saturate(pos[0].xyxy * float4(-1, -1, 1, 1) - pos[0].w);
float4 t1 = saturate(pos[1].xyxy * float4(-1, -1, 1, 1) - pos[1].w);
float4 t2 = saturate(pos[2].xyxy * float4(-1, -1, 1, 1) - pos[2].w);
float4 t = t0 * t1 * t2;
[branch]
if (!any(t))
{
// Use backface culling to improve performance
float2 d0 = pos[1].xy * pos[0].w - pos[0].xy * pos[1].w;
float2 d1 = pos[2].xy * pos[0].w - pos[0].xy * pos[2].w;
[branch]
if (d1.x * d0.y > d0.x * d1.y || min(min(pos[0].w, pos[1].w), pos[2].w) < 0.0)
{
Out.face = i;
[unroll]
for (int k = 0; k < 3; k++)
{
Out.position = pos[k];
Stream.Append(Out);
}
Stream.RestartStrip();
}
}
}
}
```

Cube shadow maps are not only useful to store point light shadows but shadows from other light types as well. For example shadows from ellipsoidal lights, where each of the directions has its own attenuation value, can be stored in cube maps as well.![](http://altdevblogaday.com/wp-content/uploads/2011/02/shad1-300x168.jpg)


![](http://altdevblogaday.com/wp-content/uploads/2011/02/shad1-300x168.jpg)

*Image 1: Ellipsoid Lighting*


![](http://altdevblogaday.com/wp-content/uploads/2011/02/shad2-300x168.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/02/shad2-300x168.jpg)

*Image 2 -- 8 Ellipsoidal Light Shadow Maps*


![](http://altdevblogaday.com/wp-content/uploads/2011/02/shad5-300x168.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/02/shad5-300x168.jpg)

*Image 3: Ellipsoid Lighting*


![](http://altdevblogaday.com/wp-content/uploads/2011/02/Shadows1-300x175.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/02/Shadows1-300x175.jpg)

*Images 4: Many Shadows*


![](http://altdevblogaday.com/wp-content/uploads/2011/02/Shadows2-300x175.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/02/Shadows2-300x175.jpg)

*Images 5: Level Shadows*


![](http://altdevblogaday.com/wp-content/uploads/2011/02/Shadows31-300x175.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/02/Shadows31-300x175.jpg)

*Images 6: More Shadows*

**Shadow Caching**

Depending on the amount of memory that is available on the platform, caching 16-bit depth cube shadow maps might become an option. For example integrated graphics chips usually share memory with the CPU and might have a higher amount of - then usually slower- memory available. Storing for example 100 256x256x6 16-bit cube shadow maps is about 75 Mb.

To find a good caching algorithm, the following parameters might be useful:

- Distance from shadow to camera
- Size of shadow on screen
- Is there a moving object in the area of the light / shadow ?

Even if something is moving in the area of influence of the light, an update of the shadow map might not be necessary if the shadow is not easily visible from the point of view of the player. If the shadow is far away and it is hard to spot that an object is moving through the shadow, it would make sense to not update the map and to keep it cached.

The question if a light with a shadow map with a very small visible area on screen needs to be updated, follows a similar logic.

If there is not enough memory available, caching might be restricted by distance and then maps are moved in and out into the cache.

**Shadow Bias Value**

The classical shadow mapping algorithm generates a binary value based on a comparison. Because this comparison relies on hardware precision, it is prone to generate slight errors in edge cases.

In case of a regular 2D shadow map, the usual solution is to introduce a shadow bias value. Commonly this value needs to be picked by the user, which makes it scene dependent. In case of cube shadow maps that are attached to a moving light, there is no sensible way to pick a working value.

Approximating the binary comparison with an exponential function will lead to better overall results [Salvi].

![](http://altdevblogaday.com/wp-content/uploads/2011/02/ESM-300x190.jpg)


![](http://altdevblogaday.com/wp-content/uploads/2011/02/ESM-300x190.jpg)

*Image 7: Exponential Shadow Mapping Function*

```
float depth = tex2D(ShadowSampler, pos.xy).x;
shadow = saturate(2.0 - exp((pos.z - depth) * k));
```

**Softening the Penumbra**

There are many approaches that cover the softening of the Penumbra. Certainly all the probability based shadow filtering techniques that can elevate hardware filtering have a very good quality / performance ratio.

Screen-space filtering to achieve perceptually correct cube shadow maps is an area where game developers just started to do research. An implementation is described in [

[Engel](http://www.confettispecialfx.com/massive-point-light-soft-shadows)].

![](http://altdevblogaday.com/wp-content/uploads/2011/02/16-PointLightSoftShadows-300x225.jpg)


![](http://altdevblogaday.com/wp-content/uploads/2011/02/16-PointLightSoftShadows-300x225.jpg)

*Image 8: 16 Screen-Space Soft Point Light Shadows*


![](http://altdevblogaday.com/wp-content/uploads/2011/02/32-PointLightSoftShadows-300x168.jpg)

![](http://altdevblogaday.com/wp-content/uploads/2011/02/32-PointLightSoftShadows-300x168.jpg)

*Image 9: 32 Screen-Space Soft Point Light Shadows*

**Future Development**

Game developers try to move away from pre-calculated lighting and shadowing and any other pre-calculated data. The main reasons to do this are:

- hard to mimic a 24 hour cycle
- storing those light or radiosity maps on disk or even the DVD / Blu-ray required a lot of memory
- streaming the light or radiosity maps from disk or hard-drive through hardware to the GPU consumes valuable memory bandwidth
- geometry with light maps or radiosity maps is not destructible anymore (this is a reason to avoid any solution with pre-computed maps)
- while the environment is lit nicely, it is hard to light characters in a consistent way with this environment

In any case temporal coherence can be used to improve shadows and global illumination data over time.

**Acknowledgements**

I want to thank my business partner Peter Santoki for the help, feedback and encouragement while implementing the ideas covered above. I also would like to thank Tim Martin for help in researching the general topic of cube shadow map rendering and Igor Lobanchikov for the cube map optimizations trick.

**References**

[Engel] Wolfgang Engel, "Massive Screen-Space Soft Point Light Shadows",

[http://www.confettispecialfx.com/massive-point-light-soft-shadows](http://www.confettispecialfx.com/massive-point-light-soft-shadows)

[Dachsbacher] Carsten Dachsbacher, Marc Stamminger, "Reflective Shadow Maps",

[http://www.vis.uni-stuttgart.de/~dachsbcn/download/rsm.pdf](http://www.vis.uni-stuttgart.de/~dachsbcn/download/rsm.pdf)

[http://www.vis.uni-stuttgart.de/~dachsbcn/publications.html](http://www.vis.uni-stuttgart.de/~dachsbcn/publications.html)

[DachsbacherSii] Carsten Dachsbacher, Marc Stamminger, "Splatting Indirect Illumination",

[http://www.vis.uni-stuttgart.de/~dachsbcn/download/sii.pdf](http://www.vis.uni-stuttgart.de/~dachsbcn/download/sii.pdf)

[Kaplanyan] Anton Kaplanyan, Wolfgang Engel, Carsten Dachsbacher,

"Diffuse Global Illumination with Temporally Coherent Light Propagation Volumes",

pp 185 - 203, AK Peters, 2011

[RawK] RawK®,

[http://www.confettispecialfx.com/rawk%C2%AE-graphics-demo-for-sandy-bridge](http://www.confettispecialfx.com/rawk%C2%AE-graphics-demo-for-sandy-bridge)

[Salvi] Marco Salvi, "Rendering Filtered Shadows with Exponential Shadow Maps", ShaderX6

Marco Salvi's website:

[http://pixelstoomany.wordpress.com/?s=Exponential](http://pixelstoomany.wordpress.com/?s=Exponential)

## No comments:

Post a Comment