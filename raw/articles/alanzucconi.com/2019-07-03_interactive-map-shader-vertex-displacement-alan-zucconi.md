---
title: 'Interactive Map Shader: Vertex Displacement - Alan Zucconi'
url: https://www.alanzucconi.com/2019/07/03/interactive-map-01/
author: Alan Zucconi
published: '2019-07-03'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This online course is dedicated to **interactive maps**, and how to create them using Shaders in Unity.

![](../../assets/5fbb2a0e1309dd77.gif)

This is a tutorial in three parts:

**Part 1:**[Interactive Map Shader: Vertex Displacement](https://www.alanzucconi.com/?p=10641)- Part 2:
[Interactive Map Shader: Scrolling Effect](https://www.alanzucconi.com/?p=10778) - Part 3:
[Interactive Map Shader: Terrain Shading](https://www.alanzucconi.com/?p=10782)

This effect will serve as the base for more advanced techniques, such as holographic projections and even Black Panther’s sand table.

A link to download the Unity package for this tutorial can be found at the end of this article.

The inspiration for this tutorial comes from a tweet that [Baran Kahyaoglu](https://twitter.com/brnkhy) posted to showcase some of the work he has been doing for [Mapbox](https://twitter.com/Mapbox).

The scene (minus the map) comes from the Unity Visual Effect Graph Spaceship demo (below), which you can download [here](https://github.com/Unity-Technologies/VisualEffectGraph-Samples).

## Anatomy of the Effect

The first thing is easy to notice is that geographical maps are *flat*: when used as textures, they lack the three-dimensionality that a true 3D model of that same region would have.

The first solution you can implement is creating a 3D model of the region you want in your game, and them using the geographical map as its texture. That works perfectly, but is time-consuming and stops you from implementing the “scrolling” effect seen in Baran Kahyaoglu’s video.

It is obvious that the best way to move forward is to go for a more technical approach. Luckily, shaders can be used to alter the geometry of a 3D model. This can be exploited to shape any flat plane into the valleys and mountains of the region we want.

For this tutorial, I will use a map of the [Quillota region](https://www.google.com/maps/place/Quillota,+Valparaiso+Region,+Chile/) in Chile, which is known for its characteristic hills. The image below shows a texture of the region applied to a circular mesh.

![](../../assets/df4a6c854b12deb7.png)

While hills and mountains can be seen, they appear completely flat. This destroys any illusion of realism.

## Normal Extrusion

The first step is to use shaders to alter the geometry using a technique called **normal extrusion**. What is needed is a **vertex modifier**: a function capable of manipulating the individual vertices of a 3D model.

How you use a vertex modifier changes based on the type of shader you have. In this tutorial, we are showing how to edit a **Surface Standard Shader**, which is one of the types of shaders that you can create with Unity.

There are many ways we can manipulate the vertices of a 3D model. One of the very first techniques that most vertex shaders tutorial teach is the **normal extrusion**. The idea is to push each vertex “outwards” (*extrude*), giving a more inflated look to a 3D model. The concept of “outwards” comes from the fact that each vertex is moved along its normal direction.

![](../../assets/2076d42560daa0c8.png)

This works very well for smooth surfaces, but can create some weird artefacts for models which vertices are not properly welded. This effect was also explained in one of my very first tutorials: [A Gentle Introduction to Shaders](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/), where I showed how to **extrude** and **intrude** a 3D model.

![](../../assets/63a6c9d359aa8e9c.gif)

Adding normal extrusion to a surface shader is easy. Each surface shader has a `#pragma`

directive, which is used to provide additional pieces of information and commands. One of these is `vertex:vert`

, which indicates that the function called `vert`

will be used to process each vertex of the 3D model.

The edited shader looks like this:

#pragma surface surf Standard fullforwardshadows addshadow vertex:vert ... float _Amount; ... void vert(inout appdata_base v) { v.vertex.xyz += v.normal * _Amount; }

Since we are changing the position of the vertices, we also need to use `addshadow`

if we want the model to correctly cast shadows on itself.

### ⭐ Recommended Unity Assets

## Normal Extrusion With Textures

The code we have used in the section above works correctly, but is far from the effect we want to achieve. The reason is that we do not want to extrude all vertices by the same amount. We want the surface of our 3D model to match the valleys and peaks of the geographical region it represents. Firstly, we need to somehow store and retrieve the information of how raised each point on the map is. We want, in a nutshell, the extrusion to be modulated by a texture, which encodes the heights of our landscape. Such textures are often referred to as **heightmaps**, although it is not uncommon to see them called **depthmaps**, based on the context. Once the height information is available, we can modulate the extrusion of a flat plane based on the heightmap. As seen in the diagram below, this allows controlling which areas will be raised and which ones will be lowered.

![](../../assets/29bb739c079334ec.png)

It is relatively easy to find a satellite image of the geographical area of your interest, and its associated heightmap. Below, you can see a satellite map of Mars (left) and its heightmap (right), which have been used in this tutorial:

I have covered the concept of depthmaps extensive in another series titled [Inside Facebook 3D Photos: Parallax Shaders](https://www.alanzucconi.com/2019/01/01/facebook-3d-photos/).

For this tutorial, we will assume that the heightmap is stored is a grayscale image in which black and white correspond to the lower and higher altitudes, respectively. We also need these values to be scaled *linearly*, meaning that (for instance) a difference in colours of ![Rendered by QuickLaTeX.com 0.1](../../assets/421fe30d9295aa64.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 0.1](../../assets/421fe30d9295aa64.png)

![Rendered by QuickLaTeX.com 0.9](../../assets/8c592d825ecd9fcf.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

*logarithmic scale*.

Sampling a texture requires two pieces of information: the texture itself, and the **UV coordinates** of the point we want to sample. The latter can be accessed through the field `texcoord`

stored in the `appdata_base`

structure. That is the UV coordinate associated with the vertex currently being processed. Sampling textures in a *surface function* is done using `tex2D`

, although `tex2Dlod`

is required when we are in a *vertex function*.

In the snippet below, a texture called `_HeightMap`

is used to modulate the amount of extrusion performed on each vertex:

sampler2D _HeightMap; ... void vert(inout appdata_base v) { fixed height = tex2Dlod(_HeightMap, float4(v.texcoord.xy, 0, 0)).r; vertex.xyz += v.normal * height * _Amount; }

The result can be seen quite clearly below:

There is one small simplification that can be done in our case. The code seen so far is supposed to work on any geometry. However, we can assume that our surface is completely flat. In fact, what we really want is to use this effect on a flat plane.

Consequently, we can remove `v.normal`

and replace it with `float3(0, 1, 0)`

:

void vert(inout appdata_base v) { float3 normal = float3(0, 1, 0); fixed height = tex2Dlod(_HeightMap, float4(v.texcoord.xy, 0, 0)).r; vertex.xyz += normal * height * _Amount; }

This was possible because all coordinates in `appdata_base`

are stored in **model space**, meaning that they are relative to the centre and orientation of the 3D model. Translating, rotating and scaling an object using its *transform* in Unity change the position, rotation and scale of the object, but leaves its original 3D model unaffected.

## What’s Next…

In the next part of this online course, we will explore how to implement a scrolling effect, so that we can actually move the geometry around.

**Part 1:**[Interactive Map Shader: Vertex Displacement](https://www.alanzucconi.com/?p=10641)- Part 2:
[Interactive Map Shader: Scrolling Effect](https://www.alanzucconi.com/?p=10778) - Part 3:
[Interactive Map Shader: Terrain Shading](https://www.alanzucconi.com/?p=10782)

### Unity Package Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The full package for this tutorial is available on [Patreon](https://www.patreon.com/posts/28104018), and it includes all the assets necessary to reproduce the technique here presented.

## Leave a Reply Cancel reply