---
title: Wave Function Collapse tips and tricks
url: https://www.boristhebrave.com/2020/02/08/wave-function-collapse-tips-and-tricks/
author: Boris
published: '2020-02-08'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve been experimenting a lot with constraint-based procedural generation these days. Specifically the [Wave Function Collapse](https://github.com/mxgmn/WaveFunctionCollapse) algorithm (WFC). I’ve even made my own [open source library](https://boristhebrave.github.io/DeBroglie/), and [unity asset](https://assetstore.unity.com/packages/tools/modeling/tessera-procedural-tile-based-generator-155425).

WFC is a very flexible algorithm, particularly with the enhancements I’ve designed, but at the same time, I’ve found it’s quite hard to actually get it to produce *practical *levels useful for computer games. The key difficulty is WFC doesn’t have any global structure to it, all it does it make the output generation look like the input locally, i.e. when viewing small rectangles of output at a time.

In this article, I share what I’ve learned to take your constraint based generators to the next level.

## Basics

It’s hard to use WFC if you don’t know how it works. It’s a [constraint based ](https://en.wikipedia.org/wiki/Constraint_programming)procedural generation algorithm that has been getting more attention recently. It has virtually nothing in common with the [quantum physics concept](https://en.wikipedia.org/wiki/Wave_function_collapse) it is named after.

WFC is easy to set up – you give the algorithm a sample map, and it generates more maps that *look like* the original map, by re-using small snippets from it.

It comes in two forms – adjacent, and overlapped. It can be run in 2d or 3d, even on [hexagonal](https://boristhebrave.github.io/DeBroglie/articles/features.html#topology) or [irregular](https://twitter.com/OskSta/status/1164926304640229376) grids. Most of my tips will be relevant regardless of how you choose to use it.

I suggest playing with [this demo](http://oskarstalberg.com/game/wave/wave.html) to give yourself a feel for it, and reading [this introduction](https://github.com/mxgmn/WaveFunctionCollapse) if you are technically inclined.

## Tileset design

WFC is a tile based algorithm. In that sense it’s only as good as the tiles you give it to work with. I’m no artist, so I have little to say on painting pretty tilesets (though [see here](https://www.boristhebrave.com/2013/07/14/resynth-tileset/)), but a good tileset also requires some technical understanding, to get the most out of.

### Marching Cubes

[Marching cubes](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/) is an algorithm that chooses which tiles to place according to whether each vertex of the tile is solid or empty. Here’s the list of tiles used for 2d.

![](../../assets/12b98c7af5e616f9.svg)


We don’t need to understand the full algorithm, but the idea of designing tiles by thinking solely about their behaviour at the corners is a very powerful one. It is used in many of the best tile designs, as it is an easy way to ensure the tiles always slot together.

It’s particularly powerful for WFC. That’s because if you miss out a few tiles, WFC doesn’t care. It’ll plan around that and never build configurations that require those tiles. Very handy in 3d as there are dozens of potential tiles to design, some of them only needed in very obscure situations. See below in Foundations where I use that trick even further.

Knowing [other tile patterns](https://www.boristhebrave.com/2013/07/14/tileset-roundup/) can also be helpful, but Marching Cubes is the best.

### Rooms

Sometimes simple tilesets are the easiest to work with. This 4 tile combo (one tile is empty) easily generates square rooms.

![](../../assets/91c9ab189d00dff4.png)

![](../../assets/1921b9a5df1d6173.png)

The size of the rooms can be easily tweaked by fiddling with the weights used for each tile. After adding doors and corridor tiles, you can create a variety of man made floor plans.

### Foundations

Some of the fun of WFC can be playing around with tilesets. If you just drop a tile, WFC tries it’s best with what is remaining. Sometimes, that can give radically different results, as Maxim Gumin demonstrates in this image:

![](../../assets/016b48591530370b.png)

We can exploit this behaviour to encourage WFC to generate a lot of recognizable structures.

Here’s a castle example (inspired by [@greentecq](https://twitter.com/greentecq/status/1025348928634408960)):

The tileset I used for this is here:

![](../../assets/556e3a80948b975d.png)

These tiles have an important property – all the tiles are at least as wide on the base as their are at their tops. This means it’s impossible to arrange the tiles in an unsupported way. WFC will immediately pick up on this fact, and create buildings with good foundations.

### Recursive subdivision approximation

While we are on the subject of forcing certain behaviour by picking the right tileset, I discovered that if your tileset consists of straight roads and forks, but no corners, you can get a reasonable approximation of [recursive subdivisions ](http://weblog.jamisbuck.org/2011/1/12/maze-generation-recursive-division-algorithm)(without the recusive bit). This is quite good for grid layouts.

### Big Tiles

It’s possible to amend WFC to support tiles that multiple times bigger than a normal tile. [It’s supported in my addon Tessera](https://www.boristhebrave.com/permanent/20/01/tessera_docs_2/articles/big_tiles.html), for example.

Big tiles have all sorts of uses. Because they spread over the grid boundary, you can use them to include smoother, wider curves than is normally possible while aligning to the grid. They are also great for large set pieces, or just to disguise the tile based nature of the generation.

Here’s an instructive example from [Oskar Stålberg’s](https://twitter.com/OskSta) [Bad North](https://www.badnorth.com/) which shows how he’s used large tiles to give smoothly curving beaches, chunky houses and extra cliff variation.

## Constraints

WFC is at heart a constraint based algorithm. That means that it tries to generate levels that fit a certain set of criteria. In pure WFC, there’s only one critieria – that levels look locally like the input sample. But here I discuss some enhancements to WFC that add extra sorts of constraints.

### Fixed tiles

It’s very easy to fix certain tiles before generation in WFC. They then get seamlessly integrated into the generation.

This has a huge number of uses. Here are some ideas:

- Fix the entrance and exit points of a level
- Pre-author some content, and let WFC draw around it.
- Generate parts of the level with a different algorithm, then fill in the details
- Draw the boundary / floorplan for the level, and let WFC fill in the interior

### Path constraint

The [path constraint](https://www.boristhebrave.com/permanent/20/01/tessera_docs_2/articles/path.html) is my novel contribution to WFC. It’s immensly powerful, but a full description probably requires another article.

This constraint looks *globally* across the entire generated output, and forces there to be a path between anotated tiles. Or equivalently, it forces a subset of tiles to form a single [connected component](https://en.wikipedia.org/wiki/Component_(graph_theory)). The fact it is global makes it a complement to WFC’s normal behaviour, which is entirely locally focussed.

I’ve found adding it makes a big difference to the look of a generated level. Without it, WFC will often generate a bunch of disconnected rooms or areas, which looks unrealistic and not something a human would plan.

![](../../assets/c8c334aab89055f4.png)

![](../../assets/3e2361dcac54a06f.png)

### Drawing rivers and roads

Another thing the Path constraint is good at is… drawing paths. By default, the path constraint only ensures there **is** a route between tiles. It doesn’t actually ensure that the path is simple as possible. So for rivers and roads, it’ll often draw T-junctions at unnecessary places. The trick is to either not have any T-junction tiles, or, if you do, give them a very low weight so they are rarely picked unless necessary.

I like to use fixed tiles to pin the destination points of the path. Then the Path constraint is oblidged to insert tiles that force the rest of the path to connect.

![](../../assets/a2d35e74df178d44.png)

If you want to play with paths, I have a small javascript demo available [here](https://www.boristhebrave.com/2018/04/28/random-paths-via-chiseling/).

## Variety

### Alternate tiles

It’s super easy to add variant tiles to WFC. Just add the tiles to the list of possible tiles, and ensure it has the same connections as the original tile it is replacing. Or you can do it as a post-processing step, as is common in other procedural generation styles.

![](../../assets/2c9fc738fa78e2db.png)

### Vary tiles by level

If you’ve put a lot of effort into the design of your tileset, you’ll find the random nature of WFC starts to hurt. It’ll use the all of the tileset, meaning you might get a level with lava and snow and desert all intermingled. This frequently doesn’t make any sense.

An easy way to restore some consistency is decide in advance which [biome](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/#biomes) a level is going to be, and then disabling all tiles that don’t make sense in that biome.

[Bad North](https://www.badnorth.com/) (again) is an excellent example of this. Some levels have cliffs entirely banned, others have a lot of forestry, and others include ruins and graveyards. This gives each level a distinct feel, without you having to change generation style a great deal.

![](../../assets/7aabbf438378b3b1.png)


![](../../assets/7aabbf438378b3b1.png)

### Vary tiles across the map

You can go even further with mixing up the tileset.

If WFC is that if you generate a large map with it, it starts to look very samey. This is another consequence of it being a *local* constraint solver.

The best solution I’ve seen for this is in [Caves of Qud](https://www.reddit.com/r/proceduralgeneration/comments/exopj6/wfc_dungeon_generation_with_pathing/). In their developers talk on the generation ([1](https://www.gdcvault.com/play/1026313/Math-for-Game-Developers-End), [2](https://www.gdcvault.com/play/1026263/Math-for-Game-Developers-Tile)) they describe how they subdivide their map into different areas, then run WFC with specific settings on subsets of the map. That means they can have a ruins area, and a city area, and they use totally different templates and tiles.

![](../../assets/0c8d2567504e71fd.png)


![](../../assets/0c8d2567504e71fd.png)


[Math for Game Developers: Tile-Based Map Generation using Wave Function Collapse in ‘Caves of Qud’](https://www.gdcvault.com/play/1026263/Math-for-Game-Developers-Tile)## Conclusion

WFC, like all constraint based generation technique, has a case of *“be careful what you wish for”*. It’s easy to set up, and get some good looking results, but nailing down the exact details you want for your game can be very hard.

I hope I’ve presented a number of techniques to help tame that beast, but ultimately, the best way is to design your game to the strengths of procedural generation, rather than trying to force things too much.

I would definitely recommend trying [Bad North](https://www.badnorth.com/) and [Caves of Qud](https://www.reddit.com/r/proceduralgeneration/comments/exopj6/wfc_dungeon_generation_with_pathing/). Both are stellar examples of WFC in the wild, and the developers have put a lot of thought into how it works best for their games.