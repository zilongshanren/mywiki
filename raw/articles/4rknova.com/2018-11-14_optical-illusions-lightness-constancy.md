---
title: Optical Illusions, Lightness Constancy
url: https://www.4rknova.com/blog/2018/11/14/illusions-lightness-constancy
author: Nikolaos Papadopoulos
published: '2018-11-14'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

Lightness constancy is the perception that brightness of lit and dark surfaces remains constant under different illumination conditions. This perceptual phenomenon allows us to recognize objects as having stable surface properties despite dramatic changes in lighting. This is essential for navigation and object recognition in the real world.

## How the Brain Processes Lightness

The human visual system doesn’t simply measure raw light intensity. Instead, it interprets multiple visual cues and extrapolates sensory data to estimate the actual reflectance properties of surfaces. Our brain excels at recognizing visual patterns including spatial cues, illumination features, and the relationship between objects and their environment.

When we look at a scene, the visual cortex performs sophisticated computations to separate illumination from reflectance. It considers:

**Spatial context**: How surfaces relate to each other**Shadow boundaries**: Sharp or soft edges that indicate lighting conditions**3D geometry**: How objects occlude light and cast shadows**Prior knowledge**: Expectations about how the world typically looks

## The Checker Shadow Illusion

The popularized “Checker Shadow Illusion,” created by Edward H. Adelson in 1995, demonstrates this effect dramatically. A cylinder is strategically positioned on a flat surface with a checkerboard pattern. A light source is placed behind the cylinder and casts a shadow on the flat surface.

In the demonstration below, two tiles are labeled **A** and **B**:

**Tile A**: A dark tile outside the shadow**Tile B**: A light tile inside the shadow

The remarkable fact is that tiles A and B have **identical pixel values**. They reflect the exact same amount of light to your eye. However, your visual system interprets them as having different surface properties because:

- The brain recognizes the shadow cast by the cylinder
- It compensates for the reduced illumination in the shadowed region
- It interprets tile B as a lighter surface in shadow rather than a darker surface in light
- Simultaneously, it sees tile A as a dark surface in full illumination

This demonstrates that our perception of lightness is not a direct measurement of luminance, but rather an inference about surface reflectance that accounts for the lighting conditions. The visual system essentially “discounts the illuminant” to extract stable object properties.

Lightness constancy is not just a curious illusion. It’s a fundamental feature of human vision that has important implications:

# Implementation

Below is a live, interactive GLSL implementation of the Checker Shadow Illusion rendered using raymarching techniques. The scene features:

- A procedurally generated checkerboard pattern
- A cylinder casting realistic soft shadows
- Tiles A and B labeled for easy identification

**To experience the illusion**: Click and hold on the image to draw a line connecting tiles A and B. This reveals that both tiles share the same color value, despite appearing dramatically different in the full scene. The line effectively removes the spatial context that causes your brain to apply lightness constancy.

The demonstration is rendered entirely in a fragment shader using signed distance fields for geometry and soft shadow computation for realistic penumbra. The letters are drawn using custom SDF functions.