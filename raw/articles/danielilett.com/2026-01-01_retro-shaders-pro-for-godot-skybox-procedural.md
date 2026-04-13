---
title: Retro Shaders Pro for Godot - Skybox (Procedural)
url: https://danielilett.com/retro-shaders-godot/retro-skybox-procedural/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The Retro Skybox (Procedural) shader adds a color gradient sky and a cloud overlay to the scene. You’ll need to add a large sphere which encapsulates all the objects in the scene for this effect to work.

![Skybox Procedural](../../assets/894e8a1e0ef3aaac.png)


# Retro Properties

**Ground Color**- Skybox color close to the horizon.**Sky Color**- Skybox color at the very top of the sky.**Color Mix Power**- Lets you configure which of**Ground Color**or**Sky Color**are more strongly mixed in the sky gradient.**Cloud Height Threshold**- Controls how far the clouds extend. The first value determines a cutoff point for 0% opacity, and the second value determines at what point the clouds use 100% opacity.**Cloud Sizes**- Values used for the noise generator while creating the cloud shapes.**Cloud Density Threshold**- Controls the amount of cloud that appears. The first value thresholds the generated noise values. The second value controls where the clouds reach 100% opacity.**Cloud Color**- Tint applied to the clouds.**Cloud Velocity**- How fast the clouds scroll across the sky.**Resolution Limit**- Pixelates the noise texture used for generating the cloud patterns.**Combine Mode**- Choose how to combine the two cloud maps.- Cloud value = Cloud Size 1
*(operator)*Cloud Size 2.

- Cloud value = Cloud Size 1