---
title: 'Realms Development Blog #1'
url: https://www.vertexfragment.com/ramblings/realms-dev-1/
author: Steven Sell
published: '2020-06-04'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

![Realms DevBlog 1](../../assets/d0b96307567770b4.png)


**Since Last Blog:** 469 commits, 100955 lines added, 39550 lines removed.

Considering that this is the first public update about *Realms*, it is probably a good idea to give a short overview of its background. In brief, it is a roguelike that I have been working on in my limited free-time over the past two years.

It began as a very conventional top-down, turn-based, 2D tile-based roguelike ala *Dungeon Crawl: Stone Soup*, and it remained this way for the first year of development. I have always been a fan of classic roguelikes and at the time was just learning about the ECS (Entity-Component-Systems) programming paradigm (as opposed to the more traditional Object-Orientated). While experimenting with ECS it dawned on me that a roguelike would be the perfect vessel for that programming technique. And so combining ECS with some ideas that had been floating in my head for years, *Realms* was born on July 18, 2018.

At the time I debated between using Unity or Unreal, both of which I had experience with, but the release of a brand-new ECS library for Unity won me over. Since then it has evolved from 2D to 3D, top-down to high-angle (but not isometric!), turn-based to real-time, and tile-based to, well, not tile-based. I could speak at length about why each of those changes were made, and the resulting shift in the underlying systems and infrastructure, but the short answer is: my bad 3D assets look better than my bad pixel art, and frankly I just find the game more fun this way.

While the first 12 months were developing a traditional roguelike, the next handful of months were spent on the conversions and major changes need to migrate to 3D.

During all of this time the game was based on a dungeon setting, which was very dark and dreary. At this point I had reached a level in the system development where there were two paths that could be taken:

- Focus on game systems (AI, inventory, abilities, resources, etc.) and test them in the dungeon setting.
- Focus on world/map generation.

Both would need to be done, and it really didn’t matter too much which was done first. So I had decided to get some fresh air and focus on the second option, at least enough to have an entire map in which to develop and test my systems.

Which brings us to the development focus of the last few months: world generation, custom terrain, water flow, settlements and paths.

There were some other experiments during this time (such as a brief foray into a cel-shaded style), but those were the primary achievements.

While the world generation was in place fairly early on in *Realms* history, it underwent a large number of updates in preparation for generating an exterior area.

My approach to world generation is similar to my approach to *Realms* as a whole: start with big features, and then layer on small details. The generation system is modular, and can be compared to node-based tools such as *Substance Designer*. You start with a coherent noise heightmap, add regions on top of it, further adjust the heightmap based on regions as necessary, spawn entities, generate rivers, build settlements, etc. In my opinion, the beauty of the system is that any single generation step (encompassed in a `MapModule`

) can be pulled out, added in, replaced, updated, etc.

This allows for a highly customizable system which lends itself to rapid development. In fact, maps are defined by a JSON file which fully configure the generation process. And of course the whole thing is governed by a PRNG seed value.

Below are three different examples of the same map configuration, but using different seeds.

![Three examples of world generation - changing only the seed.](../../assets/7bde76bd6515495f.png)


When switching to work on the great outdoors I initially made use of the built-in Unity terrain. This worked well enough after creating a wrapper which allowed it to fit into my existing infrastructure.

However, the smoothly sloped terrain never really seemed to fit. Even though I had left 2D behind, I still wanted to maintain some of the blocky/tile-based aesthetics of more traditional roguelikes. And since the Unity terrain would never be able to match this style, I opted to create my own. However, my initial commit of the new terrain system summed up my feelings regarding the development:

[2020-04-03] Started on custom terrain (what am I getting myself into)


Work on it went smooth enough, and initially I had a blocky terrain. But this struck me as feeling too voxely and I did not want to go the *Minecraft*-clone route. So I added the next great revolution in gaming - diagonal edges.

There are further improvements that will need to be made, such as holes in the terrain, but they can be completed relatively easily in the future.

![Blocky vs Diagonal Terrain](../../assets/47945824acfb4706.png)


The fluid flow system was added shortly after the new terrain system. It is currently controlled as part of world generation, specifically the `TerrainFlowModule`

.

Using this module one simply specifies a start point for the flow, and the direction it should head. It then flows over the terrain heightmap, flowing around hills (or cutting through them if necessary). Future additions will allow the fluid to flow to a specific point and to better support large bodies.

For example, the two rivers shown in the [World Generation](https://www.vertexfragment.com#world-generation) section are generated by a handful of lines of JSON:

```
{
"Type": "TerrainFlowModule",
"RegionOverride": "River",
"StartPoint": [64.0, 10000.0],
"StartVariance": [8.0, 0.0],
"Direction": [0.0, 0.0, -1.0],
"Width": 1
},
{
"Type": "TerrainFlowModule",
"RegionOverride": "River",
"StartPoint": [192.0, 10000.0],
"StartVariance": [8.0, 0.0],
"Direction": [0.0, 0.0, -1.0],
"Width": 2
}
```


A little bit of time was also spent on the water shader, though in my experience water is an effect that one can easily sink *a lot* of time in getting to look just right. My goal was a more stylized water with some “foam” to show flow direction. And while it will definitely be an area of focus in the future, for now it is good enough.

Additionally, the flow vectors can be queried by the other game systems so in the future items may float along the river, movement will be directly affected, etc.

![Two rivers meeting.](../../assets/3c3c58a6deb11c46.gif)


The primary focus for the entire month of May was on settlement generation.

A settlement can, theoretically, range from a single building, to a small farm, to a fort, or even a large city. They are generated by adding the appropriate module to the world definition which references an accompanying location definition file (as settlements are a subset of locations internally), which is just another JSON file.

Settlements all have the following properties:

- A region which they occupy.
- A border, composed by generating a polygon shell of the region. This border may be walled.
- Number of entrances to the settlement, regardless of whether it is walled or not.
- Pathing information, such as if the settlement entrances should be connected by a path.
- Prefab pools which define which prefabs (eg buildings) may be spawned, and their likelihood.

Internally the generation process follows the rough flow of: generating the polygon shell of the region, adding walls if desired, creating entrances in the walls, generating primary paths through the settlement, segmenting plots of land, selecting prefabs to spawn and placing them into plots (and splitting plots as necessary), and finally generating paths from the prefabs to the main path.

Of course each step in this process could be detailed in length, but in general it tries to be as flexible as possible.

And just like the overall map generation, settlements are created by adding incrementing layers of detail. Each layer is relatively simple, but the final product is complex. Below shows a top-down view of a walled settlement with zero, one, and then two prefab buildings placed within it, along with the connecting paths.

![Zero, one, and two buildings in the same settlement.](../../assets/98ca5fcc64055afb.png)


Work on paths was one of the things that made me question doing a procedural roguelike.

Something that is normally placed by a level designer/artist without a second thought shouldn’t involve this much programming! But it did.

Initially paths started as texture-based and rendered as just another layer in the terrain. However this approach lacked detail and freedom, and that implementation was quickly replaced. Currently all paths are simply line segments which are turned into custom meshes which lie on top of the terrain mesh.

This allows for paths to be placed anywhere, using any material, and to be of arbitrary width. This approach will also allow for future improvements such as ramps or cutouts into terrain to traverse inclines. It is also simple to query where the nearest path is (or if an entity is on one) to allow features such as increased movement speed on a path, prevention of monster spawns within a given distance to a path, AI following/preferring a path over going through the wilderness, etc.

Currently paths can be explicitly defined segments, which is used by settlements when performing a pseudo-raycast algorithm to place the primary path, or one may specify a location and then an A* implementation creates a path to that location from the nearest path in the world.

This latter approach is how the entrances to a prefab, marked by an entity with a `PathMarkerComponent`

, are connected to the primary path through the settlement.

*Whew!* That was a lot, but there is still so much to go. There is also much more which could be discussed as only the most superficial overview of each of these systems was given, and these only represent ~12.5% of the development time of *Realms*.

But looking towards the future, the primary short-term goals are:

- Continue refining and adding onto settlement generation.
- Asset and prefab (building) creation.
- Paths through the map as a whole, and not just isolated within the settlement. This includes bridges, ramps, etc.
- Populating the right third of the map - that giant brown part shown in the top-down views.

From there it will be either working on the actual game systems or the underground (caves, dungeons, etc.) which will of course play a large part.

Additionally more development blogs will be released whenever a sufficient amount of work has been completed. This could be in a week, month, or a quarter depending on progress.