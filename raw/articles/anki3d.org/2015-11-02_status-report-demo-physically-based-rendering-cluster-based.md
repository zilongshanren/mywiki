---
title: 'Status report: Demo, physically based rendering, cluster based deferred shading,
  preparing for Vulkan'
url: https://anki3d.org/status-report-demo-physically-based-rendering-cluster-based-deferred-shading-preparing-for-vulkan/
author: Panagiotis Christopoulos Charitos
published: '2015-11-02'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

It’s been a while. AnKi’s development is continuing with some slowdown (I am a dad now). Some of the new features that landed in the codebase since the last update:

- Physical based rendering. Seems everyone is using it and now I can understand why.
- Cluster based deferred shading. Changed the (CPU hybrid) tile based with a brand new one that divides the space into clusters. It’s CPU hybrid once again. Avalance is (was) using something similar.
- Added tone mapping with eye adaptation.
- The lighting is fully HDR now.
- Added support for particles that react to lights. The new cluster based renderer allows me to do that which is pretty cool.
- Reworked the graphics backend to make it Vulkan friendly. I’ll start with the Vulkan backend when the drivers become a bit more stable (now they are in early beta state).
- Finally I worked with an artist for a few months to produce a game level. This level is helping me optimize the engine for real life scenarios. Ultimately I’ll produce a tech demo with it.

For the future:

- Continue creating a UI library (boring).
- Expand on a new idea for reflections.
- Expand on a new idea for global illumination
- Integrate Newton Game Dynamics even further (create joints and other stuff).
- Start on the Vulkan backend.