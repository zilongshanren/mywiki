---
title: Shadows are EVIL
url: https://claire-blackshaw.com/blog/2010/05/shadows-are-evil/
author: Claire Blackshaw
published: '2010-05-17'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Shadows are EVIL](../../assets/4e402aebc4c1a4e8.png)

### Shadows are EVIL!

Okay above you see rough and blurred. The rough pass uses a single sample against the depth buffer. Those bloody pixels are a result of the resolution of the shadow map.

The blurred insanity is a shadow method called PCSS, based on the White Paper, “Integrating Realistic Soft Shadows into Your Game Engine” by Kevin Myers, Randima (Randy) Fernando, & Louis Bavoil. Sadly some of there stuff uses Shader Model 4 so I did my best approximation.

Not happy with either method… pulling my hair out.