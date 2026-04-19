---
title: Tileset Roundup
url: https://www.boristhebrave.com/2013/07/14/tileset-roundup/
author: Boris
published: '2013-07-14'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Following my development of [Resynth Tileset](https://github.com/BorisTheBrave/resynth-tiles), I’ve been doing some thinking on the nature of tilesets, and the possible ways to auto tile them – that is, to paint tiles as is with a brush and letting the computer do the tile selection. Let’s review a few possible ways of doing so.

Just to be clear, I’m only interested at the moment in square, non-rotatable tiles. Rotation is another discussion, but excludes the more interesting tilesets. Adding alternative tiles is also not considered, though it is pretty easy to add in.


### Marching squares

The most popular layout generally used is what I’d call **Marching Squares**, though it is often unnamed as it is so ubiquitous:

Marching Squares requires you to mark each corner as solid or empty. You sometimes see a variant where it is descrbed as marking the center of the tile instead, but that’s inaccurate – you’ve just offset the grid by half a tile in each direction instead.

Artists love Marching Squares because it only requires drawing 16 tiles, and programmers love it as it is very simple to choose the correct tile using a lookup table and the simple formula for the right tile:

`tile_index = topLeft + 2 * topRight + 4 * bottomLeft + 8 * bottomRight`


where each variable is 0 or 1 according to if that corner is solid or not.

This is a trick of binary counting that is [explained](http://www.saltgames.com/2010/a-bitwise-method-for-applying-tilemaps/) [well](http://en.wikipedia.org/wiki/Marching_squares#Isoline) [elsewhere](http://blog.project-retrograde.com/2013/05/marching-squares/).

This tileset is used by both [Tiled](https://github.com/bjorn/tiled/wiki/Using-the-Terrain-Tool) and [tIDE](http://tide.codeplex.com/wikipage?title=tIDE03_image) for auto tiling.

Special mention goes to some sets that either substitute or add an additional two “diagonal” tiles which are empty at the center rather than solid:

*(note: “marching squares” also refers to a procedure for computing outlines of shapes, which is totally unrelated. I think my usage is the more common one nowadays)*

### The Blob

For all it’s benefits, Marching Squares proves to have two shortcomings. Firstly, you have to mark the corners as solid/empty, not the tiles themselves. This often feels a bit unnatural when trying to lay things out, as you only feel rather indirect influence on any given tile. Secondly, the fact there are only sixteen tiles starts to become visible to the eye rather easily. There’s only so many shapes you can make.

Hence the blob:

The blob, coined in [this article](http://www.squidi.net/mapmaker/musings/m091016.php), uses 48 tiles – 47 solid and 1 empty. It covers all possible borders a solid tile could have with other tiles of its own kind or of distinct tiles.

As code, it’s somewhat less pretty:

```
if not left or not top: topLeft = False
if not left or not bottom: bottomLeft = False
if not right or not top: topRight = False
if not right or not bottom: bottomRight = False
neighbour_index = (
topLeft + 2*top + 4*topRight +
8*left + 16*right +
32*bottomLeft + 64*bottom + 128*bottomRight)
pick_tile = {0: 0, 2: 1, 8: 2, 10: 3, 11: 4, 16: 5, 18: 6,
22: 7, 24: 8, 26: 9, 27: 10, 30: 11, 31: 12, 64: 13,
66: 14, 72: 15, 74: 16, 75: 17, 80: 18, 82: 19, 86: 20,
88: 21, 90: 22, 91: 23, 94: 24, 95: 25, 104: 26, 106: 27,
107: 28, 120: 29, 122: 30, 123: 31, 126: 32, 127: 33,
208: 34, 210: 35, 214: 36, 216: 37, 218: 38, 219: 39,
222: 40, 223: 41, 248: 42, 250: 43, 251: 44, 254: 45, 255: 46}
tile_index = pick_tile[neighbour_index]
```


To explain this, we start with 8 variables which indicate whether the eight surrounding tiles are solid or not. The corner tiles are only relevant if both edge tiles are solid, so I mark them as empty in any other case. Then, like with Marching squares, we sum up the borders in binary to get a unique index for each combination. The total value is between 0 and 255.

However, there’s only 47 possible values, all the others are identical to one of these except for the irrelevant corners. So I renumber everything to go from 0 to 46, for convenience. Obviously, you only apply this algorithm to the solid tiles, you can just use the single remaining tile for all empty squares.

An alternative algorithm just uses a lookup table of size 256, which is simpler, but longer. You can see the table [here](http://forums.tigsource.com/index.php?topic=9859.msg721744#msg721744).

### Sub-blob

After playing around with the blob pattern for a while, you start to notice that despite using 48 tiles, the variation isn’t really that good unless you really work for it when making the tiles. You can see the problem here – all these tiles have a similar top left, even though the rest of the tile is different.

It turns out, if you consider just one quarter quadrant of each tile, there aren’t many possibilities. It can either be an inner or outer curve, a horizontal or vertical divide, or solid:

That means if we make 5 subtiles for each quadrant, we can get a tileset that can fill in for the blob with only 20 subtiles (plus the empty tile, unchanged), as long as we are willing to do some assembly. Here’s the tile set, I’ve colored each subtile with a border indicating which quadrant it belongs to.

Each blob tile can be made out of the right choice of 4 subtiles, one from each quadrant, for example.

In code you might write:

```
top_left_quadrant_tile_index = left + 2* top
if left and top and topLeft: top_left_quadrant_tile_index = 4
top_right_quadrant_tile_index = right + 2* top
if right and top and topRight: top_right_quadrant_tile_index = 4
bottom_left_quadrant_tile_index = left + 2* bottom
if left and bottom and bottomLeft: bottom_left_quadrant_tile_index = 4
bottom_right_quadrant_tile_index = right + 2* bottom
if right and bottom and bottomRight: bottom_right_quadrant_tile_index = 4
```


This tileset is used by the [RPG Maker VX community](http://blog.rpgmakerweb.com/tutorials/anatomy-of-an-autotile/), where it is called TileA2 ground autotile. I’m calling it the **sub-blob** pattern, which is catchier.

There’s also [a tool](https://www.assembla.com/code/rpg-maker-to-tiled-suite/subversion/nodes) which converts from sub-blob to blob pattern, though it doesn’t use the same tilesheet layout I have.

*(note: for compatibility with RPG Maker, I’ve omited the empty tile from the tileset, but properly speaking it is still necessary. You’ll need to strip out the grey borders before it matches RPG Maker)*

### Micro-blob

You may have noticed I’ve cheated when creating my sub-blob example. Unlike a higher quality tileset, I’ve re-used some subtiles in several subquadrants. Sometimes it’s nice to have the flexibility of specifying these independently, it’s often necessary to make patterns line up. But other times you don’t need it, and can throw away the duplicates. This leaves just 13 subtiles (plus the empty tile), which is even better than marching squares!

As far as I know, no one is really using this tileset at the moment. I’m calling it the **micro-blob**.

## Summary

So there you have a few different ways to neatly tile automatically. There’s really lots more to say – we haven’t covered handling mixing more than two different textures, or some of the more esoteric layouts like [this monster](http://opengameart.org/content/complete-tileset-template), but I think you’ve got a good selection above.

Which one you select really depends on what you are trying to achieve, and how many tiles you are willing to create. The more tiles, the more flexibility you’ll have to design something that looks organic.

## Credits

All tileset images are generated from [this image](http://commons.wikimedia.org/wiki/File:Rarotonga_Island.jpg), using [Resynth Tileset](https://github.com/BorisTheBrave/resynth-tiles) and some manual image manipulations. Feel free to use these tilesets under [CC By 3.0](http://creativecommons.org/licenses/by/3.0/). They all have tile size 64, and 10 pixel padding/border, except the subtiles, that use half that.