---
title: First version of new random level generator for Super Flying Thing
url: https://blog.gemserk.com/2011/09/30/first-version-of-new-random-level-generator-for-super-flying-thing/
published: '2011-09-30'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Two weeks ago I was working to improve random level generation of Super Flying Thing, the objective was to make the levels a bit more interesting.

Previous generator was really simple, the idea was to define where the starting and destination planet will be and then generate a lot of “garbage” in the way, sometimes with no possible path between both planets.

New level generator does more work to generate a bit more interesting level. Basically the idea is to use some pre generated tiles:

Tiles are defined by SVG groups in a SVG file with custom meta data defining with which tile can be paired.

Based on that information, the generator creates a pattern and based on that pattern and the tiles, it creates the level.

For example, if we have four tiles {A, B, C, D} where A is the where the start planet should be and D where the destination planet should be, and we have the possible links {A -> B, A -> C, B -> B, B -> C, B -> D, C -> B, C -> C, C -> D}, then a possible level could be ABBCBCD (using a regular expression could be defined with something like `A(B|C)+D`

).

So, a very basic pseudo algorithm could be something like this:

```
tiles.add(startTile)
currentTile = startTile
while (currentTile != endtile) {
tile = getPossibleNextTile(currentTile);
tiles.add(tile);
currentTile = tile;
}
```


Where getPossibleNextTile() method uses the meta data of the tile to define randomly a possible next tile.

Here is how a random generated level looks like:

As the title says, this is the first version of the generator, there are a lot of possible improvements to be made and/or create a new generator and throw this one to the trash can.

After writing the post I realized that there is not so much information and the algorithm is pretty basic but I hope it could be of help anyway.