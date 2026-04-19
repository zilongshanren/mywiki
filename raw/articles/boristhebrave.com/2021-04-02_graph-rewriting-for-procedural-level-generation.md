---
title: Graph Rewriting for Procedural Level Generation
url: https://www.boristhebrave.com/2021/04/02/graph-rewriting/
author: Boris
published: '2021-04-02'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve been doing this series on how [games do level generation](https://www.boristhebrave.com/category/level-generation/) for some time, and I have a complete beauty for you.

I’ve spent a lot of time deconstructing [Unexplored](https://store.steampowered.com/app/506870/Unexplored/), a 2017 indie game by Joris Dormans. It just *nails* procedurally generated zelda-like dungeons, and I had to know for myself how the magic happens. Fortunately, most of the generation logic is written in a custom language, PhantomGrammar, so between that and some help from the developers, I think I’ve got a pretty good idea how it works.

The ideas of Unexplored are so interesting that I felt they deserved an article in it’s own right. The game is centered around a concept called [ Graph Rewriting](https://en.wikipedia.org/wiki/Graph_rewriting), which, while well understood academically, is rarely used in games. I’m going to spend

**this article**talking about that technique alone, then how

[PhantomGrammar specifically uses and extends it](https://www.boristhebrave.com/2021/04/02/phantomgrammar-and-ludoscope/). Finally I will talk about how

[these techniques are put together in Unexplored](https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/)to make such sophisticated levels.

## Graphs

[ Graphs](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) are a computer science concept (nothing to with charting). A graph contains a number of

**nodes**, and

**edges**between them. They are very good for representing relationships between things. I discussed graphs quite a bit in

[Lock and Key Dungeons](https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons/).

An example of a graph would be Facebook friendships. Each node is one user, and there is an edge between any pair of users that are friends. Another example is the internet, where each page is a node, and each link is an edge. The latter is a ** directed graph** as each link as a clear direction, it is from one page to another.

![](../../assets/ed5dab2fed73396f.png)

In this diagram, the shapes and letters are data attached to each node. I’ll also use numbers when I need to uniquely identify a node.

## Graph Rewriting

**Graph Rewriting** is much like textual replacement – we have a find pattern which matches a small subset of the entire data and a replace pattern that will replace the matched part only. I covered a bit how find-and-replace has many uses in [my Diablo writeup](https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/), but that was on a fixed grid.

![](../../assets/0d73c5a0fee6fc48.png)

[“Generating Missions and Spaces for Adaptable Play Experiences” Joris Dormans and Sander Bakkes](http://sander.landofsand.com/publications/Dormans_Bakkes_-_Generating_Missions_and_Spaces_for_Adaptable_Play_Experiences.pdf)

The above is an example of a replacement rule.

The rule has a left side, and a right side. The left hand side is what to find – in this case, it looks for a node of type A connected to a node of type B. We’ll call these nodes 1 and 2.

The right hand side is what to replace with. Node 1 has now become a node of type a, and node 2 has become a node of type A. Two new nodes have been created, and the edges have been moved around.

Using the numeric identifiers, we can distinguish between changing an existing node and adding / deleting nodes. This is important as the found pattern will only be part of a larger graph, and we want to preserve edges that aren’t part of the pattern, as demonstrated below.

![](../../assets/257e4f0d5fb6c2ef.png)

(1) shows a graph before we apply the above rule.

(2) shows us matching the rules find pattern to part of the graph.

(3-6) show changing the graph according to the replacement pattern.

(7) is the graph after the rule is done. Note that if we applied the rule a second time, it would match the newly create A and B, and make an even more complicated graph.

Graph rewriting may seem like a simple concept but in fact it’s a very expressive system. It’s easy to write rules that generate long chains, forks, hubs and more complex structures. You might want to contrast it with [L-Systems](https://en.wikipedia.org/wiki/L-system), which are another procedural generation technique. L-Systems also works via replacement, and can produce some beautiful patterns.

## Graph Rewriting in the World

Graph Rewriting is not a common technique, but it comes up more frequently than you might think. Often it’s in a limited form where only certain sorts of replacements are possible. Please let me know of other examples if you find them!

[Enter the Gungeon](https://www.boristhebrave.com/2019/07/28/dungeon-generation-in-enter-the-gungeon/) uses some graph replacement rules to vary the content of it’s dungeons. But typically the find patterns are only a single room.

[Dungeon Architect](https://docs.dungeonarchitect.dev/ue4/snap-flow/snap-flow-graph), a popular Unity/Unreal asset of procedurally generated dungeons, supports complex patterns, but no loops.

![](../../assets/aa8d6180b25f957c.png)

In [their paper “Generating Missions and Spaces for Adaptable Play Experiences](http://sander.landofsand.com/publications/Dormans_Bakkes_-_Generating_Missions_and_Spaces_for_Adaptable_Play_Experiences.pdf)” Dormans and Bakes describe how simple rules that generate and re-order lock/keys can be combined to generate a complex structure.

In fact, Joris Dormans has spent a lot of his career thinking carefully about Graph Rewriting for games. He’s written multiple academic papers on it, it influenced machinations.io, a games-design startup he co-founded, and it has formed the core for games created by his solo-dev development studio, Ludomotion.

Over the course of all this work, he built tools to help develop these ideas further. Most notable is PhantomGrammar and Ludoscope, which include numerous extensions to graph rewriting to make it easier to work with and more practical. [We’ll look at those next](https://www.boristhebrave.com/2021/04/02/phantomgrammar-and-ludoscope/).