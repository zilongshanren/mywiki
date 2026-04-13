---
title: Retro Shaders Pro for URP - Retro Base Lit (Shader Graph)
url: https://danielilett.com/retro-shaders-pro/retro-lit-sg/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The **Retro Base Lit (Shader Graph)** is a variant of **Retro Lit** which is designed to make it easier for you to extend the effects yourself. If you want to create a retro shader with custom behavior, I recommend making a copy of this graph and making edits to that copy.

Unfortunately, it wasn’t possible to incorporate every retro effect into the Shader Graph version, but I think it still gives you a good basis for making edits. If you have some HLSL knowledge, then go ahead and make changes to the original **Retro Lit** shader!

# Parameters

**Base Color**- The albedo color of the object.**Base Texture**- An albedo texture which can be used to apply more color detail than**Base Color**alone.**Resolution Limit**- The new texture resolution. Note that this is rounded down to the next power of 2 (e.g. 196 would actually mean a texture resolution of 128).**Snaps Per Unit**- The vertices of the mesh will snap to this number of snap points per meter along each axis (in view space, i.e., relative to the camera).**Color Bit Depth**- How many possible color values can exist per channel. Typically, the maximum for a PNG image would be 256.**Color Bit Depth Offset**- Adds a small offset to prevent color darkening, which is common when reducing the color depth. The 0 to 1 range of this parameter represents an addition of 0 to 1/(color depth) to the output color.**Alpha Clip Threshold**- Any pixels with output alpha below this value will be culled, if Alpha Clipping is enabled on this material.**Affine Texture Strength**- How strongly the shader should apply affine texture warping effects. 0 means the shader uses perspective-correct mapping, and 1 means full affine texture mapping.