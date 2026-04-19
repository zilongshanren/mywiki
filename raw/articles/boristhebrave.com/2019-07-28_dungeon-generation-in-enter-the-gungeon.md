---
title: Dungeon Generation in Enter The Gungeon
url: https://www.boristhebrave.com/2019/07/28/dungeon-generation-in-enter-the-gungeon/
author: Boris
published: '2019-07-28'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve been playing a lot of [Enter The Gungeon](https://store.steampowered.com/app/311690/Enter_the_Gungeon/) recently. It’s a great, brutally hard, twin stick bullet hell that reminded me a lot of [Binding of Isaac](https://store.steampowered.com/app/113200/The_Binding_of_Isaac/). But as I’ve been playing it more and more, I realized that the dungeon design actually shows some subtle genius.

![](../../assets/9f6063c354f7865a.jpeg)

There are many procedural generators out there that produce sensible level layouts that manage pacing and rewards correctly, and there are other generators out there that provide levels that include loops and compact layouts. But it’s hard to find both in a single game. Really, the only other game I’ve heard attempting this is [Unexplored](https://store.steampowered.com/app/506870/Unexplored/).

So, naturally, I broke out the decompiler to reveal all of *Gungeon*‘s secrets to me. I’ll share with you what I found.

On the face of it, *Gungeon*‘s levels look rather straightforward. Here’s a typical map.

![](../../assets/ceb1626c54f787a9.png)

The player starts at the entrance ![](../../assets/4ad1757c6c5288e5.png)

![](../../assets/6904c21490026e98.png)

![](../../assets/df346be1908c1a9d.png)

![](../../assets/2d814c96e9a484ae.png)

![](../../assets/81763b77a86d81ba.png)


So far this seems unremarkable. You can find a lot of level generators online that jam together a bunch of random rooms with connections between them.

What’s special becomes apparent as you play. The levels… just feel a bit more planned than mere chance would indicate. The boss room is always a reasonable distance from the start. Rooms with enemies are always reasonably spaced with breather rooms, shops and hubs. And most of all, many of the chests are hidden behind one way loops.

![](../../assets/1a4c8ba5f7ae9c09.png)

That red line is a one way corridor. If you want to get to the room with a chest in, you have to go the long way around. The majority of chests in the game either are at the end of a one way loop, or deep enough into the level to force you to fight many rooms just for that chest. No risk – no reward.

The secret to this pacing is that general layouts have been carefully pre-authored. Here’s the layout that was used to generate the above.

Normal rooms are randomly picked rooms with enemies, hub rooms are larger rooms with more exits. Reward and boss should be self-explanatory. Not shown are “connector” rooms, which are enemyless rooms, often with a environmental hazard. The other rooms are either prespecified, or drawn from a specific table of rooms.

There’s a handful of these layouts, called flows, per stage in *Gungeon*. The Hollow has the fewest with 4, while the Gungeon Proper has the most at 8. They’re not generic – each is designed around a specific feature that you can notice with experienced play. This might be a gigantic loop, or an important multi way fork, or having to travel through the shop to get to the end. They’re so noticeable, that speedrunners eventually spotted the differences and [created charts ](https://www.speedrun.com/Enter_the_Gungeon/guide/1ijr7)indicating how to find the boss as fast as possible. I’ve made a full list of layouts to download [here](http://boristhebrave.com/content/2019/07/gungeon_flows.zip).

You may have spotted that the flow diagram and the map don’t actually correspond perfectly. There’s an extra room directly below the shopkeeper room that doesn’t correspond, and there’s these weird corridor rooms ![](../../assets/f8fb221a586fe4b3.png)


The process starts with a randomly picked flow file, like the one drawn above. It’s a [graph data structure](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)), meaning it stores the relationships between rooms, but nothing about their positioning. Each room includes metadata about what type of room it is, and what connections it should have. The connections are actually directed – each flow chart starts from a root node, and then forms a tree of children nodes. Then extra connections break the tree structure to add loops. I think this is mainly a quirk of how the game was developed, but it is handy for some of the map analysis routines that all loops have a well defined beginning and end.

#### Flow Transformation

The flow file is transformed in a few different ways. Firstly, some specified rooms are replaced with lines of rooms of random length. This feature is only used on the later, larger, stages. Similarly, some sections of the flow file have alternate paths, and one of them is selected at random. This feature is only used twice.

Then, some extra nodes are “injected”. This feature is quite flexible and is is used for all sorts of purposes.

Each injection contains data specifying what sort of thing should be inserted, where it should be inserted, probability of spawning, and any pre-conditions that must be met (such as having a [master round](https://enterthegungeon.gamepedia.com/Master_Round), high [curse](https://enterthegungeon.gamepedia.com/Curse), or having not yet rescued a character). For example, secret rooms usually spawn at dead ends, but have a 1/5 chance of being attached to any room. They have a 90% chance of appearing, and have no pre-requisites.

Nearly every special room in the game is specified with node injection, including vendors (other than main shop), jails, fireplace and elevator rooms.

![](../../assets/3dc1415bb8d84488.png)

It’s also at this point that the generator picks a specific room for each node. This is mostly based on what stage you are on and what type of room is wanted. There’s a huge list of rooms – nearly 300 for the first stage, but it’ll avoid picking the same room twice.

Nodes of type “connector” work differently. They have their rooms picked later, while layout occurs. These are often long, thin rooms, so picking one with a sensible orientation is vital.

#### Composites

Once we’ve got the completed flow, it is broken down into “composites”. Each composite is either a single loop of rooms, or a set of connected, loopless rooms (i.e. a [tree](https://en.wikipedia.org/wiki/Tree_(graph_theory))). This is done by finding the smallest loop in the map, and cutting it out as a composite. This is repeated until no loops are left. The rest of the map is a bunch of disconnected trees, and connections between individual composites.

#### Composite Layout

Each composite is then laid out separately, in a separate map. They’ll get composed together later.

To lay out a composite, the first room is put an arbitrary spot. Then rooms are added to the layout one by one, by picking a pair of exits, one in the new room, and one in the layout. Exits are are pre-defined locations in the metadata for each room. The new room is then aligned so that its exit connects directly to the exit of the previous room. Then we repeat.

To be more specific, tree composites are laid out by walking the tree [depth first](https://en.wikipedia.org/wiki/Depth-first_search). The algorithm only picks pairs of exits that locate the new room without overlapping with what has been placed so far. Generally, the algorithm prefers to select exits far from already used exits. If layout isn’t possible, it will [backtrack](https://en.wikipedia.org/wiki/Backtracking) and regen the choice of room, up to 3 times.

Meanwhile, loop composites are laid out by adding entries from the loop, alternately at either end of a line. To begin with, exit pairs are picked randomly (with preference for opposing walls, west-east or north-south). Once the loop is half constructed, it starts to prefer exit pairs that bring the two unclosed ends of the loop closer together. When it has constructed all the rooms, it still needs to add one more connection between the last two rooms. It picks another pair of exits. If possible, it constructs a small rectangular room between those exits. Otherwise it pathfinds between the exits, and makes a “room” that is just a narrow corridor. The corridor must be between 4 and 30 units long (50 in the mines).

#### Final Assembly

At this point small individual pieces of the dungeon have been connected to each other, but the composites themselves still needed to be put together into the full map.

![](../../assets/817aeeeb4cf680a4.png)

As you can see, the remaining connections don’t really leave much choice in this case. But there can be harder cases than before. The map is walked over, starting with the room with the most connections. As before, for each connection to make, a pair of exits are chosen. If the two rooms are in disconnected parts of the map, then the two map pieces are aligned next to each other to give a short path. Otherwise, pathfinding is used to construct a route.

And that’s it for level layout. The rest is picking enemies and decorations for the rooms, which is a different matter altogether.

## Final thoughts

It seems designing a procedural generator that gave a satisfactory play experience was a key goal of the developers. They obviously went through a lot of iterations to get it right – there is loads of generation code that appears to be unused as they tweaked the formula to get it perfect.

One particular trick is that they generate the parts of the map that are hardest / most important first. The generator emphasizes making tight loops and short corridors for the most central parts of the level, and then tries to fit everything else around that.

As with my [Diablo 1 writeup](https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/), I’m struck by how effective it is to generate part of the dungeon in a more abstract form, in this case, a graph with no position information, and only later make everything more concrete. The “injection” customization would just not be possible if we went straight to dealing with a tile based map, and it allows the control of pacing and scope to be easily separated from details of positioning and details.

I also admire how extensible the whole system is. Unity encourages a very [data-driven](https://en.wikipedia.org/wiki/Data-driven_programming) approach. Adding a new room, layout, or even special behaviour are all doable by adding additional objects into the appropriate tables. This must have been a huge boon as Dodge Roll cranked out several free DLCs, and no doubt encourages [mods](https://modthegungeon.eu/).

![](../../assets/b698c923fa519c42.png)

## Bonus stuff

Studying this generation was my first chance to observe how a professional unity game is constructed. The devs at Dodge Roll did a great job writing this code. It’s very readable, and in some places, quite funny – it seems their fondness for punny names extends to the code itself. Some of my favourites include:

- The fluid engine in the game called
`DeadlyDeadlyGoopManager`

- The dungeon generation code is called
`Dungeonator`

- The various stages are called
`CASTLEGEON/GUNGEON/MINEGEON/CATACOMBGEON`

etc. I have to wonder if the devs were inspired by Diablo 1, which has a very similar layout. - Literally every room is named, usually something punny (or after Joe, the presumably egotistic artist on team)

I also noticed originally there were plans for space, jungle, wild west and “belly” themed stages. Alas ’twas not to be. Dodge Roll have decided their work on *Gungeon* [is done](https://www.pcgamesinsider.biz/indie-interview/68862/why-dodge-roll-has-decided-to-part-ways-with-enter-the-gungeon/). I look forward to playing their next game, and hope they put just as much love and thought into it.

This is a super great break-down. You are spot on in our intentions, and how much emphasis we put on things like loops, and overall feel of the layouts. Our goal was to approximate a Zelda dungeon with each generation. This was a metric butt-load of work, and something few people consciously notice. We like to believe that it adds a lot to the pacing and feel, so even if the player isn’t thinking about it, the layout’s just feel

right.Hoping to one day make it even better, if the right project comes along.For the record Joe only put his name in the room filenames to differentiate them from the others made (by the designer, Dave), so that they could get checked over. It was never the plan for Joe to make so many of the rooms, but plans are ephemeral in game development, and especially in the Gungeon.

Interesting read! Thanks for dissecting 🙂

I’m making my own rouge-like game and this really helpful and a good read!

thank you very much