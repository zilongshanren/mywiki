---
title: Dungeon Generation in Binding of Isaac
url: https://www.boristhebrave.com/2020/09/12/dungeon-generation-in-binding-of-isaac/
author: Boris
published: '2020-09-12'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

The Binding of Isaac, and its remake, Binding Of Isaac: Rebirth are one of my favourite games of all time. It’s a roguelite twin stick shooter, much like [Enter the Gungeon](https://www.boristhebrave.com/2019/07/28/dungeon-generation-in-enter-the-gungeon/).

The dungeons it generates are particularly iconic. I’ve seen countless tutorials online offering how to do Isaac-like generation, but I was interested in how the original did it. To my suprise, most tutorials get it wrong. In this article I go over how the generation works, including a Javascript demo.

Though I did work through a [decompilation](https://gist.github.com/elucidater/6965659), and brush up on my rusty knowledge of Flash (I wrote my own actionscript decompiler back in the day), I was also very fortunate that ** Florian Himsl**, the developer of Isaac, and

**, one of the key developers of Rebirth, were both happy to answer my questions. In fact, Florian has recently made**

[Simon Parzer](https://twitter.com/simonparzer)[a video describing the algorithm](https://www.youtube.com/watch?v=1-HIA6-LBJc). Check out

[his whole channel](https://www.youtube.com/c/GameSquid/videos)for development details on his latest game, Squid Invaders.

Given his write up, this article is somewhat redundant, but if you want the gory details, press on.

## The Core Algorithm

Isaac is heavily inspired by the 2d zelda games, and generates maps similar to their dungeons.

![](../../assets/10087eaad8d37bba.png)

It’s a bunch of square rooms that connect adjacently to each other. Several rooms are special – there’s always a shop ![](../../assets/882898d8a4981bb6.png)

![](../../assets/d8c9c1e47a59b2da.png)

![](../../assets/c354aeaf03411971.png)

![](../../assets/262528414bb7828e.png)


The game itself is a linear progression of such levels, typically two per “chapter”. The maps get slightly larger for later levels, and the contents of rooms change, but the layout algorithm is essentially the same every time.

The first version of Isaac was developed in under 3 months, so Himsl had to be incredibly efficient with his time. The key design is elegantly simple. First, a floorplan is generated. Then some rooms are designated as special rooms. Then the interior of each room is picked from an appropriate pool.

### Floorplan

Isaac is generated on a 9×8 grid. For convenience, the cells are numbered numerically, with the units digit indicating the x position and the tens digit indicating the y postion. This means you can move up, down, left, and right just by adding +10, -10, +1 and -1. The cells with an x position of 0 are unused (always empty), which means that most of the code doesn’t need worry about the boundaries of the map. So the top left cell of the map is 01 and the bottom right cell is 79.

The floorplan just decides which cells will contain rooms – the contents of the room is decided later.

First, the number of rooms is determined by formula `random(2) + 5 + level * 2.6`

. I.e. levels start with 7 or 8 rooms, and increase by 2 or 3 each time.

The game then places the starting room, cell 35, on a queue. It then loops over the queue. For each cell in the queue, it loops over the 4 cardinal directions and does the following:

- Determine the neighbour cell by adding +10/-10/+1/-1 to the currency cell.
- If the neighbour cell is already occupied, give up
- If the neighbour cell itself has more than one filled neighbour, give up.
- If we already have enough rooms, give up
- Random 50% chance, give up
- Otherwise, mark the neighbour cell as having a room in it, and add it to the queue.

If a cell doesn’t add a room to any of its neighbours, it’s a dead end, and it can be added to a list of end rooms for use later.

In the case of maps needing more than 16 rooms, the starting room is reseeded into the queue periodically to encourage more growth.

As the above starts with a single room, and repeatedly expands outwards, it’s essentially a breadth first exploration. The restriction that it won’t add a room which already has 2 neighbours keeps the rooms in separate corridors that never loop around.

The floorplan is then checked for consistency. It must have the right number of rooms, and the boss room cannot be adjacent to starting room. Otherwise, we retry from the start.

### Special Rooms

Boss rooms are placed by reading the last item from the end rooms list. Because of the outward growth, this is always one of the rooms furthest from the start area.

Then, the Secret Room is placed. These are added to the floorplan, and one of the few exceptions to rooms not being placed adjacent to multiple existing rooms. In fact, it prefers it. The generator randomly searches for an empty cell that is next to at least three rooms, and not next to any end rooms. If doesn’t find one after 300 attempts, it loosens the criteria a bit, and after 600 attempts it loosens it even futher. This procedure ensures that the secret room will always be placed, but generally they are wedged near intersections so they are next to a lot of rooms.

Nearly all other special rooms are placed at a random end room. Some rooms are guaranteed to spawn, while others have a small chance or criteria. For example, Sacrifice rooms appear 1 in 7 times, unless you are at full health, in which case they appear about 1 in 3 times.

### Normal Rooms

Adjacent rooms always have a door (or destructible wall) in the exact center and every room is designed to always be accessible from a four directions. Thus, there’s no special considerations required when choosing rooms – they will always work.

Rooms are randomly picked from a pool. Rooms include both the layout (pits, fires, boulders etc) and the monsters. Both are subject to random variations like champion monsters, tinted rocks, and red fireplaces.

For normal rooms, there are 3 pools of rooms – easy, medium and hard. The first stage in a given chapter draws easy and medium rooms, and the second stage from medium and hard. The first chapter, the Basement, has 174 normals rooms in the pools. The “alternative chapters” such as the Cellar which can replace the Basement randomly, have a slightly different set of rooms.

### Curse of the Labyrinth

One of the most interesting extras in the code is double sized maps. These occur randomly, and also for several of the games challenge modes. Aside from the obvious duplication of special rooms and two adjacent boss rooms, it has lots of small details too:

- 80% more normal rooms (max 45)
- Only use the 6 furthest away end rooms for special rooms
- It pulls from easy, medium, and hard room pools.
- Randomly adds extra normal rooms to the floorplan with similar placement logic to Secret rooms.

## Demo

I’ve put together a simplified example of the generator in javascript for you to play with. The full code can be found [here](https://www.boristhebrave.com/permanent/20/09/isaac_gen/gen.js).

## Rebirth

![](../../assets/0147f48e36c71363.jpg)

Binding of Isaac: Rebirth is a remake of the original Binding of Isaac by [Nicalis](https://en.wikipedia.org/wiki/Nicalis) who were known at the time for their [VVVVVV](https://www.nicalis.com/games/vvvvvv) and [Cave Story](https://www.nicalis.com/games/cavestory+) ports. It was ported to C++ and all the sound and graphics redone. Over the years, it’s recieved a number of DLCs on top of the original’s already impressive selection of items and enemies.

Though Rebirth has a lot of fun new features, the main contribution to the level generation is adding larger, irregularly shaped rooms.

![](../../assets/6fed41cab0016664.png)

With the full set of DLC (Afterbirth+ at time of writing), there’s 11 large rooms: 2×2, 2×1, L-shaped, and narrow corridors, in various rotations.

![](../../assets/d596410b1ef9593e.png)

This was implemented by Simon Parzer as a careful modification of Himsl’s original code.

Instead of looping over the cardinal directions, it loops over all exits of a room instead. There can be up to 8, on a 2×2 room.

When it comes to inserting a room, it randomly tries to use a big room instead. The neighbour check still only applies to the first cell, the one by the door, but it does check that there is empty space for the rest of the room. That means that big rooms can cause some loops in the level. Commonly two large rooms are generated side by side, complete with a pair of doors leading between them.

If there’s no space for the room, another candidate is tried. When large rooms are successfully inserted, there’s a 95% they are removed from the pool.

Even more code was needed to handle large boss rooms. Recall that boss rooms are always placed as far as possible from the starting room. If a large room is desired, the generator replaces the designated single room. As boss rooms are always dead ends, the replacement is checked that it not adjacent to any extra rooms. Sometimes the replacement is still not possible, so all the endpoints at max distance from the start room are tried before giving up entirely.

When it comes to selection rooms, the adjacent rooms on the floorplan are now considered, and some rooms are only picked if it determines that no doors are needed.

![](../../assets/fdd948488fe71e4a.jpg)

## Conclusion

Isaac’s generator is not the fanciest I’ve seen, but it works incredibly well for so little code. That’s probably why it’s such a popular target for emulation. The simplicity lends itself to tweaks and extensions, as seen in Rebirth. Incredible work.

You’ll also notice that this game continues the trend I’ve observed where the floorplan is generated separately from the details of the room. I’ve noted in my [Diablo 1](https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/) and [Enter the Gungeon](https://www.boristhebrave.com/2019/07/28/dungeon-generation-in-enter-the-gungeon/) articles why this can be so powerful.

I didn’t spot a great deal of interesting details while decompiling this one. The best I can report is that the location of the reward room is located in a variable called “boner” – short for Bonus Room apparently. There’s also sorts of minutiae of how different items have subtle side effects, but I’ll leave that for the [data miners](https://bindingofisaacrebirth.gamepedia.com/Dataminer#Trivia).

From here, why not check out Himsl’s entire youtube series on the [inner functioning of the game](https://www.youtube.com/playlist?list=PLm_aCwRGMyAdCkytm9sp2-X7jfEU9ccXm), or heck, just go play Isaac and see the levels for yourself. I hear Repentance, the latest DLC, will be out this year. And I can recommend master designer Edmund McMillen’s other games too (particularly Super Meat Boy).

Hi there!

Nice article! I am trying to implement sort of procedural dungeon generation for my prototype, and this really helped.

Thanks!