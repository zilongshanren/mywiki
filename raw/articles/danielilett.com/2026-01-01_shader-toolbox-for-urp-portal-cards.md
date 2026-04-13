---
title: Shader Toolbox for URP - Portal Cards
url: https://danielilett.com/shader-toolbox/portal-cards/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Fades colors based on depth-distance from scene elements, and fades alpha based on camera distance. Based on a concept from the game Abzû.

# Parameters

## Portal Card Properties

**Fade Thresholds**– Blend the color based on the distance between the mesh and the depth of the last rendered object at the same screen coordinate. Pixels with distance below the x-value get tinted with Fog Start Color, and pixels with distance over the y-value get tinted with Fog End Color, with a smooth transition in between.**Distance Thresholds**– Fades the alpha of the mesh based on the distance between the camera and the mesh pivot point. The mesh becomes invisible at distances over the y-value, and is at full alpha at distances below the x-value.**Edge Fade**– Fades the edges of the mesh based on UV corodinates, with separate values for the U- and V-axes.**Fog Start Color**– Color of the portal fog close to the mesh.**Fog End Color**– Color of the portal fog far away from the mesh.