---
title: Classification of Tilesets
url: https://www.boristhebrave.com/2021/11/14/classification-of-tilesets/
author: Boris
published: '2021-11-14'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Many years ago I started looking at [different sorts of tiles sets used by artists](https://www.boristhebrave.com/2013/07/14/tileset-roundup/). A good tile set is flexible enough to allow tiles to be re-used in a lot of situation, but simple enough that the tiles can be easily created. Ideally, it would enable [autotiling](https://www.boristhebrave.com/2021/09/12/beyond-basic-autotiling/) or otherwise be easy to design levels with.

Though I covered a few different techniques back then, I fell short of any systematic discussion of tiles. Here I plan to take a more rigorous approach, in the hopes of making a common language for referring to different tile sets, and pointing out the key variations in design. Maybe we’ll even discover something new, like [Mendelev predicting new elements for the periodic table](https://en.wikipedia.org/wiki/Mendeleev%27s_predicted_elements).

You can explore many of the tilesets discussed using the ** Tileset Creator** tool I made.

Table of Contents

So what is it I mean by a “tileset”? I mostly use Unity’s terminology:

A **grid** defines a collection of **cells**, which are basically a bunch of hollow shapes in space, which connect to each other. **Tiles** are the things that you insert into cells – each cell holds exactly one tile. You record the choice of tile for each cell in a **tilemap** (or tilemap layer, in some systems).

Typically, you want to make a fairly small collection of tiles, and re-use those same tiles accross the whole map. That collection is a **tileset**. Sets are just an unordered bag of tiles, so for convenience a tileset is often displayed as a **tile palette**, which is like a mini tilemap that lays out the tiles in a specific way so it’s easy to find the one you are looking for.

Thus, when I say tileset, I’m ignoring systems that build a tile out of smaller components, and the specific ordering or layout of the tiles. I *just *care about how many unique things there are to plonk down on the map. For convenience, I’ll usually ignore variant tiles that are designed as drop-in replacements for antoher tile, as they don’t really impact the discussion.

So, by way of example, the most common grid is a square grid. It has rectangular cells, each of which is adjacent to 4 other cells. Here’s a typical tileset for a square grid. I display it with two different palettes which are both popular. This tileset is called marching squares/cubes, after [the auto-tiling technique it is linked with](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/).

Tiles like this are often used as a quick way of drawing terrain.

The other popular tileset is called the [blob pattern](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/blob.html), but I’ve seen many more. And there’s lots of variations too. We’ll try and cover everything under a single approach!

Before going into how to classify tilesets, let’s go over a very basic form of auto tiling, which will serve as the key idea later.

While auto-tiling can take a [wide variety of forms](https://www.boristhebrave.com/2021/09/12/beyond-basic-autotiling/), we’re just going to imagine we’re making a function that is given a boolean for each corner of a square tile, and need to work out which tile to use. The booleans can come from any source – perhaps they are randomly generated, or a level designer specified them. This sort of autotiling is called marching cubes, and I have more [detailed tutorial here](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/).

The standard way to write such a function is to give each corner a power of 2, and then sum up all the ones that are “on”. In this case, it indicates that we want tile 11.

Other tilesets have similar auto tiling technique, I discuss the blob pattern for example, [here](https://www.boristhebrave.com/2013/07/14/tileset-roundup/). In each case, you end up using some labels on vertices, edges, faces (in 3d) and the cell centers, and some formula to relate those to the tile to place.

My classification of a tileset breaks a tileset down into 4 aspects:

- Cell type
- Tile identification
- Symmetries
- Restrictions

These combine to give a short code that describes tileset. For example, the marching cubes tileset above has code “**S-V2**“, which means it is on square tiles, has tile identification V2, and no symmetry or restrictions.

Cell type is pretty obvious. Most tilesets are on a square grid, but you also see cube based ones, or hex and triangle. I use codes S, C, H and T for these cell types.

This is the most important part of the code. Tile identification asks “**what is the minimal amount of information needed to uniquely identify a tile in the tileset**“.

Answering this usually requires you to think like an autotiler would. Like we discussed above, imagine you could store information on the vertices (corners), edges and faces of each cell, and then have some lookup system that had to pick the tile based on that.

So for this tileset, you store a value on each **vertex**, and the value be one of **two** things. So we’d give it identification “V2”. Combined with the cell designator, that makes the tileset’s code S-V2.

Doing the the same thing on triangles, we could make T-V2.

You could also do marching cubes with three different values, which would be S-V3.

Or there is a tileset often called [wang tiles](https://en.wikipedia.org/wiki/Wang_tile) that uses edges rather than vertices. That would be S-E2.

The full set of tile parts is vertices, edges, faces and cells, with codes V, E, F, C. Faces is only used for 3d tiles, and cell indicates that one value is stored per tile.

Not all tilesets can be identified with just one of V, E, F, C. The blob pattern, for example, requires you to distinguish tiles that have different edges, but *also* different corners, as otherwise these two tiles would be hard to tell apart. So it would use code S-V2E2.

Both edges and corners have values on them in this tileset

Symmetry is one of the key ways of reducing the amount of tiles in a set. It’s very common to only create a tile once, then rotate or mirror it to use it in more circumstances. I denote these with R for rotation and M for mirroring.

Below you can see S-V2, compared with S-V2-R, which allows any rotation. You can see there are much fewer tiles in the latter, only 6 vs 16.

In cases where the axis matters (usually for 3d cases), you can include x, y or z after R or M to indicate rotating about that particular axis or reflecting through that particular axis. So C-V3-RyMx would be 3d marching cubes, rotating around the y-axis (vertical in Unity’s co-ord system) and reflecting in the x axis (and thus also in the z-axis, by rotating).

Tile identification shows the amount of information needed to uniquely identify a tile. But it’s often the case that it is too much information, and some combinations do not correspond to any tile. For example, in the blob pattern, there’s no tile with a solid corner but empty edges next to that corner.

Such “missing” tiles are noted in the restrictions section. I don’t have a fancy notation for this part, you must just write out the requirements. In the blob case, if either of the edges of a corner are empty, then the corner must also be empty. So you could write “`edge = 0 ⇒ adjacent vertex = 0`

“. (⇒ is the logic symbol meaning “implies”). But there’s other ways of expressing the same thing. I use “-Blob” as a shorthand to indicate this particular restriction.

Minecraft style blocks don’t really connect with each other at all. You just pick the value for a cell and that’s it. So you’d call that tileset C-C100 (i.e. cubes tiles, each with a single value that identifies them). Perhaps we should write C-C*n* to indicate we’re not too interested in the exact value of *n*? Similarly, text based roguelikes use S-C*n* as the letters do not join up at all, but exist in a square grid.

There’s also many beautiful examples of tiles at [cr31’s stagecast](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/intro.html). Here’s a classification of them:

| CR31 | My Classification |
|---|---|
|

[2-Corner](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/2corn.html)[3-Edge](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/3edge.html)[3-Corner](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/3corn.html)[Blob](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/blob.html)[Reduced sets](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/reduced.html)*(uses restrictions section)*[Block Tiles](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/block.html)[1-side Edge](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/1sideedge.html)[1-side Corner](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/1sidecorn.html)[Angled Paths](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/angled.html)Note how often several tilesets have the same classification. This is an important point – classification just shows how the tiles in a tileset relate to each other, the actual art in the tile still has a huge impact on how they are interpreted. This is best seen in CR31’s [blob gallery](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/blob_g.html) – the same tileset can can be seen as trenches, walls or water features in a way I find quite surprising.

![](../../assets/fc1a2d2dea792c84.png)

[2-Corner](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/2corn.html),

[1-side Corner](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/1sidecorn.html)and

[Angled Paths](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/angled.html)all share the same classification S-V2, but they give quite different looks and behaviour.

It’s also interesting to note that the tile classification does *not* fully specify how to autotile them. Above, you can see that any two tiles in [1-side Corner](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/1sidecorn.html) can be placed adjacent (hence, “1-side”) unlike [2-Corner](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/2corn.html), where the corners must match. But both are classified the same.

Similarly, for the blob pattern, I’ve classified each tile in terms of values on the edges and vertices. But autotilers usually use a much simpler scheme where you paint each cell, and the edges and vertices are inferred from there.

This sort of classification is useful as it enables us to explore the space of possible tilesets. In an [article on triangle grids](https://www.boristhebrave.com/2021/05/23/triangle-grids/), I mentioned that using triangular shaped cells generally requires a lot fewer tiles. We can now see that directly by comparing square and triangle variants of the same thing.

| Square Tileset | Square Count | Triangle Tileset | Triangle Count |
|---|---|---|---|
| S-V2 | 16 | T-V2 | 16 |
| S-V2-RM | 6 | T-V2-RM | 4 |
| S-V3 | 81 | T-V3 | 54 |
| S-V3-RM | 22 | T-V3-RM | 11 |

We can also invent new tilesets with this notation. If S-V2E2–Blob is the 47 tile blob tileset, then we could equally apply the same thing to triangles or hexes. Or talk about S-V2E2-RM-Blob, which reduces the tile count to 16 with symmetry.

While I don’t think that this classification technique is really perfect, as I’m sure it doesn’t capture all details, and doesn’t even work for some tilesets, my hope is that some systemization will encourage you to think about all the different possibilities.