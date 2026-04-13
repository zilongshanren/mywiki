---
title: Shader Toolbox for URP - Gooch
url: https://danielilett.com/shader-toolbox/gooch/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

**Gooch** shading is a non-photorealistic technique that is often used in computer-aided design programs. Objects are drawn with basic colors, where lighting highlights are drawn with warm colors (e.g. yellow) and shadowed areas with cold colors (e.g. blue). This version applies an extra specular highlight on top.

Personally, I’m a fan because it sounds like “goose”.

# Parameters

## Gooch Properties

**Warm Color**- Color to use for lit areas of the mesh.**Cold Color**- Color to use for shadowed areas of the mesh.**Temperature Offset**- A skew value to move the distribution of warm and cold colors.**Specular Power**- Power applied to the specular highlights. Higher values result in a smaller highlight.**Specular Color**- Controls the color of the specular highlights that appear on the mesh surface.**Use HCL Color Space**- Converts the color to the Hue-Chroma-Luminance color space before performing the warm-cold mapping. Results in a nicer transition from warm to cold than when using RGB color space.