---
title: Snapshot Shaders 2 - Fog
url: https://danielilett.com/snapshot-shaders-2/fog/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Overlays two kinds of fog onto the scene: distance-based fog which gets thicker as you get further from the camera, and height-based fog which operates on world height.

# Parameters

## Distance-based Fog

**Distance Strength**- Visual strength of the distance-based fog.**Start Distance**- The distance from the camera at which distance-fog starts appearing.**Start Distance Color**- Color of the distance-fog at the*Start Distance*.**Full Strength Distance**- The distance from the camera at which distance-fog is at maximum strength.**Full Strength Distance Color**- Color of the distance-fog at the*Full Strength Distance*.**Distance Falloff**- Controls the color curve between the*Start*and*Full Strength Distances*.

## Height-based Fog

**Height Strength**- Visual strength of the height-based fog.**Start Height**- The height in world space at which height-fog starts appearing.**Start Height Color**- Color of the height-fog at the*Start Height*.**Full Strength Height**- The height in world space at which height-fog is at maximum strength. Note that if this value is lower than start height, the fog gets stronger as height drops, and vice versa.**Full Strength Height Color**- Color of the height-fog at the*Full Strength Height*.**Use Fog At Skybox**- Should the fog be visible at the skybox?**Skybox Height**- A modified height value to use at the skybox. For all distances between*Full Strength Distance*and the skybox distance, the shader will interpolate between*Full Strength Height*and*Skybox Height*. This ensures a smooth gradient transition between both fog values at the skybox, so I recommend making this value much lower than*Full Strength Height*.**Height Falloff**- Controls the color curve between the*Start*and*Full Strength Heights*.