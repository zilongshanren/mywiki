---
title: Distractions
url: https://claire-blackshaw.com/blog/2010/05/distractions/
author: Claire Blackshaw
published: '2010-05-15'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Distractions](../../assets/4e402aebc4c1a4e8.png)

So climbing into bed last night I got a great idea.

Debug the Light ViewProjection matrix by using a camera with the same matrix. Well you know how I managed to knock together that skybox so quickly. Well I dug into it…. YIKES.

I managed to get the sky shader down from 64 instructions to 27 instructions, and remove 4 branches. Sadly the sun doesn’t look great. On the bright side the Sky Sphere now respects it’s World Transform. Light amount now tied into horizon. Removed that horrible change line. Lost the tinting.

So this is what happened…

Oh wait I can clean up those 2 lines quickly… later… Hmm this could be improved… later… wasn’t I meant to be coding something?

Yeah so now after all that fiddling, I’m now working on the shadows again.