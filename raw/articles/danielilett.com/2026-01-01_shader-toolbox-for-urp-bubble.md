---
title: Shader Toolbox for URP - Bubble
url: https://danielilett.com/shader-toolbox/bubble/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

A soapy **Bubble** effect with iridescent colors. The colors are visible in the Fresnel light on the object.

This effect can be used together with the custom `_CameraTransparentTexture`

included in **Shader Toolbox for URP**. See the section above for setup tips.

# Parameters

## Surface Options

**Workflow Mode**- Choose between Metallic and Specular workflows. This affects how the shader calculates lighting and changes some of the options presented to you.**Surface Type**- Toggle between*Opaque*and*Transparent*rendering.**Render Face**-Choose whether to render*Front*,*Back*, or*Both*faces**Alpha Clip**- Toggle whether the shader should apply the*Alpha Clip Threshold*.**Alpha Clip Threshold**- Pixels with final base color alpha values below this threshold will be culled if*Alpha Clip*is enabled.**Receive Shadows**- Toggle whether realtime shadows should be applied to the object.

## Lit Properties

**Base Color**- The albedo color of the object. The alpha channel may be used for transparency.**Base Texture**- Similar to**Base Color**, can be used to change the albedo color of the object. The tiling and offset settings used for this texture are applied to the other Lit textures supplied to the material.**Metallic**- Appears only in*Metallic*workflow mode. Controls how metallic the object is – 1 means the object is fully metallic, whereas 0 means it is completely non-metallic.**Specular Color**- Appears only in*Specular*workflow mode. Controls the color of specular highlights that appear on the object’s surface.**Smoothness**- A value between 0 and 1 representing how smooth the surface is. Rough surfaces tend to have no specular highlights, while totally smooth surfaces tend to have small, bright highlights. The smoothness value is equal to the texture sample multiplied by the slider value.**Convert From Roughness**- Some 3D modelling packages output roughness textures instead of smoothness textures. Ticking this option will convert a roughness texture applied to the**Smoothness**slot into smoothness data.**Normal Map**- A texture representing normal vector directions on the object surface. The slider controls the strength of the augmented normal vector data.**Heightmap**- A texture which lets you simulate raised or lowered parts of the surface using UV offsets. Using this option incurs an increased performance impact.**Ambient Occlusion**- The amount of lighting that falls into small crevices on the object surface. 1 means the surface is fully lit, while 0 means that part of the surface is obscured (occluded).**Emission Color**- Applies an emissive color to the surface, which will be visible regardless of whether the object is in shadow.

## Bubble Properties

**Color Ramp Texture**- A texture encoding the transition of colors along the edge of the bubble.**Fresnel Power**- Power applied to the Fresnel lighting equation.**Fresnel Noise Strength**- How strongly the noise offsets the color ramp.**Fresnel Noise Scale**- Scale of the noise offset applied to the color ramp.**Iridescent Strength**- How strongly the color ramp is applied to the Fresnel light.**Iridescent Flow Direction**- Which direction, in world space, the flow map scrolls in.**Refractive Index**- The ratio between the speed of light in the bubble and in the air next to the bubble. Higher values result in stronger visual distortion.**Use Emission**- Should the Fresnel light be output to*Emission*, or*Base Color*?**Camera Texture Mode**- Should the shader sample the`_CameraOpaqueTexture`

(default) or`_CameraTransparentTexture`

?