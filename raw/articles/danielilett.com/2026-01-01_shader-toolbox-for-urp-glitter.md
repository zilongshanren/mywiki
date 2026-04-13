---
title: Shader Toolbox for URP - Glitter
url: https://danielilett.com/shader-toolbox/glitter/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Overlays a Voronoi-based pattern of small fragments across the surface of the object which glint when viewed at different angles.

# Parameters

## Surface Options

**Workflow Mode**- Choose between Metallic and Specular workflows. This affects how the shader calculates lighting and changes some of the options presented to you.**Surface Type**- Toggle between*Opaque*and*Transparent*rendering.**Render Face**-Choose whether to render*Front*,*Back*, or*Both*faces**Alpha Clip**- Toggle whether the shader should apply the*Alpha Clip Threshold*.**Alpha Clip Threshold**- Pixels with final base color alpha values below this threshold will be culled if*Alpha Clip*is enabled.**Receive Shadows**- Toggle whether realtime shadows should be applied to the object.

## Lit Properties

**Base Color**- The albedo color of the object. The alpha channel may be used for transparency.**Base Texture**- Similar to**Base Color**, can be used to change the albedo color of the object. The tiling and offset settings used for this texture are applied to the other Lit textures supplied to the material.**Metallic**- Appears only in*Metallic*workflow mode. Controls how metallic the object is – 1 means the object is fully metallic, whereas 0 means it is completely non-metallic.**Specular Color**- Appears only in*Specular*workflow mode. Controls the color of specular highlights that appear on the object’s surface.**Smoothness**- A value between 0 and 1 representing how smooth the surface is. Rough surfaces tend to have no specular highlights, while totally smooth surfaces tend to have small, bright highlights. The smoothness value is equal to the texture sample multiplied by the slider value.**Convert From Roughness**- Some 3D modelling packages output roughness textures instead of smoothness textures. Ticking this option will convert a roughness texture applied to the**Smoothness**slot into smoothness data.**Normal Map**- A texture representing normal vector directions on the object surface. The slider controls the strength of the augmented normal vector data.**Heightmap**- A texture which lets you simulate raised or lowered parts of the surface using UV offsets. Using this option incurs an increased performance impact.**Ambient Occlusion**- The amount of lighting that falls into small crevices on the object surface. 1 means the surface is fully lit, while 0 means that part of the surface is obscured (occluded).**Emission Color**- Applies an emissive color to the surface, which will be visible regardless of whether the object is in shadow.

## Glitter Properties

**Noise Scale**– How frequently the Voronoi noise pattern is tiled across the surface of the mesh**Noise Rotation Speed**– How quickly the random values increase over time, rotating the random vector direction that is used for glint calculations.**Glitter Offset**– A modifier which determines how likely is is that a glitter particle actually reflects light.**Sparkliness**– Higher values mean glitter particles reflect with a narrower angle range, causing the object to look ‘more sparkly’ when moving around it.**Glitter Color**– Color of the glitter particles at one end of the generated noise range.**Glitter Color 2**– Color of the glitter particles at the other end of the generated noise range.**Fresnel Power**– Power applied to the Fresnel calculations. Higher values mean thinner Fresnel highlights around the rim of the object.**Fresnel Color**– Color multiplier for the Fresnel lighting.**Spot Offset**– An angle offset applied to the Voronoi pattern generator. A value of zero results in an even grid of glitter particles.**Spot Thresholds**– Smoothstep thresholds values applied to the glitter particles. The second value should be at least as large as the first. Values above zero typically result in circle shapes, whereas values near zero will give you jagged glitter particle shapes.