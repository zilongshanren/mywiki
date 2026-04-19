---
title: 'Still Wakes the Deep in 3D: Rendepth Reshade Depth Boost Update 1.1.0'
url: https://cybereality.com/still-wakes-the-deep-in-3d-rendepth-reshade-depth-boost-update-1-1-0/
author: Cybereality
published: '2025-04-20'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

I’ve ported my Rendepth shader to a [ReShade](https://reshade.me/) plug-in for 2D-to-3D conversion of Windows PC games. Not every title has depth buffer access (needed for the depthmap reprojection) but some new games like Assassin’s Creed: Shadows are supported, and likely around 500 older titles should work. The video embedded is from [“Still Wakes the Deep”](https://store.steampowered.com/app/1622910/Still_Wakes_the_Deep/) which seems to work particularly well with my plug-in.

Game itself is friggin’ fire, and well worth playing even if you don’t have the gear to run it in 3D. This video was recorded live, as I never played more than like 10 minutes here just for testing. Really amazing graphics that look incredible in 3D. YouTube3D video plays on Meta Quest, or with old red/cyan 3D glasses, but honestly it looks best on the new “glasses-free” 3D monitors, like the one from Acer (or upcoming from Samsung). Extremely hard to demonstrate this or prove it in any way, unless you actually see the hardware unit in person.

If you want to check it out, [the MIT License source code is free on GitHub](https://github.com/outmode/rendepth-reshade). You can also find it on my new website, [rendepth.com](https://rendepth.com). Designed for 3D displays supporting half-width SBS mode. Popular XR glasses, like [the XREAL One](https://us.shop.xreal.com/products/xreal-one), support this, or “glasses-free” 3D displays from [Acer Predator SpatialLabs View](https://www.acer.com/us-en/predator/monitors/spatiallabs-view-27). It may be possible to run on VR headsets, like Meta Quest 3, however it would require 3rd party apps, and I haven’t tested this yet. There’s also a newly developed red/cyan anaglyph mode, using a color filter optimized for LCD displays.

This is also the first video of the 1.1.0 update that boosted stereoscopic depth by around 4x from the initial release. I did test some other higher settings after this, and it appears this level of 3D is about as far as I can push the algorithm safely. I plan to test and support more games and hardware as I go, but, in terms of quality, this looks pretty close to “as good as it gets” for the method I developed.