---
title: A Tile Too Far
url: http://hacksoflife.blogspot.com/2010/01/tile-too-far.html
author: Benjamin Supnik
published: '2010-01-27'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've been playing with shading algorithms lately. One such algorithm is the "number puzzle". The basic idea is to take a repeating texture that is divided into sub-tiles and randomly move the tiles around. This is implemented in-shader by separating the UV coordinates and randomizing the bits that represent the "tile". (This is usually all but the lowest N bits.) The tile choice is made by sampling a random noise map, and the UV input to that comes from the upper bits so that it is stable (e.g. so we only switch tiles at the tile boundary).


One nice property of the number puzzle is that if you don't have shaders, you simply get a repeating texture. This is handy because the art assets and code doesn't have to be cased out for a fixed function case - we end up with uglier, but valid output.


It occurred to me today that the number puzzle can be atlased - that is, the random tile we pick could be constrained by the upper bits of the UV map, so that (by using a broad "space" of UV coordinates) we can pick from a set of tiles within a larger texture. This is a win because it means we can texture atlas and thus merge a bunch of differently tiled surfaces into one batch.


There is just one problem with this technique, one that might be a deal breaker as long as fixed function is necessary: when the shader is off, the atlasing gets ignored and we end up with junk. There really isn't a good way around this..wrapping + atlasing are, as far as I know, incompatible in the fixed function pipeline.

Is fixed function still necessary? OpenGL 2.0 GeForce and ATI cards are everywhere now, even the cards in Dell/Compaq/Aldi etc. computers that previously were rubbish are now at least 512MB OpenGL 2.0 PCIe. In my hobby code games I don't even bother providing a render path for non-vbo, non-shaders. I like to keep an eye on the Steam hardware stats:


ReplyDeletehttp://store.steampowered.com/hwsurvey

X-Plane users may not be using quite as current hardware as the average Half-Life 2 player but surely they are not that far off.

If it were just what the users have, I wouldn't support fixed function. But...in my experience, being able to turn off the advanced path has immense debugging and customer support value, and is often the difference between "run in safe mode for a month until new drivers come out" vs. "return the product for a refund." As we migrate up the hardware spec, I think we'll start treating fixed function more and more as a safety net, but as long as tech support is still landing users in that safety net fairly often, I have to think about not ripping fixed function out just yet.

ReplyDelete