---
title: Snapshot Shaders Pro - Light Streaks
url: https://danielilett.com/snapshot-shaders-pro/light-streaks/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Adds horizontal light streaks emitted by strong light sources in the scene.

Note: this effect works best when HDR is enabled on your camera and your scene contains strong light sources or emissive materials. A luminous intensity of 1 corresponds to a full-white, non-emissive object.

![Light Streaks](../../assets/ed27553532e47ef0.jpg)


# Parameters

**Strength**- How far the light streaks extend.**Luminance Threshold**- Any pixel below this luminance will not emit light streaks.**Downsamples**- This divisor is applied to the screen resolution in the x-direction. Higher values reduce the quality but improve performance.