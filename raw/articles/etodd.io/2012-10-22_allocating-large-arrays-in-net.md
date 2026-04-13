---
title: Allocating large arrays in .NET
url: https://etodd.io/2012/10/22/allocating-large-arrays-in-net/
published: '2012-10-22'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Allocating large arrays in .NET

I experienced a strange memory issue with Lemma this week. Memory usage skyrocketed each time I loaded a level; it never dropped back down.

Now granted, I am definitely the garbage collector's worst nightmare. (I'll just say this: closures. Closures *everywhere*.) But at this point I am setting fields to null all over the place and manually calling GC.Collect() after unloading a level, all to no avail.

Enter the .NET [Large Object Heap](http://msdn.microsoft.com/en-us/magazine/cc534993.aspx). See, the .NET garbage collector actually compacts the regular .NET heap by relocating small objects to fill the fragments. For exceptionally large objects, it's simply too expensive to relocate them, so the runtime allocates them on the Large Object Heap, which is not compacted.

I'm allocating huge 80x80x80 pointer arrays; definitely Large Object material. This means the virtual address space is not actually freed when the arrays are deallocated. This isn't quite as bad as it sounds, since the virtual memory system probably reclaims the physical memory. But eventually, I would hit the address space limit. Which I did on a few occasions.

My solution is to put the unused arrays into a "free" queue instead of letting the GC deallocate them. Then, when I need a new array, I first check if I can pull an old unused one off the queue, only allocating a new one if no old ones are available. This works for me because my arrays are largely the same size.

It's fairly easy to implement. Here's a rough approximation of my code before:

```
public class Map
{
public Box[, ,] Data;
public Map()
{
this.Data = new Box[80, 80, 80];
}
}
```


And after:

```
public class Map
{
private static Queue<Box[, ,]> free = new Queue<Box[, ,]>();
public Box[, ,] Data;
public Map()
{
if (Map.free.Count > 0)
this.Data = Map.free.Dequeue();
else
this.Data = new Box[80, 80, 80];
}
protected override void delete()
{
base.delete();
Map.free.Enqueue(this.Data);
}
}
```


Hope this helps if you stumble on the same problem.