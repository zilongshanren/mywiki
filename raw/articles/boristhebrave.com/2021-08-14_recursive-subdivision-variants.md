---
title: Recursive Subdivision Variants
url: https://www.boristhebrave.com/2021/08/14/recursive-subdivision-variants/
author: Boris
published: '2021-08-14'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

You are probably familiar with Recursive Subdivision – also known as Binary Space Partitioning – as a procedural generation technique. Like all the best proc gen, it’s a simple idea, that produces complex output. I’m here to discuss some variants that others have used to produce interesting results.

Table of Contents

The idea is you start with a large rectangular space, and divide it in two horizontally or vertically. That gives two rectanges, which you can repeat the process to get even smaller, more nested rectangles, and so on.

Note that the terms “recusive subdivision” and “binary space partitioning” mean something different in other CS/gamedev contexts. Use of these things for procedural generation is a tiny fraction of their power.

This technique is classically used for [city road networks](https://imgur.com/a/04UZQ) and [mazes](http://weblog.jamisbuck.org/2011/1/12/maze-generation-recursive-division-algorithm).

To make a maze, each subdivision introduces a wall, and then you randomly insert a hole somewhere in that wall. After drawing all the partitions, it’s possible to fully navigate the map, but only by navigating the various holes.

Less commonly, it’s used to [generate room-and-passage dungeons reminiscent of Rogue](http://roguebasin.com/?title=Basic_BSP_Dungeon_generation). You apply the subdivisions as normal, but rather than filling each subdivision fully, you put a room in each section, and draw passages between the rooms.

![A simple roguelike dungeon of 16 rooms, with passageways between them and dotted lines indicating the original subdivisions.](../../assets/88b4077db3780766.png)

It can also be used to make [pretty good charts](https://en.wikipedia.org/wiki/Treemapping).

![](../../assets/ae7f68c2ba7db2b8.png)

This is the usual case. You have a rectangle, you randomly split it along an axis. Looks basic, but it gives a lot of mileage once you start applying it recursively.

You can customize it somewhat by changing how the split gets chosen. Is it random, or do you always split the longest length. Are splits down the middle, or off to one side?

The main short comings are the fact is only generates rectangles, and the technique is easily revealed as the first subdivision stretch accross the entire area, and usually stands out once you start adding smaller subdivisions.

![](../../assets/509375a9acbd0d91.png)

The most obvious addition is to switch from starting with a rectangle, to starting with an arbitrary polygon. Then each slice produces smaller polygons, which we can recurse on. Even better, if you start with a [convex polygon](https://en.wikipedia.org/wiki/Convex_polygon) the subdivided ones remain convex, which simplifies a lot of difficulty of subdivision.

![](../../assets/02c9b1319e227be1.png)

If using polygons solves the most obvious “tell” of recursive subdivision, the rectangles, then bent subdivision solves the second, that the earliest slices are really long and stick out. It doesn’t look natural for evolved layouts like roads.

Oleg Dolya proposes solving this by adding exactly one kink to the subdivision. This breaks up the line considerable, and allows both ends of the line to terminate perpendicular to the boundary, and generally adds a level of messiness that I really love.

Oleg has more details on his [own page](https://www.patreon.com/posts/49191011).

![](../../assets/ea41e3bc19011403.png)

Other way to break up the line is to do some sort of random path instead of keeping things straight. Jamis Buck shows how you can do random cellular growth to get a nicer subdivision. His [blog post](https://weblog.jamisbuck.org/2015/1/15/better-recursive-division-algorithm.html) illustrates the idea very clearly, including animations. Note that as he is using recrusive subdivision to make mazes, the long subvidisions manifest as what he calls “bottlenecks”, choke points that clearly divide the graph in two.

It reminds me a bit of [the approach taken by Lenna’s Inception](https://bytten-studio.com/devlog//2014/09/15/overworld-overview-part-2/), where different spaces are iteratively grown until they fill the entire area.

![](../../assets/46b610a9804045eb.png)

I discovered this subdivision in my [Diablo 1 write up](https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/) where it is used in the catacombs levels. It divides the level into 5 sections – one central one and 4 surrounding pieces. I really like it as it’s dead simple, but it avoids having too long a cut. The asymmetry of the central square vs the outer ones also leads to a lot more interesting patterns – realistically, most cities / dungeons / whatever are not uniformly dense, and often have more going on in center than the edges.

I explore more subdivisions of this type in [Exploring Rectangle Subdivisions](https://www.boristhebrave.com/2025/05/03/more-recursive-subdivision-variants/).

![](../../assets/ba50a4e22280b46a.png)

I’m sure this technique is used all over the place, but it’s used to great effect in [this write-up of Pokemon Mystery Dungeon’s level generation](https://www.youtube.com/watch?v=fudOO713qYo). This is the only subdivision scheme that looks more regular than the basic subdivision, so it definitely has its uses.

Pokemon Mystery Dungeon in particular gets more milage out of using a grid by sometimes treating certain cells differently:

- Keep a cell entirely empty
- Keep a cell empty, except for passageways travelling to other cells
- Randomly merging adjacent cells

NB: The equivalent for polygonal systems would be Voronoi partitioning, I guess.

[This page](https://gitlab.com/chriscox/offgrid/-/wikis/home) documents a rectangle based scheme that looks irregular, but it very easy to compute.

![](../../assets/0780bc90b6a3bd3e.png)

If you are recursively dividing, there’s no obligation to divide to the same depth everywhere. This can be used to keep some large spaces available, or add some non-uniformity.

That’s it. Let me know if you’ve seen some other neat techniques in this area.

Some random thoughts:

You can also divide a triangle into four smaller triangles, you can

kind ofdivide a “flat-top” hexagon into seven smaller “pointy-top” hexagons, and you cankind ofdivide a pentagon into six smaller pentagons → see “Penrose tiling”.I don’t know if you would need triangle or pentagon-tiling in any practical application, besides for being interesting. Hexagons are useful in strategy games. Battlebrothers has a hexagon overworld and hexagon tactic maps. (But both they are consist of flat-top hexagons.)

Maybe golden-ratio rectangles are also interesting for some applications.

Recursive subdivision can also be used to efficiently store a map in a tree that was created in any way. → “Quadtree”

Hi! Really nice article and visuals! Just letting you know that two of the images seems to be down or with a bad url (“An animation of a maze…” and “A breakdown of Singapure…”).

Thanks, I’ve fixed now.

Oh that was fast! And they are really cool. Thank you!