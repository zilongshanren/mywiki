---
title: Shader Toolbox for URP
url: https://danielilett.com/shader-toolbox/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

**Shader Toolbox** is a collection of useful shaders and subgraphs for URP. Whether you’re creating a photorealistic or stylized game, there’s something in this pack for you!

This pack adds 11 new shaders, ranging from a more customizable version of the **Lit** shader to **Glass** effects, to stylized **Voronoi Lava** and non-photorealistic lighting with the **Gooch** shader. Transparent effects support the use of the new `_CameraTransparentTexture`

included in the pack, which lets you add a second transparent object pass which can see regular transparents in the camera texture.

Use the menu button on the left to navigate through each effect in the pack.

# ✨ Features

*Shader Toolbox for URP* comes with a heap of shaders, subgraphs, and extra goodies that will speed up your game development.

## 🎨 Plenty of shader effects

With effects focusing on photorealism, such as a flexible **Default Lit** shader and a bright, emissive **Dissolve** shader, to stylized shaders like the **Inverted-Hull Outlines**, **Bubbles**, and **Gooch** effects, and utility effects like **Dither Transparency** and **Stochastic Lit**, there’s plenty of choice, with more effects planned for the future.

## 🪟 Use transparent objects in a new version of Scene Color

If you’ve ever used the `Scene Color`

node in Shader Graph or sampled the `_CameraOpaqueTexture`

in HLSL, you’ll know that shaders typically can’t see any information about transparent objects. Now they can, with the new `_CameraTransparentTexture`

. Shader Toolbox comes with the ability to render a second transparent pass for specific objects, with the ability to see any object rendered after the regular transparent objects pass. It’s a bit more expensive, but it genuinely makes the impossible now possible!

## 📖 A library of subgraph nodes

This pack comes with a library of subgraphs which can slot into your Shader Graphs. Color conversions, lighting helpers, better texture sampling, and useful vector operations are all part of the library at your fingertips with *Shader Toolbox*.