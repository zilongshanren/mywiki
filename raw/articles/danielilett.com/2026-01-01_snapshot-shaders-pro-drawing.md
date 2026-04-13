---
title: Snapshot Shaders Pro - Drawing
url: https://danielilett.com/snapshot-shaders-pro/drawing/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Shades in the scene with a brush stroke pattern. Darker parts of the scene have a more noticeable stroke effect.

This effect requires the **Drawing Texture** to be set in order to work properly. An example is provided at **Resources/Textures/DrawingTex.png**.

![Drawing & Outline](../../assets/f9c60a1f5dd81dfb.jpg)


# Parameters

**Strength**- How noticeable the effect is.**Drawing Texture**- The texture which encodes what the drawing pattern looks like.**Animation Cycle Time**- The number of seconds taken for one animation cycle (where a cycle involves the effect ‘bouncing’ twice by moving the UV coordinates used by the drawing texture).**Tiling**- The number of times the drawing texture is tiled (in the y-direction).**Smudge**- Strength of the additional UV smudging effect (pixels are translated slightly based on the colour value of the pencil effect at this pixel).**Depth Threshold**- Pixels past this depth (normalised between 0 and 1) will not be ‘drawn’.