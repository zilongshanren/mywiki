---
title: Dungeon Generation in Diablo 1
url: https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/
author: Boris
published: '2019-07-14'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

[Diablo 1](https://en.wikipedia.org/wiki/Diablo_(video_game)) is a classic 1996 hack and slash action RPG. It was one of the first popular attempts at bringing roguelikes to the masses, from the niche ascii art. It’s spun a host of sequels, and imitators. It’s known for a dark, moody atmosphere that intensifies as the player descends into the dungeon beneath the town of Tristram. It was one of the first games I played with procedurally generated maps, and it blew me away that generating such convincing areas was even possible.

I recently discovered that thanks to the discovery of various debug symbol files accidentally left lying around, several fans took it upon themselves to [reverse-engineer the source code](https://github.com/diasurgical/devilution) and clean it up into a good guess at what the original game is like. Thus began a week long deep dive into how exactly did lead developer, David Brevik, actually craft these levels. It may have taken away some of the magic of the game, but I learnt lots of techniques I think are applicable to anyone developing a similar game, which I share with you below.

Thanks to David Brevik and the Blizard North team for making such an amazing game, and to [galaxyhaxz](https://github.com/galaxyhaxz) and the Devilution team for their amazing work restoring this game into a readable state.

You can hear [Brevik talk about the generation](https://www.youtube.com/watch?v=VscdPA6sUkc&t=71m42s) in his postmortem, but here I include all the gory details, and my own interpretation of them.

# Overview

Diablo is an isometric tile based game. The game consists of 4 stages, each of 4 levels. The stages are "Cathedral", "Catacombs", "Caves" and "Hell". There’s also some fixed levels, like the town of Tristram, which I will not cover here. Diablo has a separate level generation routine for each of the 4 stages, so I’ll first discuss features, and then how each stage works separately.

I’m only really interested in how the levels are generated. For details on quests, monsters, etc, I can recommend [Jarulf’s Guide To Diablo and Hellfire](http://www.lurkerlounge.com/diablo/jarulf/jarulf162.pdf) which discusses these aspects in exhaustive detail.

# Common features

Although there’s a separate level generator for every stage, there are some common features they all share.

## Dungeons and tiles

Every level of the game is generated to fill a 40 by 40 grid of tiles. The x-axis corresponds to south east on the map, and the y-axis to south west.

These tiles are actually only used for level generating purposes. Once the level is created, each tile is subdivided into 4 "dungeon pieces" for rendering.

![](../../assets/3ae90b737dbb0624.png)

This more fine grained grid is used for determining what is walkable, and also allows for a more efficient re-use of graphics memory. I’ve written about [subdividing tile schemes in the past](https://www.boristhebrave.com/2013/07/14/tileset-roundup/).

This means that a typical diablo map has over a hundred tiles, many of which are subtle variations of another, to account for all possible ways they can connect up. We’ll talk about this more later.

To my surprise, unlike other games in the series, dungeons maps are not assembled out of pre-authored chunks. Almost everything is done on a per-tile basis with algorithms.

## Multi stage process

Each dungeon routine is split into two stages. The "predungeon generation" doesn’t deal with choice of tiles at all. It just generates a array of which tiles are walkable, where there are doors, and a few other high level details. Then as a second stage, the predungeon is converted to an array of tiles, and further tile aware generation and changes are done afterwards.

This must have been tremendously convenient as a designer. You can tinker with the floor plan completely independently from choice of tile and stylistic choice. But in many cases the two are somewhat interlinked to give a more coherent feel.

All the predungeon stages work by starting with an entirely solid level, and recursively setting parts of the level to be floor tile. The details are covered later.

## Set Pieces

Set pieces are pre-authored chunks of level that are simply pasted verbatim into an otherwise randomly generated level. They are used for the majority of the quests in the game. There can only be one set-piece per level, and the choice of positioning is custom to each stage.

![](../../assets/665a8b719aa65855.gif)

## Minisets

Minisets are another way that pre-authored content reaches a level. These are small patches, often around 3×3, which are inserted randomly into the dungeon. There’s a simple pattern matching scheme so that they only get put in "valid" positions. They are often coded with additional requirements, e.g. that minisets cannot be placed to near each other, and cannot overlap set pieces and so on. Some minisets always find and replace, some only do so at a fixed probability.

Minisets are used for a wide variety of purposes in Diablo. They are used for placing larger tile based objects, such as stairways, but they are also for fixing up combinations of tiles that don’t properly connect together and adding some random variation to tiles.

![](../../assets/6a8a6450a5427ac8.png)

## Theme Rooms

Theme rooms are small spaces enclosed by a wall and a door. They typically have some preset objects randomly in them. For example, libraries always have a book case bracketed by two candles, and some random book stands and monsters. Monster pits have a ton of monsters and a random item, and so on.

In cathedral levels, the generator already makes appropriate rooms, so they are detected via [floodfill](https://en.wikipedia.org/wiki/Flood_fill) and re-purposed. In other stages, open spaces are found and then a rectangle of walls and a door is drawn for the purpose.

Each theme room type has specific requirements as to size and what stages it generates on.

![](../../assets/e4cde9cf1b4cf26f.jpg)

## Tile Substitutions

Several of the maps have special customization of tiles, but they all share in common that some tiles can be swapped out for equivalent variations. More common tiles (like floors and flat walls) tend to have more variants to break up the monotony. Tile substitutions are set to never be used twice too near each other.

## Pattern matching and "fixups"

As discussed, minisets already work as basic find and replace mechanism to fix faults with the generators. But most stages include several routines to detect and fix more specific problems. I won’t go into specifics here as there are loads of them. Suffice to say that Diablo is pretty buggy and it’s apparent once they got closer to release it was easier to just add detection for specific problems rather than address the underlying issues.

One common fixup is "lockout", which detects if it’s not possible to walk across the entire dungeon, and restarts generation if it fails.

## Quests

Most quests are handled by set pieces, but a few have custom logic. For example, "Zhar the Mad" generates in library theme rooms, "Poisoned Water"’s entrance is generated by a miniset, and the "Anvil of Fury" has specific level generation code. I won’t cover the specifics, but the code is littered with specific checks for quests.

# Cathedral

The cathedral is easily the most iconic of the diablo stages. It is defined by its long rows of gothic arches, boxy rooms and providing many choke points via doorways. Let’s delve into how it is constructed.

## Predungeon

The first thing that is done is to draw the spine of this map. It randomly chooses to place up to 3 10×10 rooms in predefined positions along the central x or y axis. A wide corridor is also drawn along the axis to connect the room. If there’s a set piece on this level, it always goes in the center of one of these rooms. These central rooms are also marked as ineligible for adding extra walls too later, so they are always a large open space.

All other rooms are generated by a recursive "budding" technique in a function called `L5roomGen`

which is initiated from each of the above rooms, and the choice of axis.

`L5roomGen Listing`


- Passed in a rectangle of the initial room to bud off, and a preferred axis.
- 1 in 4 chance of switching the preferred axis between X and Y.
- Pick a random size for the new room, either 2, 4 or 6 tiles on each side.
- For each side of the initial room along the selected axis (i.e. SE/NW for X, SW/NE for Y):
- Align the new room rectangle to the center of that edge of the initial room
- Check nothing has been drawn there yet and we haven’t reached the edge of the map. A one tile border is required for walls.
- If the check passes, draw the room in.

- For each room that was drawn, invoke
`L5roomGen`

recursively, passing in the new room, and the opposing axis to the one just used.

The net effect of this procedure is to start with a few rooms in a large amount of solid tiles, and then repeatedly glue extra rectangles to carve out more walkable space. At this stage, all "rooms" are open on one side, as each new room is placed directly adjacent to the previous room, with no gap for a wall.

The generator now counts the number of walkable tiles generated. If it doesn’t meet a minimum threshold that increases every level, the dungeon is scrapped and retried.

## Dungeon

So far, the only tiles placed are solid and floor. We need to replace those with actual wall tiles. Diablo uses marching squares for this, which I’ve [discussed in a previous article](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/).

However, it uses an unusual variant. The cathedral tileset includes walls, but they are always at the back edge of the tile. So there’s a tile with a wall on the north-east face, but not one for the south east face. To get walls for the other sides, you have to find a solid tile which has an extra wall extending outside the tile boundary. This sounds weird, but it’s actually very convenient for depth sorting walls (though David Brevik himself said it was the [number #1 mistake](https://www.youtube.com/watch?v=VscdPA6sUkc&t=20m17s)).

To deal with this, Diablo skips some walls during marching cubes:

The extra walls are added in a later fixup step. I think this simple procedure is one of the most responsible for the cathedral’s "look". Because opposing walls are attached to solid tiles, if you have two rooms that are separated by one tile of walls, the opposing wall is simply not created. That means that separators between rooms are "thinner" than you could normally get with the resolution marching cubes is done at.

Once the basic walls are placed, the generator also 4 free standing columns to each of the three central rooms, and a colonnade of arches for the central hallway. This helps the cathedral look more deliberately constructed than the other levels, and helps players orient themselves.

Then the generator randomly adds dividing walls. Dividing walls always run straight along an axis from one wall to another. They start at corners, which tends to make them neatly divide areas into boxes. 25% of the time the wall is a series of arches, 25% of the time a series of arches with bars covering the entry, and otherwise is a solid wall. For bars and solid walls, a door or arch is randomly added somewhere along the dividing wall to ensure the space is still walkable.

A floodfill routine identifies potential theme rooms.

Stairs are placed to connect to other levels. The dungeon is retried if these cannot be placed.

Then comes a raft of mini sets, fixups and substitutions I’m not going to go into. My favourite is the PANCREAS1 miniset, which has a 1% chance of placing a chunk of bloody flesh on a floor tile. Finally 5-10 lamps objects are dotted around to give some decoration.

![](../../assets/eb6535b43b0aff5f.png)

# Catacombs

Whereas the Cathedral feels like a designed building, the Catacombs has a much more haphazard feel. It’s characterized by squarish rooms connected to each other via mazy winding corridors. It has wide openings instead of doors in many places, increasing the chance the player will be mobbed by many enemies.

The catacombs is also where the generation algorithm is most advanced. I suspect time pressures caused simpler approaches to be taken for later stages.

## Predungeon

The predungeon routine for catacombs is actually somewhat unique. The other stages have a simple boolean indicating if there is floor or not (plus a bitset for additional details). The catacombs stores its predungeon in an ascii map, much like the classic roguelikes. That’s not too much of a surprise considering [David Brevik explicitly took inspiration for Diablo from Angband](https://www.rpgfan.com/feature/david-brevik-interview/).

The main room generation is a recursive algorithm again, this time recursive subdivision. The function `CreateRoom`

is called with the entire 40×40 dungeon area, with a 1 tile border removed.

`CreateRoom Listing`


`CreateRoom`

is passed a rectangle which is the area it is meant generate rooms inside. It’s also passed details about the originating room (initially null)- If the area is too narrow, exit.
- Pick a random size for the room between 4 and 9 tiles each side, respecting the max size of the area to put the room in.
- Pick a random position for the room in the area.
- Draw the room into the ascii map. The drawing uses
`'.'`

for floor tiles,`'#'`

for a surrounding wall, and`'A'`

,`'B'`

,`'C'`

and`'E'`

to mark the 4 corners. - If there is an originating room:
- Pick a random tile on the closest sides of the originating and new room.
- Record that information in a hallway list to be used later.

- Cut the remaining parts of the area excluding this room into 4 rectangles.
- For each rectangle, shrink the size by two tiles to ensure space between rooms, then recursively call
`CreateRoom`

with that rect as the area, and the created room as the originating room.

If there’s a set piece it will always be this first room created by CreateRoom, and it’ll be forced to a large enough size to fit the set piece.

After calling `CreateRoom`

, there will be an ascii array something like the following (thanks to [nomdenom](https://github.com/nomdenom) for extracting this):

```
A##B
#..#
A####B #..#
#....# #..#
#....# C##E
#....#
C####E A#####B
#.....#
#.....#
A########B #.....#
#........# #.....#
#........# C#####E
#........# A#B
#........# #.#
#........# #.#
#........# #.#
#........# #.#
#........# #.#
C########E #.#
#.# A#B
C#E #.#
A####B #.#
#....# #.#
#....# #.#
#....# #.#
C####E #.#
#.#
A#####B C#E
#.....#
A###B #.....#
#...# #.....#
C###E #.....#
C#####E
```


In this case, the bottom most room was the "root" room created initially.

Then the hallways information is used. A line is drawn between each recorded pair of points. When it intersects a wall, a `'D'`

is written, and when it intersects a solid tile `','`

is used. Hallways are randomly of width 1, 2 or 3. The corner tiles are used to assist navigation.

Doors are skipped if they would be adjacent to another door and hallways can overlap, helps obfuscate the simplicity of the generator..

After all halls are written, the ascii is cleaned up. Corner tiles become wall tiles, and all `' '`

tiles adjacent to a `','`

also become walls. Finally, `','`

is replaced with `'.'`

. That leaves a dungeon plan like the following.

```
####
#..#
###### #..#
#....# #..#
#....# #D##
#....# #.#
#D#### ##D####
#..# #.....#
#..# ###.....#
##D######## #.D.....#
#........# #.#.....#
#........# ### #.##D####
#........# #.### #.##...#
#........###.D.# #.##...#
#........##..#.# #.##...#
#........##..#.# #.##...#
#........##..#.# #.##...#
#........##..#.# #.##...#
###D#######..#.# #.##...#
#.......#..#.# #.###D##
###.....#..### #.# #.#
#######D##.# #.# #.#
#....#.# #.# #.#
#....D.# #.# #.#
#....###### #.# #.#
##D####....## #.# #.#
#...........# #.# #.#
####....###D####.# ###
######.....##.#
#####.D.....##.#
#...D.#.....D..#
#####.#.....####
#########
```


As you can see, this routine can leave quite a lot of empty space on the map. Hence the next thing the generator does is "fill voids". This looks for any contiguous stretch of wall that it can glue extra rectangles of floor to. The rectangles much be at least 5×5 and at most 12×14.

Fill voids continues until there are at least 700 tiles, or the retry threshold is reached. If it doesn’t get to 700 then the dungeon is restarted from scratch.

That gives us a the final predungeon seen below.

```
##########
#........# ###########
#........# #.........#
#........# #.........#
#........# #.........# ####
#........# #.........# #..#
#######..###.........# #..#
#..............# #..#
#..............# #D##
#..............# #.#
#D####.........# ##D####
#..# ########### #.....#
#..# ###.....#
##D######## #.D.....#
#........# #.#.....#
########........# ### #.##D####
#...............# #.### #.##...#
#...............###.D.# #.##...#
#...............##..#.# #.##...#
#...............##..#.# #.##...#
#...............##..#.# #.##...#
#...............##..#.# #.##...#
#......###D#######..#.# #.##...#
#......# #.......#..#.# #.###D##
#......# ###.....#..### #.# #.#
#......#########D##.# #.# #.#
#.........# #....#.# #.# #.#
#.........# #....D.# #.# #.#
#.........# #....###### #.# #.#
#.........# ##D####....## #.# #.#
#.........# #...........# #.# #.#
#.........# ####....###D####.# ###
#.........# ######.....##.#
#.........# #####.D.....##.#
#.........# #...D.#.....D..#
########### #####.#.....####
#########
```


## Dungeon

Again, catacombs departs from the standard level formula. Rather than use marching squares (which assigns tiles based on 2×2 rects in the predungeon), there is a custom pattern matching routine that matches looks at each 3×3 rect in the predungeon to decide the corresponding tile in the dungeon. The patterns specify whether each predungeon tile should be wall, floor, door or solid, or some combination of the above. I’m not sure why.

The rest of the function should sound familiar if you’ve read the cathedral. Up/down staircases are placed, the dungeon is checked to see it’s fully navigable, and various fixes are run. Theme rooms are inserted as described in the Common Section, then a bunch of minisets and substitutions.

I think the minisets fiddle around with doorways, but they’re pretty tedious to read without a tool so I didn’t go to far into it.

# Caves

The caves stages are filled with wide open spaces and rivers of lava. The walls of the area are rough and wobbly. The only rectilinear components are some wooden planking that is evidently a later addition than the caves themselves.

This stage is one of the most visually stunning in the game due to the animated lava and as it feels a marked departure from the room-like structures found earlier. I was quite surprised therefore to discover much of the generation is modeled after the cathedral stage, with some clever ideas to make it feel more "cave like".

## Predungeon

Caves starts with a single random room of size 2×2 somewhere near the center of the map. It then calls the `DRLG_L3CreateBlock`

routine on each edge of that block.

When rectangles are drawn in this level, they are not just a normal fill. The interior is always solid, but every tile on the edge has a 50% of being floor, and otherwise is left as solid.

`DRLG_L3CreateBlock Listing`


- This function takes a rectangle edge, i.e. a starting point, a direction and a length.
- Choose a new block size to create, between 3-4 on each size.
- Align the new block randomly against the input edge.
- If there’s not space to draw the block, exit.
- Draw the block.
- If a 1 in 4 chance, exit.
- Recursively call
`DRLG_L3CreateBlock`

with the 3 edges of the block other than the one we came in from.

Though the routine is similar to `L5roomGen`

above, the fact is uses a much smaller block size and draws rough boundaries means it gives a much more organic feel. It also doesn’t include a 1 tile boundary for walls, so unlike the previous generators it can create loops.

After blocking out the rough shape of the dungeon, the generator applies some erosion routines:

- First it finds 2×2 areas of tiles that two solid tiles diagonally opposite from each other. These formations are often fiddly to deal with when doing marching squares, so one of the solid tiles is replaced with floor, randomly.
- Any solid tiles that are solos, surrounded by 8 floor tiles, are replaced with floor.
- Any long, straight section of walls are randomly roughened up by replacing 50% of them with floor tiles.
- Diagonals are cleaned up a second time.

All of these routines add more floor tiles, so the map is more open than it was before.

If there are less than 600 floor tiles, the map is retried.

## Dungeon

The predungeon is converted to tiles via marching squares. Unlike the cathedral and catacombs, the tileset is much more conventional, and includes nearly all combinations needed for marching squares. But it’s missing tiles for diagonally opposing walls – those were cleaned up in the predungeon phase so never come up.

Next is a bunch of minisets, as usual. There are several minisets that identify a free standing section of wall and replace it with stalagmites and floor, adding to the openness.

The a pool of lava is added. This is done by looking for a contiguous section of wall by [floodfill](https://en.wikipedia.org/wiki/Flood_fill). If it can find a section of wall / solid tiles that is less than 40 tiles that is completely surrounded by floor tiles, it is replaced with lava. The dungeon is retried if a pool cannot be found.

![](../../assets/4312d5581aaab48e.png)

Then some rivers of lava are added. The generator takes several attempts at drawing a river that starts at the pool of lava and terminates in a wall. The requirements are that the river never doubles back on itself, must be between 7 and 100 tiles long and there must be a valid spot to place a bridge tile. The bridge tile ensures that the whole map remains traversable. Up to 4 rivers can be added, if space is found.

Then theme rooms are placed. In this stage, the walls of theme rooms are wooden fencing, which cannot be walked through, but can be seen through. More wooden fencing is involved in two further routines. The first gives wooden cladding to any remaining sections of walls that are long straight segments. The second draws a line of fencing across the map, from one wall to the opposing, then inserts a door. Unlike the cathedral generation, it doesn’t look for corners to start these walls.

![](../../assets/964fb5a3be0fa613.png)

# Hell

Hell is the final stage of Diablo. The focus at this point is really on the monsters and the level design takes a back seat. It has one of the smallest tile sets in the game, and much of that is used for the oversized staircases and pentagrams. Hell levels tends to be a few square rooms and a symmetric layout.

## Predungeon

The generation of Hell starts with a random room of size 5-6 each side (larger if there is a quest set piece), then applies the same recursive budding used in the cathedral. The generation is restricted to a 20×20 area though.

A vertical and horizontal corridor extending to the edge of the 20×20 area is added.

Finally, the predungeon is mirrored vertically and horizontally to get to full size.

## Dungeon

The predungeon is converted to tiles by marching squares again. Then walls are added similarly to the cathedral, and theme rooms, like the catacombs and caves.

# Conclusions

I enjoyed reading this code a lot. Though it’s clearly buggy, the naming conventions are a mess and some things couldn’t be reconstructed into quality source code, it’s also clearly very battle tested code, and brimming with clever ideas.

Here are some of my key take aways:

- The devil is in the detail – the individual components are not crazy complex, but they combine together to give something that looks great. I imagine the devs just kept plugging away at improving the quality until the levels went from good to amazing. The number of tiles and combinatorial complexity of the tile sets is very high too – you cannot do that without a lot of attention to how things connect up.
- Pattern matching find-and-replace is very powerful, you can do a wide range of effects with it. It fixes buggy generation, adds variability, inserts pre-authored content, handles erosion, you name it!
- Seperation of dungeon generation into a walkability map (predungeon) and tile generation is also very handy, both for design and debugging.
- If you want to give different areas a different feel, writing a separate algorithm is a great way of doing that. A lot of code can be re-used while still creating a very different overall feel.
- When in doubt, glue more rectangles onto the side of things.

Excellent analysis. Thanks for sharing!

Now if only Blizzard would read your breakdown to emulate since they’ve obviously forgotten the secret sauce. Well written.

Awesome

I have 400+ screen captures of level oddities in Diablo 1. (36Mb)

I may have to create a YouTube video.

Broken walls, catacomb entry pillar without a staircase, lava-locked beasts,

levels with the exact same dungeon layout…

Jade Amulet of the Zodiac, +20 to all attributes, +30% resistance to all.

Dragon’s Amulet of the Zodiac, +20 to all attributes, mana +60.

Boris, thank you so much for writing this! It is really wonderful to be able to read the insights of someone with deep understanding of map level generation. Even after reversing it, I don’t think we (on the Devilution team) have as good of an understanding of the code as you do 🙂

I have a tool for you to help with this, called miniset_dump 1. It converts the minisets to Tiled TMX format, and also converts the tilesets to PNG format.

If you want to try the tool out, simply run these steps (you need an original version of diabdat.mpq and diablo.exe, version 1.09b).

`git clone https://github.com/sanctuary/opensource-ami`


cd opensource-ami

./get_tools.sh

go install ./...

ln -s /path/to/diablo-v1.09b.exe diablo.exe

ln -s /home/u/_share_/diabdat.mpq diabdat.mpq

make

Jari, I’d love to take a look if you feel like sharing. We are tracking bugs present in the original Diablo 1 game in the GitHub issue https://github.com/diasurgical/devilution/issues/64. Please post a comment there and we’ll look further into it! 🙂

Cheers,

Robin

P.S. I may not notice if you reply to this post. So to get in touch, just ping me on GitHub (I’m mewmew).

(I posted this comment just recently, but it did not show up, so this is my second try)