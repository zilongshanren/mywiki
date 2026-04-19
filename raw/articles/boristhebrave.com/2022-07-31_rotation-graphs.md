---
title: Rotation Graphs
url: https://www.boristhebrave.com/2022/07/31/rotation-graphs/
author: Boris
published: '2022-07-31'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

[Graphs](https://en.wikipedia.org/wiki/Graph_(topology)) are a data structure [we’ve already talked a lot](https://www.boristhebrave.com/tag/graphs/). Today we’re looking at extension of them which is both obvious and common, but I think is rarely actually discussed. Normal graphs are just a collection of nodes and edges, and contain no spatial information. We’re going to introduce **rotation graphs **(aka [ rotation maps](https://en.wikipedia.org/wiki/Rotation_map)) that contain just enough information to allow a concept of turning left or right – i.e. rotation.

Table of Contents

A **rotation graph** is an undirected graph where each outgoing edge is [labeled](https://mathworld.wolfram.com/LabeledGraph.html) with the integers 0 to d-1, where d is the number of outgoing edges (the **degree** of the vertex). The labels from a given node are each unique. A **rotation map** is the function that given a node and an edge label, returns the neighbor node that edge leads to, and the edge label that would lead back to the first node. The two forms are basically equivalent representations.

For example, we could have a rotation graph labeled like so:

[half-edges](https://en.wikipedia.org/wiki/Doubly_connected_edge_list)” for this reason.

Which corresponds to a rotation map:

| From | To |
|---|---|
| (A, 0) | (B, 0) |
| (A, 1) | (C, 0) |
| (B, 0) | (A, 0) |
| (B, 1) | (C, 1) |
| (C, 0) | (A, 1) |
| (C, 1) | (B, 1) |

The easiest way to think about it, is that on a normal graph, each node has an *unordered* set of neighbours. But for a rotation graph, the neighbours are instead in a neat, *ordered *list.

This is why they are secretly incredibly common. When coding a graph, you often store the neighbours in a list anyway. Why not make that order actually mean something?

It turns out these additional labels are all you need to add a sense of direction to graphs.

Imagine I am standing on node A, and “facing” towards edge label 1. If the edges are labelled clockwise, then I can “turn” right by increasing the edge label by 1. And I can turn left by decreasing it. In either case, I need to wrap around from 0 to d-1 and visa versa. And you can perform a combined “step forward then about-face” by following the rotation map to a new node, and a new edge label.

So we have a rudimentary sort of [tank controls](https://en.wikipedia.org/wiki/Tank_controls) for navigating the graph. All without introducing any notion of position. It’s like each edge warps you from the exit of one node to the entrace of another, basically like a bunch of levels with connectors between them.

It turns out you can actually accomplish a lot with these sort of tank controls. Let’s look at some examples.

Something I’ve often played with is viewing 3d meshes as graphs, with each face becoming one node, and adjacent faces having an edge between their nodes. In fact, they work a lot better as rotation graphs than normal graphs.

I’ve found this sort of mesh representation incredibly useful over the years. It allows you to easily describe motion over the surface of the mesh without any reference to the shape of the mesh (just it’s [topology](https://www.blenderbasecamp.com/what-is-mesh-topology-in-3d-modeling/)). No messing around with 3d vectors needed.

I used this represention in my [celtic-knots](https://github.com/BorisTheBrave/celtic-knot) plugin for blender, which can turn any mesh into celtic style knotwork. And I use it extensively in [Tessera](https://assetstore.unity.com/packages/tools/level-design/tessera-pro-161077) as a way of extending WaveFunctionCollapse from working on square grids, to working on any graph with nodes of degree 4.

Rotation graphs capture one of the fiddliest parts of working this way with meshes – the fact is that each face has a local sense of which way is up. When transitioning between faces, you often need to apply some sort of adjustments. The rotation map spells out exactly what sort of adjustment. If you leave a node via edge label 0, and arrive via edge label 1 (for example, going from node D to node E in the cube diagram above), then that tells you a 90 degree rotation is needed. And indeed, if you unfold the cube to leave D and E next to each other, that rotation is immediately apparent:

Another neat trick is to reconstruct the mesh from the rotation graph. If you repeated step-forward-and-about-face, then turn one notch clockwise, then you’ll circle a vertex of the original mesh until you get back to where you started. You can use these loops to determine the vertices (equivalently, the nodes of the dual graph).

Rotation graphs can be viewed as a “lite” version of the [half-edge data structure](https://en.wikipedia.org/wiki/Doubly_connected_edge_list), which also has a lot of uses in geometry processing.

[HyperRogue](https://roguetemple.com/z/hyper/) is an extraordinary roguelike, played on a constantly shifting hyperbolic tiling.

![](../../assets/f403c54d3e76e8a5.png)

Tiles in HyperRogue have either 6 or 7 neighbours, and and form a grid using some sophisticated maths. They are in [hyperbolic space](https://en.wikipedia.org/wiki/Hyperbolic_geometry), which needs a special projection to be converted to a 2d image. But all those details can be ignored for purposes of navigation, AI and game logic, because [under the hood](https://github.com/zenorogue/hyperrogue/blob/master/locations.cpp), it just generates a rotation graph for any tile near the player.

Each step in the world involves following the rotation map (i.e. a step-plus-about-face), then we increase the edge label by an additional 3 or 4 to keep the player oriented roughly forward. When stepping onto a 7 sided tile, the choice of edge label has to be randomized as there is no opposite edge which keeps the player facing exactly the same way.

**vividlope** is another game where user movement is based off a weirdly shaped mesh. Rotation graphs solve the confusion of what happens during sharp edges and curved segments. Note how the pushed barrels follow the curve of the level – they are just moving “forward”, where forward is changing over time.

The most common, but a less visible use of rotation maps is in room-to-room (or level-to-level) transitions in games. Many games dispense with showing connecting corridors, and just sort of teleport the player between separately loaded areas. But there’s no obligation for these areas to be rigidly located with respect to each other and often in games they’re not.

This is made a bit more obvious, say, in a game like Zork.

![](../../assets/987e8c2fd3265f5f.png)

In Zork, you start the game West of House. Going “north” actually moves you north-eastish in the game world. And to go back, you cannot go south, you must go “west”. The edge label “north” actually causes to turn 90 degrees around the house. Games like Zork often store these relations as a rotation map. So that, if you lock a door from one side, the game can easily determine that other side of the door, in a completely different room, is also locked.

Even Metroidvanias like Hollow Knight, which pride themselves on consistently laid out maps, [cheat this way occasionally](https://youtu.be/kMQTvSIAehQ?t=1467).

One limitation of Rotation Graphs is that they only work for [orientable](https://en.wikipedia.org/wiki/Orientability#Orientability_of_manifolds) surfaces.

Orientable basically means that “clockwise” has a well defined meaning. Surfaces like a [Möbius strip](https://en.wikipedia.org/wiki/M%C3%B6bius_strip) aren’t orientable as completing a full loop leaves you mirrored compared with where you started. You need an extra boolean to track mirroring in the rotation map to support this (which HyperRogue does, I believe).

You can also run into trouble with graphs that don’t represent a surface at all. After all, if you number the edges 0 to d-1 in a clockwise loop, it’s implied there’s a surface that you are turning clockwise on. It’s possible to enhance the concept to support things like [honeycombs](https://en.wikipedia.org/wiki/Honeycomb_(geometry)), but it’s fairly extensive.