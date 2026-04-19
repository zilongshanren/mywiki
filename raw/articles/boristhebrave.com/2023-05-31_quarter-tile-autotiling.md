---
title: Quarter-Tile Autotiling
url: https://www.boristhebrave.com/2023/05/31/quarter-tile-autotiling/
author: Boris
published: '2023-05-31'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Since Oskar posted about it, I see an increasing amount of praise for his [Dual Grid proposal for autotiling terrains](https://twitter.com/OskSta/status/1448248658865049605). It works by drawing tiles at a half-cell offset to the base grid, creating a dual grid, and using marching squares autotiling to select which tile to draw based on the terrains the corners of the dual grid, which is the *centers* of base grid.

This is a great scheme. It’s simple, only needs a few tiles and can be extended quite easily. It’s used in many games.

But, it does have some drawbacks. The dual grid is difficult to get your head around. You have to worry about [ambiguous tiles](https://www.boristhebrave.com/2022/01/03/resolving-ambiguities-in-marching-squares/). And despite being a substantial improvement over the [blob pattern](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/blob.html), it still requires drawing quite a number of different tiles.

I’m here to explain an alternative, **quarter-tile autotiling**. Quarter-tiling has also been called sub-tiles, [meta-tiles](https://github.com/mapeditor/tiled/issues/1421) (when doubling instead of halving). I’ve previous described as [micro blob](https://www.boristhebrave.com/2013/07/14/tileset-roundup/#Micro-blob), which is the same thing with precomposition. It’s best known for being the [tiling built into the RPG Maker engine](https://www.rpgmakerweb.com/blog/classic-tutorial-how-autotiles-work).

Quarter-tiling is pretty easy to implement, and requires substantially less effort to create tiles for, as it uses fewer, smaller tiles. That does mean it’s not possible to produce as much tile variation as marching squares. But there’s plenty of techniques for adding that back.

Later, we’ll look at [ortho-tiles](https://www.boristhebrave.com/2023/05/31/ortho-tiles/) – an extension of quarter-tiles to irregular, non-square, grids.

Table of Contents

Quarter-tile autotiling, as it names suggests, is based on splitting each cell in the base grid, into 4 cells, each half the height and width of the base cell. We then fill those quarter-cells with half size tiles called quarter-tiles.

Each quarter-tile is chosen based on the terrain of the current cell, and the 3 other cell it’s adjacent or diagonal to. So, the bottom right quarter-tile would look one cell right, one cell down, and one cell down and right.

There’s 6 rules total to chose which quarter tile to use, shown below. A “*” indicates we don’t care what terrain that tile has.

Alternatively, you can use a [bitmask](https://www.boristhebrave.com/2021/11/14/classification-of-tilesets/#A_Recap_on_Auto-Tiling) to find the matching tile:

The rules for the other three quadrants are the same, just rotated. If your tiles rotate, then only the 5 quarter-tiles above are needed for the entire tileset. Otherwise, it requires 14-20 tiles, depending on how much you share the same quarter-tile in different quadrants.

Applying them, you can get something like this:

So why would you want to use quarter tiles, when marching squares is so handy? Well, it really comes down to there being fewer, smaller tiles, and not having to deal with the confusion of a dual grid.

But less tiles comes at a cost. This sort of tiling has far less variation between tiles, which can give it an artificial look. And some popular styles of tile are simply not possible. Because all the quarter-tiles are half size, you cannot make swooping curves of radius larger than half the size of a tile, something perfectly possible with marching squares.

You also cannot draw tiles where both terrains are roughly equal in spacing. Doing so would mean that the border between them ends up on the dividing line between quarter-tiles, which causes problems. Instead you need one terrain to shrink or grow a bit, so that the border ends up wholly contained inside the quarter tiles.

Marching Squares would handle this

| Marching Squares | Quarter-tiles | |
|---|---|---|
| Tiles needed (with rotation) | 6 | 5 half size |
| Tiles needed (no rotation) | 16 | 14-20 half size |
| Terrain data stored on… | Vertices (dual grid) | Cells |
| Handles larger curves and borders | Yes | No |
| Multiple terrains | Yes | No |

In 3d it works much the same, you’d split a cube into 8 smaller cubes, and the choice of which eighth-tile to use would depend on the cell, 3 adjacent cells, and 4 other cells. I think with full rotations and reflections, 10 tiles are needed (vs 15 for marching cubes).

Splitting up the grid into quarter-cells is a lot of coding, and not all that well supported in engines. In practise, it’s far more common to assemble the quarter-tiles into every possible full tile ahead of time. This gives you the 48 tiles of the blob pattern. Then those tiles can be handled normally by the game engine, including normal autotiling.

There’s a number of tools that do this step for you, such as [TileGen](https://assetstore.unity.com/packages/tools/sprite-management/tilegen-tileset-generator-automatic-rule-tiles-149809) or [Tilesetter](https://led.itch.io/tilesetter). I cover this idea a bit more in [this article on autotiling](https://www.boristhebrave.com/2021/09/12/beyond-basic-autotiling/#Layered_tiles), and [on an older article](https://www.boristhebrave.com/2013/07/14/tileset-roundup/).

![](../../assets/2d2180dd9e55cb2e.png)

Marching squares extends quite logically to multiple terains, instead of using just solid/empty booleans. I’ve got [a whole article on it](https://www.boristhebrave.com/2021/12/29/2d-marching-cubes-with-multiple-colors/). But it does require quite a lot of tiles.

There’s no obvious extension for quarter tiles. Generally, i’ve seen games take one of two approaches:

1) Overlap multiple seperate autotilings with transparency, one per terrain.

2) Design tiles for each pair of terrains, and pick the two most prominent one for each quarter tile. You end up with some “sharp” transitions, but often the main features are still preserved.

![](../../assets/507348234ef4d4c9.webp)

In my next article, I discuss [ortho-tiling](https://www.boristhebrave.com/2023/05/31/ortho-tiles/), an extension of quarter-tiles to any grid of polygons.