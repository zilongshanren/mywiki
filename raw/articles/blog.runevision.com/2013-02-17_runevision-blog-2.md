---
title: runevision blog
url: https://blog.runevision.com/2013_02_17_archive.html
published: '2013-02-17'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

*This post is about The Cluster, my 2.5D platform game under development with focus on non-linear exploration, set in a big, continuous world. You can read all the posts about The Cluster here.*

In this post I'm creating an overview of the different technical aspects of The Cluster and listing links to posts I've written in each area. I'm also describing areas I haven't written about (yet).

If there's any of these areas you'd like to hear more about, let me know in the comments. This can help me decide which areas to prioritize in future posts.

### Level Design

The level design in The Cluster is "deliberate", meaning that aspects of a level are created on purpose rather than randomly, like it is the case in games like MineCraft. With gameplay that doesn't allow removing or adding terrain, the levels have to be guaranteed to be traversable from the start.

- Maze Generation and Key/Lock Placement

### Terrain Generation

The terrain in The Cluster is based on a 3D grid of blocks (popularly known as "voxels" although they are not really) and mesh geometry is generated based on this. The geometry has smoothed edges and support for textured transitions at edges and between blocks of different materials.

- Level Geometry
[Sweet Sweet Edges](http://blog.runevision.com/2011/05/eas-sweet-sweet-edges.html)(2011)[First Peek at Levels](http://blog.runevision.com/2010/06/first-peek-at-levels-in-eas.html)(2010)- Level Props
- Using Imposters

### AI / Path-finding

The enemies in The Cluster are not simply patrolling back and forth on a platform - they have the ability to follow the player almost anywhere, or flee away.

- Game Play Implications
- Procedurally Created Path-finding Graph

### Camera Behaviour

A side-scrolling game is not the hardest to create a basic working camera behavior for, but there is a lot that can be done to elevate the behavior from "good enough" to "great". One thing is having the camera look ahead rather than trailing behind, but without introducing sudden camera moves when changing direction. (The classic Sonic games did this too.) Another is to frame what's important at the position where the player is currently at.

- Tips for a Platformer Camera
- Level Aware Framing

### Use of Threading

The Cluster originally used a clumsy mix of Unity co-routines and threading for its procedural generation, but it has since been rewritten to do all generation completely in a background thread, except for the actual instantiations, which happen in the main thread, spread out over multiple frames.

- Generate in Background Thread, Instantiate in Main Thread
- Working With Unity Objects in Threads

### Layers of Infinite Grids

Originally, The Cluster was divided into "levels". The levels lined up seamlessly so wouldn't be noticed by the player, but in the implementation they were completely separate. Tons of code was used to deal with the boundaries of the levels. Every algorithm that handled some kind of grid, and which looked at neighbor cells in that grid, had to have special boundary case handling for the edges, which was a pain.

In 2012 I completely rewrote this to instead be based on a set of layers of infinite grids. Each layer loads/generates chunks on demand, but exposes an interface where this is abstracted away making the layer in essence "infinite". Layers can depend on lower layers with a specified amount of "padding". A layer can then freely access a lower layer as long it is doesn't try to access it outside of the contractual bounds. This approach has removed the need for almost all boundary case handling related to edges of grids. At the same time it has enforced a much more well-structured division of information and storage in the generation algorithms.

[Rolling Grids for Infinite Worlds](http://blog.runevision.com/2013/05/rolling-grids-for-infinite-worlds.html)(source code) (2013)- Layers Upon Layers (or How to Avoid Dealing with Boundary Cases)
[Layer-Based Procedural Generation](http://blog.runevision.com/2013/09/layer-based-procedural-generation-for.html)(video) (2013)

### Debug Options

With a game as complex as The Cluster there is a need for tons of different kinds of debug information that can easily be switched on and off while running the game. For a long time, this was a bit tedious to maintain, but I recently found a more or less elegant way to add debug options in-place in the code where it's needed and have the GUI that displays the available debug work pick-up all the options automatically, without any maintenance.

- Automatic GUI for Debug Options

I'll update and maintain this post as I write more posts, and as the game evolves.