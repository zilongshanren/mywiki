---
title: runevision blog
url: https://blog.runevision.com/2013/
published: '2013-09-22'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

One of the problems you'll face when creating an infinite procedurally generated world is that your procedural algorithm is not completely context-free: For example, some block might need to know about neighboring blocks.

![](../../assets/79b677d4fcae98a1.jpg)

To use graphics processing as an example, you might have an initial noise function which is completely context-free, but very often an interesting procedural generation algorithm will also involve a blur filter, or something else where the local result depends on the neighboring data. But since you only have a part of the world loaded/generated at a time, what do you do at the boundaries of the loaded area? The neighboring pixels or data isn't available there since it isn't loaded/generated yet. The layer-based approach I describe in this post and video is a way to address this issue.

I hinted at this layer-based approach in the overview post [Technologies in my Procedural Game The Cluster](http://blog.runevision.com/2013/02/technologies-in-my-procedural-game-eas.html). I have also written a post [Rolling Grids for Infinite Worlds](http://blog.runevision.com/2013/05/rolling-grids-for-infinite-worlds.html) with the source code for the RollingGrid class I use for achieving practically infinite grids; only bounded by the Int32 min and max values.

I use two different layer-based approaches in The Cluster: *Encapsulated layers* and *internal layers*.

*Encapsulated layers* are the most flexible and what I've been using the most. Encapsulated layers can depend on other encapsulated layers, but don't know about their implementation details, and different encapsulated layers can use completely different sizes for the chunks that are loaded. I might go more in details with this some other time.

Recently I implemented the simpler *internal layers*. Internal layers are tightly coupled. They share the same grid, but chunks in the grid can be loaded up to different layer levels. I explain this in more detail in this video below.

That's it for now. You can read [all the posts about The Cluster here](http://blog.runevision.com/search/label/TheCluster).

### 2024 update: LayerProcGen framework released

I've now released a framework called [LayerProcGen](https://github.com/runevision/LayerProcGen) as open source which implements the layer-based procedural generation techniques discussed here.


I want to share how I do the rolling grids I use in The Cluster that in essence acts as infinite 2D arrays.

Originally, my procedural game The Cluster (*you can read all the posts about The Cluster here*) was divided into "levels". The levels lined up seamlessly so wouldn't be noticed by the player, but in the implementation they were completely separate. Tons of code was used to deal with the boundaries of the levels. Every algorithm that handled some kind of grid, and which looked at neighbor cells in that grid, had to have special boundary case handling for the edges, which was a pain.

In 2012 I completely rewrote this to instead be based on a set of layers of infinite grids. Each layer loads/generates chunks on demand, but exposes an interface where this is abstracted away making the layer in essence "infinite". This approach has removed the need for almost all boundary case handling related to edges of grids.

An infinite grid could be implemented as a dictionary, but dictionaries have a large overhead. I wanted performance that was much closer to a regular 2D array. A rolling grid *is* just a 2D array with some very lightweight number conversions on top.

You can use rolling grids when you load/generate data (such as chunks of the world) in a grid locally around some position; typically the player's position. As the position moves, you load/generate new chunks in front, and destroy the ones that are now further away in order to keep the loaded chunks centered around the position in focus. You have to make sure yourself that you don't have cells loaded that are too far apart, and you also need to not attempt to read cells that are further out than the currently loaded area.

### Usage

When creating the grid you'll need to know the maximum size of the area you may need to have loaded at once. E.g. you can create a 40x40 grid if you know you'll never have chunks loaded simultaneously that cover more than a 40x40 area.

`RollingGrid<LevelChunk> myRollingGrid = new RollingGrid (40, 40);`


When a new data cell has been loaded/generated you assign it to the grid like this:

`myRollingGrid[x, y] = myNewLevelChunk;`


When you have destroyed a data cell, you must set it to *null* in the rolling grid:

`myRollingGrid[x, y] = null;`


That's it!

### RollingGrid class

Note about the code: You'll have to replace Logic.LogError() with your own favorite logging mechanism of choice.

```
public class RollingGrid<T> where T : class {
private int m_SizeX, m_SizeY;
private int[] m_ColItems, m_RowItems;
private int[] m_ColIndices, m_RowIndices;
private T[,] m_Grid;
public RollingGrid (int sizeX, int sizeY) {
m_SizeX = sizeX;
m_SizeY = sizeY;
m_Grid = new T[sizeX, sizeY];
m_ColItems = new int[sizeX];
m_RowItems = new int[sizeY];
m_ColIndices = new int[sizeX];
m_RowIndices = new int[sizeY];
}
public T this[int x, int y] {
get {
int modX = Util.Mod (x, m_SizeX);
int modY = Util.Mod (y, m_SizeY);
if ((m_ColIndices[modX] != x && m_ColItems[modX] > 0) ||
(m_RowIndices[modY] != y && m_RowItems[modY] > 0))
Logic.LogError ("Position ("+x+","+y+") is outside "
+"of RollingGrid<"+typeof (T).Name+"> current area.");
return m_Grid[modX, modY];
}
set {
int modX = Util.Mod (x, m_SizeX);
int modY = Util.Mod (y, m_SizeY);
// Check against book-keeping
if (m_ColItems[modX] > 0 && m_ColIndices[modX] != x)
Logic.LogError ("Trying to write to col "+x+" ("+modX+") "
+"but space already occupied by col "+m_ColIndices[modX]);
if (m_RowItems[modY] > 0 && m_RowIndices[modY] != y)
Logic.LogError ("Trying to write to row "+y+" ("+modY+") "
+"but space already occupied by row "+m_RowIndices[modY]);
T existing = m_Grid[modX, modY];
// Early out if new and existing are the same
if (existing == value)
return;
// Don't allow overwriting
if (existing != null && value != null)
Logic.LogError ("Trying to write to cell "+x+","+y+" "
+"but cell is already occupied");
// Set value
m_Grid[modX, modY] = value;
// Do book-keeping
m_ColIndices[modX] = x;
m_RowIndices[modY] = y;
int delta = (value == null ? -1 : 1);
m_ColItems[modX] += delta;
m_RowItems[modY] += delta;
}
}
public T this[Point p] {
get { return this[p.x, p.y]; }
set { this[p.x, p.y] = value; }
}
}
```


You'll also need this Modulus function which return a number between 0 and *period* no matter of the input *x* is positive or negative. I use these modified modulus and division functions all over the place in my game, wherever I need to convert between different coordinate systems.

```
public class Util {
public static int Mod (int x, int period) {
return ((x % period) + period) % period;
}
public static int Div (int x, int divisor) {
return (x - (((x % divisor) + divisor) % divisor)) / divisor;
}
}
```


If you're wondering why there's two native modulus (%) operations in there instead of simply only adding *period* if the number is negative, it's because I measured it to be faster than the cost incurred by a branch - see [branch prediction](http://en.wikipedia.org/wiki/Branch_predication).

### Automating it further

A single rolling grid can be nice in itself, but the real beauty in The Cluster is how the different data layers automatically keep track of which chunks needs to be loaded and unloaded based on dependencies from higher level layers. But that's material for future posts.


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


I wrote a blog entry on the Unity site called [Automatic Setup of a Humanoid](https://web.archive.org/web/20130228034432/http://blogs.unity3d.com/2013/02/07/automatic-setup-of-a-humanoid/) detailing the work I did for the Mecanim animation system in Unity 4 on automatically detecting human bones in arbitrary skeleton rigs.

Names of bones, bone directions, bone length ratios, and bone topology all provide hints to which bones should be mapped to what. While none of those sources are very reliable on their own, they can be combined and used in a search algorithm to get rather reliable results.

![](../../assets/e967a78d9fabd879.jpg)