---
title: Sprite Doodle Shader Effect - Alan Zucconi
url: https://www.alanzucconi.com/2019/04/16/sprite-doodle-shader-effect/
author: Alan Zucconi
published: '2019-04-16'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This online course will teach you how to recreate a popular sprite doodle effect using Shaders in Unity. If this is an aesthetic that you want in your game, this tutorial will show you how to achieve it without the need to draw dozens of different images.

Such a style has become increasingly popular over the past few years, with many games such as [GoNNER](https://store.steampowered.com/app/437570/GoNNER/) and [Baba is You](https://store.steampowered.com/app/736260/Baba_Is_You/) heavily relying on it.

![](../../assets/2678a073261163cf.gif)

This tutorial covers everything you need to know, from teaching the basics of shader coding to the maths used. At the end, you will also find a link to download the complete Unity package.

This series is also strongly inspired by the success of [Doodle Studio 95!](https://fernandoramallo.itch.io/doodle-studio-95).

## Introduction

In my blog, I tend to cover rather advanced topics, from the [mathematics of inverse kinematics](https://www.alanzucconi.com/?p=8368) to [atmospheric Rayleigh scattering](https://www.alanzucconi.com/?p=7472). Making such complex subjects understandable to a larger audience is something that I find very rewarding. But the number of people who are both interested and have the necessary technical knowledge to understand them is not that large. So it should not be surprising that sometimes, the things that go viral, are the very simple ones. This is definitely the case for one of [Nick Kaman](https://twitter.com/SmashyNick)‘s recent tweet, in which he showed how to create a **doodle effect** in Unity.

After 1000 likes and 4000 retweets, it was obvious that there is a great need for simpler tutorials that even people with little to no background in shader coding can follow.

If you are looking at a professional, effective way to animate 2D sprites with full artistic control, then I cannot recommend [Doodle Studio 95!](https://fernandoramallo.itch.io/doodle-studio-95) enough (GIF below). You can also see a selection of games on itch.io that are using it [here](https://itch.io/games/made-with-doodle-studio-95).

![](../../assets/4d33958c2ae93445.gif)

## Anatomy of the Doodle Effect

In order to reproduce the doodle effect, we first need to understand how it works and which techniques have been used.

**Shader Effect.** First of all, we want this effect to be as light as possible, requiring no additional scripts. This is possible through the use of **shaders**, instructs Unity how to render 3D models (even flat ones!) on the screen. If you are unfamiliar with the world of **shader coding**, [A Gentle Introduction to Shaders](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) is probably the best resource to get you started.

**Sprite Shader.** Unity comes with many types of shaders. If you are using the 2D tools provided by Unity, you might want to work with **sprites**. If this is the case, what you need is a **Sprite Shader**, which is a special type of shaders designed to be compatible with Unity’s `SpriteRenderer`

. Alternatively, you can start from a more traditional **Unlit shader**.

**Vertex Displacement.** When drawing sprites by hand, no two frames are going to be the same. What we want is to somehow make a sprite “wobble” to simulate such effect. There is a very efficient way to do this in shaders, which relies on **vertex displacement**. This is a technique that allows changing the position of a 3D object’s vertices. If we nudge them randomly, we can get the desired effect.

**Snapping Time.** Hand-drawn animations usually have a low framerate. If we want to simulate – let’s say – five frames per second, we need to change the position of the sprite vertices five times per second. However, Unity is likely to run the game a much higher refresh rate; possibly 30 or even 60 frames per second. To make sure our sprite does not change 60 times per second, we need to work on the timing component of the animation.

### Step 1: Extending the Sprite Shader

If you try to create a new shader from Unity, you will be prompted with a rather limited selection. The closest shader we can start from is the **Unlit Shader**, although is not necessarily the best one for this specific application.

If we want this doodle shader to be fully compatible with Unity’s `SpriteRenderer`

, we need to extend its existing **Sprite Shader**. Unfortunately, there is no way to access it from within Unity itself.

The way to get it is to visit the [Unity download archive](https://unity3d.com/get-unity/download/archive) and to download the **Build in shaders** pack for the version of Unity you are currently working on. That is a zip file which contains the source code for all the shaders that are shipped with that specific build of Unity.

![](../../assets/9f94bd0c81731d8a.png)

Once downloaded, extract it and look for a file called `Sprites-Diffuse.shader`

in the folder `builtin_shaders-2018.1.6f1\DefaultResourcesExtra`

. That is the file we will use for this tutorial.

![](../../assets/559682bce9a99489.png)

### Step 2: Vertex Displacement

Inside the `Sprites-Diffuse.shader`

there is a function called `vert`

; that is the **vertex function** previously discussed. Its name is not important, as long as it matches the one indicated in the `vertex:`

section of the `#pragma`

directive:

#pragma surface surf Lambert vertex:vert nofog nolightmap nodynlightmap keepalpha noinstancing

The vertex function, in a nutshell, is invoked on each vertex of a 3D model and decides how to map it on the 2D screen space. For the purpose of this tutorial, we are only interested in understanding how to displace an object.

The parameter `appdata_full v`

contains a field called `vertex`

, which contains the 3D position of each vertex in **object space**. Changing its value moves the vertex. So, for instance, the snippet below would translate an object with this shader by one unit along the X axis.

void vert (inout appdata_full v, out Input o) { v.vertex = UnityFlipSprite(v.vertex, _Flip); v.vertex.x += 1; #if defined(PIXELSNAP_ON) v.vertex = UnityPixelSnap (v.vertex); #endif UNITY_INITIALIZE_OUTPUT(Input, o); o.color = v.color * _Color * _RendererColor; }

By default, 2D games made in Unity only operates on the X and Y axes, so we need to change `v.vertex.xy`

to move the sprite on the 2D plane.

### ⭐ Recommended Unity Assets

#### Random Displacement

The doodle effect alters the position of each vertex randomly. Sampling **random numbers** in a shader have always been a tricky subject. This is mostly due to the stateless architecture of GPUs, which makes harder (and inefficient) to replicate the same algorithm used by most libraries (including `Mathf.Random`

).

The original submission by Nick Kaman relied on a noisy texture that, when sampled, gave the illusion of randomness. Depending on your context, this might not be the most efficient approach because it doubles the number of texture lookups that the shader has to perform.

Hence, many shaders rely on rather obscure and chaotic functions that, even though they fully deterministic, look pattern-less to us. And since they have to be stateless, each random number has to be generated with its own seed. This works well because the position of each vertex should be unique. We can use it to associate a random number to each vertex. We will discuss the implementation of this random function later; for now, let’s call it `random3`

.

We can use `random3`

to generate a random displacement for each vertex. In the example below, the random numbers are scaled with a property called `_NoiseScale`

, which allows controlling how strong the displacement is.

void vert (inout appdata_full v, out Input o) { ... float2 noise = random3(v.vertex.xyz).xy * _NoiseScale; v.vertex.xy += noise; ... }

Now we have to actually write the code for `random3`

.

![](../../assets/64bf38ca5d7ddfde.png)

#### Randomness In a Shader

One of the most used and iconic pseudo-random functions used in shaders comes from a 1998 paper by W.J.J. Rey, titled “*On generating random numbers, with help of y= [(a+x)sin(bx)] mod 1*“.

float rand(float2 co) { return fract(sin(dot(co.xy ,float2(12.9898,78.233))) * 43758.5453); }

The function is deterministic (meaning that is it not *truly* random), but behaves so erratically that it looks completely random. Such functions are called **pseudo-random**. For this specific tutorial, I am using a more advanced function, by [Nikita Miropolskiy](https://www.shadertoy.com/view/XsX3zB).

Generating pseudo-random number in a shader is a very complex subject. If you are interested in knowing more about it, [The Book of Shaders](https://thebookofshaders.com/10/) has a nice write up that is related to this. Also, [Patricio Gonzalez Vivo](https://gist.github.com/patriciogonzalezvivo) has compiled a large repository of pseudo-random functions that you can use in your shaders, titled [GLSL noise](https://gist.github.com/patriciogonzalezvivo/670c22f3966e662d2f83).

### Step 3: Adding Time

With the code written so far, we are in a position where each point is displaced by the same amount each frame. This makes for a wonky sprite, not for a doodle effect. To fix this, we need to find a way to change the effect over time. One of the easiest ways is to use both the vertex position and the current time to generate the random number.

In this specific case, I have simply added the current time in seconds, `_Time.y`

, to the vertex position.

float time = float3(_Time.y, 0, 0); float2 noise = random3(v.vertex.xyz + time).xy * _NoiseScale; v.vertex.xy += noise;

More advanced effects might more sophisticated ways to integrate time into their equation. But since we are only interested in a discontinuous random effect, adding the two values is more than enough.

![](../../assets/b7a894267a0eb7b6.gif)

#### Snapping Time

The major issue of adding `_Time.y`

is that this causes the sprite to animate each frame. This is undesirable, since most hand-drawn animations have a low framerate. Instead of being continuous, the time component should be discretised. This means that if we want five frames per second, it should only change five times per second. To use a more familiar term, the time should “*snap*” to one-fifth of a second. The only allowed values should be ![Rendered by QuickLaTeX.com \sfrac{0}{5}=0](../../assets/b8979de174756e08.png)

![Rendered by QuickLaTeX.com \sfrac{1}{5}=0.2](../../assets/9bc819bca27a0ebc.png)

![Rendered by QuickLaTeX.com \sfrac{2}{5}=0.4](../../assets/a49ebdcc19052d13.png)

![Rendered by QuickLaTeX.com \sfrac{3}{5}=0.6](../../assets/d4926a28c6b27b26.png)

![Rendered by QuickLaTeX.com \sfrac{4}{5}=0.8](../../assets/b73e0774cc5954b0.png)

![Rendered by QuickLaTeX.com \sfrac{5}{5}=1](../../assets/534e0babe3586306.png)


Snapping has been covered already on this blog, in the article [How To Snap To Grid](https://www.alanzucconi.com/2015/07/22/how-to-snap-to-grid-in-unity3d/). In that article, it was proposed a solution to the problem of snapping the position of an object on a spatial grid. The mathematics, and consequently the code, are the same if we want to snap a time to a temporal grid.

The following function takes a number `x`

and snaps to integer multiples of `snap`

.

inline float snap (float x, float snap) { return snap * round(x / snap); }

Which updates our code to:

float time = snap(_Time.y, _NoiseSnap); float2 noise = random3(v.vertex.xyz + float3(time, 0.0, 0.0) ).xy * _NoiseScale; v.vertex.xy += noise;

![](../../assets/b8ae00399d104e5d.gif)

## Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity package for this effect [here](https://www.patreon.com/posts/26141364).

### Additional Resources…

In the past few months, there has been a surge in the number of games which feature a doodle aesthetics. I want to believe this is also due to the success of [Doodle Studio 95!](https://fernandoramallo.itch.io/doodle-studio-95-educational-license), a tool for Unity developed by [Fernando Ramallo](https://twitter.com/compositeredfox). If this is the style you want for your game, I strongly advise you to invest in this awesome tool.

## Leave a Reply Cancel reply