---
title: Hologram Shaders Godot - Basic
url: https://danielilett.com/hologram-shaders-godot/basic/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The Basic hologram gives you the bare basics, such as Fresnel light and transparency.

![Basic](../../assets/538a2a192d34a275.png)


# Properties

## Basic PBR Properties

These properties control the basic interactions between Godot’s lighting and the object. Includes the crucial emissive color settings that control the appearance of the holograms.

**Output Mode**- Controls whether the shader outputs color to Albedo, Emission, or both.**Base Color**- Controls the color of the object.**Base Texture**- Also controls the color of the object. This is multiplied by**Base Color**.**Normal Texture**- Used to change the normal vectors on the surface, which influences lighting interactions. May not be noticeable due to the usage of bright emissive light.**Normal Strength**- A value between 0 and 1 which controls how strongly the**Normal Texture**impacts the surface normals.**Alpha Clip Threshold**- Any pixel with an output alpha value below this value is culled entirely.

## Fresnel

Fresnel adds light to the edge/rim of an object.

**Fresnel Power**- The size of the Fresnel/rim. Higher values mean the rim is smaller, but this should be a value above 0.**Fresnel Color**- Color of the Fresnel/rim light. Can be different to the**Base Color**.**Use Scene Intersections**- Should the shader detect when a pixel is just in front of another scene object? Note: only able to detect opaque objects.**Intersection Power**- The size of the intersections. Larger values mean a thinner intersection glow.