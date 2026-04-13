---
title: Modifying textures using libGDX Pixmap in runtime
url: https://blog.gemserk.com/2011/10/06/modifying-textures-using-libgdx-pixmap-in-runtime/
published: '2011-10-06'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Since the beginning of Super Flying Thing, I wanted the game to behave in some aspects similar to [Worms](http://www.worms2.com/) (and other games). One of those aspects is the destructible terrain, I love that feature and that is why I am prototyping some stuff to see if we can add that feature to the game or not.

The next video shows how I am using the Pixmap class of [libGDX](https://code.google.com/p/libgdx/) library to modify textures dynamically.

In the previous video there are two textures, they start with the same pixmap data. Then I start to paint and erase pixels from each texture to show how the pixmap operations works over the two pixmaps. Finally, I start rotating both textures and then paint and erase stuff again, to show how I am transforming from game world coordinates to each pixmap coordinates.

### Pros

Destructible terrain. If that works, then we could add some new game play options, like throwing missiles (weapons!!) or killing yourself in order to destroy some part of the map and open paths. Or some power like a shield or something where you move through the terrain destroying it.

We could create some kind of in game level editor for people to make their own levels (and possibly share their stuff). We could make that now using tiles maybe, but I believe making the levels from textures could be easily used by any player (maybe kids). I feel like an in game level editor similar to Inkscape (what I am using right now) is advanced stuff for a typical player.

We could also make more [interesting random levels](https://blog.gemserk.com/2011/09/30/first-version-of-new-random-level-generator-for-super-flying-thing/) (using some other techniques).

### Cons

Having to handle all this texture modification information implies we have to use more memory since we can’t reuse textures, and that could be a problem in limited devices.

Another problem is that textures created with Pixmaps are not being managed by libGDX, that means if the game is paused (you had a phone call for example) and the textures were disposed, then when the games continues the texture data will not be automatically loaded by the library, so we need to manage the texture ourselves.

Also, we will probably lose Box2D collisions calculations as our world is currently made by Box2D polygons, and we will have to create our own bitmap collision calculations.

### Conclusion

Working the terrain as textures is really interesting but also harder and we have to prototype more to know if this is possible or not. However, I will keep dreaming with this feature.

Hope you the post, and if you know some techniques that could help or want to make another contribution, feel free to comment, we will appreciate it.