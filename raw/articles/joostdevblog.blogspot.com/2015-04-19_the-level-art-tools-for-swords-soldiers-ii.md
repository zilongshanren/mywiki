---
title: The level art tools for Swords & Soldiers II
url: http://joostdevblog.blogspot.com/2015/04/the-level-art-tools-for-swords-soldiers.html
author: Joost van Dongen
published: '2015-04-19'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers II](http://www.swordsandsoldiers2.com)(coming to Wii U on May 21st!) we wanted to create detailed and varied levels. Because of the number of maps and their large size we needed art tools that provide a lot of automation to be able to populate them quickly. At the same time we wanted to allow customisation and control over the details to create unique, designed places. Today I would like to show the tools that

[Ronimo](http://www.ronimo-games.com)programmer Machiel van Hooren developed for our artists. Check especially the awesome demo video at the end!

Our starting point was the level editing tools we made for

[Awesomenauts](http://www.awesomenauts.com). Those are very flexible and not tied to a single game, so we could pretty much use all of them directly in Swords & Soldiers II. However, the shape of the levels in Swords & Soldiers II is very different: the Awesomenauts tools are built around rectangular boxes, not curving landscapes. Nevertheless they provided a really strong beginning. I made a short video montage about the Awesomenauts tools for a

[blogpost](http://joostdevblog.blogspot.nl/2012/11/introducing-editors-of-ronitech.html)a couple of years ago, here it is again for those who hadn't seen it before:

The first thing we needed to add for Swords & soldiers II was curving terrain. The core gameplay takes place on a single line with little slopes and hills. So we made a new feature with which our artists place TerrainNodes in the level, and then the engine automatically generates a smooth terrain that goes through those TerrainNodes.

To calculate a smooth line through those points we use standard bezier splines. We also tried using slightly simpler Hermite splines, but we didn't like the look of those. Bezier splines usually come with additional control points for more control over the curvature. To simplify things we calculate the control points automatically based on the previous and next TerrainNode. This gives slightly less control, but that turned out to be fine for our artists and it makes the tools simpler and faster to use.

![](../../assets/fb1754a20c37c488.jpg)

The next step is terrain layers. We wanted to add as much depth to our 2D art as possible. Having more terrain layers in the foreground and background is a good way to accomplish this.

The most obvious method is to just allow our artists to create more terrain layers by hand at different parallax depths. However, efficiency was also a goal, so we wanted to avoid creating all those layers by hand. Therefore we made it so that the parallax layers are copies of the main terrain. To be able to create some diversity we added settings for things like random noise, different textures and colour modifications. Not only is it faster to create levels with these copied terrain layers, it also means that if the main terrain is edited (and it often is), then the background and foreground layers automatically change with it. This makes iteration and modification much quicker.

![](../../assets/335aa8cf6aa127d6.jpg)

The big limitation this creates is that the hills in the background are the same as those on the playground. Sometimes our artists wanted to break free from this pattern. We could have tried making the terrain tools more flexible to accommodate for this, but often the big background objects aren't hills, but an inn, or a wall, or something else. The solution was simple: the artists just placed a big texture of a hill in the background and that's it.

![](../../assets/414116ba4b71d262.jpg)

Plants, small vegetation and other props are all tied to the landscape. To help place those quickly we created ObjectDroppers. An ObjectDropper attaches one or more objects to a terrain layer, allowing an artist to drop a bunch of bushes or flowers on the landscape quickly. Props are dropped using a random seed and the artist can try different seeds to look for one that he likes. With a bunch of prop types a level can have its basic setting in place really quickly, after which the artist can focus on adding the unique flavours. Since the dropped props are tied to the landscape, modifying the terrain also automatically modifies the props, making tweaking the terrain that much faster.

![](../../assets/1c4c0c491a56bbbb.jpg)

Our level artist Ralph Rademakers even used ObjectDroppers to place bigger objects like trees. By working efficiently with these tools Ralph was able to dress up the simpler levels in just a few days per level, using the textures drawn bij Adam Daroszewski and Gijs Hermans.

The other main tools used for the level art are things we inherited from Awesomenauts: placing textures and animations in levels and recolouring them. You can find some good examples of the power of in-engine recolouring in this blogpost:

[Using 2D daylight assets to create a night level](http://joostdevblog.blogspot.nl/2014/11/using-2d-daylight-assets-to-create.html).

Now that I have discussed the tools, let's have a look at them in action in this little video:

I think the main lesson that can be learned from the Swords & Soldiers II level art tools, is that it's sometimes a good idea to limit control to make the workflow faster. The ObjectDroppers create a lot of objects at once, giving much less control than placing them by hand, but also being much, much faster. Similarly, the background and foreground terrain layers being copies of the main layer is limiting, but also very efficient. Where required our artists had enough other tools to break through the limitations by hand, resulting in a good balance between automation and old fashioned handwork.

## No comments:

## Post a Comment