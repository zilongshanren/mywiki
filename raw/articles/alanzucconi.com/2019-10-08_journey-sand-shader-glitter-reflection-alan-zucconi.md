---
title: 'Journey Sand Shader: Glitter Reflection - Alan Zucconi'
url: https://www.alanzucconi.com/2019/10/08/journey-sand-shader-5/
author: Alan Zucconi
published: '2019-10-08'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the fifth part of the online series dedicated to Journey Sand Shader.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) - Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) - Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) **Part 5.**[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059)- Part 6.
[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

In this fifth post, we will recreate the shimmering reflections that are typically seen on sand dunes.

Shortly after the publication of this series, [Julian Oberbeck](https://twitter.com/fleity) and [Paul Nadalack](https://twitter.com/littleBugHunter) made their own attempt at recreating a Journey-inspired scene in Unity. You can see in the thread below how they have improved the glitter reflection to have more temporal coherence. You can read more about their implementation on IndieBurg’s article [Mip Map Folding](https://indieburg.com/blog/posts/20200110-mip-map-folding).

The previous lecture in this online course covered the two basic specular reflections features in *Journey*‘s sand rendering: **rim lighting** and **ocean specular**. This post will explain how to implement the last variant of specular reflection: **glitter**.

![](../../assets/6e3530ca4bd23fda.png)

If you have visited an actual desert, it is hard not to notice how shimmering the sand really is. As discussed in the third lecture, [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054), each grain of sand can potentially reflect light in a random direction. By virtue of sheer numbers, some of these reflected rays will hit the camera. This causes random points of the sand to appear as very bright. These glitters are also very sensitive to movement, as even the slightest misalignment will prevent the reflected rays from hitting the camera.

Other games, including [Astroneer](https://store.steampowered.com/app/361420/ASTRONEER/) and [Slime Rancher](https://store.steampowered.com/app/433340/Slime_Rancher/), have used glitter reflections for sand and caves.

It is easier to appreciate these shimmering specs in the zoomed images below:

![]() | ![]() |

It is undeniably true that the glitter effect that can be seen on real dunes is solely determined by the fact that some grains of sand randomly reflect light back into our eyes. Technically speaking, that is something that we have already modelled in the second part of this online course, [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054), when we have modelled the random distribution of the normals. So why do we need yet another effect for this?

The answer might not be so obvious. Let’s imagine that we try replicating the glitter effect using the normals only. Even if all normals would point towards the camera, the sand still would not shimmer. This is because the normals can only reflect as much light as available in the scene. So, at best, that approach could only reflect 100% of the light back (if we had completely white sand).

What we want here, however, is different. To make a pixel appear so bright that light *leaks* on its nearby pixels, the colour must be greater than ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

**bloom filter** is applied to the camera using a **post-processing effect**, colours brighter than ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

**HDR rendering**, where HDR stands for **High Dynamic Range**.

So no, normal mapping cannot be easily used to create glitter surfaces. This is why such an effect is more conveniently implemented as a separate process.

## Microfacet Theory

To approach this scenario more formally, we need to treat the dunes as if they were made out of microscopic mirrors, each one with a random orientation. This approach is called **microfacet theory**, where a **microfacet** is the technical name of one of these tiny mirrors. The Mathematical foundation of most modern shading models is based on microfacet theory, including [Unity’s Standard shader](https://docs.unity3d.com/Manual/shader-StandardShader.html).

The first step is to divide the dune surface in microfacets, and to find the orientation of each one. As already discussed, we have done something similar already in [Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054), where the UV position of the dune’s 3D model was used to sample a random texture. The same approach can be reused here, to associate a random orientation to each microfacet. The size of each microfacet will depend on the scale of the texture, and on its **mipmap level**. Our task is to reproduce a particular aesthetics, not to embark on a quest for photorealism; this approach will be good enough.

Once we have sampled a random texture, we can associate a random direction with each grain of sand/microfacet that makes up the done. Let’s call it ![Rendered by QuickLaTeX.com G](../../assets/9a44c9841f215396.png)

**glitter orientation**, which is the **normal direction** of the grain of sand we are looking at. An incoming ray of light that hits the glitter will be reflected assuming the microfacet as a perfect mirror which is facing the direction ![Rendered by QuickLaTeX.com G](../../assets/9a44c9841f215396.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


![](../../assets/cb2b0e4654e7cca2.png)

Once again, we can use the **dot product** between ![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

![Rendered by QuickLaTeX.com V](../../assets/c746ecbc0d34d082.png)


One approach is to take the power of ![Rendered by QuickLaTeX.com R \cdot V](../../assets/ef926d8af5cd6a5f.png)

[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057&preview=true). If you try, you will see that the result looks very different from what seen in *Journey*. Glitter reflections should be rare, and very bright. The simplest solution is to only consider the glitter reflections for which ![Rendered by QuickLaTeX.com R \cdot V](../../assets/ef926d8af5cd6a5f.png)


### ⭐ Recommended Unity Assets

## Implementation

We can easily implement the glitter effect described in the paragraph above thanks to the `reflect`

function in Cg, which allows calculating ![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)


sampler2D_float _GlitterTex; float _GlitterThreshold; float3 _GlitterColor; float3 GlitterSpecular (float2 uv, float3 N, float3 L, float3 V) { // Random glitter direction float3 G = normalize(tex2D(_GlitterTex, uv).rgb * 2 - 1); // [0,1]->[-1,+1] // Light that reflects on the glitter and hits the eye float3 R = reflect(L, G); float RdotV = max(0, dot(R, V)); // Only the strong ones (= small RdotV) if (RdotV > _GlitterThreshold) return 0; return (1 - RdotV) * _GlitterColor; }

Technically speaking, if ![Rendered by QuickLaTeX.com G](../../assets/9a44c9841f215396.png)

![Rendered by QuickLaTeX.com R](../../assets/f79aae724cd4788a.png)

`reflect`

. While this is true for a static frame, what happens if the lighting source is moving? This could either be because the sun itself is moving, or because there is a point light attached to the player. In both cases, the sand would lose temporal consistency between a frame and the next one, causing the glittering effect to appear at random locations. Using the `reflect`

function, instead, allows for a much more stable rendering.

You can see the result below:

If you remember the first post in this series, the glitter component is added to the final colour.

#pragma surface surf Journey fullforwardshadows float4 LightingJourney (SurfaceOutput s, fixed3 viewDir, UnityGI gi) { float3 diffuseColor = DiffuseColor (); float3 rimColor = RimLighting (); float3 oceanColor = OceanSpecular (); float3 glitterColor = GlitterSpecular (); float3 specularColor = saturate(max(rimColor, oceanColor)); float3 color = diffuseColor + specularColor + glitterColor; return float4(color * s.Albedo, 1); }

That is likely to cause certain pixels to end up with a colour greater than ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057)), so that shimmering grains of sand can also be seen where the dunes are well lit.

There are many ways in which this technique can be improved. It all depends on the final look that you want to achieve. Both [Astroneer](https://store.steampowered.com/app/361420/ASTRONEER/) and [Slime Rancher](https://store.steampowered.com/app/433340/Slime_Rancher/), for example, rely on this effect only at night. This can be achieved by modulating the strength of the glitter effect based on the direction of the sunlight.

The quantity `max(dot(L, fixed3(0,1,0),0))`

, for instance, is ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


## What’s Next…

In this fifth part of the online series about the sand rendering in Journey, we continued working on the specular reflections, adding tiny glitters to the dunes to make it even more realistic.

The next part, [Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061), will conclude this online series by adding ripples based on the dunes inclination.

- Part 1.
[A Journey Into Journey’s Sand Shader](https://www.alanzucconi.com/?p=10050) - Part 2.
[Journey Sand Shader: Diffuse Colour](https://www.alanzucconi.com/?p=10052) - Part 3.
[Journey Sand Shader: Sand Normal](https://www.alanzucconi.com/?p=10054) - Part 4.
[Journey Sand Shader: Specular Reflection](https://www.alanzucconi.com/?p=10057) **Part 5.**[Journey Sand Shader: Glitter Reflection](https://www.alanzucconi.com/?p=10059)- Part 6.
[Journey Sand Shader: Sand Ripples](https://www.alanzucconi.com/?p=10061)

### Credits

The videogame [Journey](http://thatgamecompany.com/journey/) is developed by **Thatgamecompany** and published by **Sony Computer Entertainment**. It is available for PC ([Epic Store](https://www.epicgames.com/store/en-US/product/journey/home)) and PS4 ([PS Store](https://www.playstation.com/en-gb/games/journey-ps4/)).

The 3D models of the dunes, backgrounds and lighting settings were made by [Jiadi Deng](https://github.com/AtwoodDeng/JourneySand).

The 3D model of the Journey’s player was found on the (now closed) FacePunch forum.

## Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

If you want to recreate this effect, the full Unity package is available for download on [Patreon](https://www.patreon.com/posts/30540389/). It includes everything needed, from the shaders to the 3D models.

## Leave a Reply Cancel reply