---
title: Snapshot Shaders 2 - Underwater
url: https://danielilett.com/snapshot-shaders-2/underwater/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Offsets the UVs of the screen according to a flow map texture, giving the scene an undulating appearance. This effect can also overlay caustics onto the scene based on a caustics texture, which is sampled multiple times and scrolled in different directions.

# Parameters

## Underwater Settings

**Wave Flow Map**- A texture representing the movement of screen UVs. The red and green channels of the image encode the strength and direction of movement of each part of the screen.**Wave Strength**- How strongly the*Wave Flow Map*should distort the screen UVs.**Wave Flow Tiling**- How many times the*Wave Flow Map*should be tiled over the screen.**Wave Flow Speed**- How quickly the*Wave Flow Map*scrolls over the screen.

## Caustics Settings

**Caustics Mode**- Caustics are complex light reflections and refractions caused by curved surfaces, such as water ripples. You can choose:*Off*- Don’t display caustics.*Triplanar*- Sample the caustics along the XY, YX, and XZ planes and blend the three results based on surface normals. This uses triple the number of texture samples compared to the*Light Aligned*option.*Light Aligned*- Align the caustics sample to the direction of the main light.

**Caustics Texture**- Texture to use for the caustics.**Caustics Tint**- Tint applied to the caustics. Use the alpha channel to control the overall strength.**Causting Tiling 1 & 2**- How frequently to tile the caustic texture samples. I recommend making these values different, but still relatively close to one another.**Caustics Scroll Velocity 1 & 2**- How quickly the caustics scroll over scene objects. I recommend using opposite values on each axis (e.g. if the x-component for one velocity is positive, make the other negative).**Caustics Color Separation**- How far the individual color channels of the caustics texture get separated. Warning: this will triple the number of texture samples you are already computing.**Caustics Start Fade**- The distance from the camera where the caustics begin fading out.**Caustics Fade Falloff**- The distance over which the caustics fade from full to zero strength.