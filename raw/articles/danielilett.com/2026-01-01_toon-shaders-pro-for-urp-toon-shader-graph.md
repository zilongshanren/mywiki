---
title: Toon Shaders Pro for URP - Toon (Shader Graph)
url: https://danielilett.com/toon-shaders-pro/toon-graph/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

This is a variant of the Toon shader which was recreated in Shader Graph. It is intended to give you a base for modifying and extending *Toon Shaders Pro* to create your own effects which use the base toon cel-shading lighting style. Currently, this version of the effect only supports the Specular workflow.

![Toon](../../assets/c9c797fc2b05b70b.png)


# Parameters

## Surface Options

**Surface Type**- Toggle between*Opaque*and*Transparent*rendering.**Render Face**- Choose whether to render*Front*,*Back*, or*Both*faces**Alpha Clip**- Toggle whether the shader should apply the*Alpha Clip Threshold*.**Alpha Clip Threshold**- Pixels with final base color alpha values below this threshold will be culled if*Alpha Clip*is enabled.**Receive Shadows**- Toggle whether realtime shadows should be applied to the object.**Shadow Thresholds**- Provide a toon-style cutoff to the realtime shadows.

## Toon Properties

### Diffuse Settings

**Use Second Threshold**- When ticked, the shader introduces a third lighting tint value for diffuse lighting and lets you specify two thresholds: one for dark -> midtones, and another for midtones -> light.**Base Color**- The albedo color of the object.**Base Texture**- An albedo texture to apply more color detail than using*Base Color*alone.**Base Texture Tiling and Offset**- Lets you scale and translate the texture across the object surface. Note that these values are also used to scale and translate*Specular Map*and*Normal Map*.**Light Tint**- Color multiplier applied to fully-lit areas of the object.**Middle Tint**- Only active if*Use Second Threshold*is ticked. Color multiplier applied to midtones on the object.**Shadow Tint**- Color multiplier applied to shadowed regions of the object**Diffuse Thresholds**- Provide a toon-style cutoff to the diffuse lighting. Diffuse lighting comes from the angle between the light and the normal vector of the object surface.

### Specular Settings

**Specular Color**- Controls the specular color of the object. You can also attach a specular map.**Specular Strength**- Global multiplier for all specular highlights. If set to 0, there will be no visible highlights.**Specular Offset Noise Map**- Use a noise texture, such as Perlin noise, to modify the shape of the specular highlights.**Specular Offset Noise Strength**- Controls the strength of the offset applied to specular light values.**Glossiness**- How glossy the surface of the object is. Higher values result in smaller specular reflections, which looks shinier.**Specular Thresholds**- Provide a toon-style cutoff to the specular lighting. Specular lighting arises due to the angle between the viewer and the light rays reflected from the light source in the normal vector of the object’s surface.

### Rim Lighting Settings

**Rim Color**- Multiplier for rim light.**Rim Thresholds**- Provide a toon-style cutoff to the rim lighting. Rim lighting (also called Fresnel) comes from the angle between the viewing angle and the normal vector of the surface. Typically, looking at the object at shallow angles results in high rim lighting.**Rim Extension**- Lets you extend rim lighting across the surface further than usual.

### Normal Mapping Settings

**Normal Map**- Normal maps modify the surface normals for finer details that are difficult to capture with mesh geometry alone.**Normal Strength**- Larger values have a more pronounced effect on the surface normals.

# Usage Tips

- You can duplicate this graph and modify the copy if you’d like to create your own effects, or use the
**CalculateToonLighting**subgraph in any of your graphs. It has many inputs, but I’ve tried to include sensible default values where possible.