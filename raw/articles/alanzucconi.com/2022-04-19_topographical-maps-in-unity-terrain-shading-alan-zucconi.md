---
title: 'Topographical Maps in Unity: Terrain Shading - Alan Zucconi'
url: https://www.alanzucconi.com/2022/04/19/topographical-maps/
author: Alan Zucconi
published: '2022-04-19'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will teach you how to recreate a very popular effect in games: topographical maps.

![](../../assets/477e574efe94a516.gif)


![](../../assets/477e574efe94a516.gif)

This is a two-part series, which will cover all the necessary aspects—from the Maths to the shader code—to make this possible:

A link to download the full Unity package is also available at the end of the tutorial.

## Introduction

Maps have always been part of modern video games. From “Super Mario World” to “Pokémon”, they became somehow iconic, and nowadays is hard to find an exploration game which does not feature any kind of map.

![](../../assets/d5dae97f2f00a83f.jpg)


![](../../assets/d5dae97f2f00a83f.jpg)

Some games, on the other hand, delegate to the map a central part of the core gameplay. This is definitely the case for [Firewatch](https://store.steampowered.com/app/383870/Firewatch/) (below), the critically acclaimed title developed by [Campo Santo](https://twitter.com/camposanto) in 2016.

![](../../assets/80cad460177cafa3.jpg)

In most games, Firewatch included, the map is actually pre-rendered on a texture. This gives full artistic control, but strongly limits the possibility of real-time terrain editing. The purpose of this tutorial is to show how to render a **Unity terrain** into a **topographical map**, using just a **shader** and a **post-processing effect**.

Several other games are featuring, one way or another, topographical maps. For instance, a lot of [Per Aspera](https://store.steampowered.com/app/803050/Per_Aspera/) aesthetics relies on them to better convey the asperity of the Martian terrain (below).

![](../../assets/8a0eb702205366f3.jpg)


![](../../assets/8a0eb702205366f3.jpg)

The style used in this tutorial is inspired by [In Other Waters](https://store.steampowered.com/app/890720/In_Other_Waters/) (below), a game developed by [Gareth Damian Martin](https://twitter.com/JumpOvertheAge) which levels are entirely played on topographical maps (well, *bathymetric charts* actually, since the game takes place underwater!). I had a chance to play an early build of the game when it got featured in the Leftfield Collection at EGX Rezzed 2018, and almost immediately after I started working on this tutorial.

![](../../assets/fd6c72bedcf03c87.jpg)


![](../../assets/fd6c72bedcf03c87.jpg)

Yes, it indeed took me four years to publish it. 😅 But at the time I wanted to wait at least for *In Other Waters* to come out first. And by the time it finally did, I had a full-time job as a Lecturer and the pandemic hit. So thank you for being so patient with me!

I also want to mention a similar—yet unrelated—piece of work from Sam Loeschen on Twitter.

## Effect Anatomy

There are countless ways in which topographical maps can be created in a game. The most obvious is to bake them, which means to include a texture which has already the desired effect. This is the case for games like *Firewatch* and *In Other Waters*, where the maps are indeed images which were authored externally.

While this approach works very well for a variety of cases, it is not the most exciting as it prevents from performing any real-time terrain manipulation. For this reason, the effect presented in this tutorial is completely done at run-time. If your terrain height changes, so will your map.

Out of the many possible ways in which such an effect can be achieved, I have chosen a rather simple—yet effective—one. This works in two steps, which are covered in two separate articles, both relying on two separated types of shaders.

It is worth mentioning that the current tutorial is based on the Unity built-in pipeline. However, it could technically be re-implemented for the Universal or the High-Definition pipelines as well.

### Part 1: Terrain Shading

The first step uses a custom material to paint each pixel a different colour, based on its y coordinate in world space. This is done using a technique not dissimilar to how Cel shading works:

## Part 2: Edge Detection

The second step operated on tops of the first one. A postprocessing effect is reacting to changes in colour, drawing pixels in between the boundaries of two regions:

Once both textures are available, they can be used to simulate a variety of different maps. This is because both the shading and the outlines are separate, so they can be combined as you like. As it often happen in my tutorials, I have made a very simple examples which exists only to showcase a bare minimum setup. If you end up using this tutorial for your own game, please feel free to reach out to me as I would be very happy to see how you managed to include and elevate this aesthetics.

### ⭐ Recommended Unity Assets

## Terrain Preparation

### Step 0: Creating the Terrain

The first step to create a topographical map out of a Unity terrain is to… create the terrain itself! You can add a terrain object to your scene by click on *GameObject > 3D Object > Terrain*. This will add a new game object which contains a special component called “*Terrain*“.

![](../../assets/17e7619608011fe6.png)

You can use the various tools offered to edit the terrain to your liking. Note that every time a new terrain game object is created this way, Unity will also create an asset called “*New Terrain*” in the “*Assets*” folder. That is the file that stores the information about the terrain, grass and trees.

When you are satisfied with your terrain, it might look like this:

![](../../assets/69ee880514842319.png)

### Step 1: Topological Shader

Topographical maps usually show lines at fixed height intervals. Drawing these lines in a single shader is tricky, so the best way is to solve a simpler problem first. Instead of drawing lines, it is much easier to colour the terrain based on is height, as seen in the image below:

![](../../assets/3670e58659fc104e.png)

For better artistic control, we use a ramp that maps each specific height interval to a different colour. The image below has been generated using the ramp below:

![](../../assets/6a3f7669ef10b1b3.png)

You are not limited to grayscale. Quite the opposite, you can associate different colours to different height intervals to obtain the shaded look often seen in other geographical maps (below).

![](../../assets/75d4156cbd30782f.jpg)

## Creating the Shader

The next step is to create a custom shader that changes the colour of the terrain based on its height. Since this is a stylised effect that does not require any lighting, we can start from a basic **Unlit Shader**.

### Retrieving the World Position

By default, the Unlit Shader created by Unity does not provide a way to access the world position of the 3D model that is applied to. Correcting this is very easy, but the way to do it changes depending on the type of shader you started from. The default Unlit Shader is a **Vertex and Fragment Shader**, because it essentially uses two steps to render a 3D model. You can find more information in the tutorial called [Vertex and Fragment Shaders in Unity3D](https://www.alanzucconi.com/2015/07/01/vertex-and-fragment-shaders-in-unity3d/), but as a massive oversimplification, this is how they work.

First, a **vertex function** is evaluated for each vertex of the model. Its main purpose is to use the position, rotation and scale of the game object (along with the current camera) to find where the model needs to be drawn on the screen. It basically maps the model, which lives in a 3D scene, onto a flat 2D screen. The vertex function can also be used to retrieve other important pieces of information, such as the world position of each vertex. This is done by filling a data structure that Unity calls `v2f`

(meaning: *vertex to fragment*).

The second step in the shader is the **fragment function**, which uses the `v2f`

structure to determine the final colour of each pixel (which is often, even though improperly, called a *fragment*).

This workflow is different if you are using a **Surface Shader**. To see how to retrieve the world position of a vertex from a surface shader you can refer to this tutorial on [Surface Shaders in Unity](https://www.alanzucconi.com/2015/06/17/surface-shaders-in-unity3d/).

The first step to make the vertex position available to the fragment function is to add a variable to the `v2f`

structure, which in this case has been called `wPos`

.

struct v2f { // Not needed //float2 uv : TEXCOORD0; //UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; // World position float3 wPos : TEXCOORD1; };

The real calculation happens in the vertex function, which is called `vert`

in a newly created Unlit shader. The position of a vertex in object space (which is, assuming the 3D model is centred at ![Rendered by QuickLaTeX.com \left(0,0,0\right)](../../assets/9c927f629b30dd3d.png)

![Rendered by QuickLaTeX.com \left(1,1,1\right)](../../assets/bce2cc7e9acfa390.png)

![Rendered by QuickLaTeX.com \left(0,0,0\right)](../../assets/9c927f629b30dd3d.png)

`appdata`

. From there, calculating the actual world position can be done performing a multiplication with the matrix `unity_ObjectToWorld`

, which Unity initialises with the parameters of the camera.

v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); // Not needed //o.uv = TRANSFORM_TEX(v.uv, _MainTex); //UNITY_TRANSFER_FOG(o,o.vertex); // World position o.wPos = mul(unity_ObjectToWorld, v.vertex).xyz; return o; }

In linear algebra, matrix multiplication can be used to rotate and translate objects. To understand how this works, you can refer to [A Gentle Primer on 2D Rotations](https://www.alanzucconi.com/?p=4275).

### Terrain Shading

Now that the `v2f`

structure has been initialised with the vertex position, it is possible to complete this shader by adding the layered effect to the fragment function, which Unity calls `frag`

.

The idea is to remap heights to colours, using a ramp texture provided to the shader using a **Material**. To perform this remapping, however, we first need to know which height corresponds to the left side of the texture, and which one to the right side. To do this, we need to add two properties to the shader which I have called `_MinY`

and `_MaxX`

.

Textures are sampled using UV coordinates, which go from ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

`v2f`

so that `_MinY`

is mapped to ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

`_MaxX`

is mapped to ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

**linear interpolation**, and it has been explored in great details in several articles, including [Linear Interpolation](https://www.alanzucconi.com/2021/01/24/linear-interpolation/) and [The Secrets of Colour Interpolation](https://www.alanzucconi.com/2016/01/06/colour-interpolation/).

fixed4 frag (v2f i) : SV_Target { // Not needed // sample the texture //fixed4 col = tex2D(_MainTex, i.uv); // apply fog //UNITY_APPLY_FOG(i.fogCoord, col); // i.wPos.y: [_MinY, _MaxY] // u: [0, 1] fixed u = (i.wPos.y - _MinY) / (_MaxY - _MinY); u = saturate(u); // Posterize fixed4 col = tex2D(_RampTex, fixed2(u, 0.5)); return col; }

The height is retrieved from the `y`

component of `wPos`

, and we expect its value to be in between `_MinY`

and `_MaxY`

. Subtracting `_MinY`

remaps it between ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

`_MaxY - _MinY`

. Finally, dividing by `_MaxY - _MinY`

produces a variable between ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


This variable, `u`

, is then used to sample the ramp texture, to retrieve the final colour of the pixel. The result can be seen below:

## What’s Next…

This first part covered the terrain shading necessary to create a topographical map effect in Unity. The second part of this series will cover the edge detection.

### Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The [Unity package](https://www.patreon.com/posts/64968718) contains everything needed to replicate the visual seen in this tutorial, including the shader code, the C# scripts and a test scene with the terrain.

![](../../assets/477e574efe94a516.gif)


![](../../assets/477e574efe94a516.gif)

## Leave a Reply Cancel reply