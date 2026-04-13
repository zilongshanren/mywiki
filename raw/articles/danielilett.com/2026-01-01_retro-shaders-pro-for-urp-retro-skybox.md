---
title: Retro Shaders Pro for URP - Retro Skybox
url: https://danielilett.com/retro-shaders-pro/skybox-cubemap/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The Retro Skybox shader works similar to the built-in Skybox (Cubemap) shader, except it supports lowered resolutions and restricted color depth. You can also overlay a procedurally-generated cloud texture.

![Skybox with clouds](../../assets/903378bb9f65d1ae.gif)


# Properties

## Resolution & Orientation Properties

**Resolution Limit**- The new texture resolution. Note that this is rounded down to the next power of 2 (e.g. 196 would actually mean a texture resolution of 128).**Rotation**- How far to rotate the skybox around the y-axis, in degrees.

## Sky Background Color Properties

**Background Mode**- Choose whether to use a color gradient or a cubemap for the base sky color.**Ground Color**- In*Gradient*background mode, the color of the bottom part of the sky below the horizon.**Sky Color**- In*Gradient*background mode, the color at the very top of the sky.**Color Mix Power**- Lets you configure which of*Ground Color*or*Sky Color*are more strongly mixed in the sky gradient.**Base Color**- Main albedo color of the object.**Base Cubemap**- Which cubemap to use for the sky. Values are multiplied by**Base Color**.**Color Depth**- How many possible color values can exist per channel. Typically, the maximum for a PNG image would be 256.**Color Depth Offset**- Adds a small offset to prevent color darkening, which is common when reducing the color depth. The 0 to 1 range of this parameter represents an addition of 0 to 1/(color depth) to the output color.**Use Point Filtering**- When enabled, the texture uses point filtering, which looks blockier than bilinear filtering.**Dithering Mode**- Choose whether to dither in screen space, texture space, or not at all.

## Procedural Cloud Properties

**Use Clouds**- Turn procedurally generated clouds on or off.**Cloud Height Threshold**- Controls how far the clouds extend. The first value determines a cutoff point for 0% opacity, and the second value determines at what point the clouds use 100% opacity.**Cloud Density Threshold**- Controls the amount of cloud that appears. The first value thresholds the generated noise values. The second value controls where the clouds reach 100% opacity.**Cloud Color**- Tint applied to the clouds.**Cloud Sizes**- Values used for the noise generator while creating the cloud shapes.**Cloud Velocity**- How fast the clouds scroll across the sky.**Combine Mode**- Choose which operation to use to combine the two cloud patterns: add, subtract, multiply, or divide.