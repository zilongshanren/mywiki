---
title: Shader Toolbox for URP - Dissolve
url: https://danielilett.com/shader-toolbox/dissolve/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The **Dissolve** effect can cut away parts of the mesh and display a glowing edge along the cutoff boundary. This effect can cut away parts of the mesh on one side of a plane, or over a specific distance from an origin point.

In *Plane* mode, the plane is represented using a point on the surface of the plane and the normal direction of the plane. The included **DissolvePlane.cs** script can automatically send data from a plane to the material.

# Parameters

## Surface Options

**Workflow Mode**- Choose between Metallic and Specular workflows. This affects how the shader calculates lighting and changes some of the options presented to you.**Surface Type**- Toggle between*Opaque*and*Transparent*rendering.**Render Face**-Choose whether to render*Front*,*Back*, or*Both*faces**Alpha Clip**- Toggle whether the shader should apply the*Alpha Clip Threshold*.**Alpha Clip Threshold**- Pixels with final base color alpha values below this threshold will be culled if*Alpha Clip*is enabled.**Receive Shadows**- Toggle whether realtime shadows should be applied to the object.

## Lit Properties

**Base Color**- The albedo color of the object. The alpha channel may be used for transparency.**Base Texture**- Similar to**Base Color**, can be used to change the albedo color of the object. The tiling and offset settings used for this texture are applied to the other Lit textures supplied to the material.**Metallic**- Appears only in*Metallic*workflow mode. Controls how metallic the object is – 1 means the object is fully metallic, whereas 0 means it is completely non-metallic.**Specular Color**- Appears only in*Specular*workflow mode. Controls the color of specular highlights that appear on the object’s surface.**Smoothness**- A value between 0 and 1 representing how smooth the surface is. Rough surfaces tend to have no specular highlights, while totally smooth surfaces tend to have small, bright highlights. The smoothness value is equal to the texture sample multiplied by the slider value.**Convert From Roughness**- Some 3D modelling packages output roughness textures instead of smoothness textures. Ticking this option will convert a roughness texture applied to the**Smoothness**slot into smoothness data.**Normal Map**- A texture representing normal vector directions on the object surface. The slider controls the strength of the augmented normal vector data.**Heightmap**- A texture which lets you simulate raised or lowered parts of the surface using UV offsets. Using this option incurs an increased performance impact.**Ambient Occlusion**- The amount of lighting that falls into small crevices on the object surface. 1 means the surface is fully lit, while 0 means that part of the surface is obscured (occluded).**Emission Color**- Applies an emissive color to the surface, which will be visible regardless of whether the object is in shadow.

## Dissolve Properties

**Noise Scale**- Scale of the noise pattern used for the edge lip of the dissolve effect.**Noise Strength**- How strongly the noise pattern distorts the edge lip shape.**Origin Type**- Whether the effect uses*Plane*mode or*Point*mode.**Cutoff Point**- In*Point*mode, this is the origin point from which the dissolve emanates. In*Plane*mode, this is a point that lies on the plane.**Cutoff Direction**- Only visible in*Plane*mode. Represents the normal vector direction of the plane.**Cutoff Height**- How far from the plane or point that the dissolve starts (or ends).**Flip Direction**- When enabled, the dissolve will instead occur the opposite direction of the plane (*Plane*mode), or at negative distances from the point (*Point*mode).**Glow Color**- Color of the glowing lip. Can be applied as emissive or base light.**Glow Thickness**- Width of the glowing lip edge.**Use World Space**- When enabled, world space positions are used for all quantities in the shader. Otherwise, object space is used.**Use Emission**- Apply the glowing lip to the graph*Emission*output. Otherwise, it is applied to*Base Color*.