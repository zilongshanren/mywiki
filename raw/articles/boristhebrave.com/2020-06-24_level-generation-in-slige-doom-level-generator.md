---
title: Level Generation in SLIGE (Doom level generator)
url: https://www.boristhebrave.com/2020/06/24/level-generation-in-slige/
author: Boris
published: '2020-06-24'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

It’s time for another in my series on [how games do level generation](https://www.boristhebrave.com/category/level-generation/). Let’s take a look at [SLIGE](https://www.doomworld.com/slige/), a random level generator for [Doom](https://en.wikipedia.org/wiki/Doom_(1993_video_game)). The original Doom. That’s right, we’re going back to the early 90s for this one.

Doom was one of the first games designed from the ground up to friendly to modding, and consequently the community around it exploded. In the years following its release, level packs and tools started to circulate for free. It was only a matter of time until someone designed a random level generator.

SLIGE was one of the first. It quickly became [infamous](https://doom.fandom.com/wiki/Top_10_Infamous_WADs) because newcomers would often attempt to pass off the level it creates as their own. But they’d inevitably get caught – SLIGE levels have a very distinctive feel, as you can see in the video below.

SLIGE may not be the most sophisticated level generator out there, but its fame caught my eye. It was under development by author **David Chess** for a number of years, and so has lots to explore. In this article, we’ll delve into how exactly it works.

## A bit about Doom

Doom was developed by [id software](https://en.wikipedia.org/wiki/Id_Software), which was already a successful game developer by the 90s. They’d noticed that their previous game, [Wolfenstein 3D](https://en.wikipedia.org/wiki/Wolfenstein_3D), was being hacked on by fans to add new levels and alter the data. Both John Carmack, lead developer, and John Romero, lead designer, looked on such hacking fondly, and planned Doom from the start to encourage it.

At the time, it was a radical business plan – the engine Carmack had made for Doom was groundbreaking, and id’s business model at the time involved sequels (often dubbed “episodes”) reusing the same engine. It turned out fears of lost revenue were unfounded, as the mods created mostly stayed non-profit, and id was able take some of them commercial, and licence out the engine for other games (such as [Heretic](https://en.wikipedia.org/wiki/Heretic_(video_game))). Or perhaps Doom was such a massive success, it never really mattered what money they left at the table.

Anyway, the upshot of this was that all the game data was separated from the game itself, into a file called a WAD (short for “Where’s All the Data”). All a budding designer or automatic level generator had to do was create a WAD file, and Doom.exe could load it.

WAD files themselves were as innovative as the rest of the doom engine. They broke from the rectilinear grids of Wolfenstein 3d and similar games, and instead the level was described by a series of straight lines (called linedefs) which defined the walls for a level, and sectors, which described the areas of the level, bounded by specific linedefs. The level maps are entirely 2d – features such as stairs, windows, elevators, even doors, were made by carefully varying the height of the ceiling and floors, which could be set in attributes of the sector. Other sector and linedef attributes controlled what textures to show, lighting, interactivity and so on. Other sections of data controlled placement of enemies and objects (“things”), graphics, sound etc.

Nowadays, we’d recognize the structure of lines and sectors as the edges and faces of a [polygon mesh](https://en.wikipedia.org/wiki/Polygon_mesh), albeit in 2d. The same structure is essentially still in use today, for example the [BMesh](https://docs.blender.org/api/current/bmesh.html) objects used in Blender.

I really don’t have space to go into all the incredible techniques that John Carmack pioneered in Doom and his other games. Suffice to say, he’s a programming genius of the highest order.

## Delving into SLIGE

Fortunately for us, [the SLIGE source code](https://github.com/Sunlitspace542/SLIGE) has survived to the present day. It’s written in ANSI C, with no dependencies. It simply spits out a WAD file according the a configuration file and random seed. The WAD file does need to be post-processed after generation before Doom can load it. This is needed to calculate the [BSP-tree](https://en.wikipedia.org/wiki/Binary_space_partitioning), another key innovation of the Doom engine.

From a glance, it’s clear that Chess was not big on abstraction, and many modern programming idioms are completely absent. This is completely contrary to my looks at [Diablo](https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/) and [Enter the Gungeon](https://www.boristhebrave.com/2019/07/28/dungeon-generation-in-enter-the-gungeon/), both of which used an abstraction layer to simplify the task of building a level.

SLIGE is a single 14 thousand line C file, and the majority of it works directly with sectors and linedefs in memory in a format very similar to how they will appear in the WAD file.

This tight integration gives the author more control over the output, but does make it quite verbose to do simple things. Fortunately, there is a suite of functions for basic geometry such as subdividing a linedef, and another set for making random desicions from the seed.

That said, there are some key structures in the code that represent higher level concepts.

### Rooms and links

SLIGE draws a level in pieces – **rooms**, which contains enemies and pickups, and **links**, which are straight corridors between rooms. Both are essentially axis-oriented rectangles. This gives SLIGE levels a very blocky feel to them, as manually designed levels usually take advantage of Doom’s support for arbitrary angled walls, and irregular sector shapes.

But even though the base plan is a rectangle, both rooms and links are subject to a great deal of random variations. Rooms can have recesses, secret nooks, traps, raised sections, etc, while links can be stairs, elevators, teleporters, and include windows and embelishments. One of my favourite is “twinned” corridors, where the rectangle is split in two and the link building function recusively invoked – very clever.

![](https://www.doomworld.com/slige/slash1.gif)

### Quests

Rooms handle the moment by moment level building, but **quests **are what give a level its structure. Quests are what we’d now call a type of [lock-and-key](https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons/) generator. They give a level structure that has no loops, and exactly one way to complete the level. They’re not totally linear though – you may get a key, and then need to backtrack to a fork to get to the door the key was needed for.

SLIGE initializes each level with a single quest: the goal is to get to the level end. The quest also has a randomly picked minimum number of rooms (usually 18). It generates a starting room (with a characteristic “S” watermark in it).

SLIGE proceeds to add a new room near the most recently created room, and draw a link between them. This continues until there’s enough rooms for the quest, or there’s no space for the next room. Either way, the quest is over, and we put put the quest end in the final room. For the level end quest, that would be the exit gateway that marks the end of the level.

If that were all, the levels would be completely linear. But each time a room is created, there is a random chance of a **fork**.

### Quest Forks

When a fork occurs, the current quest is pushed onto a stack, and a new quest started. The remaining minrooms of the old quest is randomly subdivided between the old and new quest. A new goal is chosen for the quest, one of the following:

- KEY – a key will be placed at the end of the quest
- SWITCH – similar to KEY, just with a pressable button instead
- GATE – a teleporter will be placed at the end of the quest.
- NULL – short dead end with a minor pickup at the end

In each case, the route to the old quest is blocked off, requiring players to complete the new quest before returning to the old one. For KEY/SWITCH that means a locked door. For GATE, it is an impassible window with the other end of the teleporter tantalising you on the other side. NULL quests do not block off the original quest, leaving players with a decision about which way to go.

![](https://www.doomworld.com/slige/slige1.gif)

Multiple forks for one room can be generated, though they are rarer and unlikely to fit.

A new room is generated that links to the current room for each fork, and the room building mechanism starts from there, potentially doing further forks along the way.

Eventually though, the new quest comes to an end. Something is placed in the final room, then the old quest is popped from the stack, and generation resumes from the room that was previously locked.

Level generation ends when the quest stack is fully popped and the intial level end quest is done.

### Other Level Generation Bits

There’s a chance that any SWITCH quest will get randomly replaced with a KEY quest. When doing so, it generates a key-activated switch, so you need to get the key, hit the switch, then go through the door.

In some circumstances, the level end goal gets replaced with an arena goal, which teleports you to a large room to fight one of a random selection of bosses, getting a [soul sphere](https://doom.fandom.com/wiki/Supercharge) to help.

![](../../assets/6d0a025c8ced4c2f.img)

There’s also code to add secret exits to levels and sometimes patios – extra rooms open to the sky with grass and plants.

### Generating Enemies And Pickups

SLIGE levels are designed to be very finely tuned difficulty-wise. It doesn’t just slap down a bunch of random enemies and call it a day. Instead, it keeps a running estimate, for the level generated so far, of how much health, armor and ammo a good player should have.

A separate estimate is tracked for each difficulty level. Each time an enemy is added, the estimates are updated for how much a player would lose fighting that enemy. When the values drop too low, then pickups are eligible to be generated, in appropriate places (quest ends, secret areas and nooks). When values are high enough, monsters are generated in appropriate places (any room).

The calculations are quite finely tuned to keep the game well balanced. Here are some neat tricks I found:

- When traps are generated, it assumes players will lose some health, except on the hardest difficulty.
- It assumes players will use big armour pickups more optimally on harder difficulties (pick up armor too early and you’ll hit the armor cap, wasting some of the pickup).
- Ammo is tracked separately for each weapon, and it knows what weapons are available at a given point in the level. The health and ammo cost of a monster depends on what weapons you have when you fight it.
- The higher the difficulty, the more likely it assumes the player is to find secret areas.

When generating monsters, it naturally only picks monsters that the player should enough health and ammo to defeat. It also have several random variations to keep gameplay interesting. Rooms typically have 2-9 monsters in but sometimes have nothing and sometimes have as many as possible. Monsters are randomly [deaf](https://doom.fandom.com/wiki/Deaf), different classes of monsters may be filtered out and there is a level setting that controls how homogenous a room with multiple monsters is.

### Themes and Level Settings

A great deal of work went into ensuring that the levels have a consistent feel to them. This mostly manifests in two ways.

Each room has a bunch of “theme” settings. This controls the textures used on the walls, ceilings and door, and what sort of items spawn in it. When a new room is created, it inherits the theme of the previous, with some random mutations. When forks occur, the theme is changed more than usual. A configuration file supplied with the program specifies which textures go well together, so it never generates rooms that are too discordant (for example mixing the gothic and sci-fi textures that are prevalent).

![](https://www.doomworld.com/slige/nukroom.gif)

Even more important are the **level settings**, which are generated once at the start. There’s a [huge variety](https://github.com/Sunlitspace542/SLIGE/blob/master/SLIGE.C#L993) of these, and they enable or disable different parts of the generator. So, you might get a level with no stairs, only elevators, or with only certain enemies, or particularly dark. Most of the time, the settings are not a boolean, but a probability controlling the frequency of a particular feature throughout the level. Some rare settings make quite specific levels – sometimes all enemies will come in pairs, or flooded with lava.

Fixing these parameters at the start goes a long way to make a level consistent, and more memorable. It’s a great way of avoiding generating [10,000 bowls of oatmeal](https://galaxykate0.tumblr.com/post/139774965871/so-you-want-to-build-a-generator). But it had a secondary purpose, too. Remember, SLIGE ran offline, and then generated WAD levels that could be independently distributed. If the generator hit across a particularly good combination, that WAD would be passed around and proliferate; survival of the fittest. That would give the author a chance to see what sort of settings were successful, and tweak future iterations towards that. And tweak he did – by the time development ceased in 2000, SLIGE had reached version 485!

## Conclusion

When I first saw the output of SLIGE, I was unimpressed. It generates endless series of repetitive, boxy rooms. But now I delve into the source code, I see that David Chess’s priorities are simply very different, and he’s done a stunning job given the limitations of Doom.

The focus is not on having the best floorplan, but having the best *gameplay*, which is achieved by careful tuning of the difficulty, and choosing randomness that gives a consistent experience over a level (or series of levels), and holds back surprises and special features to be used sparingly. The quest system doesn’t generate hugely ambitious levels, but it’s enough to provide some structure and pacing to the experience. While I don’t think SLIGE provides endless variety, it meters out what it does have very efficiently.

Honestly, a lot of modern roguelikes could stand to learn a few lessons from SLIGE. Nowadays, it’s common to pre-author a thousand rooms, so things look very polished, but not actually code many ways to alter them, or put them together coherently. That’ll be particularly evident in the next game I’ll look at, [the Binding of Isaac](https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/).