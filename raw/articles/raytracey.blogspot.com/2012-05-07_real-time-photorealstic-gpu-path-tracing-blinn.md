---
title: 'Real-time photorealstic GPU path tracing: Blinn'
url: http://raytracey.blogspot.com/2012/05/real-time-photorealstic-gpu-path.html
author: Sam Lapere
published: '2012-05-07'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Quasi-random, more or less unbiased blog about real-time photorealistic GPU rendering

Monday, May 7, 2012

Real-time photorealstic GPU path tracing: Blinn

I got the Blinn shader working at last. It adds a huge amount of realism and completely transforms the scene. In the screenshots below, it's only applied to the roads and some metal objects:

Creating photorealistic graphics with a path tracer is a piece of cake, but good post processing (hdr bloom, tonemapping), lighting and materials will still make the difference between a flat looking, lifeless scene and a believable, lifelike one, so I'll keep concentrating on those areas.

Hi Mikko, thanks for the interesting link (I've actually been following that blog for a while).

Btw, are you working on the Reset game(http://reset-game.net/)? If so, extraordinary photoreal visuals, you are bringing rasterization to new heights. It looks better than everything out there.

## 9 comments:

When using Blinn do you find a difference in convergence times? In theory you are now waiting for 2 components per pixel to converge.


Once Jacco gets fresnel working this is going to look insane ...

It converges a little bit slower than pure diffuse, but the realism you get in return is goddamn amazing.

Wow! The Blinn shader looks tremendous! It's really looking amazing.


Is it just me, or are the colours hyper-saturated?

Sean, thanks. The colors are indeed oversaturated (default color settings that came with the new code). I'll have a look at the settings.

It looks really, really good! You should be proud!


Your goals are photo-realism, no? What do you expect you'll have to do to get there?

Creating photorealistic graphics with a path tracer is a piece of cake, but good post processing (hdr bloom, tonemapping), lighting and materials will still make the difference between a flat looking, lifeless scene and a believable, lifelike one, so I'll keep concentrating on those areas.

Oh goody, more of this please. Everything is Shiny!

Hi Mikko, thanks for the interesting link (I've actually been following that blog for a while).


Btw, are you working on the Reset game(http://reset-game.net/)? If so, extraordinary photoreal visuals, you are bringing rasterization to new heights. It looks better than everything out there.

Yes, I am. Thank you so much!

Post a Comment