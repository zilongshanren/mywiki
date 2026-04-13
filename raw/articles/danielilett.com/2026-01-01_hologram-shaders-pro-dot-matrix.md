---
title: Hologram Shaders Pro - Dot Matrix
url: https://danielilett.com/hologram-shaders-pro/dot-matrix/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The Dot Matrix hologram renders an ordered series of small dots with configurable size and distance between dots.

![Dot Matrix](../../assets/ed0a4a1056f76047.jpg)


# Properties

## Basic PBR Properties

These properties control the basic interactions between Unity’s lighting and the object. Includes the crucial emissive color settings that control the appearance of the holograms.

**Output Mode**- Controls whether the shader outputs color to Base Color, Emission, or both.**Base Color**- Controls the color of the object.**Base Texture**- Also controls the color of the object. This is multiplied by**Base Color**.**Normal Texture**- Used to change the normal vectors on the surface, which influences lighting interactions. May not be noticeable due to the usage of bright emissive light.**Normal Strength**- A value between 0 and 1 which controls how strongly the**Normal Texture**impacts the surface normals.**Alpha Clip Threshold**- Any pixel with an output alpha value below this value is culled entirely.**Metallic**- A value of 0 means the lighting on the surface is like a non-metal (wood, paper, plastic). 1 means it is like metal**Smoothness**- A value of 0 means the object is completely rough. 1 means it is highly polished and smooth.**Ambient Occlusion**- A value of 0 means no ambient light reaches the object. 1 means the full ambient light reaches the object.

## Dot Matrix Pattern

These settings control the density and spacing of the screen-space dots.

**Dot Size**- The size, in pixels, of each dot on-screen. All dots are perfectly square.**Dot Space**- The size, in pixels, of the space between dots. The spacing is the same on each axis.**Rotation Radians**- How much to rotate the gridline system, in radians.

## Dynamic Resolution

Certain holograms depend on the screen resolution. When using dynamic resolution (FSR or DLSS), Unity sometimes uses the pre-upscaling resolution in shaders, resulting in incorrect results for some shaders. These properties let you adjust the resolution used in shaders.

**Upscaling Amount**- When using dynamic resolution (FSR or DLSS), it may help to modify this setting to ensure the scaling of the dot pattern remains constant.