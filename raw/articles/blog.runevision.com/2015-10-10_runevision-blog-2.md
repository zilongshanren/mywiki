---
title: runevision blog
url: https://blog.runevision.com/2015_10_10_archive.html
published: '2015-10-10'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

Procedural generation has gotten a lot more popular since my interest in it started 10 years ago. Today most game developers and even many gamers know what it means in broad terms.

In this piece I want to highlight fundamental differences between three approaches to procedural world generation: The simulation approach, the functional approach and the planning approach. The approaches are not only algorithmically very different but are also suitable for different types of games and gameplay. Here's a breakdown and analysis, with lovingly hand-drawn - err, *mouse*-drawn - illustrations.

### The three approaches

**The simulation approach** attempts to create an environment by simulating the processes that creates it. Terrain erosion, vegetation distribution based on plants competing over sunlight and nutrients, fluid dynamics, fire propagation and genetic algorithms all fall under this approach. Simulation approaches are not always based on reality. For example cellular automata simulations can be used to create nice cave patterns even though this is not mimicking how caves are formed in reality. The defining trait of simulations is that it's a process with calculation steps that are repeated many times in order to reach the end result.

![](../../assets/a95a227766db5875.png)


![](../../assets/a95a227766db5875.png)

**The functional approach** deals only with the desired end result and attempts to approximate it directly with a mathematical function. For height field based terrain, this could be using a Perlin Noise function, a fractal function, or any combination of many different functions to determine the height for a given coordinate. Similar functions (but for 3D coordinates) can be used for voxel terrain. For vegetation, mathematical functions can be used to determine the probabilities for various types of plants to appear at a given spot.

![](../../assets/0cc5adeedc787de8.png)


![](../../assets/0cc5adeedc787de8.png)

**The planning approach** doesn't primarily try to mimic nature at all, but instead plans out an area according to level design principles. For a terrain it might create a mountain range that can only be passed in a specific spot, or it could carve out a cave which contains a key inside that unlocks a vital door elsewhere. For vegetation it might create dense trees that block the player from taking an unwanted shortcut, or it might place plants and flowers in specific spots to try to create a certain emotion or feel related to that spot.

![](../../assets/0ad6548364b58fd2.png)


![](../../assets/0ad6548364b58fd2.png)

We'll get back to the planning approach in a bit. For now, let's compare the simulation and functional approaches.

### Context or no context

An important distinction of the functional approach is that the value at a given coordinate can be evaluated without regard for neighboring points. This is both a strength and a weakness.

The strength is that the generation is simpler and that it can more easily be divided up into smaller parts that don't rely on each other. No arrays need to be used for the generation except to store the end result and this means lower memory requirements.

For games with a pseudo-infinite world, such as Minecraft and No Man's Sky, the lack of dependencies on neighboring points (at least for terrain generation) is important. Since the world is generated in chunks on the fly, a point may need to be evaluated without the neighboring points being available yet, because they are in a different chunk that doesn't exist at this point in time.

![](../../assets/96dd426c155ed2dc.png)


![](../../assets/96dd426c155ed2dc.png)

The weakness of the functional approach is that certain things can just not be calculated meaningfully without context. For example, consider a river that flows from a source and downwards wherever the terrain goes down the steepest. Given a mathematical function that defines a terrain, it's not generally possible to determine where the river would flow without considering the terrain at many different points at once. Similarly, it's not possible to calculate how light and shadow propagates in a space without having the context of the surrounding geometry available.

There are ways to get around these limitations by mixing functional techniques with simulation techniques. Once a pass of functional calculations have run, a different pass of simulation can run on top, which has does context information. For game worlds that are not generated all at once - and that includes all pseudo-infinite worlds - this has to be handled very carefully to work correctly.

One example is calculation of lighting in Minecraft. The terrain is calculated fully functionally (with user-created modifications on top). After that, the lighting is simulated with proper context information about the terrain. However, the fact that the lighting simulation needs context means that lighting near the edge of a chunk needs terrain data from the neighboring chunk in order to be simulated. How far out can a change in geometry affect the lighting? 2 blocks? 10 blocks? 100 blocks? This, along with the block size of chunks, affects how many neighboring chunks must have been "geometry calculated" before a given chunk can be "lighting simulated".

It just so happens that chunks in Minecraft are 16x16 (vertically they take up the entire world height), while lighting propagates only 15 blocks. This conveniently means that only the 8 neighboring chunks need to be geometry calculated in order for sufficient lighting context to be available for a chunk. This is very likely not to be a coincidence. Having light propagate further than the size of one chunk would have had large negative consequences for the performance.

![](../../assets/62301816f00bdcd1.png)


![](../../assets/62301816f00bdcd1.png)

*(Disclaimer: My explanation of lighting in Minecraft is based on a few facts combined with speculation on my part. I can't guarantee it actually works the way I describe but it's entirely conceivable.)*

Other types of simulation can not as easily be limited to a specific range. One option here is to just ignore the simulation for chunks or parts of the world that haven't been generated yet, and just simulates the best they can with the information generated so far. Maybe a river only begins flowing once the player gets close enough to its source that the chunk containing the source is generated, and that's okay. But for other games where any rivers present should appear to have always been there and not just suddenly begin flowing based on player location, it can be a tricky or impossible problem to solve.

### Topology and traversability

Consider for a moment a game with a player character that can not dig holes or build structures (except maybe at very specific spots). It could be Zelda, Grand Theft Auto, Mario, Half-Life, Metroid or really most other games. What would it mean if there was a hole too deep to jump out of? A gap too wide to jump over? Or a tall wall with a vital objective on the other side but no way to get past it? Basically you would be stuck. It would be game breaking.

![](../../assets/a95a142de86cc937.png)


![](../../assets/a95a142de86cc937.png)

Games like Minecraft would have tons of these stuck situations if it wasn't for the ability to dig and build. But in the majority of games - games where the player can generally not modify the environment much - the level design needs to guarantee that you won't get physically stuck with no means to progress.

These games need to guarantee that the topology is such that it can be traversed by the player, so that all locations can be reached that needs to be reached.

Here's the kicker: Neither the simulation nor the functional approach can make such guarantees. (Well except in boring cases; for example if the world is so flat and without obstructions that the player can go in any direction at any time.)

Let's say we uneven terrain with caves. The simulation and functional approaches can easily be used to create interesting terrain of this type, but very little can be guaranteed about it. Maybe it creates some cliffs, but you don't know if you can get to the top, or if it's too steep all the way around. Or maybe it creates a cave underground, but you don't actually know if it's connected to the surface or not.

![](../../assets/8627b263ed218eb9.png)


![](../../assets/8627b263ed218eb9.png)

For the functional approach, this is because it evaluates every point without context - and topology cannot be determined without context. Again, the exception is terrain where it's trivial to get to any point, but that's not useful for directed, non-sandbox gameplay. The point is that it's virtually impossible to create a mathematical function that creates interesting level/world design where it's non-trivial to reach a given goal location, yet still guaranteed to be possible. Maybe it's doable - and if so that would be highly interesting - but I've yet to have seen it pulled off in practice.

For the simulation approach, the context is usually available, but simulation is not concerned with making guarantees about topology or traversability, just like there are no such guarantees in nature. If a simulation algorithm did make such guarantees, it would really at least partially be a planning algorithm instead.

The planning approach then is the one that can make these guarantees. In fact, much of the planning in planning algorithms is typically centered around ensuring such guarantees.

If you have read articles describing procedural generation for rogue-like games, they typically describe how multiple rooms are placed on the map, and an algorithm ensures that they are all connected with passages. Maybe certain rooms are guaranteed to only be reachable via one passage. More advanced ones may have keys for locked doors, and need to ensure that a key for a locked door is not placed behind the locked door, and similar.

![](../../assets/1f9915c69ac8e63e.png)


![](../../assets/1f9915c69ac8e63e.png)

Most games with planning algorithms take place in sequences of maps with limited size, which each are generated all at once. It's trickier, though absolutely possible, to use the planning approach on pseudo-infinite worlds generated on the fly in chunks. It typically requires planning at several scopes, with a large-scale planning algorithm handling the overall design of the world. This algorithm can then delegate responsibility of the more fine grained planning to algorithms creating the individual chunks. Often, each chunk is given certain criteria it must meet in order to fit into the overall plan. There can be an arbitrary number of such layers of responsibility.

I'm not aware of any shipped games that are pseudo-infinite and use the planning approach - let me know if you do! My own game in development, [The Cluster](http://blog.runevision.com/search/label/TheCluster), uses this approach, and I write about various aspects of the generation and design on [my blog](http://blog.runevision.com/).

### Generation approaches and effects on gameplay

We have discussed how the simulation and functional generation approaches cannot make guarantees about topology and traversability. What this means is that they are essentially mostly suited for games with sandbox gameplay, for example where the player can dig and/or builds anywhere in order to make non-traversable environments traversable. Often these games also don't have any specific locations that must be reached, with the goals being loosely defined or completely absent.

More traditional "directed" games have carefully constructed level design that can be traversed without freely modifying the environment. For these games certain guarantees must be made. For this to be done procedurally, a planning approach must be used.

We have also discussed the implications for pseudo-infinite games that are generated in chunks on the fly. For these games the functional approach has very advantageous properties in that it doesn't require context. The simulation approach can be used only to a very limited extent, while the planning approach can be used fine, but needs very careful division of responsibility between different generation algorithms at different layers of scope or abstraction.

### Mixing and matching

While a procedural game typically has one approach that dominates its generation strategy, there's no problem in mixing and matching the different approaches. For example, a game might use a planning approach for the overall level design, use a bit of simulation to enhance aesthetic properties of the terrain that doesn't affect traversability, and then use a functional approach to place vegetation.

![](../../assets/6df06008ba744ef5.png)


![](../../assets/6df06008ba744ef5.png)

The dominating approach could be said to be the one that affects gameplay the most, and specifically determines how the player can move around in the world and achieve objectives. For anything that doesn't affect gameplay directly, or only in aesthetic ways, the choice of approach is more of an open question.

I hope this article has been helpful in giving insight into various approaches to use for procedural world generation, either for analyzing other games or for use in designing your own. If you have great examples of games using the various approaches to good effect, let me know!