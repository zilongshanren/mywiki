---
title: Screen-Space Subsurface Scattering Improvements
url: https://cybereality.com/screen-space-subsurface-scatting-improvements/
author: Cybereality
published: '2025-09-14'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/f6ea0fc5215b30dd.png)

Trying to validate and finalize all the shaders on my GL project. Still a bunch of editor features left to do, but the graphics are where I want so will just need to work on the boring stuff now and optimize. Brought back the old skin shader (screen-space sub-surface scattering, SSSSS, say that 3 times fast!) from GPU Gems 2. Above shown with the fallback not needing curvature maps, though if the model had it that works as well. Wanted to have little (or no) pre-computation steps or non-standard texture requirements. The shader here uses partial derivatives to estimate the curve on the mesh. This is fairly cheap, but also has major artifacts (discontinuity) on polygon edges. For high-poly models, or at medium distance (like in a 3rd person game), it should look fine, and I tweaked it so even close up it’s not a deal-breaker.

Still having issues with the shadow mapping (even using 4K maps above) and might need some work on the hair being too transparent. But these may be a matter of tweaking weights/bias and not needing new code or methods. Just going through everything now, found a bunch of bugs, but most were small things slightly off and not too major. Also spent some time this week on asset loading and saving, will post later, still not fully implemented.