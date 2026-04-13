---
title: Retro Shaders Pro for Godot - Retro Skybox
url: https://danielilett.com/retro-shaders-godot/retro-skybox-cubemap/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The Retro Skybox shader works similar to the built-in Skybox (Cubemap) shader, except it supports lowered resolutions and restricted color depth. You can also overlay a procedurally-generated cloud texture.

![Skybox with clouds](../../assets/903378bb9f65d1ae.gif)


# Retro Properties

**Base Color**- The base color of the sky.**Base Texture**- A cubemap texture containing the sky colors.**Resolution Limit**- Sets an upper bound on the resolution of*Base Texture*.**Color Depth**- How many possible color values can exist per channel. Typically, the maximum for a PNG image would be 256.**Color Depth Offset**- Adds a small offset to prevent color darkening, which is common when reducing the color depth. The 0 to 1 range of this parameter represents an addition of 0 to 1/(color depth) to the output color.**Use Point Filtering**- When enabled, the texture uses nearest neighbor filtering, which looks blockier than bilinear filtering.