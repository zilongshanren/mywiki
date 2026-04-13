---
title: 'Journey Sand Shader: Diffuse Colour - Alan Zucconi'
url: https://www.alanzucconi.com/2019/10/08/journey-sand-shader-2/
author: Alan Zucconi
published: '2019-10-08'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the online series dedicated to Journey Sand Shader.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) **Part 2.**[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052)- Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) - Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) - Part 5.
[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059) - Part 6.
[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

In this second post we will focus on the lighting model used in the game, and how to recreate it in Unity.

In the previous instalment of this series, we have laid the foundation for what is going to become our take on Journey’s sand shader. As previously discussed, the **lighting function** is used in **surface shaders** to calculate the light contribution, which results in a surface exhibiting shades and highlights. In Journey, we have identified several effects that fall into this category. We will start by tackling the most basic (and simple) effect that is at the very core of this shader: its **diffuse lighting**.

![](../../assets/8f169aa12f342002.png)

For now, let’s ignore all of the other effects and components, so that we can only focus on the **sand lighting**.

The custom lighting function seen in the previous post, called `LightingJourney`

, is simply delegating the calculation of the sand’s diffuse colour to a function called `DiffuseColor`

.

float4 LightingJourney (SurfaceOutput s, fixed3 viewDir, UnityGI gi) { // Lighting properties float3 L = gi.light.dir; float3 N = s.Normal; // Lighting calculation float3 diffuseColor = DiffuseColor(N, L); // Final color return float4(diffuseColor, 1); }

By keeping each effect self-contained in its own function, we are programming in a more modular and clean way.

## The Lambertian Reflectance

Before introducing Journey’s diffuse lighting, it is good to start showing what a “basic” diffuse lighting function looks like. The simplest lit shading technique for matte materials is based on a principle known as **Lambertian reflectance**. It is a model that well approximate the look of most non-shiny, non-metallic surfaces. It is named after Swiss polymath **Johann Heinrich Lambert**, who introduced the concept in 1760.

There is a basic idea behind the concept of Lambertian reflectance: *the brightness of a surface depends on the amount of light it receives*. Geometrically, this can be seen in the diagram below, where a sphere is illuminated by a light source far away. While the red and green regions of the sphere receive the same amount of light, they have significantly different surface areas. If light on the red region is spread over a larger area, it means that each red unit receives less light, compared to the green ones.

![](../../assets/02734e79c40b4cbb.png)

Technically speaking, the Lambertian reflectance depends on the relative angle between the *surface* and the *incoming light*. Mathematically, we say that it is a function of the **surface normal** and the **light direction**. Those quantities are expressed using two vectors of length one (called **unit vectors**), ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

*directions* in the context of shader coding.


From a closer inspection, we can see that a surface receives the maximum amount of light when its normal is aligned with the light direction. Conversely, no light is received when the two unit vectors are orthogonal to each other.

![](../../assets/707de5ff1386f8c8.png)

It appears that the angle between ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com 100\%](../../assets/ebb002339cfff8eb.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 0\%](../../assets/0808ef679bd38dfb.png)

![Rendered by QuickLaTeX.com 90^{\circ}](../../assets/beeb8f069f99cde8.png)

*vector algebra*, you might have recognised that the quantity that represents the Lambertian reflectance ![Rendered by QuickLaTeX.com I](../../assets/c2ab42bcab55cee7.png)

![Rendered by QuickLaTeX.com N \cdot L](../../assets/c572b3bd99533e5a.png)

*N dot L*“), where the operator ![Rendered by QuickLaTeX.com \cdot](../../assets/5202de5cdcd354ab.png)

**dot product**.

(1) ![Rendered by QuickLaTeX.com \begin{equation*} I = N \cdot L\end{equation*}](../../assets/ab67869c436cbabc.png)


The dot product measures how “aligned” two vectors are to each other, and ranges from ![Rendered by QuickLaTeX.com +1](../../assets/07166c3ac7d7ae94.png)

![Rendered by QuickLaTeX.com -1](../../assets/5209a4a606950b66.png)

[Physically Based Rendering and Lighting Models](https://www.alanzucconi.com/2015/06/24/physically-based-rendering/).

### Implementation

Both ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

`s.Normal`

and `gi.light.dir`

. For simplicity, they will be renamed just `N`

and `L`

in the shader code.

float3 DiffuseColor(float3 N, float3 L) { float NdotL = saturate( dot(N, L) ); return NdotL; }

The `saturate`

function keeps the value clamped between ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com -1](../../assets/5209a4a606950b66.png)

![Rendered by QuickLaTeX.com +1](../../assets/07166c3ac7d7ae94.png)


float NdotL = max(0, dot(N, L) );

### ⭐ Recommended Unity Assets

## The Diffuse Contrast Reflectance

While the Lambertian reflectance shades most materials well, it is neither physically based nor photorealistic. Historically speaking, most 3D games from the older generation heavily relied on Lambertian shaders. Games which are relying on this technique often *feel* old, because they might unintentionally resemble the aesthetic of older titles. Unless this is your intention, the Lambertian reflectance should be avoided in favour of more modern approaches.

One such model is the [Oren-Nayar reflectance model](https://en.wikipedia.org/wiki/Oren%E2%80%93Nayar_reflectance_model), which was originally discussed in [Generalization of Lambert’s Reflectance Model](http://www1.cs.columbia.edu/CAVE/publications/pdfs/Oren_SIGGRAPH94.pdf) in a paper published in 1994 by Michael Oren and Shree K. Nayarin. The Oren-Nayar model is a generalisation of the Lambertian reflectance, and is specifically designed for rough surfaces. The developers of Journey initially wanted to use Oren-Nayar reflectance as the base for their sand shader. However, that idea has been dropped, due to its computational cost.

In his talk from 2013, Technical Artist John Edwards explained that the actual reflectance model devised for Journey’s sand was based on a series of trials and errors, Their intention was not to recreate a photorealistic rendering of a desert, but to give life to a precise and immediately recognisable aesthetics.

Following his indication, the shading model they have devised follows this equation:

(2) ![Rendered by QuickLaTeX.com \begin{equation*} I = 4 * \left( \left(N\odot \left[1, 0.3, 1\right]\right) \cdot L\right)\end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-73d1932fd0e9821f4d3f6697a2c72f0e_l3.png)


where ![Rendered by QuickLaTeX.com \odot](../../assets/a3eba2add5b3cda5.png)

**element-wise product** between two vectors.

float3 DiffuseColor(float3 N, float3 L) { N.y *= 0.3; float NdotL = saturate(4 * dot(N, L)); return NdotL; }

The reflectance model ([2](https://www.alanzucconi.com#id1615438801)) was referred by John Edwards simply as **diffuse contrast**, so that is the name that will be used for the rest of this tutorial.

The animation below shows a comparison between a Lambertian shading (left) and Journey’s diffuse contrast (right).

## From Black & White To Colours

All the animations seen so far are black and white because they were showing the values of their reflectance model, which ranges from ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

`NdotL`

as the coefficient to interpolate between two colours: one for the fully shaded and one for the fully lit sand.

float3 _TerrainColor; float3 _ShadowColor; float3 DiffuseColor(float3 N, float3 L) { N.y *= 0.3; float NdotL = saturate(4 * dot(N, L)); float3 color = lerp(_ShadowColor, _TerrainColor, NdotL); return color; }

## What’s Next…

In this second part of the online series about the sand rendering in Journey, we focused on how the dunes were shaded, using a custom reflectance model.

In the next part, [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054), we will explore how to give three-dimensionality to the dunes using bump mapping.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) **Part 2.**[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052)- Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) - Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) - Part 5.
[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059) - Part 6.
[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

### Credits

The videogame [Journey](http://thatgamecompany.com/journey/) is developed by **Thatgamecompany** and published by **Sony Computer Entertainment**. It is available for PC ([Epic Store](https://www.epicgames.com/store/en-US/product/journey/home)) and PS4 ([PS Store](https://www.playstation.com/en-gb/games/journey-ps4/)).

The 3D models of the dunes, backgrounds and lighting settings were made by [Jiadi Deng](https://github.com/AtwoodDeng/JourneySand).

The 3D model of the Journey’s player was found on the (now closed) FacePunch forum.

## Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

If you want to recreate this effect, the full Unity package is available for download on [Patreon](https://www.patreon.com/posts/30540389/). It includes everything needed, from the shaders to the 3D models.

## Leave a Reply Cancel reply