---
title: The Poor Man's Voxel Engine
url: https://etodd.io/2015/02/18/the-poor-mans-voxel-engine/
published: '2015-02-18'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# The Poor Man's Voxel Engine

This is not a tutorial. It's a story. A Voxel Odyssey.

The story starts with 19 year old me in a dorm room next to the Ohio State stadium. I don't have the repo from this stage of development (SVN at the time), but I remember the process clearly.

![](../../assets/80a4510ed4fd278a.jpg)


![](../../assets/80a4510ed4fd278a.jpg)

[Photo by Kristen Sutton](http://www.osu.edu/imageoftheday/index.php?pick=2009-04-13)

XNA 4 comes out in
[September 2010](http://blogs.msdn.com/b/shawnhar/archive/2010/09/18/10063476.aspx).
I immediately dive in. This turns out to be a poor life decision.

For some reason, one of the very first things I implement is motion blur. I think this is Lemma's first screenshot, although at this point, it's a cartoony third-person game called "Parkour Ninja":

![](../../assets/aad8c863458ac666.jpg)


![](../../assets/aad8c863458ac666.jpg)

I skip past the initial naive implementation of spawning a cube for each voxel
cell. My first move is to iterate over these individual cells and combine them
into larger boxes using
[run-length encoding](https://en.wikipedia.org/wiki/Run-length_encoding).

![](../../assets/e595fe11e375e47e.png)


![](../../assets/e595fe11e375e47e.png)

![](../../assets/e710f9b5eb7f7438.png)


![](../../assets/e710f9b5eb7f7438.png)

![](../../assets/d46e4ec70f4a437a.png)


![](../../assets/d46e4ec70f4a437a.png)

Performance is already a problem even at small scales. I'm re-optimizing the entire scene every time I make an edit. Obviously, my next move is to only optimize the parts I'm editing.

This turns out to be difficult. Take this example:

I add a cube at the top of this stack. To optimize this into a single box, I have to search all the way to the bottom of the stack to find the beginning of the large box, then add 1 to its height and delete my little cube addition.

To speed this process up, I allocate a 3D array representing the entire scene. Each cell stores a pointer to the box it's a part of. Now I can query the cells immediately adjacent to my new addition and quickly get a pointer to the large box next to it.

Removals are the next challenge. My first idea is to split the box back into individual cells, then run the optimizer on them again.

![](../../assets/3e62ec431175a202.png)


![](../../assets/3e62ec431175a202.png)

![](../../assets/277df81c780f6967.png)


![](../../assets/277df81c780f6967.png)

![](../../assets/ac515aa74b5c02be.png)


![](../../assets/ac515aa74b5c02be.png)

![](../../assets/dd1b7233e56ca51d.png)


![](../../assets/dd1b7233e56ca51d.png)

This turns out to be horribly slow. I soon realize that rather than splitting the box into individual cells, I can skip a few steps and split it into "sub-boxes". I still run the optimization algorithm afterward, but I can make its life easier.

I am thrilled to get this demo running on my roommate's Xbox 360. It fails to impress the girls in the neighboring suite.

### Goodbye Xbox

I quickly run into more issues. The CLR's floating point performance is absolutely abysmal on Xbox 360. The physics engine breaks down and cries after spawning 10 boxes or so. I decide to target PCs instead.

### Textures

I render scenes by copying, stretching, and scaling a single cube model. Slapping a texture on this cube turns out to be a horrible idea that looks something like this:

![](../../assets/229123b47d6b700f.png)


![](../../assets/229123b47d6b700f.png)

To avoid texture stretchiness, I eventually write a shader to generate UVs based on the position and normal of each vertex. Here's the final version for reference:

```
float2x2 UVScaleRotation;
float2 UVOffset;
float2 CalculateUVs(float3 pos, float3 normal)
{
float diff = length(pos * normal) * 2;
float2 uv = float2(diff + pos.x + (pos.z * normal.x), diff - pos.y + (pos.z * normal.y));
return mul(uv, UVScaleRotation) + UVOffset;
}
```


### Instancing

Next, another performance crisis. Somehow I realize that doing a whole draw call for each and every box in a scene is a Bad Idea™. So I take the obvious step and... use hardware instancing. Yes.

Incredibly, I'm actually proud of my work so far. Somewhere around this time I also discover my lifelong love of terrible music.

*is*this game?

### Improved level format

At this point, I'm saving and loading levels via .NET's XML serialization. Apparently XML is still a good idea in 2010. The voxel format is simply a 3D array represented as an XML string of ASCII 1s and 0s. Every time I load a level, I have to re-optimize the entire scene. I solve this by storing the boxes themselves in the level data as a base64 encoded int array. Much better.

### Per-surface rendering

I start building larger levels and run into another graphics performance problem. The engine is simply pushing too many triangles. In a complex scene, a significant chunk of boxes are surrounded on all sides by other boxes, completely hidden. But I'm still rendering them.

I solve this problem by breaking each box into its individual faces. I actually iterate across the whole surface to determine what parts (if any) are visible. Shockingly, this turns out to be terrifically slow. I eventually mitigate the issue by caching surface data in the level file.

I render all these surfaces via... drum roll... instancing. Yes, really. I open
Blender, create a 1x1 quad, export it, and instance the heck out of that
thing. These are dark times. But I'm finally able to render some larger
landscapes:
![](../../assets/414a2fc5dcecbe74.jpg)


### Physics

Time to see some cool physics. I now have two kinds of voxel entities: the
static voxel, represented in the physics engine as a series of static boxes,
and the dynamic voxel, represented as a single physics entity with a compound
collision volume constructed of multiple boxes (I should plug the incredible
[BEPUPhysics](http://www.bepuphysics.com/) for making this
possible). It works surprisingly well:

Around this time I also switch to a deferred renderer, which is why I spawn an unreasonable number of lights at the end of that video.

### Chopping down trees

Now it's time to take physics to the next level. My goal is simple: I want the player to be able to cut down a tree and actually see it fall over, unlike Minecraft.

This lofty dream is basically a graph problem, where each box is a node connected to its adjacent neighbors. When I empty out a voxel cell, I need a fast way to determine whether I just partitioned the graph or not.

So I add an adjacency list to the box class. Again, shockingly, calculating adjacency turns out to be a huge bottleneck. I later cache the adjacency data in the level file, which eventually balloons to several megabytes.

Now every time the player empties out a voxel cell, I do a breadth-first search
through the *entire* scene, marking boxes as I go. This allows me to
identify "islands" created by the removal of the voxel cell. I can then spawn
a new physics entity for that island and break it off from the main scene.

I eventually come up with the idea of "permanent" boxes, which allows me to stop the search whenever I encounter a box that cannot be deleted.

I design a new enemy to showcase the new physics capabilities. I also test the limits of awkwardness and social norms by narrating gameplay footage in a dorm room full of people studying.

### Chunks

Around this time I learn about
[broadphase collision detection](http://www.metanetsoftware.com/technique/tutorialB.html).
My engine is scattering thousands of static boxes around the world, which
makes it difficult for BEPUPhysics' broadphase to eliminate collision
candidates. At the same time, it's becoming obvious that rendering the entire
world in a single draw call is a bad idea.

I fix both of these issues by splitting the world into chunks. Each chunk has a static triangle mesh for physics, and a vertex buffer with basically the same data for rendering. Since I have to regenerate both of these meshes every time a chunk is modified, the chunk size can't be too large. Also, smaller chunks allow for more accurate frustum culling.

At the same time, the chunks can't be too small or the draw call count will explode. After some careful tuning I eventually settle on 80x80x80 chunks.

![](../../assets/52a5bc22e41eceb9.jpg)


![](../../assets/52a5bc22e41eceb9.jpg)

### Partial vertex buffer updates

This is probably the low point.

By now, I am incredibly proud of my "loosely coupled" architecture. I have a Voxel class and a DynamicModel class which know nothing about each other, and a ListBinding between the two which magically transforms a list of Boxes into a vertex buffer.

Somehow, probably through questionable use of the .NET Timer class, I locate a bottleneck: re-sending an entire vertex buffer to the GPU for every voxel mutation is a bad idea. Fortunately, XNA lets me update parts of the vertex buffer individually.

Unfortunately, with all the surface culling I do, I can't tell where to write in the vertex buffer when updating a random box. Also, how to shoe-horn this solution into my gorgeous cathedral architecture.

This conundrum occurs during the "dictionary-happy" phase of my career. Yes. The ListBinding now maintains a mapping that indicates the vertex indices allocated for each box. Now I can reach into the vertex buffer and change things without re-sending the whole buffer! And the voxel engine proper still knows nothing about it.

This turned out to never really work reliably.

### Multithreading

I lied earlier, this is probably the low point.

Voxel mutations cause noticeable stutters by now. With no performance data to speak of, I decide that multithreading is the answer. Specifically, the worst kind of multithreading.

I spawn a worker thread, sprinkle some locks all over the place, et voilà! It's multithreaded. It gains perhaps a few milliseconds before the main thread hits an unforeseen mystical code path and the menu somehow manages to acquire a lock on the physics data.

I am ashamed to admit that I never got around to correcting this colossal architectural faux pas.

![](../../assets/cd95c8cef8f5b06a.jpg)


![](../../assets/cd95c8cef8f5b06a.jpg)

### Large Object Heap

I'm now building large enough levels to run into memory issues. Turns out, the
.NET runtime allocates monstrous 80x80x80 arrays differently than your
average object. I write more about this
[here](https://etodd.io/2012/10/22/allocating-large-arrays-in-net/).

Long story short, the garbage collector doesn't like to clean up large objects. I end up writing a custom "allocator" that hands out 3D arrays from a common pool. Later, I realize most of the arrays are 90% empty, so I break each chunk into 10x10x10 "sub-chunks" to further reduce memory pressure.

This episode is one of many which explain my present-day distaste for memory-managed languages in game development.

### Graduation

I graduate and work at a mobile game studio for the next year. The engine doesn't improve much during this time, but I start to learn that almost everything I know about programming is wrong and incomplete.

![](../../assets/50e7b5fcb4537122.jpg)


![](../../assets/50e7b5fcb4537122.jpg)

I leave my job in February 2014 and continue hacking the engine. By now it's over 30k LOC and I am morally and spiritually unable to start over on it.

### Goodbye allocations

With my newfound awareness of the .NET heap, I realize that my vertex arrays for physics and rendering are also probably landing in the Large Object Heap. Worse, I am reallocating arrays every time they change size, even if only to add a single vertex.

I genericize my
[Large Object Heap allocator](https://github.com/et1337/Lemma/blob/master/Lemma/Util/LargeObjectHeap.cs)
and shove the vertex data in there. Then, rather than allocating arrays at
exactly the size I need, I round up to the next power of 2. This cuts the
number of allocations and makes it possible for my allocator to reuse arrays
more often.

### Goodbye cathedral

I finally throw out the "loosely coupled" ListBinding system and pull the vertex generation code into the voxel engine itself. The resulting speed boost is enough for me to go back to re-sending entire vertex buffers rather than faffing about with partial updates.

### Goodbye index buffer

Up to this point, I've been maintaining an index buffer alongside the vertex buffer. In a much overdue stroke of "genius", I realize that since none of the vertices are welded, the index buffer is just a constantly repeating pattern, which is in fact the same for every voxel.

I replace the individual index buffers with a single, global buffer which gets allocated to the nearest power of 2 whenever more indices are needed.

### Bit packing and compression

Many numbers in the level data format are guaranteed to fall in the 0-255
range. My friend decides to pack these numbers more efficiently into the
integer array. He writes about it
[here](http://geel.io/post/88710536090/efficient-bitpacking-in-lemma).

I also pull in third party library #27
([SharpZipLib](https://icsharpcode.github.io/SharpZipLib/)) and
start zipping the level files. These changes cut the file size to under 30% of
the original.

### Goodbye UV optimization

I've been storing a huge amount of surface data like this:

```
class Box
{
public struct Surface
{
public int MinU, MaxU;
public int MinV, MaxV;
}
public Surface[] Surfaces = new Surface[]
{
new Surface(), // PositiveX
new Surface(), // NegativeX
new Surface(), // PositiveY
new Surface(), // NegativeY
new Surface(), // PositiveZ
new Surface(), // NegativeZ
};
}
```


edit: as a side note, [/u/humbleindent points out](https://www.reddit.com/r/gamedev/comments/2wdaw4/the_poor_mans_voxel_engine/coqhglv) that this would be faster:

`public Surface[] Surfaces = new Surface[6];`


I do this so that I can resize surfaces that are partially hidden, like this:

![](../../assets/1359e69898cf4bb4.png)


![](../../assets/1359e69898cf4bb4.png)

![](../../assets/93472a7ce60d77a5.png)


![](../../assets/93472a7ce60d77a5.png)

At some point in the vertex buffer overhaul, I realize that performance-wise, the physics engine doesn't care what size the surface is.

I use this fact to speed up mesh generation. I generate 8 vertices for the corners of each box, then copy them where they need to go in the vertex buffers.

Really, the graphics engine doesn't care much about the size of the surface either, aside from fill rate. What matters is whether the surface is there or not.

With this in mind, I kill the UV optimization code and store the surfaces in memory and in the level file like this:

```
class Box
{
public int Surfaces;
}
```


The bits of the int are boolean flags for each surface. Yes, I could do it in a byte. Actually, maybe I should do that. Anyway, this simplifies my level loading and saving code, cuts my file sizes down to about 512kb on average, and drastically reduces memory usage. Axing the UV optimization routine also speeds up mutations.

### Conclusion

![](../../assets/c6f98172af3bccf1.jpg)


![](../../assets/c6f98172af3bccf1.jpg)

Clearly, this article is mostly useless if you're interested in writing your own voxel engine. The final result is far from perfect. I just want to share the petty drama of my past four and a half years. I for one thoroughly enjoy reading about other people's struggles. Maybe that's weird.

[Lemma](http://lemmagame.com) is set to release May 2015. The entire
game engine is [on GitHub](https://github.com/et1337/Lemma). If you
enjoyed this article, try these:

[The Poor Man's Postmortem - Lemma](https://etodd.io/2015/06/25/the-poor-mans-postmortem-lemma/)[The Poor Man's Character Controller](https://etodd.io/2015/04/03/poor-mans-character-controller/)[The Poor Man's Dialogue Tree](https://etodd.io/2014/05/16/the-poor-mans-dialogue-tree/)[The Poor Man's Gameplay Analytics](https://etodd.io/2014/02/19/the-poor-mans-gameplay-analytics/)

Thanks for reading!