---
title: runevision blog
url: https://blog.runevision.com/2013/05/
published: '2013-05-02'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

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