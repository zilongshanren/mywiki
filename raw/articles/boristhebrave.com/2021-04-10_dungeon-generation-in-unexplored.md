---
title: Dungeon Generation in Unexplored
url: https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/
author: Boris
published: '2021-04-10'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

It’s rare that you see a game that gives top billing in its marketing to the quality of its procedurally generated levels. Normally PCG is sprinkled in a game to add a bit of variety, or to make up for the lack of actual level design. But, for 2017’s [Unexplored](https://store.steampowered.com/app/506870/Unexplored/), the rest of the game is there to justify the stellar levels.

Unexplored presents itself as a fairly standard roguelite – enter a randomly generated dungeon, descend 20 levels and retrive the amulet of Yendor. The gameplay features a realtime combat based around timing and aiming your swings, but otherwise plays things by the book.

![https://cdn.akamai.steamstatic.com/steam/apps/506870/ss_af6440b995f113d35999af111e0e0e80aa77c53b.600x338.jpg?t=1574761931](../../assets/38362708e210926f.jpg)

But it doesn’t take long realize why they much such a big deal out of the procedural generation. Unexplored level design takes more after 2D Zelda games than it does Rogue. Instead of just wandering at random, you quickly find that the path forward is blocked, forcing you to solve puzzles, find items and keys, defeat enemies to continue. There’s a huge variety of structure, all randomly generated, but nearly every level is a tightly packed, interesting space.

[Full video here](https://www.youtube.com/watch?v=_wvkTT-6P3Q&list=PLKrfA5RMeajfna6xcOe8WThxcDlxL58Xw)

So far I’ve discussed some of the key concepts for this sort of level generation: [Lock and Key Dungeons](https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons/) and [Graph Rewriting](https://www.boristhebrave.com/2021/04/02/graph-rewriting/). Then I described [the ](https://www.boristhebrave.com/?p=931)[tools](https://www.boristhebrave.com/2021/04/02/phantomgrammar-and-ludoscope/) Dormans used to design everything. But I was a bit brief on how simple find-replace rules can build such complex dungeons. So this article we’ll dive into those rules, building on that previous knowledge. The details and images you’ll see come more or less straight out of Ludoscope.

I can’t talk about everything. There are two main generators – one for the dungeon as a whole, and one for floorplans of each level. Each one has many modules and about 5000 individual find-replace rules. The Ludoscope tooling allowed Dormans to iterate very rapidly! That does mean a lot of the “secret” for the varied dungeons is simply a ton of different manually coded cases.

![](../../assets/7fad1f23a1f1104d.png)

I’m going to focus on the floorplan generator, and abridge things somewhat, but it’s still a long article. If you just want the highlights, I’d read the [general structure section](https://www.boristhebrave.com#General_structure_of_a_floorplan), then [Cyclic Dungeon Generation](https://www.boristhebrave.com#Cyclic_Dungeon_Generation), and skip the rest.

Table of Contents

By the time we start generating floor plan, the dungeon generator has already created 20 level requests, and marked each one with some specifics it needs, like exits/entrances, items and bosses. It also decides some high level details of the level, such as the name.

The floorplan generator then takes each one of those level requests, and generates all the rooms, additional encounters and enemies, and then designs a tile-based map to hold everything.

There’s around 50 PhantomGrammar modules in in the generator, but it’s easier just to look at the main steps:

[Designing the overall layout](https://www.boristhebrave.com#Designing_the_Overall_Layout)- First, a square grid of empty cells is constructed.
- Then a start, end, and large rough circle are drawn on the grid.
- One of the major cycle types is chosen, and the circle converted to use it.
- Minor cycles add complications to the main one
- Add some dead ends
- Shuffle some of the nodes

[Resolve specifics that have been left general so far](https://www.boristhebrave.com#Resolution_of_Abstraction)- Choose puzzles, locks, doors, enemies
- Decide which nodes are enclosed rooms, caves, width of corridors
- Randomly add treasures

[Convert from grid of graph nodes to tile map](https://www.boristhebrave.com#From_Graph_to_Grid)- Double the grid resolution, fill in corridor tiles between nodes.
- Increase the grid resolution 5x
- Draw rooms and corridors
- Draw special rooms and set pieces
- Randomize terrain with some noise
- Pick position of items/enemies within rooms
- Smooth off sharp edges, randomly draw vegetation


Here’s a timelapse for a particular level.

Each level is designed on a 5×5 (or similar) grid of graph nodes. Because almost all subsequent operations are done via graph replacement which has no notion of shape, location or rotation, this grid ensures that the ensuing graph still follows a 2 dimensional plan. The grid nodes are never deleted or moved, just annotated, so when we come to turn the graph into a tilemap later, it’s an easy operation.

One of the first things the generator does is draw a start, end, and a big roughly circular loop stretching between them. We’ll get to “why a loop” shortly, but first I’ll show how graph replacement can be used to draw shapes, as an illustration of how one codes in a graph replacement system.

PhantomGrammar replacement rules are very flexible, but one limitation is that each rule always matches a fixed number of nodes. Therefore, anything of variable size, or high complexity, needs to be broken down into a series of smaller rules that can operate on different parts of the overall graph, often setting intermediate values to be “fixed” by later rules.

Even this diagram is somewhat abridged – there’s 40 different rules involved in this process, mostly needed accounting for variations.

Similar, simpler, patterns occur all over the code. Whenever something of variable size is needed, there’s a set of rules to set the intial condition, more rules that “grow” the pattern repeatedly, and a final cleanup step.

The drawn circle goes on to become the backbone of the level structure. [Dormans calls this a “ cyclic dungeon generator”](https://ctrl500.com/tech/handcrafted-feel-dungeon-generation-unexplored-explores-cyclic-dungeon-generation/), and it’s a feature that gives the levels a meaningful arc of progress and pacing.

The idea is simple. The generator draws a large circular loop, with a entrance and goal node attached. The entrance and exit divide the loop into two indpendent arcs, both leading between the entrace and the goal. The game then picks from a number of predefined **major cycle types** which each specify how to use those two arcs. The cycle type defines the narrative ebb and flow of the level.

The simplest cycle type simply uses the two arcs as two alternative routes the goal, each with a different set of obstacles.

![](../../assets/73583ea7e7992233.png)

More sophsticated cycles can make use of the arcs in a wide variety of ways.

![](../../assets/cac9148bb3262e53.png)

Many games have pre-authored high level structure, but this specific approach has a lot to recommend:

- Drawing random circles is easy.
- Because the structures have two parallel arcs to work with (rather than a more common tree structure), there’s a lot more possible interesting ways to arrange them. And it’s easy to arrange for a
[one way door](https://tvtropes.org/pmwiki/pmwiki.php/Main/DoorToBefore)to cut down on player backtracking, a common trick used in hand authored dungeons. - The cycle types are extremely general. They
**only**control the main flow of the dungeon, and specify very little about specific forks, layout or details, which are all filled in later. Many of the cycle types contain special rules to make them more generic, such as randomly picking what sort of obstacles are found on an arc, or randomly locating where keys appear.

![](../../assets/14f47fbe16913d1e.png)

Unexplored has 24 different cycle types, several of which are shown in the diagram above. Most of the cycles involve placing keys, doors and one way “valves” to force player progress to follow a known plot. But not all have a strict path. Hubs, for example, have the entire loop easy to navigate, but lock the actual exit behind some sort of challenge. Hubs are used for levels with multiple exits. Another oddball cycle type is the lake “cycle”, which treats the loop as the border of a large central lake, and has a more free roaming feel than many other designs.

After the major cycle has been generated, extra nodes are added to complicate the dungeon futher. Minor cycles, are short detours from the main cycle that can be added, often including more keys and obstacles.

There’s also rules for making cycles longer, or adding dead ends. Combinations of these rules are run until the level has grown to the desired size.

Once the overall layout has been decided, we actually need to populate the dungeon with specific enemies, puzzles, rewards and so on. But for a generator with this level of complexity, it won’t do to simply pick things at random. Doing so would make it very difficult to tune, and impossible to get a cohesive feel to levels.

Instead, the generator starts off with very abstract terms, and progressively refines things until everything has been fully decided. For example, rooms start off just as a specific “path” node, which is handled by the major cycle. Then later, we’ll decide what sort of node we have (cave / tunnel / room, etc). A step even later than that categorizes rooms into specific types (library / forge/ prison etc) and even later, appropriate items and decorations are chosen to fit those rooms.

Unexplored uses two main techniques. **Biomes** are used to encourage consistent choices between otherwise independent systems, and **non-terminal symbols **to indicate a placeholder for that needs resolution later.

One of the first things chosen about a level is associating it with one or more themes. Themes are broad concepts like “fire”, “wood”, “caves” and more specific items like “allrooms”, “waterfalls”. The themes themselves don’t directly affect the level at all, but many resolution steps will reference the level theme to conditionally enable/disable content.

For example, the fire theme can cause lava to generate, fight fire based enemies, ban water feature from the map and cause fire themed items to appear more frequently. The minor themes often enable some specific feature, so you’ll suddenly find a level full of one way paths, or teleports, and so on.

Themes are one of many similar annotations (collectively, what I am calling “biomes”) that are set early on to influence later choices. Some others include:

- Enemy pools are set per level
- Roles are set on sub-areas of the dungeon by the major cycle to indicate what sort of obstacle you are likely to encounter
- Terrains types are used to pick a consistent set of tiles for styling the level.
- Mystery types are used in one of the expansions to tie together a thread of clues into a coherent story.
- Node types determine the set of rules that are used for shaping each part of dungeon
- Room types determine a set of rules to run local to that room (usually to add decorations)

![](../../assets/659884e9135aa838.png)

[A non-terminal symbol](https://en.wikipedia.org/wiki/Terminal_and_nonterminal_symbols) is an graph node that has a replacment rule associated it. They are literally a stand-in for something that will be decided more concretely later.

For example, early stages of the generator use a node type called “Obstacle”. It’s not a specific obstacle, it can be anything that impedes the player, such as an enemy, puzzle or trap. Only late in the generator do we decide what specific one it is, usually with reference to the theme and role. That means all the intermediate parts of the generator can have patterns that match any obstacle. Obstacles are sometimes tagged with specific data such as a difficulty level, so they aren’t picked completely at random.

Another important non-terminal pair is a Lock and Key. As discussed in [lock and key dungeons](https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons), these aren’t literally collectable keys and locked doors, it can stand for *anything* where the player must first locate they key before being able to traverse the lock, be it a key item, switch, or pieces of knowledge. The same lock/key structure is used for both hard locks where the player must find the key, and soft locks, where the key isn’t strictly necessary, it just helps.

![](../../assets/1afe299b09fee43a.png)

Like Obstacles, Locks/Keys have many rules in the middle parts of the generator that deal with them before they’ve been resolved, so those rules work regardless of what sort of key it is. Keys have a special edge pointing to their corresponding Lock, so even as the two nodes are shuffled and moved around the graph, they can always be kept consistent.

Many of the non-terminals stores similar relationships, such as hints to what they hint about, enemies to patrol areas. These extra relationships allow the nodes to be manipulated while ensuring the dungeon is still completable, and makes sense.

In fact, the relationships are part of the level output. This information is not only fantastic for debugging, but the game uses it as a sort of safety check. At any time, you can “Pray For Help”, and the game can determine what’s stopping you making further progress, and fix things.

![](../../assets/904664c5e3baeec8.png)

After the resolution phase, we have a a graph of nodes, each heavily annotated with the specifics of how it should appear, which it should contain, etc. But we still have no actual map.

![](../../assets/48e9458b59682417.png)

The basic 5×5 grid that all the previous generation used is expanded by a factor of two to make space for corridor pieces between each node, which are marked as either barriers or doors.

![](../../assets/ba22952525bc7196.png)

Then the grid is expanded by a factor of 5 to give the actual grid of the map.

![](../../assets/640f88d5942e49e2.png)

Each 5×5 block then has special rules applied to it to give it a specific shape. Doors are shrunk to a single tile, and rooms are grown into a larger rectangle with a boundary wall. Most other areas, such as barriers, caves, tunnels etc, have small cellular automata to give them a rough shape. There are some more elaborate patterns baked in, such as narrow bridges, or tauntingly out of reach rewards.

![](../../assets/3babffae4a6645fc.png)

Though much of the game is spent in open caves, rooms are given special attention. Each room is tagged with a specific type according to what is in it, such as a library, forge, store room and so on. Each room type comes with a special set of rules about how to generate its interior. This customises the cosmetic appearance of the room, what items appear in it, and set pieces.

Set pieces are specific small features that are placed with a pattern matching process. For example, libraries have multiple bookshelf set pieces. Each bookshelf looks for an appropriate place to be drawn – it needs to be placed against a wall, and not cover up a door or other important feature. Some of the set pieces have quite complicated rules. E.g. Decorative columns need to find an appropriate empty corner to start in, then have other patters for increasing the length of the colonnade across the width of a room.

Items are similarly placed with rules. Many items can go on any empty space just sitting on the floor, but chests have several patterns to generate nice alcoves.

Terrain gives some cosmetic variation to the natural areas of levels, such as fields, forests and so on.

Terrain defines a simple 2 tone pattern by randomly assigning a value to each cell, then applying some smoothing. PhantomGrammar has [specific operations](https://www.boristhebrave.com/?p=780) for dealing with cellular automata like this. The two tones become terrain types A and terrain B. Then, inside terrainB, 4 seed points are picked and then two more terrain types (C and D) are made by growing outward from those seeds. The border of the level is forced to terrain type A, and extra B cells are drawn to cut off C and D regions.

![](../../assets/0da29626c5996dfd.png)

The 4 terrain types are then superimposed on a level. The exact use of the terrains varies by levels. Usually, they each become a different tile type, but some special levels have further processing to cluster vegetation into specific patterns.

Now that the majority of the level is locked in, there is little left to do. Items are placed in appropriate places, and some vegetation laid down. There’s numberous fixup and small cosmetic tweaks that are done at this stage, then all that remains is to pass the tile map plus annotations to the game engine, which can construct a level at runtime from

![](../../assets/81b67800338b158f.png)

I’ve done my best to give some details on the generation. Unexplored is one of the most complicated systems I’ve seen, but I suspect thanks to the system of graph rewriting, and the Ludoscope tool, it became feasible to be designed by a single developer. That’s truly a powerful system worth more attention.

But I also see many trends in common with other games I’ve looked at. I’ve spoken many times of the power of generating something abstract first and filling in the details second. This pattern is repeated over and over again in Unexplored, in little and large. Though it might be better to describe it here as three phases – Unexplored has a sort of middle phase where the abstract dungeon is warped, manipulated and made more complex before any resolution starts.

Another take away is that Unexplored feels pretty varied simply because of the amount of rules authored. While there’s no pre-authored levels, there’s all sorts of story vignettes, puzzles, hints and adventures which have been explicitly designed. I’m sure the tooling made this sort of thing easy to add, but it still represents a lot of design work that procedural generation does not shortcut.

I’d say the strength of Unexplored’s dungeons is in their coherency and structure, packed into a compact space. As Joris himself has [observed](https://twitter.com/DormansJoris/status/1375324332491210763), “*it is so much more interesting to generate small levels than it is to generate large ones*“.

I will probably be visiting Unexplored and Joris Dorman’s work in future, as his body of work both in academia and games is huge and has many interesting ideas in it. Analysing Unexplored has already turned [into](https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons/) [four](https://www.boristhebrave.com/2021/04/02/graph-rewriting/) [separate](https://www.boristhebrave.com/2021/04/02/phantomgrammar-and-ludoscope/) [articles](https://www.boristhebrave.com/?p=798), and it’s still more compressed than I would have liked.

I’m particularly looking forward to [ Unexplored 2: The Wayfarer’s Legacy](https://store.steampowered.com/app/1095040/Unexplored_2_The_Wayfarers_Legacy/) which is built using similar tools, but is

[even more ambitious](https://www.ludomotion.com/blogs/level-generation/index.html)in scope. The graphics are vastly improved and and looks like

[it’ll feature NPC AI](https://twitter.com/DormansJoris/status/1214545863109959681)using the same graph system. Dormans’ work is slowly making the field of procedural generation a little less… unexplored.

![](../../assets/8737f78f97f7644f.png)