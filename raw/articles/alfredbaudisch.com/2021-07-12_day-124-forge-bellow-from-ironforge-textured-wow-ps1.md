---
title: 'Day 124: Forge Bellow from Ironforge Textured (Wow PS1)'
url: https://alfredbaudisch.com/dailies/day-124-forge-bellow-from-ironforge-textured-wow-ps1/
author: Alfred Reinold Baudisch
published: '2021-07-12'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

In terms of "PS1 look", the last daily that I was satisfied with was [Day 112: Tauren Mill Rigged and Animated (World of Warcraft PS1)](https://alfredbaudisch.com/dailies/day-112-tauren-mill-rigged-and-animated-world-of-warcraft-ps1/). The other ones don't exactly look PS1-like.

With this one, I think I nailed the visuals and style again. Differences in the process:

- The
**initial texture for projection**, has been prepared at**1024×1024, then scaled down to 512×512 using Bicubic**interpolation**then 256×256 without interpolation**. - After projection,
**the texture used for painting was also 256×256**, everything without any interpolation (in Blender: Closests). - The
**AO was baked in a 1024×1024**empty texture and then scaled down**to 256×256 as Bicubic**and placed**on top of the texture in a Multiply**Layer. - The
**brightness and contrast**of the final texture were tweaked a bit. - In Gimp, I ran
**Posterize -> 24**(normally I would pick 16).