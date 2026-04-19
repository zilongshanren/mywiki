---
title: Ortho-tiles
url: https://www.boristhebrave.com/2023/05/31/ortho-tiles/
author: Boris
published: '2023-05-31'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

[Last time, we looked at quarter-tiles](https://www.boristhebrave.com/2023/05/31/quarter-tile-autotiling/). This was an auto-tiling technique for square grids. Each cell in the grid is associated with a terrain (i.e. either solid or empty). Then the squares were split in four, and each quarter was assigned an appropriate quarter-tile.

Otho-tiles extends this procedure to work with irregular grids, even non-square grids. We just have to alter the procedure a little, and be ready to deform the quarter tiles fit in place.

## Ortho?

Ortho is a [Conway Operator](https://en.wikipedia.org/wiki/Conway_polyhedron_notation). It can be thought of as the extension of dividing a square into 4. It divides each n-gon into n “kites” or “ortho-cells”. Each kite is a four sided shape containing the cell center, one corner, and the midpoint of the two edges adjacent to that corner.

The appeal of the ortho operation is it can take any polygonal grid, no matter how irregular, and convert it into a grid of 4 sided shapes. And it’s much easier to work with something that has a consistent number of sides.

## Tiling rules

Ok, so we can convert a grid of polygons into a grid of kites. We want to treat each kite of this grid like we treated the quarter cells of the square grid in the previous article. [To remind you](https://www.boristhebrave.com/2023/05/31/quarter-tile-autotiling/), that means we want to pick an appropriate tile to fill them, according to the following rules.

As the kites always have 4 sides, it’s easy to design similar to fit any particular shape of kite. We’ll call these new set of tiles, **ortho-tiles**. They’re exactly like the quarter-tiles of the previous article, extended to more polygons.

Having the tiles and tile rules is only half the answer though. We also need to change how we read values from the grid.

With quarter-tiles, we read the value of the current cell, two adjacent cells, and one diagonal cell. Those 4 values are then fed into the rules above. The current cell and the adjacent cells can still be easily located for a kite, but what is the “diagonal” cell? For some circumstances, like a hex grid, there is no diagonal cell, while for others, like a triangle grid, there are multiple!

The trick is to use the following rule. “*The value used for a given corner is the minimum value of all cells that share that corner*“. Or, equivalently, a vertex is considered solid only if all the cells that share that vertex are solid.

Then, everything works.

Note that in all cases, only 6 tiles are used, rotated appropriately. Hex grids are often annoying to make tilesets for as there are so many cases, but ortho-tiles side steps that by subdividing to quads first.

## Irregular grids

The example above demonstrates a hex grid and a triangle grid. I created a separate set of ortho-tiles for each, to fit the specific shapes required. But you can just take the tiles designed for squares, the original quarter tiles, and *warp* them to fit any other quadrilateral. As we started by subdividing polygons into quadrilaterals, that means it’ll work on any grid at all.

Here’s an example:

Despite the superficial similarity to Townscaper, this actually uses a [tiny handful of tiles](https://twitter.com/slava_dev/status/1619111830911074312).