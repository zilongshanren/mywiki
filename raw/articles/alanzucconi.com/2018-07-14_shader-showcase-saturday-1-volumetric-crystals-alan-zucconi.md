---
title: 'Shader Showcase Saturday #1: Volumetric Crystals - Alan Zucconi'
url: https://www.alanzucconi.com/2018/07/14/shader-showcase-saturday-1/
author: Alan Zucconi
published: '2018-07-14'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

When a 3D object is drawn on the screen, only its outer shell is actually rendered. This works for most solid and opaque materials, but is not powerful enough to bring life to transparent and translucent materials. Currently, this is one of the biggest limitations of most modern game engines. **Volumetric rendering** is a technique that allows rendering materials with a complex internal structure. The topic has been covered extensively on a tutorial tilted [Volumetric Rendering](https://www.alanzucconi.com/2016/07/01/volumetric-rendering/), specifically designed for Unity.

In this post, however, I want to highlight some of the best volumetric effects that I have recently seen on the Internet. Not all the effects shown here might be *actually* using volumetric rendering, but they all give the illusion of being more than just empty shells.

## Space-Time Crystals

This effect, created by game developer and artist [Max Gittal](https://twitter.com/maxSigma_), uses a volumetric technique called **raymarching** to simulate an internal structure within empty 3D models. Each crystal is rendered having a solid code inside, which is distorted by an additional texture.

## World In A World

This portal effect is used by “Altered State”, a game currently being developed by [Austin Schaeffer](https://twitter.com/SchaefferAustin). The effect seen above was created using Shader Forge, and used a technique called **stencil buffers **to render another part of the scene inside the cube. You can find more about stencil buffers in [Non-Euclidean Cubes](https://www.alanzucconi.com/2015/12/09/3873/), a tutorial that explains how to re-create the impossible geometries seen in the iconic game “Antichamber”.

## Cubeeverse

Game developer [Davide Ciacco](https://twitter.com/ciaccodavide) has created this interesting effect in which a cube is reflecting a nebula. The author has not explained how such an effect was achieved, but I suspect a **cubemap** and a normal-dependent distortion might be involved.

## Crystal Ball

Technical artist [Taizyd Korambayil](https://twitter.com/DeepSpaceBanana/) has recently shared this beautiful crystal ball shader created using Unreal Engine 4. Taizyd has posted an earlier version of this effect on Twitter ([here](https://twitter.com/DeepSpaceBanana/status/962845547693527047)). It is very easy to appreciate how much work has gone into its making.

## Leave a Reply Cancel reply