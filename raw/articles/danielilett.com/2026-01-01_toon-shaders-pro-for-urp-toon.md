---
title: Toon Shaders Pro for URP - Toon
url: https://danielilett.com/toon-shaders-pro/toon/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The **Toon** shader lets you separate the diffuse, specular, and rim lighting and the shadows shown on the object and apply cutoff thresholds for each. You can also specify tint values for the areas of the mesh in light and darkness, or apply a normal map for even more interesting lighting.

![Toon](../../assets/c9c797fc2b05b70b.png)


# Parameters

## Surface Options

**Workflow Mode**- Choose between*Metallic*and*Specular*workflows. This affects how the shader calculates lighting and changes some of the options presented to you.**Surface Type**- Toggle between*Opaque*and*Transparent*rendering.**Render Face**- Choose whether to render*Front*,*Back*, or*Both*faces**Alpha Clip**- Toggle whether the shader should apply the*Alpha Clip Threshold*.**Alpha Clip Threshold**- Pixels with final base color alpha values below this threshold will be culled if*Alpha Clip*is enabled.**Receive Shadows**- Toggle whether realtime shadows should be applied to the object.**Shadow Thresholds**- Provide a toon-style cutoff to the realtime shadows.

## Toon Properties

### Diffuse Settings

**Use Second Threshold**- When ticked, the shader introduces a third lighting tint value for diffuse lighting and lets you specify two thresholds: one for dark -> midtones, and another for midtones -> light.**Base Color**- The albedo color of the object.**Base Texture**- An albedo texture to apply more color detail than using*Base Color*alone.**Base Texture Tiling and Offset**- Lets you scale and translate the texture across the object surface. Note that these values are also used to scale and translate*Specular Map*and*Normal Map*.**Use Vertex Colors**- Choose whether the tint should be affected by vertex colors.**Light Tint**- Color multiplier applied to fully-lit areas of the object.**Middle Tint**- Only active if*Use Second Threshold*is ticked. Color multiplier applied to midtones on the object.**Shadow Tint**- Color multiplier applied to shadowed regions of the object**Diffuse Thresholds**- Provide a toon-style cutoff to the diffuse lighting. Diffuse lighting comes from the angle between the light and the normal vector of the object surface.

### Metallic & Specular Settings

**Metallic**- How metallic the object’s surface is, as a slider from 0 to 1. You can also attach a metallic texture, where the red channel controls the metallic strength. Only appears in*Metallic*workflow mode.**Specular Color**- Controls the specular color of the object. You can also attach a specular map. Only appears in*Specular*workflow mode.**Smoothness**- How smooth the surface of the object should be. Rough materials should be close to zero, and perfectly smooth objects should be set to 1. Influences how specular and environment lighting affect the object**Convert From Roughness**- When ticked, the values in the*Smoothness*map are inverted (some external programs output roughness maps instead of smoothness).**Specular Offset Noise Map**- Use a noise texture, such as Perlin noise, to modify the shape of the specular highlights.**Specular Offset Noise Strength**- Controls the strength of the offset applied to specular light values.**Specular Boost**- Increases the strength of the specular highlights to account for the darkening effect when the cutoff is applied.**Specular Thresholds**- Provide a toon-style cutoff to the specular lighting. Specular lighting arises due to the angle between the viewer and the light rays reflected from the light source in the normal vector of the object’s surface.**Global Illumination Strength**- Slider from 0 to 1 which controls how strongly environmental lighting affects the object.

### Rim Lighting Settings

**Rim Color**- Multiplier for rim light.**Rim Thresholds**- Provide a toon-style cutoff to the rim lighting. Rim lighting (also called Fresnel) comes from the angle between the viewing angle and the normal vector of the surface. Typically, looking at the object at shallow angles results in high rim lighting.**Rim Extension**- Lets you extend rim lighting across the surface further than usual.

### Normal Mapping Settings

**Normal Map**- Normal maps modify the surface normals for finer details that are difficult to capture with mesh geometry alone.**Normal Strength**- Larger values have a more pronounced effect on the surface normals.

# Usage Tips

- Each of the thresholds use smoothstep under the hood so that you can soften the transition between light and dark. If you want to use a single, hard step transition, use the same value for both min and max.
- Lighting is additive, so the diffuse, specular, and rim contributions are added together. Contributions from each light are added together. Consequently, using many additional lights might end up with exceptionally bright objects.
- You can achieve a clean, block-color aesthetic by leaving the
*Base Map*and*Normal Map*blank and attaching the**Outline**effect also included in this pack. However, normal mapping can achieve quite striking visuals when combined with toon lighting. - Highly metallic objects tend to reflect lots of environmental reflections, which don’t have the toon lighting ramp applied. If you don’t want that, you can tone down the global illumination amount.