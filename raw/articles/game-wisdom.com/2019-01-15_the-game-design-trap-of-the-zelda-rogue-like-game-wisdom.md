---
title: The Game Design Trap of the "Zelda Rogue-Like" - Game Wisdom
url: https://game-wisdom.com/critical/zelda-rogue
author: Josh Bycer
published: '2019-01-15'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

Procedural and random generation are the cornerstones of rogue-like design, and we have seen many games push these elements further than they have ever been. This past year with *Dead Cells*, and games like *The Binding of Isaac*, *Spelunky*, and of course *Dwarf Fortress*, all provide replayability thanks to those elements.

One game design trap I see is developers trying to build a “Zelda Rogue-Like” experience, and while this may sound like the next evolution of procedural design, it just doesn’t work from a game design perspective.


## Procedural vs. Randomized:

As always, let’s quickly define the difference between procedural and randomly generated content. Randomized content refers to set elements that are shuffled around in a level. Enemy positions in Dead Cells, or what treasures appear in The Binding of Isaac are examples of this.

Procedural design is when the game creates something from scratch either before or during the running of the game. Loot generation in an ARPG and the level design in Spelunky are examples of this.

Rogue-likes typically feature both kinds of generation to define the experience, and it’s important to understand how much they impact the gameplay.

## The Degrees of Random:

Not all random or procedurally-generated elements are equal in the eyes of the player and their impact on the gamespace.

We’ve spoken about how just because your game has random (or even procedural) elements in it, doesn’t make it replayable. Many titles that make use of either form will still adhere to a specific progression curve. Survival games are a huge example of this: no matter how much the environment is generated, the player still has to gather resources in a specific order — see Minecraft as an example.

Without having a better term to use, we can say that there are hard and soft elements that can be randomized or procedurally created in a game. A soft element is something that does not impact the gameplay or progression loop of a title: Where enemies spawn, basic environments, biome positions.

A hard element does impact the player’s ability to play the game and change what they can and cannot do at one time: What upgrades spawn, new items, biome types, enemy types, new resources, etc.

The important factor is that what the player is doing in the game must be effected in order for playthroughs to feel different to them. This is why loot in ARPG design works so well: as every new piece of gear changes the player’s build.

Normally, just changing the map around doesn’t lead to different experiences, as the player is still doing the same thing. The reason why Spelunky holds up so well is that even though the core gameplay doesn’t change, by giving the player new levels to go through, it keeps creating different tests of the player’s ability.

And that takes me to this idea of a Zelda Rogue-Like and the inherent problems with it.

## The Legend of Rogue:

*The Legend of Zelda* franchise is considered to be one of the best action-adventure series in the industry. Similar to the Souls franchise, every aspect of Zelda is hard-coded to push and guide the player through to the very end. Even *Breath of the Wild* being the most open-ended take on Zelda still introduced progression points in the form of the guardians, the master sword, etc.

Being able to take that handcrafted design and progression and put it in a procedurally-designed world sounds like a holy grail form of gameplay. Unfortunately there are several design flaws with this concept.

When we look at the Zelda gameplay loop, the player is essentially doing two things — exploring to find points of interest (dungeons, items, etc), and performing the task of said point of interest. The latter is more interesting and more important compared to the former.

The world of a Zelda game is always inherently designed to force progression — this simply means that the environmental design will guide the player to what they need to do. It’s the same concept as what we see in Soulsborne titles, and how placing harder enemies in an area creates a metaphorical roadblock to tell the player to come back later.

By trying to randomize the world ends up making things less interesting and more frustrating. Because the world is always going to be different, it means that from a design standpoint, you have to make the environmental design less complicated in order to accommodate the shuffled nature.

Outside of the points of interest, the world itself will always be less interesting to go through compared to a hard-coded game.

Not only that, but it creates a situation where the player could find points of interest and have no idea if they’re supposed to be there or not. The beauty of Zelda’s formula was that the dungeons and points of interest always build on top of the previous. This makes the progression curve more interesting and allows the designers to keep raising the stakes with each new dungeon.

Breath of the Wild went in a different direction by making every dungeon beatable with your basic load-out and balancing the areas based on how easy or hard it was to reach them.

Another problem is that because the upgrades are the only elements that change the game experience, simply shuffling or procedurally generating the environment is not changing how someone plays the game. A popular design that developers use is generating the overworld map while still making the points of interest hard-coded; see the game *Darkwood* as an example. The issue is that once again, changing the environment around is not impacting how someone plays the game.

If the player always needs item X, Y, and Z in order to win, then all you’re doing by shuffling the environment is changing the amount of time needed to get those items. As we already mentioned, you cannot develop unique or differing challenges in the overworld, as you are unable to know what order the player is getting their upgrades. What’s worse is if the points of interest are set up to use items from the other ones, but the player has no idea of knowing that when they first arrive.

This is why the better rogue-likes focus on a core gameplay loop that then grows out and changes based on what is given to the player. Both the *Binding of Isaac* and *Dead Cells* have their runs changed dramatically based on what items show up, not what environments they go through. While *Spelunky* sticks with a basic gameplay loop, but mixes up what the player is doing via the level generation.

The key element of any successful rogue-like is how many ways you can provide the player with a different experience. When it comes to Zelda-rogues, every one that I’ve played makes me wish that the environment was fixed and the points of interest were… well, more interesting.

## A White Whale of Game Design:

You would think that creating a procedural-generated take on the Legend of Zelda format would be the perfect game, but I’ve yet to see someone fully accomplish this task (and before anyone says it, the Legend of Zelda randomizers don’t count). The amount of work it would take to get these gameplay loops in sync is beyond most design teams and a modest budget.

The point of a good rogue-like is never about getting to the end, but all the varying ways the middle can turn out differently. The other extreme where this could work would be procedurally generating a gamespace around different pools of items/points of interest, but again, that would require a lot of work.

Speaking to a developer on the Game-Wisdom discord, we chatted privately about this kind of design. The design is definitely possible, but would require a greater focus on the procedural algorithm to create areas that would be solvable based on what items or abilities would drop in that respective seed.

To end this post: **Can you think of other dream concepts of game design that just don’t work in reality?**