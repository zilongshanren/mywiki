---
title: Shader Toolbox for URP - Mesh Explosion
url: https://danielilett.com/shader-toolbox/mesh-explosion/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The **Mesh Explosion** effect expands individual triangles of the mesh away from some origin point. These triangles can have gravity applied over time.

Note that a **BakeFaceColors.cs** script is included that will bake each triangle center point into the vertex colors of the mesh. This is useful for drawing the exploded mesh.

# Parameters

## Surface Options

**Workflow Mode**- Choose between Metallic and Specular workflows. This affects how the shader calculates lighting and changes some of the options presented to you.**Surface Type**- Toggle between*Opaque*and*Transparent*rendering.**Render Face**-Choose whether to render*Front*,*Back*, or*Both*faces**Alpha Clip**- Toggle whether the shader should apply the*Alpha Clip Threshold*.**Alpha Clip Threshold**- Pixels with final base color alpha values below this threshold will be culled if*Alpha Clip*is enabled.**Receive Shadows**- Toggle whether realtime shadows should be applied to the object.

## Lit Properties

**Base Color**- The albedo color of the object. The alpha channel may be used for transparency.**Base Texture**- Similar to**Base Color**, can be used to change the albedo color of the object. The tiling and offset settings used for this texture are applied to the other Lit textures supplied to the material.**Metallic**- Appears only in*Metallic*workflow mode. Controls how metallic the object is – 1 means the object is fully metallic, whereas 0 means it is completely non-metallic.**Specular Color**- Appears only in*Specular*workflow mode. Controls the color of specular highlights that appear on the object’s surface.**Smoothness**- A value between 0 and 1 representing how smooth the surface is. Rough surfaces tend to have no specular highlights, while totally smooth surfaces tend to have small, bright highlights. The smoothness value is equal to the texture sample multiplied by the slider value.**Convert From Roughness**- Some 3D modelling packages output roughness textures instead of smoothness textures. Ticking this option will convert a roughness texture applied to the**Smoothness**slot into smoothness data.**Normal Map**- A texture representing normal vector directions on the object surface. The slider controls the strength of the augmented normal vector data.**Heightmap**- A texture which lets you simulate raised or lowered parts of the surface using UV offsets. Using this option incurs an increased performance impact.**Ambient Occlusion**- The amount of lighting that falls into small crevices on the object surface. 1 means the surface is fully lit, while 0 means that part of the surface is obscured (occluded).**Emission Color**- Applies an emissive color to the surface, which will be visible regardless of whether the object is in shadow.

## Explosion Properties

**Expansion Mode**- How should the mesh expand outwards? In*Normal*mode, the mesh expands along vertex normals, which can result in the triangles getting larger. In*Offset*mode, the mesh expands away from an origin point in 3D space (per vertex). In*Colors*mode, the mesh expands away from the origin point using a position vector baked into the vertex colors (this allows you to have per-triangle offsets).**Explosion Origin Point**- Only appears in*Offset*or*Colors*mode. Determines the origin point in space from which the explosion effect expands.**Explosion Distance**- How far the explosion has travelled from the origin.**Debris Shrink Speed**- How swiftly the triangles get smaller as the distance increases.**Gravity**- How quickly the triangles fall along the y-axis.**Random Offset Range**- A random modifier applied to the explosion distance for each vertex. High values might result in high levels of distortion.