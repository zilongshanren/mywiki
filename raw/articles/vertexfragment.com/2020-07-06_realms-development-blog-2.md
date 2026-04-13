---
title: 'Realms Development Blog #2'
url: https://www.vertexfragment.com/ramblings/realms-dev-2/
author: Steven Sell
published: '2020-07-06'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![Realms DevBlog 2](../../assets/75cf6968a62ec8e3.png)


**Since Last Blog:** 71 commits (541), 15311 lines added (116266), 7707 lines removed (47257).

The past month was spent nearly entirely on paths and pathfinding.

While I knew a pathfinding overhaul would be needed, it was hoped that this wouldn’t be for a few months still. However the bulk of the work is now done and *Realms* has a flexible and fast pathfinding system that should serve it well.

In addition to paths and navigation, some other things that were worked on, but won’t be discussed, include:

- Additional physics colliders and bug fixes.
- Completed “roof turning off when inside” logic.
- Lightweight profiler -
`TimingProfiler`

- as the Unity profiler would crash in the A* implementation. - Custom gizmos (line, sphere, etc.) as neither the Unity Gizmos or Handles wanted to work for me when visualizing the navigation node graphs.

![Path through the map, connecting points of interest.](../../assets/ee73fab2eeb7d00f.png)


A new map generation module was added aptly called `PathModule`

. This is used to generate a physical path through the world, connecting various different points together.

A path can connect locations, such as settlements and bridges, random points in regions, or other even points relative to others. For example,

```
{
"Type": "PathModule",
"RelativeLocationStart": "Bridge",
"RelativeLocationStartOffset": [ -256.0, 0.0 ],
"LocationEnd": "Bridge",
"PathWidth": 2
},
{
"Type": "PathModule",
"LocationStart": "Bridge",
"LocationEnd": "Fort",
"PathWidth": 2
}
```


is used to generate the path flowing through the map as shown above.

Note that the first module specifies a relative point that is actually off of the map. The location is clamped to the edge, but it ensures that the path has the appearance of coming in from further into the world.

The module is used to connect two locations, while the actual generation is (was) performed by a custom A* implementation. This was an implementation that was carried over from the 2D version of _Realms_.

It was a dynamic (for lack of a better name) implementation which crawled the terrain at the time of the request. This was able to generate well formed paths but had some pretty serious drawbacks. Chief among these were:

- It was limited to only navigation across the terrain.
- It was slow. Like, really slow.

While the first issue was an obvious drawback, the A* implementation was still useable for the use-case of physical path generation. However the performance prevented it from being a realistic solution.

How bad was it? 30 seconds for a long path. Yea.

The main cause of the slowdown was due to the dynamic nature of the implementation. The actual A* implementation, primarily consisting of the frontier structure, was plenty fast, however it had to query the underlying scene and terrain systems at each step. Below is an excerpt from one of the early internal profilings of the A* implementation:

```
{
"StandardScene.TrimEntityList": {
"Name": "StandardScene.TrimEntityList",
"Invocations": 85696,
"ElapsedMs": 16,
"MsPerInvocation": 0.00018670649738610905,
"Percentage": 0.00017947481183187697
},
"StandardScene.GetNearbyEntities": {
"Name": "StandardScene.GetNearbyEntities",
"Invocations": 85696,
"ElapsedMs": 27322,
"MsPerInvocation": 0.31882468259895447,
"Percentage": 0.30647567555440891
},
"AStarPathFinder.CalculateHeightDifferentialCost": {
"Name": "AStarPathFinder.CalculateHeightDifferentialCost",
"Invocations": 609489,
"ElapsedMs": 210,
"MsPerInvocation": 0.00034455092708810165,
"Percentage": 0.0023556069052933851
},
"AStarPathFinder.AStar": {
"Name": "AStarPathFinder.AStar",
"Invocations": 1,
"ElapsedMs": 28078,
"MsPerInvocation": 28078.0,
"Percentage": 0.31495586041346507
}
}
```


As we can see, the `StandardScene.GetNearbyEntities`

took 27 seconds by itself, nearly a third of a millisecond per query.

This forced me to perform a deep dive on the underlying `QuadTree`

, which is used by the `StandardScene`

, and optimize it. These updates to the scene tree, such as a greater degree of caching and reducing memory allocations, reduced the processing time from 30 seconds to about 900 milliseconds.

While this is a huge improvement it was still far too slow to be used in a real-time scenario. Improvements to the A* implementation, primarily aimed at reducing the number of tiles checked, further reduced the timing to 230 milliseconds.

Much better, but still not good enough. To achieve the performance that was needed, and to allow for arbitrary pathfinding over more than just the terrain, a new solution was needed.

Parallel-Bidirectional A* (PBA*) was the new solution.

What is it? It is exactly what it sounds like: a parallel implementation of A* which search from two directions at the same time. It is a custom implementation that is based roughly on the paper [_PNBA*: A Parallel Bidirectional Heuristic Search Algorithm_](http://homepages.dcc.ufmg.br/~chaimo/public/ENIA11.pdf), though admittedly the algorithm described in the paper didn’t help me much but it did get the idea to start forming in my head.

The current pathfinding is a two-step process:

- At map generation, or when relevant entities are added/removed, a system of navigation nodes (
`NavNode`

) are generated/updated. - When a path is requested, the PBA* implementation finds the
`NavNode`

closest to the desired start and end points of the path and then traverses the node graph to connect them.

This first step, generation of the navigation nodes, is key to both speeding up the pathfinding and making it more flexible. Paths are no longer limited to the terrain and can go anywhere there is an underlying `NavNode`

.

There are currently two ways a `NavNode`

may be generated:

- During map generation, using the
`TerrainNavNodePlotterModule`

which generates navigation nodes across the terrain. - Via a
`NavNodeSpawnComponent`

attached to any entity. This generates nodes on or around an entity with multiple patterns to choose from.

Regardless of how a node is created, they all track the following data:

**Position:**the world position of the node.**Cost:**the isolated cost of moving into the node. Nodes that are close to multiple entities or are on terrain height differentials (cliff edges) have a higher cost.**Clearance:**the distance to the nearest entity which blocks navigation.**InFlow:**indicates if the node is in a flow field (river).**Connections:**collection of connections (edges) to other nodes in the graph.

These parameters are then used by the PBA* implementation when performing the pathfinding.

The image comparison below shows a path (in magenta) from a start point (sphere in the courtyard) to an end point (player pawn) which navigates through the barracks building. The slider reveals the underlying navigation nodes, which are colored based on their clearance value. Nodes with a higher clearance are green, and those with lower are red. Nodes which do not have sufficient clearance for the requested path (minimum clearance of 0.5) are hidden.

Not only does the usage of navigation nodes allow for arbitrary paths (not limited to the terrain), but they also allow for creatings paths of differing sizes. The same graph is used for paths 1 unit wide (player), 2 units (path through the terrain), and up to 6 units which could be used for larger entities.

There are two key differences between A* and PBA*, hence the extra two letters in the acronoym.

**Bidirectional:**the search is done in two directions: from start to end, as well as end to start.**Parallel:**each direction is searched in parallel, on its own thread.

So starting at both ends, the search looks for the opposite end at the same time. Each of these searches are distinct, owning their own frontier of nodes. However, before exploring a node, they check if the opposing frontier has also visited the node. If so, the searches are considered to have converged and a path was found.

This means that each search only has to explore half of the number of nodes (as they will nearly always meet in the middle), and they are happening at the same time. Together, these characterstics mean that PBA* should only take approximately 25% of the time of traditional A*.

It can be even better than that in certain cases, especially for situations in which the end node is unavailable. In A* the entire graph has to be searched to determine that the end node can not be reached, however with a bidirectional search it can be determined almost instantly that the two points can not meet as the alternate search (starting from the end) will quickly run out of nodes in its frontier.

However, there is a downside to performing a bidrectional search which is related to the fact that the resulting path is typically a combination of two separate searches meeting in the middle. This can result in a less-than-ideal path which a traditional A* would have done a better job at. However, this problem really only presents itself in longer paths. For AI, the entity will be periodically refreshing its path which will result in the excess being removed and a more efficient path being formed.

After switching to PBA*, and the navigation nodes, the same path that previously took 230 milliseconds now only takes 5 milliseconds!

This is still relatively expensive, considering we only have 16 milliseconds per frame, but it is acceptable when considering:

- The 5 milliseconds is for a worst-case path across the majority of the map. Most paths will be much shorter and those take only fractions of a millisecond to generate.
- PBA* is, well, parallel. In the new
`Navigation`

system a request for a path between A and B is made and then either the status of the job is queried or a callback is set. This means that in practice a system will request a path one tick and then the next tick (50ms) it will use the freshly generated path.

At this point the best way to improve the pathfinding performance is to simply reduce the number of nodes that must be visited. This can be done by generating a sparser terrain navigation node graph, but it is not a priority going forward.

![A double ramp, what does it mean?](../../assets/332561cc727905c7.png)


While the path mesh existed and was used by settlements last update, it underwent a few big changes in June. Key among these were colliders, diagonal corners (to match the diagonal terrain), and ramps.

Internally all terrain paths are stored as simple 3D line segments with the `PathSegment`

class. This is just a pair of 3D points as well as a directional vector. When generating ramps these segments are checked to see if their start and end points are at different elevations.

If so, then the segment is considered a ramp candidate. Neighboring segments are checked to see if any of their path could be “borrowed” for the formation of the ramp with an ideal slope of 1/2. If sections of neighboring paths can be used, then they are allocated to the ramping segment, otherwise the ramp has a higher slope. The restrictions to the slope are determined by settings in the `PathModule`

, but typically the maximum slope is either 2 or 3.

This can lead to cases of some pretty extreme ramp slopes, but generally they are able to achieve the desired 1/2 slope. Currently the ramping segment may only borrow from other segments going in the same direction, but future updates may allow it to take from as many segments as needed to create the slope, resulting in ramp switchbacks or similar.

![Bridge over the smaller river.](../../assets/fc54ee1b3c3ac783.png)


The previous update briefly explained the work done on Settlements which were the first kind of Location added.

At the start of June a second kind of location was added - Bridges. Like settlements they are defined via a JSON file which specifies the following control parameters:

**Region:**the region in which the bridge will be placed.**MaxLength:**the maximum distance the bridge can span.**BridgeEntity:**the entity used as the body of the bridge, repeated over its length.**EndEntity:**the entity used as the endcap of the bridge.

The named region is searched for a valid location to place the bridge. If one is found the specified entities are spawned to span the gap with the other entities placed on each end.

With the addition of bridges the general location logic was refactored and metadata is retained in memory for reference later. One usage of this metadata is for determining path connection points. For settlements, these connection points are placed at each entrance, and for bridges the points are placed at each end.

These connection points are then used to generate paths through the terrain to connect different locations to each other.

World generation for *Realms* is nearing an alpha stage where a majority of the base systems are in place. This leaves the following candidates for what should/will be worked next:

- Terrain holes which allow going underground.
- Underground - cellar in the fort, cave system, etc.
- Additional points of interest for first map, finishing the fort.
- Hub World which acts as the players base of operations and portals to other realms.

The first two are directly connected, and the underground will require handling of multiple terrain/z layers.

The fourth will be the first step into adding in the actual game systems, as *Realms* is more-or-less a map generator at this point. This will also add functionality for scene transitions and saving/loading which will be significant additions.