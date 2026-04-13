---
title: Fog and dust
url: https://outerra.blogspot.com/2011/07/fog-and-dust.html
author: Outerra
published: '2011-07-21'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In addition to the existing atmospheric model that already accounts for aerosol particles in air, we have been working also on incorporating ground fog and dust. It's defined by several parameters that determine its density, light scattering properties and boundary altitude. Shaders then compute resulting attenuation and scattering of sun light for terrain and objects. The code is similar to the code computing optical properties of water, using different values and omitting the upper reflective layer.







Viewing valleys of fog from a greater distance, illuminated by evening sun.




When the amount of scattering is lowered, one gets appearance of dust. Also, thicker layers of dust/mist can cast the terrain down below into darkness



There are several things that need to be done yet - currently the fog settings act globally, covering the whole planet in a veil of mist. There's no modulation that would give the fog a nicer, non-uniform look.


Ultimately, fog (or dust) should appear dynamically according to a probabilistic model that would describe chances of it forming at a given place (climate, precipitation) on the planet in given time of day/year. Or using a real time weather report feed.

## 4 comments:

Amazing! Could stare at the walley-fog for hours...

I've been monitoring this blog/work for a while and these are the first images that have provoked me to comment.




Awesome work. I had to look twice at that first image...

It was only recently that I was admiring - and contemplated simulating - the early morning fog and mist nestled in valleys from above (in a plane).

If you can (IP and all), I really enjoy the more technical posts. Thanks.

fog3 (first pic) is very nice.


While looking at the enlarged version of this image I found something that seems non-natural to me - the fog seems to 'climb' up the hills little bit.

In short: amazing. Longer version: un-fuc**ng-believable!

Post a Comment