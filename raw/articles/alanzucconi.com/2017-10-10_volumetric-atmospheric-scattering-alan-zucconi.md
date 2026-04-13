---
title: Volumetric Atmospheric Scattering - Alan Zucconi
url: https://www.alanzucconi.com/2017/10/10/atmospheric-scattering-1/
author: Alan Zucconi
published: '2017-10-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If you have lived long enough on planet Earth, you might have wondered why the sky is usually blue, yet red at sunset. The optical phenomenon which is (mostly) responsible for that is called **Rayleigh scattering**. This tutorial will explain how to model atmospheric scattering to reproduce many of the visual effects that planets exhibit. And if you want to render physically accurate visuals for alien planets, this is *definitely* the tutorial you’ve been looking for.

![](../../assets/488fe0db18d2fa0c.gif)

You can find all the post in this series here:

**Part 1.**[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374)- Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

You can **download** the **Unity package** for this tutorial at the bottom of the page.

#### Introduction

What makes atmospheric effects so hard to recreate, is the fact that the sky is not a solid object. Traditional rendering techniques assume that objects are nothing more than an empty shell. All the graphical computation happens only on the material surfaces, regardless of what’s inside. This massive simplification allows rendering solid objects very efficiently. The aspect of certain materials, however, is determined by the fact that light can penetrate them. The final look of **translucent** objects results from the interaction of the light with their internal structure. In most cases, such interaction can be faked very effectively, as seen in the tutorial on [Fast Subsurface Scattering in Unity](https://www.alanzucconi.com/?p=7053). Sadly, this is not the case if we want to recreate a believable sky. Instead of rendering only the “outer shell” of a planet, we need to simulate what happens to the rays of light that pass through the atmosphere. Propagating the calculations inside an object is known as **volumetric rendering**, as is a topic that has been discussed extensively in the [Volumetric Rendering](https://www.alanzucconi.com/?p=5159) series. The two techniques that were presented in that series (**raymarching **and** signed distance functions**), cannot be used effectively to simulate atmospheric scattering. This tutorial will introduce a more appropriate approach to render solid translucent objects, often referred as **volumetric single scattering**.

#### Single Scattering

In a room without any light, you would expect to see nothing. Objects become visible only when a ray of light bounces off them and hit our eyes. Most gaming engines (such as Unity and Unreal) assume that light travels “in a vacuum”. This means that objects are the only things that can affect light. In reality, light always travels through a medium. In our case, that medium is the air we are breathing. As a result, the way objects look is affected by how much air light is travelling through. On the surface of Earth, the air density is relatively low; its contribution is so tiny that it can only be truly appreciated when light travels great distances. Mountains that are far away blend with the sky, although objects close to us appear virtually unaffected by atmospheric scattering.

The first step to replicate the optical effects of atmospheric scattering is to understand how light travels through a medium like air. As said before, we can only see something when light hits our eyes. In the context of 3D graphics, our eye is the camera used to render the scene. The molecules that make up the air around us can deflect the light rays traelling through them. Hence, they have the power to alter the way we perceive objects. As a massive simplification, there are two way in which the molecules in the air can affect our vision.

##### Out-Scattering

The most obvious way in which air molecules interact with light is by deflecting it, changing its direction. If a ray of light directed to hit the camera is deflected away, we are in front of a process called **out-scattering**.

![](../../assets/9ecb5b1cabaa7738.png)

A real light source can emit quadrillions of photons each second, and each one has a certain probability of hitting an air molecule. The denser the medium in which light travels, the more likely it is for a single photon to be deflected. How severely out-scattering affects light also depends on the distance travelled.

![](../../assets/262bcd8a844692c9.png)

Out-scattering causes light to become progressively dimmer, and it depends on both the distance travelled and the air density.

##### In-Scattering

When light is deflected by a particle, it could also happen that is re-directed towards the camera. This is effectively the opposite of out-scattering and, unsurprisingly, is called **in-scattering**.

![](../../assets/0aefca561e7fbeab.png)

Under certain conditions, in-scattering allows seeing light sources that are not in the camera’s direct light of sight. Its most obvious optical effect results in light halos around light sources. They are caused by the fact the camera receives both direct and indirect light rays from the same source, de-facto amplifying the number of photons received.

![](../../assets/7721aceffaeafc03.png)

#### Volumetric Single Scattering

A single ray of light can be deflected an arbitrary number of times. This means that light can travel very complex paths before reaching the camera. This poses a significant challenge, since rendering translucent materials with high fidelity requires to simulate the path of each individual ray of light. This is called **raytracing**, and is currently computationally too expensive for real-time rendering. The technique presented in this tutorial is referred as **single scattering**, since it takes into account only a single scattering event for a ray of light. We will see later how such a simplification still allows obtaining realistic results at a fraction of the cost that real raytracing would have.

The key to rendering realistic skies is to simulate what happens to light rays when they travel through a planet’s atmosphere. The diagram below shows a camera, looking through a planet. The basic idea behind this rendering technique is to calculate how light travelling from ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com P \in \overline{AB}](../../assets/5d4c8cd8a76dc8ab.png)


![](../../assets/28ff2e77b7386cbf.png)

To correctly account for how much out-scattering occurs at each point ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)


![](../../assets/4de63488127ee25b.png)

These two steps are enough to approximate most effects that can be observed in the atmosphere. However, things are compilated by the fact that the amount of light that ![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com P](../../assets/9b82d9ea78e7b06f.png)


![](../../assets/7ad5c8a7e1aa0372.png)

To sum up what we have to do:

- The line of sight of the camera enters the atmosphere at

, and exists it at

; - As an approximation, we take into account the contributions of out- and in-scattering as it happens through each point

; - The amount of light

receives comes from the sun; - The amount of light

receives is subjected to out-scattering, as it travels through the atmosphere

; - A part of the light received by

is subjected to in-scattering, which sends in the direction of the camera; - A part of the light from

that is directed towards the camera is subjected to out-scattering and deflected away from the line of sight.

![](../../assets/86f322fc54c64905.png)

#### Coming Next…

This post introduces the main concepts necessary to create a volumetric shader that reproduces atmospheric scattering. In the next post, we will start formalising these processes.

I hope you will stay with me on this journey through the atmosphere.

You can find all the post in this series here:

**Part 1.**[Volumetric Atmospheric Scattering](https://www.alanzucconi.com/?p=7374)- Part 2.
[The Theory Behind Atmospheric Scattering](https://www.alanzucconi.com/?p=7404) - Part 3.
[The Mathematics of Rayleigh Scattering](https://www.alanzucconi.com/?p=7472) - Part 4.
[A Journey Through the Atmosphere](https://www.alanzucconi.com/?p=7557) - Part 5.
[A Shader for the Atmospheric Sphere](https://www.alanzucconi.com/?p=7665) - Part 6.
[Intersecting The Atmosphere](https://www.alanzucconi.com/?p=7781) - Part 7.
[Atmospheric Scattering Shader](https://www.alanzucconi.com/?p=7793) - 🔒 Part 8.
[An Introduction to Mie Theory](https://www.alanzucconi.com/?p=7578)

##### Other Resources

- Scratchpixel 2.0:
[Simulating the Colors of the Sky](https://www.scratchapixel.com/lessons/procedural-generation-virtual-worlds/simulating-sky/simulating-colors-of-the-sky) - GPU Gems:
[Accurate Atmospheric Scattering](https://developer.nvidia.com/gpugems/GPUGems2/gpugems2_chapter16.html) - Atom’s World:
[Flexible Physical Accurate Atmosphere Scattering](https://atomworld.wordpress.com/2014/12/22/flexible-physical-accurate-atmosphere-scattering-part-1/)

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce the volumetric atmospheric scattering presented in this tutorial.

## Leave a Reply Cancel reply