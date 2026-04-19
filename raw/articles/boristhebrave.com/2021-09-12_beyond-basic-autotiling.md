---
title: Beyond Basic Autotiling
url: https://www.boristhebrave.com/2021/09/12/beyond-basic-autotiling/
author: Boris
published: '2021-09-12'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Autotiling is a system for automatically picking which tile to place on the map, based on user input. It’s a fast way to design levels without having to fiddle with every tile indivually to ensure they are all consistent. Autotiling becoming increasingly well supported by game engines.

While there’s not a great deal of standardization at the moment, I’d say that 90% of systems at the moment are based on marching squares, which chooses between 16 tiles based on user input at each corner, or blob, which chooses between 47 tiles based on user input on each tile. For example, [Godot’s Autotiling system](https://kidscancode.org/godot_recipes/2d/autotile_intro/) or [Tiled’s Terrain brush](https://doc.mapeditor.org/en/stable/manual/terrain/). I’ve written about [these and other schemes before](https://www.boristhebrave.com/2013/07/14/tileset-roundup/).

These approaches do work quite well for quickly whipping up a level, after the initial slog of creating the tiles, but when you start getting into more complex cases, a major shortcoming appears: **combinatorial explosion**.

Basically, as autotilers chose **one** tile for each situation, there needs to be a tile ready for any given combination. It’s bad enough creating 47 tiles needed for the blob pattern, but that only handles transitions between two different terrains. If you add a third, you need hundreds of tiles. And even simpler patterns [quickly blow up with a few terrains](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/4ord.html).

Today, we look at a few ways to deal with that.

## Generating tiles

The most obvious idea is to automatically generate the tiles, either in advance, or at runtime.

### Layered tiles

No one is really making 47 unique tiles for patterns like the blob. Even for simpler patterns, the majority of the art is copy pasted (sometimes rotated) from other tiles. Entire tilesets can be created systematically this way.

[Tilesetter](https://led.itch.io/tilesetter) is a tool concieved to do pretty much exactly this. You specify a base tile to serve as the background, then one or more border tiles that are placed in layers above the base tile, and they are all composited together into a single tile. It can automatically apply multiple border tiles in various combinations.

![](../../assets/9551d86e7c9cb0f7.gif)

Not only is this approach better when dealing with more that two terrains, but it can save a huge amount of work. Even if you use no rotations/reflections, and don’t rely on Tilesetter’s automated handling of corners, you still need less than half the full tileset of the blob pattern by stacking up multiple layers.

Tilesetter focusses on placing the border images inside the cell boundaries, but this technique works just as well drawing the boundaries outside the tile. [Here’s a classic article demonstrating that](https://www.gamedev.net/tutorials/_/technical/game-programming/tilemap-based-game-techniques-handling-terrai-r934/).

### Masked transitions

For higher res graphics, one can often simply blend between two textures. The mask used for blending can be re-used for many different transitions. Like above, you can stack multiple masked textures to do multi-way generators, or you could actually blend together more than two textures.

Factorio’s dev blog has an [excellent example of this](https://factorio.com/blog/post/fff-214).

![](../../assets/9ac0f091aed0e2c2.gif)

### Procedural Tiles

In some cases, the actual content of the tile can itself be generated. This is not very common as it’s hard to make good looking procedural images, and why bother with tiles at all if you can generate your whole level.

Nonetheless, I’ve experimented a bit with this in an earlier project, [resynth-tiles](https://github.com/BorisTheBrave/resynth-tiles/wiki/Tutorial).

## Winged Tiles

Sometimes having a procedural way of affecting drawing transitions outside of the cell border is too much work. A much lazier, but limited approach, is to have the tile image itself extend beyond the cell. This is generally somewhat supported by engines, but can only do fairly limited effects.

One place I’ve seen this used to great effect is [Multi-Scale Truchet Patterns](https://christophercarlson.com/portfolio/multi-scale-truchet-patterns/) by Christoph Carlson.

![](../../assets/d92470a70ff8916d.png)

The tiles for the above pattern overlap each other, but are cunningly designed so that the overlap is not visible.

![](../../assets/f86ee090f180305e.png)

Other places this effect is useful is to depict grass spilling over into other tiles, and depicting objects in isometric tiles.

## Ripple effect

[Tiled](https://www.mapeditor.org/) takes a different approach. While it does let you create tiles with complicated transitions between them, it’s also possible to create far fewer transitions, and let Tiled do the work for you. It’ll change nearby tiles as necessary to connect the newly drawn tile with the rest of the map, potentially using several different transitions.

![](../../assets/b1005953e0ad9f9d.png)

[Tiled docs](https://doc.mapeditor.org/en/stable/manual/terrain/#editing-with-the-terrain-brush):

*“Because there are no transitions from dirt directly to cobblestone, the Terrain tool first inserts transitions to sand and from there to cobblestone.*“

[Townscaper](https://store.steampowered.com/app/1291340/Townscaper/) uses a similar mechanism, where changing one tile can influence choices of tiles over an arbitrarily large area.

I still haven’t got a handle on how exactly these techniques work. Both Tiled and Townscaper are [constraint based](https://github.com/mapeditor/tiled/blob/1ba1169f99960f740e41a1e871c44333e2e7ab4e/src/tiled/wangfiller.cpp#L102) – they try to find a set of tiles that works given the rules about tile transitions.

A similar approach is to have the user define find-and-replace rules, which are then applied recursively. This is used by [Tilekit](https://rxi.itch.io/tilekit) and [Unexplored](https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/), for example.

## Untransitioned tiles

Possibly the easiest way of all is to simply use an art style that don’t require transitions at all. It worked for Minecraft.

## Summary

Well, now I write this article, it looks kinda short. Perhaps this is a bit of a non-issue in practice? Let me know if there’s any ideas I’ve missed.