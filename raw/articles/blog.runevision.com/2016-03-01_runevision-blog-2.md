---
title: runevision blog
url: https://blog.runevision.com/2016_03_01_archive.html
published: '2016-03-01'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

Pathfinding is not just for finding paths for AI agents/NPCs and similar. It’s also for procedurally *creating* paths.

![](../../assets/4059287d27e666af.png)

While working on path creation for a procedural terrain, I had the problem that the generated paths would keep having too steep sections, like this:

![](../../assets/768bece780b66933.png)


![](../../assets/768bece780b66933.png)

It was too steep and also didn’t look natural at all. I kept increasing the cost multiplier for slopes, but it didn’t help.

Then it hit me: My function just penalized the vertical distance, but it didn’t make any difference if this vertical distance came gradually or all at once.

So in fact, my cost function wasn’t trying to avoid steepness - rather it was trying to make a path where the altitude changes *monotonically*. It would do everything it could to avoid the path first going up and then down again.

But I didn’t care if the path went a *little* up and down, as long as it wasn’t too steep at any point. To achieve this behavior, I needed to penalize steep slopes more than linearly, for example by squaring it.

This has the effect of penalizing abrupt changes in altitude and reward gradual changes.

And sure enough, after the change the generated paths avoided steepness and looked much more like what humans would create.

![](../../assets/4059287d27e666af.png)


![](../../assets/4059287d27e666af.png)

Tweaking pathfinding cost functions is one of those odd little things that I really enjoy. Seeing a little change in a formula imbue a generated creation with what could be mistaken for human design is really fascinating and fun!

### Further notes

The observation-turned-blog-post in its original form ended there, but I've compiled some further notes for those who want to dig into the details.

#### Pathfinding method

Let me tell about the method I use for the pathfinding, since I was asked about this. I won't do an introduction to pathfinding in general here but assume understanding of the principles of performing pathfinding using an algorithm like *A** or similar on a *graph* of *nodes* connected by *edges*.

Such a graph can be represented in many ways. Sometimes it's a data structure with explicit data representing all the nodes and edges and how they're connected. Other times it can just be a grid (like a 2D array) and each cell is implicitly connected to the neighboring cells - maybe the 4 or 8 neighbors, depending on whether diagonal connections are used.

It doesn't really matter, and a pathfinding algorithm can typically easily be modified to work with one or the other. Apart from giving it a start node and goal node, the important part is that you can tell the algorithm:

- Which other nodes are a node connected to?
- What is the real or estimated cost of getting from one node to another?

You might have data for this stored in advance or you might calculate the answers on the fly when asked.

For the terrain pathfinding I do the latter. In fact, there is neither an explicit graph, nor any 2D array. There is no data structure at all for the pathfinding to happen inside. Instead, it's all implicit, based solely on coordinates. I tell the pathfinder what the start and end coordinates are, and there's a function for getting "neighbor coordinates" to a given coordinate. There's also a function for getting the cost of getting from one coordinate to another, as you saw earlier.

This may sound completely free-form and magical at first, but there still is a structure that must be adhered to. You must imagine a grid structure and ensure the coordinates always fall within this grid. In my case it's a plain quadratic cell grid where each cell has a size of 5. So the start coordinate, goal coordinate, and every provided neighbor coordinate must always have x and y values that are multiples of 5. You also shouldn't use floating-point numbers for this, since they can produce floating point precision errors, and even the slightest imprecision can cause the pathfinding to completely fail.

I wanted my paths to be able to have a natural, non-jagged look, so I wanted edges to come in 16 directions instead of the basic 8. The 8 additional directions are achieved by going two cells out and one to the side. This provided me with an interesting choice of whether the 8 other directions should also go two cells out, or just one.

![](../../assets/2733ebe6618cc4dd.png)


![](../../assets/2733ebe6618cc4dd.png)

In theory the second option can be weird, since if you need to move just one cell the path have to first side-step by two cells. But in practice both seems to work fine. The first images in this post were made with the first option but I later decided to use the second to avoid the path having very small-scale zig-zags.

#### Effects of different parameter values

I got asked on the proceduralgeneration sub-reddit:

How rapidly does the path change as you increase the power from 1.0 to 2.0? What happens if you go past 2.0? Does the path eventually have to spiral around the mountain or something?

I had actually been content just using the values I had found which seemed to work well enough, but now that I'd been asked, of course I wanted to find the answers too! I tried doing the pathfinding with the power values 1.5, 2.0 and 3.0 and with the multiplier values 1, 2, 3, 4, 5, 6, 7, 10, 15, 20, and 25. I had moved the multiplier inside the power function since the original version of the code, so those multipliers are multiplied onto the steepness before the resulting value is raised to the given power. Here's a table of the results.

![](../../assets/a199502691439e59.png)


![](../../assets/a199502691439e59.png)

Some notes on the result.

Overall the common theme is that the results range from straight and boring to wildly tortuous. At the extreme end, the path begins to create loops - something that should be impossible with path-finding. However, the edges I use in the path-finding can cross each other. This means that they can appear to loop even though they never pass through the same points from the perspective of the path-finding. They only begin to do this once the path-finding is so extremely sensitive to tiny changes in altitude that the small difference in altitude between one of two crossing edges is enough for it to exploit it to loop around. I should say that I only sample the altitude at the end-points of each edge, which appears to be fully sufficient except in the extreme cases like this.

Note that there are very similar occurrences across the different power values. For example, multiplier 10 at power 1.5 looks just like multiplier 6 at power 3.0, and multiplier 7 at power 2.0 looks just like multiplier 5 at power 3.0. Does this mean that any result you can get with one power value, you can also get with another? That there exists a transformation that means they're mathematically equivalent? No, I don't believe so. It feels like there's subtle differences. For example, the progression of paths with power value 3 begins to do loops before it begins to take a major detour, while for power value 2, the loops only start happening after it has begun doing a large detour. The differences are very subtle though and hard to put the finger on exactly.

One thing that's tempting to look for is qualitative differences, such as some paths doing many small zig-zags and others doing larger swoops. However, I think that's a red herring. The algorithms doesn't measure sharpness of turns or frequency of turns in any way and shouldn't be able to tell one from the other. I think that the seeming qualitative differences are thus up to unpredictable aspects of how the path-finding interacts with the terrain height function that sometimes just happen to produce one result or the other. To answer it in terms of the original question: If the terrain was perfectly conical, a path from the base to the top might equally well form a spiral, a zig-zag pattern, or any other combination of left-winding and right-winding sections.

My own pragmatic takeaway from this is that sticking with just a power value of 2 seems fine and I'd then use multiplier values between 3 and 15 depending on how straight or tortuous I want the path to be.

### Perspectives

These generated paths were a proof-of-concept for a new project I'm working on and I'm sure I'll learn more as I go along. For example, already I'm learning some things about approaches for flattening the terrain around the paths which I may share at a later point when I'm a bit more sure of my findings. For now, I hope you found this useful!

### 2024 update: Code available

I've now released a framework called [LayerProcGen](https://github.com/runevision/LayerProcGen) as open source, and one of the sample scenes generates natural paths using the technique described in this article. So a fully functional implementation is now available for study and use.