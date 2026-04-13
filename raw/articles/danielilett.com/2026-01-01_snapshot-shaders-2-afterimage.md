---
title: Snapshot Shaders 2 - Afterimage
url: https://danielilett.com/snapshot-shaders-2/afterimage/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Mixes the current frame with the contents of the previous frame with a configurable mixing proportion. Higher proportions make the screen feel ‘laggier’ as a higher number of previous frames stick around on the screen.

![Afterimage filter. Afterimage filter.](../../assets/45dfc0bee9d8107d.jpg)


# Parameters

**Afterimage Mode**– How should the afterimage be drawn?*Off*= no afterimage.*Masked*= only masked objects.*Everywhere*= the entire screen uses an afterimage, even if a mask is set.

**Persistence**– What proportion of the next drawn frame should be made up of the previous frame? Larger values cause a ‘laggier’ screen.