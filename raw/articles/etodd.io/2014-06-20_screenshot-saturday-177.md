---
title: Screenshot Saturday 177
url: https://etodd.io/2014/06/20/screenshot-saturday-177/
published: '2014-06-20'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 177

Our animator [Antonio](http://vimeo.com/ayaba) has been hard at work on new animations. Check it out!

Guys, the level editor is really close to being done. Here's some cool features:

You can link entities together. For example, you can have a door open when the player enters a trigger volume. Or have a light turn on. Or both.

The UI now displays buttons for all available commands at any given moment, and their keyboard shortcuts. Different commands are available depending on what mode you're in, and what entities are selected.

There's also Steam Workshop support! Since each player only gets 1 GB of Workshop space, and our map files were up in the 8-9 MB range, we had to make some pretty big changes to the map format. Geel did some bit twiddling to cut down the map size by 50% ([more about that here](http://geel.io/post/88710536090/efficient-bitpacking-in-lemma)), then we Gzipped everything for another 50% size decrease.

That's all for this week. Thanks for reading!