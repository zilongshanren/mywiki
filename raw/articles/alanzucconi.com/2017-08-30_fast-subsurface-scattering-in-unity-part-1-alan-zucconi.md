---
title: Fast Subsurface Scattering in Unity (Part 1) - Alan Zucconi
url: https://www.alanzucconi.com/2017/08/30/fast-subsurface-scattering-1/
author: Alan Zucconi
published: '2017-08-30'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Most (if not all) optical phenomena that materials exhibit can be replicated by simulating how the individual rays of light propagate and interact. This approach is referred in the scientific literature as **ray tracing**, and it is often too computationally expensive for any real-time application. Most modern engines rely on massive simplifications that, despite being unable to reproduce photorealism, can produce a believable approximation. This tutorial introduces a *fast, cheap and convincing* solution that can be used to simulate translucent materials which exhibit subsurface scattering.

This is a two part series:

At the end of this post, you will find a link to **download** the **Unity project**.

#### Introduction

The Standard material in Unity comes with a Transparency mode, which allows rendering transparent materials. Transparency, in this context, is implemented with **alpha blending**. A transparent object is rendered on top of existing geometry, partially showing what is behind. While this works for many materials, transparency is a special case of a more general property, called **translucency** (sometimes also called **translucidity**). While transparent materials only affect the amount of light they let through (below, left), translucent ones can alter its path (below, right).

![](../../assets/53eb8f0b952ac02c.png)

The result of this behaviour should be clear: translucent materials diffuse the light rays they let through, blurring what was behind them. Such a behaviour is rarely seen in games, since it is significantly more complex to implement. Transparent materials can be implemented naively with alpha blending, without ray tracing. Translucent materials, on the other hand, require simulating the deviation of the light rays. Such a computation is very expensive and is rarely worth it in real time rendering.

This often prevents from achieving other optical phenomena, such as **subsurface scattering**. When light hits the surface of a translucent material, a part propagates inside, bouncing between the molecules until it finds its way out. This often causes light absorbed at a specific point to be reemitted somewhere else. Subsurface scattering results in a diffuse glow that can be seen in materials such as skin, marble, and milk.

#### Real Time Translucency

There are two main obstacles that make translucency so expensive. The first one is that it requires simulating the scattering of light rays inside a material. Each ray can split in multiple ones, reflecting hundreds or even thousands of times inside a material. The second obstacle is that light received at one point is reemitted somewhere else. While this seems a minor issue, in reality, is a big deal.

To understand why, we first need to look at how most shaders work. In the realm of real-time rendering, GPUs expect a shader to be able to calculate the final colour of a material simply using local properties. For each vertex, shaders are designed to efficiently access only the properties that are local to that vertex. Reading the normal direction and albedo of a vertex is easy; retrieving the ones of its neighbours is not. Most real-time solution must work around these constraints, and find a way to *fake* the propagation of light within a material without relying on non-local information.

The approach described in this tutorial is based on the solution presented at GDC 2011 by Colin Barré-Brisebois and Marc Bouchard in a talk called [Approximating Translucency for a Fast, Cheap and Convincing Subsurface Scattering Look](https://colinbarrebrisebois.com/2011/03/07/gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurface-scattering-look/). Their solution is integrated into the **Frostbite 2** engine, which was used for DICE’s **Battlefield 3**. While not being physically accurate, the approach presented by Colin and Marc produces very believable results at a very small cost.

The idea behind their solution is very simple. In opaque materials, the light contribution comes directly from the light source. Vertices that are inclined more than 90 degrees in respects to the direction of the light, ![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)

![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)


![](../../assets/65febbcfc8a901bc.png)

Each light now accounts for two, distinct reflectances contributions: the front and back illuminations. Since we want our materials to be as realistic as possible, we will use Unity’s Standard PBR lighting models for the front illumination. What we need is to find a way to describe the contribution from ![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)


### ⭐ Recommended Unity Assets

#### Back Translucency

As discussed before, the final colour of our pixels depend is the sum of two components. The first one is the “traditional” lighting. The second one is the light contribution from a virtual light source illuminating the back of our model. This gives the impression that light from the original source actually passed through the material.

To understand how to model this mathematically, let’s picture the following two scenarios (diagrams below). We are currently drawing the red point; since it’s in the “dark” side of the material, it should be illuminated by ![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)

![Rendered by QuickLaTeX.com V_B](../../assets/dea0f34eadfc4f43.png)

![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)


![](../../assets/5a85ac07d85227da.png)

If you are not new to shader coding, this kind of reasoning should sound familiar. We have encountered something similar in the tutorial on [Physically Based Rendering and Lighting Models in Unity 5](https://www.alanzucconi.com/2015/06/24/physically-based-rendering/), where we showed how such a behaviour can be obtained using a mathematical operator called the **dot product**.

As a first approximation, we can say that the amount of back lighting due to translucency ![Rendered by QuickLaTeX.com I_{back}](../../assets/9ee1108f62ff019a.png)

![Rendered by QuickLaTeX.com V \cdot -L](../../assets/9dd1493f49c4bbe4.png)

![Rendered by QuickLaTeX.com N \cdot L](../../assets/c572b3bd99533e5a.png)

**surface normal** in the calculation, as light is simply coming out of the material, not reflecting on it.

#### Subsurface Distortion

However, the surface normal should have some influence, even if minor, on the angle at which the light is leaving the material. The authors of this technique introduced a parameter, called **subsurface distortion **![Rendered by QuickLaTeX.com \delta](../../assets/1fdc42f3f5bf3559.png)

![Rendered by QuickLaTeX.com -L](../../assets/755f228504eecf64.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)


![Rendered by QuickLaTeX.com \[I_{back}=V \cdot -\left\langle L+N \delta \right\rangle\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-88412bf84b16e9b9c5299f44abc4bbec_l3.png)


Where ![Rendered by QuickLaTeX.com \left \langle X \right\rangle = \frac{X}{\left\|X\right\|}](../../assets/a71dd6cefa208852.png)

![Rendered by QuickLaTeX.com X](../../assets/eb71558ba98cad57.png)

`normalize`

function.

When ![Rendered by QuickLaTeX.com \delta=0](../../assets/342274ec5954b708.png)

![Rendered by QuickLaTeX.com V \cdot -\L](../../assets/811bbbe81c67b8fb.png)

![Rendered by QuickLaTeX.com \delta=1](../../assets/5c35b5219c24c6d9.png)

![Rendered by QuickLaTeX.com -\left\langle L+N \right\rangle](../../assets/e393d0e2c3acb6f5.png)

**Blinn-Phong reflectance**, you should know that ![Rendered by QuickLaTeX.com \left\langle L+N \right\rangle](../../assets/813ec3b05901aed4.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

**halfway direction** ![Rendered by QuickLaTeX.com H](../../assets/21b7e9a6311e544d.png)


![](../../assets/7282569256091f6c.png)

The diagram above shows all the directions used so far. ![Rendered by QuickLaTeX.com H](../../assets/21b7e9a6311e544d.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com N](../../assets/76bbbd804dc6db36.png)

![Rendered by QuickLaTeX.com \delta](../../assets/1fdc42f3f5bf3559.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

![Rendered by QuickLaTeX.com \delta=0](../../assets/342274ec5954b708.png)

![Rendered by QuickLaTeX.com \delta](../../assets/1fdc42f3f5bf3559.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


![](../../assets/8517a17df05a56c9.png)

The purpose of ![Rendered by QuickLaTeX.com \delta](../../assets/1fdc42f3f5bf3559.png)

![Rendered by QuickLaTeX.com \delta](../../assets/1fdc42f3f5bf3559.png)


#### Back Light Diffusion

At this point in the tutorial, we already have an equation that we can use simulate translucent materials. The quantity ![Rendered by QuickLaTeX.com I_{back}](../../assets/9ee1108f62ff019a.png)


There are two main approaches that can be used. The first one relies on a texture. If you want to have full artistic control on the way light diffuses in the material, you should clamp ![Rendered by QuickLaTeX.com I_{back}](../../assets/9ee1108f62ff019a.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


The approach used by the author of this technique, however, does not rely on a texture. It creates a curve using Cg code only:

![Rendered by QuickLaTeX.com \[I_{back} = saturate\left(V \cdot - \left \langle L+N\delta \right \rangle \right )^{p} \cdot {s}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-577e07757a85aaf42b85235abb657979_l3.png)


The two new parameters, ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

*power*) and ![Rendered by QuickLaTeX.com s](../../assets/864f28b25521f331.png)

*scale*) are used to change the properties of the curve.

#### Conclusion

This post explains the technical challenges in rendering translucent materials. An approximate solution is introduced, followed the approach presented by [Approximating Translucency for a Fast, Cheap and Convincing Subsurface Scattering Look](https://colinbarrebrisebois.com/2011/03/07/gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurface-scattering-look/). The next part of this tutorial will focus on how to actually implement this effect in a shader in Unity.

- Part 1.
**Fast Subsurface Scattering in Unity** - Part 2.
[Fast Subsurface Scattering in Unity](https://www.alanzucconi.com/?p=7101)

If you are interested in more sophisticated approaches to simulate subsurface scattering for real time applications, [GPU Gems](https://developer.nvidia.com/gpugems/gpugems/part-iii-materials/chapter-16-real-time-approximations-subsurface-scattering) provides one of the best tutorials you can find.

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the necessary files to run this project (shader, textures, models, scenes) on [ Patreon](https://www.patreon.com/posts/14122322).

## Leave a Reply Cancel reply