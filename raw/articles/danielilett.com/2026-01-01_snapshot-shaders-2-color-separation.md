---
title: Snapshot Shaders 2 - Color Separation
url: https://danielilett.com/snapshot-shaders-2/color-separation/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

The individual red, green, and blue color channels can be moved away from each other uniformly, sampled, and overlaid back onto each other.

![Color Separation filter. Color Separation filter.](/img/snapshot-2/Color Separation.jpg)


# Parameters

**Separation Offset**– Direction in which the blue channel moves in UV space. The red channel moves in the opposite direction.