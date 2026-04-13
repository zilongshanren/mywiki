---
title: Retro Shaders Pro for URP - Bilinear3 Vertex Lit
url: https://danielilett.com/retro-shaders-pro/bilinear-vertex-lit/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The **Bilinear3 Vertex Lit** shader is a version of the **Retro Vertex Lit** shader which uses the three-point interpolation method which was used by the N64. This results in textures which look blurry in a unique way.

As of Version 1.5, the functionality of this shader was rolled into the Retro Lit shader. This page exists for compatibility with previous versions of the asset pack.

![Bilinear3 Vertex Lit](../../assets/505c0b3cd1e5be99.png)


# Parameters

**Base Color**- The albedo color of the object.**Base Texture**- An albedo texture which can be used to apply more color detail than**Base Color**alone.**Resolution Limit**- The new texture resolution. Note that this is rounded down to the next power of 2 (e.g. 196 would actually mean a texture resolution of 128).**Snaps Per Unit**- The vertices of the mesh will snap to this number of snap points per meter along each axis (in view space, i.e., relative to the camera).**Color Bit Depth**- How many possible color values can exist per channel. Typically, the maximum for a PNG image would be 256.**Color Bit Depth Offset**- Adds a small offset to prevent color darkening, which is common when reducing the color depth. The 0 to 1 range of this parameter represents an addition of 0 to 1/(color depth) to the output color.**Affine Texture Strength**- How strongly the shader should apply affine texture warping effects. 0 means the shader uses perspective-correct mapping, and 1 means full affine texture mapping.**Enable Dithering**- Toggle the dithering effect, which ‘blends’ between color values according to a Bayer matrix pattern when the Color Depth is reduced.**Use Vertex Colors**- Choose whether to multiply the**Base Color**using vertex colors.