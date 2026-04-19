---
title: Fast Traversal Queries of Procedurally Generated Rooms
url: https://www.boristhebrave.com/2017/07/08/fast-traversal-queries-of-procedurally-generated-rooms/
author: Boris
published: '2017-07-08'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve been playing around with procedural generation recently, and one question has repeatedly been nagging at me.

How can you randomly spice up a level while making sure you don’t accidentally block off the exit?

Jump to [the code](https://github.com/BorisTheBrave/fast-traversability-checking/blob/master/traversability.ts), the [live demo](https://www.boristhebrave.com#demo).


## The problem

To cut the problem down to the bare bones, say you’ve got a top down tile based room like this.

![](../../assets/ba517f55685f9605.png)


![](../../assets/ba517f55685f9605.png)

[fictionaldogs of ZFGC](http://zfgc.com/forum/index.php?topic=41500.0))

The player enters from the top, and leaves via the bottom. We want to add a block, ![](../../assets/6193b414ca786ed0.png)


Some locations are are ok to put the block:

![](../../assets/40c433219346be83.png)


![](../../assets/40c433219346be83.png)

Others are not, as it is no longer possible to walk out the exit.

![](../../assets/fca752743d489830.png)


![](../../assets/fca752743d489830.png)

In this room the answer is easy – you can put the block anywhere, as long as it’s not directly in front of the entrance or exit. But for a larger, more complicated room, or a larger, more complicated block, this is not so easy to solve. If the room is a huge maze, you effectively have to solve the maze to determine if blocking off one corridor makes a difference.

## Flood filling

The simple way to solve this is path finding. Or, since we don’t really care about the actual path taken, [flood filling](https://en.wikipedia.org/wiki/Flood_fill).

To determine if a block is ok to place, simply place it, and flood fill all the walkable squares starting with the entrance. If you ever reach the exit, then there’s still a path from one to the other and the block is ok. Otherwise, you must remove it and try again.

## The smart way

The problem with the above approach is it is slow. I wanted to determine all safe locations on a large map. But each location required you to flood fill the entire area from scratch.

[Disjoint-set data structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) to the rescue. This data structure lets you hold a bunch of sets, and merge any two sets together extremely efficiently.

It can often be used much like the flood fill algorithm. Simply add every tile as a set of one tile. Then for every pair of walkable tiles that are adjacent, merge the respective sets of those tiles. At the end, if the entrance and exit tiles are in the same set, then they are connected. Otherwise, they are not.

The crucial difference from flood fill is that you can walk the adjacencies in *any* order, you don’t need to seed from one point and track what is currently being processed. That means, we can do all the merging that is far away from the block first of all. Then we can re-use what is computed so far for many different block positions (or shapes), as those far away tiles will have the same connectivity properties each time.

## My algorithm

First I precompute a bunch of disjoint-set data structures (DSDS objects). I compute one for each possible vertical slice of room that sweeps either to one edge or the other:

![](../../assets/9c124d4531b97ff0.png)


![](../../assets/9c124d4531b97ff0.png)

These can be very efficiently computed serially, by processing tiles left to right, then right to left. The respective DSDS objects are also very memory efficient, as they can actually share a lot of overlapping data. (this elaboration is called a [Persistent data structure](https://en.wikipedia.org/wiki/Persistent_data_structure), the code with this article shows how it works).

Then, once you have a block placement you want to test, you find the slices that bracket it. This gives you connectivity information for the left and right sides of the block pre-computed. All you need do is continue merging sets based on connectivity in the small central column. Then, as before, you check if the entrance and exit blocks are in the same set.

That’s it. Take a look at the code [here](https://github.com/BorisTheBrave/fast-traversability-checking/blob/master/traversability.ts).