---
title: Driven WaveFunctionCollapse
url: https://www.boristhebrave.com/2021/06/06/driven-wavefunctioncollapse/
author: Boris
published: '2021-06-06'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

WaveFunctionCollapse (WFC) is a procedural generation technique for creating images and tile-based levels. I’ve discussed it [many times before](https://www.boristhebrave.com/tag/wfc/).

As a technique, it has some pros and cons. Pro: it’s almost uncannilly good at stitching together tilesets into interesting arrangements, and is pretty good at copying the style in a supplied sample image. Cons: it becomes bland and repetitive at large scales.

In my software [Tessera](https://assetstore.unity.com/packages/tools/level-design/tessera-procedural-tile-based-generator-155425), I’ve been working on various ways of customizating the generation to work around that con. But I’ve seen another way that turns WFC on its head. Instead of using WFC as a full level generator, we want to decide the overall structure of a level some other way, and then use WFC just for the details.

The thing is, adding simple constraints to WFC is basically free. The algorithm [already starts](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/) with a set of possible tiles for each position, you can easily just filter that set before you start running the algorithm. The idea is: determine your level however you like, then “**drive**” WFC by just creating tons of these simple constraints based on that level.

You can think of WFC in this case as a **tile selection algorithm**, a bit like [marching cubes](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/). But marching cubes only considers immediate neighbours when picking a tile, while WFC is able to look a little further a field and pick tiles that work together.

### Examples

Driven WFC is basically how [ Townscaper](https://store.steampowered.com/app/1291340/Townscaper/) works.

The level is actually fully determined by the user, [who draws what is solid, and what is not](https://twitter.com/exppad/status/1283520023798198273). Then each of those solidity booleans, which are set on the vertices of the grid, is used to filter what possible tiles can go in any cell touching that vertex. Then a WFC variant is run to make the actual mesh out of tiles. The tileset is based on marching cubes, but includes a lot of variants and special details. WFC ensures that all those details connect together.

I’ve experimented a bit with the same solidity scheme in [For Keep’s Sake](https://boristhebrave.itch.io/for-keeps-sake).

Another example, **Marian42’s White City. **In the latest version, broad structure of the level is specified by a height map.

In order to give WFC a bit more leeway, the heightmap is pretty coarse, and only generates WFC constraints at multiples of 8 tiles. That gives some of WFC’s characteristic style, while still letting the large scale be decided elsewhere. It also helps with infinite generators like this, as you can chunk up the WFC evaluations.