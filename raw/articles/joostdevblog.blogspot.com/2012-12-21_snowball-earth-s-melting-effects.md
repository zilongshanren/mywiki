---
title: Snowball Earth's melting effects
url: http://joostdevblog.blogspot.com/2012/12/snowball-earths-melting-effect.html
author: Joost van Dongen
published: '2012-12-21'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Snowball Earth](http://joostdevblog.blogspot.nl/2012/10/the-history-of-snowball-earth-now.html)(our cancelled game from 2008), is the melting effects. Every piece of the world is frozen and covered in snow, and by walking around with the heating turned on, the player can melt it all. In the prototype this had very few gameplay mechanics attached to it, but just seeing and hearing everything come to life is already so much fun that it could carry half the game on its own. Today, I would like to dissect this effect and give an overview of what went into it. (Spoiler: a lot of custom art by our artists Gijs, Ralph, Olivier and Martijn, and a lot of coding by me).

*The melting effects in Snowball Earth*

For those who haven't tried it yet: a couple of months ago (in

[this blogpost](http://joostdevblog.blogspot.nl/2012/10/the-history-of-snowball-earth-now.html)) we released the entire prototype we made at the time, so you can download and play it yourself. Note that this is a Torrent file, so you will need something like

[BitTorrent](http://www.bittorrent.com/intl/nl/)to download the game. Here is the download link:

![](../../assets/85f5e307f2df2e00.jpg)


Download Snowball Earth prototype

![](../../assets/85f5e307f2df2e00.jpg)

Download Snowball Earth prototype

To manage the melting, the game has a big 2D map of the level (a grid, really) and for each point on the map, it stores how much it has melted yet. By walking around, the player turns the parts of the map from frozen to green. This map is then used by all elements in the level to determine to what extend they should show up melted.

A rather simple effect is the smaller plants: they are just scaled to size 0 until they are unfrozen, at which point they grow to full scale with a nice popping animation. For variation, our artists made a couple of different popping animations, but that's about it.

Key to the joyful feeling while melting things, is that every time such a plant pops up, a little bell is heard. These bells have a number of different tones, which form a happy harmony together. When several plants are unfrozen shortly after each other, their popping creates little melodies. Thanks to

[Aline Bruijns](http://www.audiorallysounddesign.com/)for the sound design on this.

Larger plants, with which the player can have collision, are already there in frozen state. As the player melts them, their texture goes from a frozen version to an unfrozen version. Leafs and such can be made to appear during the melting by setting their alpha to black in the frozen texture, and to white in the melted texture.

![](../../assets/4a4ff9e99cde413a.jpg)

To make these plants look more lively, a vertex shader animates them with a simple waving motion. We have a couple of different shaders for different types of plants. Of course, this waving should not happen in frozen form, so this effect fades in smoothly as the plant is unfrozen.

If you have played the prototype, then you might have noticed that it takes a long time to load, and performance isn't quite that good. Current PCs can handle it fine, but in 2008 only the fastest PCs could run the prototype at a high framerate. The main reason for this is that there are a lot of plants in the level, and they are all separate objects that need to be loaded and updated. If the game had not been cancelled, getting this to work smoothly on the Wii would have been a

*huge*challenge...

Performance wasn't only a problem in the game itself: the version of 3D Studio Max we used at the time wasn't up for the challenge either. To make sure our artists could re-use the same plant in several parts of the level without needing to copy-paste the entire plant, I had made a little plug-in script object for 3D Studio. This object would automatically handle an XRef object: a reference to a plant model in another file.

However, the combination of lots of scripted plugins and lots of XRefs totally broke 3D Studio. Near the end of the project, our artists had to restart 3D Studio every hour or so, and had to constantly monitor its memory usage. At some point the memory usage would suddenly go crazy, leaving about 20 seconds to save the work... This made me a little bit afraid to use existing tools in the future again, and I am much happier with

[our own in-game tools for Awesomenauts](http://joostdevblog.blogspot.nl/2012/11/introducing-editors-of-ronitech.html)now. In our own code we can actually solve brutal bugs like this...

We also wanted grass, and because of the performance trouble, I immediately built that using something similar to a particle system. All the grass in an area is rendered as a single object, despite that pieces of grass can grow individually based on what part of the grass area had already been melted. I even made a nice little brush plug-in for 3D Studio to allow our artists to quickly draw the grass where they wanted it. Programming 3D brushes is immensely fun, it is a pity I haven't needed custom 3D brushes for something since!

![](../../assets/b56c7b2ce7290094.jpg)

Ice walls in the Snowball Earth prototype may look like they were made using physics, but to reduce coding time, their destruction animation was animated by hand by an artist. As a cute little extra, we also have smaller blocks of ice with frozen animals in them. When they are broken, the little rabbit inside starts walking around and makes rubber ducky noises when the player stands on it.

![](../../assets/87d3fcb7c6073101.jpg)

A more subtle element is the sound effects. The game has two tracks of ambience: one with sounds of birds and jungle, the other with chilly winds. These are subtly faded in and out depending on how much of the area around the player has already been melted. Few players will have actively noticed this, but this is incredibly important for the mood of the game. As the player walks from the happy jungle in an area he just finished, to the chilly winds of a new area, he cannot help but feel even more like it is time to melt it all and bring back the happiness!

So far I haven't mentioned the thing that is most noticeable in the melting effects of Snowball Earth: the ground. This is because the ground is my pride and joy in this topic and I find it interesting enough that it deserves its own blogpost! See you next week!

## No comments:

## Post a Comment