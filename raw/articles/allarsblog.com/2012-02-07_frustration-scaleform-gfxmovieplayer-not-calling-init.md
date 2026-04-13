---
title: 'Frustration: ScaleForm GFxMoviePlayer Not Calling Init'
url: https://allarsblog.com/2012/02/07/frustration-scaleform-gfxmovieplayer-not-calling-init/
author: Michael Allar
published: '2012-02-07'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

If your GFxMoviePlayer isn't calling your Init function, I bet you are loading your custom GFxMoviePlayer class through Kismet.

Apparently Kismet fires Start but not Init, at least that is the conclusion I just came to. I didn't find any documentation on this so I'm posting it here for reference.