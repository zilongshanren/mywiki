---
title: 'Journey Sand Shader: Specular Reflection - Alan Zucconi'
url: https://www.alanzucconi.com/2019/10/08/journey-sand-shader-4/
author: Alan Zucconi
published: '2019-10-08'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the fourth part of the online series dedicated to Journey Sand Shader.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) - Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) **Part 4.**[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057)- Part 5.
[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059) - Part 6.
[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

In this fourth post, we will focus on the specular reflections that make the dunes look like an ocean of sand.

One of the most intriguing effects of *Journey*‘s sand rendering, is the way dunes shine in the light. Such reflection is called **specular**, from the Latin *speculum*, which means *mirror*. **Specular reflection** is an umbrella term that includes all those types of interactions in which light is strongly reflected in one direction, instead of being scattered and diffuse. It is because of specular reflections that both water and polished surfaces appear to shine at certain angles.

*Journey* features three different types of specular reflections: **rim lighting**, **ocean specular** and **glitter reflections**, as seen in the diagram below. In this lecture, we will address the first two.

![](../../assets/c1790bbaf5a01898.png)

## Rim Lighting

You might have noticed that each level of *Journey* features a limited set of colours. While this adds to its strong and clean aesthetic, it is rather problematic for the sand rendering. Dunes are only rendered using a handful of shades, so it might be impossible to distinguish where one ends and another starts in the far distance.

To compensate for this, the edge of each dune presents a subtle shimmering effect, which highlights its contours. This prevents dunes from disappearing into the horizon, and gives the illusion of a much larger and complex environment.

Before exploring how such an effect can be achieved, let’s extend the **lighting function** presented in the first lecture to include both the **diffuse colour** (previously discussed in [Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052)) and a new generic specular component.

float4 LightingJourney (SurfaceOutput s, fixed3 viewDir, UnityGI gi) { // Lighting properties float3 L = gi.light.dir; float3 N = s.Normal; // Lighting calculation float3 diffuseColor = DiffuseColor (N, L); float3 rimColor = RimLighting (N, V); // Combining float3 color = diffuseColor + rimColor; // Final color return float4(color * s.Albedo, 1); }

In the snippet above we can see that the specular component of the rim lighting, called `rimColor`

, is simply added to the original diffuse colour.

### Fresnel Reflectance

There are many ways in which a rim lighting can be achieved. The most common in shader coding relies on the well-known **Fresnel reflectance model**.

To understand the equation behind the Fresnel reflectance, it is helpful to visualise where it occurs. The diagram below shows a dune seen by a camera (in blue). The red arrow indicates the **surface normal** to the top of the dune, which is where we want the specular reflection to be. It is easy to see that all edges of the dune share a similar property: their normal (![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

**view direction** (![Rendered by QuickLaTeX.com V](../../assets/c746ecbc0d34d082.png)


![](../../assets/503499a83f699f73.png)

Similarly to what we have done in [Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052), we can use the **dot product** between ![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com V](../../assets/c746ecbc0d34d082.png)

![Rendered by QuickLaTeX.com N \cdot V](../../assets/c22c31a8ea270ba2.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1- N \cdot V](../../assets/98b8a596b2067697.png)


Using ![Rendered by QuickLaTeX.com 1- N \cdot V](../../assets/98b8a596b2067697.png)

*sharper,* we can simply take its power. The power of a value between ![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


The Fresnel reflectance model states that the intensity of light ![Rendered by QuickLaTeX.com I](../../assets/c2ab42bcab55cee7.png)


(1) ![Rendered by QuickLaTeX.com \begin{equation*} I = \left(1 -N \cdot V\right)^\mathit{power} * \mathit{strength}\end{equation*}](../../assets/d8c8e68edb454ee7.png)


where ![Rendered by QuickLaTeX.com \mathit{power}](../../assets/890ac3ea698809b9.png)

![Rendered by QuickLaTeX.com \mathit{strength}](../../assets/dd65a08ba1b437f1.png)

![Rendered by QuickLaTeX.com \mathit{power}](../../assets/890ac3ea698809b9.png)

![Rendered by QuickLaTeX.com \mathit{strength}](../../assets/dd65a08ba1b437f1.png)

*specular* and *gloss*, although naming conventions may vary.

Equation ([1](https://www.alanzucconi.com#id1739186210)) translates very easily to code:

float _TerrainRimPower; float _TerrainRimStrength; float3 _TerrainRimColor; float3 RimLighting(float3 N, float3 V) { float rim = 1.0 - saturate(dot(N, V)); rim = saturate(pow(rim, _TerrainRimPower) * _TerrainRimStrength); rim = max(rim, 0); // Never negative return rim * _TerrainRimColor; }

Its result can be seen in the animation below.

## Ocean Specular

One of the most peculiar aspects of *Journey*‘s gameplays is that, at times, the player is literally surfing on the dunes. Lead Engineer John Edwards explained how [thatgamecompany](https://twitter.com/thatgamecompany) indeed wanted the sand to feel more like a fluid, than a solid.

This is not entirely incorrect, since sand can be thought of as a rough approximation of a fluid. And under certain circumstances, for instance in an hourglass, it does behave like one.

To reinforce the idea that sand could have a fluid component, *Journey* adds a second specular effect, which is often seen on liquid bodies. John Edwards referred to this as **ocean specular**, and the idea is to get the same type of reflection that you would see on an ocean or lake at sunset (below).

![](../../assets/3f37a0d57775ec5f.jpg)

As before, let’s change the lighting function `LightingJourney`

to include a new type of specular reflection.

float4 LightingJourney (SurfaceOutput s, fixed3 viewDir, UnityGI gi) { // Lighting properties float3 L = gi.light.dir; float3 N = s.Normal; float3 V = viewDir; // Lighting calculation float3 diffuseColor = DiffuseColor (N, L); float3 rimColor = RimLighting (N, V); float3 oceanColor = OceanSpecular (N, L, V); // Combining float3 specularColor = saturate(max(rimColor, oceanColor)); float3 color = diffuseColor + specularColor; // Final color return float4(color * s.Albedo, 1); }

### ⭐ Recommended Unity Assets

Specular reflections on water are often implemented using the **Blinn-Phong reflectance**, which is an inexpensive solution for shiny materials. It was first described by James F. Blinn in 1977 (paper: “[Models of Light Reflection for Computer Synthesized Pictures](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=D97C4795B8C3D9B479421AC3B7882EE3?doi=10.1.1.131.7741&rep=rep1&type=pdf)“), as an approximation of an earlier shading technique developed by Bùi Tường Phong in 1973 (paper: “[Illumination for Computer Generated Pictures](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.330.4718&rep=rep1&type=pdf)“).

Using Blinn-Phong shading, the luminosiry ![Rendered by QuickLaTeX.com I](../../assets/c2ab42bcab55cee7.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} I = \left(N \cdot H\right)^\mathit{power} * \mathit{strength}\end{equation*}](../../assets/7c9997d6f501733b.png)


where

(3) ![Rendered by QuickLaTeX.com \begin{equation*} H = \frac{V + L}{\left \| V+L \right \|}\end{equation*}](../../assets/7a41a093bf52b0e7.png)


The denominator of ([3](https://www.alanzucconi.com#id461237427)) divides the vector ![Rendered by QuickLaTeX.com V+L](../../assets/2b2be3e223720206.png)

![Rendered by QuickLaTeX.com H](../../assets/21b7e9a6311e544d.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

`normalize`

. Geometrically speaking, ![Rendered by QuickLaTeX.com H](../../assets/21b7e9a6311e544d.png)

![Rendered by QuickLaTeX.com V](../../assets/c746ecbc0d34d082.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

**half vector**.

![](../../assets/15c4fef93e53bfb6.png)

For a more detailed description of the Blinn-Phong reflectance, you can read [Physically Based Rendering and Lighting Models](https://www.alanzucconi.com/2015/06/24/physically-based-rendering/). Below, you can see a simple implementation in shader code.

float _OceanSpecularPower; float _OceanSpecularStrength; float3 _OceanSpecularColor; float3 OceanSpecular (float3 N, float3 L, float3 V) { // Blinn-Phong float3 H = normalize(V + L); // Half direction float NdotH = max(0, dot(N, H)); float specular = pow(NdotH, _OceanSpecularPower) * _OceanSpecularStrength; return specular * _OceanSpecularColor; }

The following animation provides a comparison between a traditional diffuse Lambertian shading and a specular Blinn-Phong one:

## What’s Next…

In this fourth part of the online series about the sand rendering in Journey, we focused on the shimmering reflections that make Journey’s dunes appear almost like an ocean.

In the next part, [Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059), we will continue working on the specular reflections, adding tiny glitters to the dunes to make it even more realistic.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) - Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) **Part 4.**[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057)- Part 5.
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