---
title: Shader Toolbox for URP - Heat Distortion
url: https://danielilett.com/shader-toolbox/heat-distortion/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The **Heat Distortion** effect uses a flow map to distort the camera texture, simulating a heat haze effect.

This effect can be used together with the custom `_CameraTransparentTexture`

included in **Shader Toolbox for URP**. See the section above for setup tips.

# Parameters

## Heat Distortion Parameters

**Heat Origin Point**- World space point where the heat emanates from.**Heat Falloff**- How quickly the heat falls off as you get further from the origin.**Distortion Map**- Flow map which controls how the heat haze distorts the image.**Distortion Strength**- How far the distortion map pushes away each pixel in the camera texture.**Distortion Velocity**- How quickly the distortion map scrolls across the screen.**Distortion Tiling**- How many times the distortion map is scaled.**Camera Texture Mode**- Should the shader sample the`_CameraOpaqueTexture`

(default) or`_CameraTransparentTexture`

?