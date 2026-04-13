---
title: Shader Toolbox for URP - Subgraph Library
url: https://danielilett.com/shader-toolbox/subgraph-library/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

*Shader Toolbox for URP* comes with a handful of subgraphs which make your life easier when creating your own graphs.

# Subgraph List

## HCL to RGB

Converts from Hue-Chroma-Luminance color space to Red-Green-Blue.

## RGB to HCL

Converts from Red-Green-Blue color space to Hue-Chroma-Luminance.

## Get Main Light

Retrieve data from the main light, such as the direction (as with the **Main Light Direction** node), color, shadow attenuation, and distance attenuation.

## Get Ambient Light

Gets ambient light data from spherical harmonics.

## Apply Normal Map

Takes in a normal map and applies its normal data to the world normal vector to produce a combined vector.

## Better Voronoi

A new version of the **Voronoi** node which outputs pixel distance from the nearest edge between cells (as well as the distance from the cell center point, as the built-in Voronoi node does).

## Find Perpendicular Vectors

Given a single vector input, this node finds two vectors which are perpendicular to that vector (and to each other), with a safety mechanism if the zero vector is input.

## Lit Default

The main subgraph which combines **Lit** properties and outputs values you can output to the graph output stack.

## Lit Stochastic

A version of the **Lit Default** subgraph which also applies stochastic texture sampling to each texture map, disrupting obvious texture tiling.

## Refract

Outputs a refracted vector given an input vector, a surface normal, and a refractive index.

## Sample Texture 2D Grad

A version of Sample Texture 2D which lets you manually supply gradient vectors.

## Sample Transparent Texture

Samples the `_CameraTransparentTexture`

. If this isn’t set up (see [Camera Transparent Texture](https://danielilett.com/shader-toolbox/camera-transparent-texture/) for details), then it will output a grey texture instead.