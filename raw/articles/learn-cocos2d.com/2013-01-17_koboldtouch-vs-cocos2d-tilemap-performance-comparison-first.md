---
title: 'KoboldTouch vs Cocos2D Tilemap Performance Comparison: First Results'
url: http://www.learn-cocos2d.com/2013/01/koboldtouch-cocos2d-tilemap-performance-comparison-results/
author: Jeremy says
published: '2013-01-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I’m currently working on a new tilemap renderer for ![Screen Shot 2013-01-17 at 01.46.23](../../../wordpress/wp-content/uploads/Screen-Shot-2013-01-17-at-01.46.23-300x197.png)


[KoboldTouch](http://www.koboldtouch.com/).

I now have an early version that’s fairly complete and does most of what cocos2d’s tilemap renderer can do. Pun intended: yes, cocos2d’s tilemap renderer really doesn’t do all that much: load and display tilemaps with multiple layers.

In fact my current implementation is one step ahead already:

KoboldTouch’s tilemap renderer doesn’t require you to use -hd/-ipad/-ipadhd TMX files and the related (often hard to use or buggy/broken) TMX scaling tools. Just use the same TMX file designed for standard resolution, then simply provide just the tileset images in the various sizes with the corresponding -hd/-ipad/-ipadhd suffixes. The tilemap looks the same on a Retina device, just with more image detail.

### Performance Comparison

Anyhow, I thought I’ll do some quick performance tests. I have a test map with 2 layers and a tiny tileset (3 tiles, 40×40 points). I’m comparing both in the same KoboldTouch project, using the slim MVC wrapper (named KTLegacyTilemapViewController) for cocos2d’s tilemap renderer CCTMXTiledMap.


All tests used cocos2d-iphone v2.1 beta 4, were release builds with the default compiler optimizations enabled and ran on an iPod touch 4 (256 MB RAM, low memory threshold around 95-110 MB) which was rebooted frequently.

The tilemap’s layers were flood-filled with actual tiles because transparent tiles did use significantly less memory in CCTMXTiledMap. And where I mention “square tiles” I count all tiles on all layers. A 1000×1000 tilemap with 2 layers therefore has 2 square million tiles.

#### CCTMXTiledMap

First I noticed that cocos2d’s tilemap renderer for whatever reason starts to display nothing when the tilemap size goes above a certain threshold. It even starts to occur with relatively small tilemaps, say 100×100. It didn’t seem to affect rendering performance though, the framerate already dropped noticably.


UPDATE:In the meantime I learned thanks to @xiotex and @jamielowesdev that most likely cocos2d renders 4 vertices per tile, and therefore hits the vertex limit of 65,536 on tilemaps that are larger than 128×128 regardless of how many layers there are. CCTMXTiledMaps can be larger and still be displayed if there is an according number of empty tiles in the map’s layers. This is a[rather prohibitive size limit].

Next I tried to narrow down the maximum tilemap size I could load. The largest tilemap I could load reliably was 250×1000 which makes half a million square tiles. It rendered at below 10 fps. The framerate fluctuated around 7 fps but the framerate counter in cocos2d is inaccurate for framerates below 10, so let’s stick with “under 10 fps” or maybe I should just say it straight: unusable.

How long did it take to load this tilemap? I used a simple stopwatch and timed it manually several times, it takes about 6-7 seconds to load a CCTMXTiledMap of this size.

Lastly I wanted to know what tilemap size you can work with and get a decent framerate. I define decent as “at least 30 fps”.

I found that a 50×1000 tilemap (100,000 square tiles) renders consistently at just over 30 fps, so that seems to be the sweet spot. This means a square tilemap of 300×300 with two layers, that’s about the maximum one can expect to get a decent framerate with on an iPod touch 4 with CCTMXTiledMap.

#### KTTilemapViewController

So how does KTTilemapViewController compare with CCTMXTiledMap?

**KTTilemapViewController can load a 2300×5000 tilemap (23 million square tiles) in under 3 seconds and renders it at 60 fps!**

This means KoboldTouch can load and use tilemaps that are 46 times larger than what cocos2d can handle technically, or 256 times larger than the largest tilemap CCTMXTiledMap users can use realistically. And it loads these much larger maps more than twice as fast. Wow! This exceeds even my wildest expectations!

[KoboldTouch’s tilemap renderer](http://www.koboldtouch.com/) clearly plays in a league of its own. That’s a tilemap size even Tiled can struggle a bit, with some operations (flood fill, resize map) taking a second or two to complete on my “Late 2009” iMac.

Still can’t quite believe it … ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


PS: I’ll make KoboldTouch version 6.1 with the new tilemap renderer available to members within the next two weeks.

PPS: Oh and if you like to help me out please take the [KoboldTouch survey](https://www.surveymonkey.com/s/BX9LKLT). I want to know what you think about it so I can make it even better.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Interesting test. I believe that the 128×128 limit is new with cocos2d 2.0, but I could be misinformed. I ran into this a few weeks ago and I’ve just started doing TMX things with 2.0 instead of the 1.x branch.

One request for your new implementation would be to have multiple tile atlases be able to load per layer with the new renderer. It’s kind of an annoying issue. Also I don’t think that some of the more freeform standards for TMX maps are implemented in CCTMXTiledMap like tile offsets and polygons.

Also, HKTMXTiledMap largely does what you are taking about as well, at least in the rendering department. The default CCTMXTiledMap is a fairly basic un-optimized class. I’m glad that it’s getting some attention!

Lastly, the TMXGenerator class is very helpful for on the fly tilemap creation.

Looking forward to playing around with your work. =)

256×256 with a single layer with no empty tiles is definitely a hard limit in cocos2d 2.1. This generates 65k vertices (4 per tile), the maximum the GPU can handle.

I guess it was the same in cocos2d 2.0 since there haven’t been any TMX code changes from what I saw. I’m pretty sure the limit wasn’t that low in v1.x though what I remember might be skewed because there were probably many empty tiles. And there was definitely always a practical limit because tilemaps that create several ten thousands of vertices render slowly.

When I went through the loader code - I used cocos2d’s loader code as a basis, cleaned it up and optimized it - I made sure all the current TMX features were supported. I think there was just one or two minor things missing, might have been either polygons or tile offsets but I can’t remember. In any case KT supports them all.

Great work, keep it up!