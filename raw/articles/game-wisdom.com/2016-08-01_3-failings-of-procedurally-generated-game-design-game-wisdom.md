---
title: 3 Failings of Procedurally Generated Game Design - Game Wisdom
url: https://game-wisdom.com/critical/procedural-game-design
author: Josh Bycer
published: '2016-08-01'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

A major evolution of game development over the years would have to be the use of procedural generation. Instead of having a linear experience that is one-and-done, you can create something that always keeps the player guessing. Rogue-likes, survival and simulator games have been using procedural generation to extend their replayability.

When it works, you have a game with almost unlimited replayability. However, as with all elements of game design, it’s not perfect and can hurt as much as help a game if not properly balanced.


## What is Procedural Generation?

Procedural generation at its basic form is an evolution of random generation in games. Random generation is when a game does not present content in the same order every time. It can be as simple as what items drop during combat, to the order of level environments and more.

Random design is based on hard values with a degree of malleability; such as opening a treasure chest and getting one of X items. Given time, a player can see all the random elements of a game, as they are preset.

Procedural generation takes things a step further. Instead of just giving the game engine or AI a list of things to choose from, the designers create an algorithm or set of instructions for the AI to use. Here, the AI will create something from this set of instructions while using random and preset values. The algorithm is designed to give the AI’s creation some structure, and more importantly, make it something that the player can actually beat.

The most famous example and one I talked about before would be from Spelunky. Spelunky featured procedural generation to create a new level every time for the player. [Designer Derek Yu talked about the creation and rules of the algorithm before](http://makegames.tumblr.com/post/4061040007/the-full-spelunky-on-spelunky).

Here, the game took the preset rules implemented by the designer, preset environments and obstacles, and creates something entirely original with them.

The key point of procedural generation is that the designer never 100% knows what the AI will create. They’ll have a pretty good idea because they designed the algorithm, but never a perfect one.

Many games feature examples of both random and procedural generation, with different degrees of both. In Diablo 3, area design and structure was kept relatively the same (not counting the rifts), but featured random events and placement of elite enemies. Loot generation was procedurally built, with the AI working off of the loot tables devised to create unique magic and higher quality gear. Again, the loot tables define the ranges and possible variables for the AI to use when creating the gear.

The Binding of Isaac used preset rooms as the foundation for its procedural engine, which stitched the levels together using the already made rooms.

With all that said, I know the design of procedural generation can add a lot to game development, but it does have several major limitations that no game can escape.

## 1: Limited Foundation

In order for procedural generation to work, the player’s own interaction with the game must be kept basic. The reason is that the algorithm has to be designed to work around every mechanic and system the player has access to. The more mechanics or abilities in the player’s toolkit, the harder it will be to create something that makes use of all of it.

This is why many games with procedural generation build the complexity horizontally in terms of items and not on the player mechanics themselves. In Don’t Starve for example, the player’s means of interacting are by using items which is a linear process every time. The procedural play comes in with how the world is built using biomes and filled with enemies and interactables.

![Don't Starve Procedural](../../assets/17537ce3a4b92523.jpg)


![Don't Starve Procedural](../../assets/17537ce3a4b92523.jpg)

Game mechanics in procedurally generated titles have to be kept basic enough for the procedural elements

Because of the limited interaction, it does actually put a limit on replayability with a procedural design.

Since the player knows their exact limits and abilities, they have a pretty good idea as to how to play the game no matter what the AI throws at them. Of course, this will still take many hours of play and a skilled player, but there really isn’t “unlimited replayability.”

## 2: Can’t Process Uniqueness

The more abstract the move set of the player is, the harder (to the point of impossible) it is to create an algorithm around it. Spelunky worked so well, because the rules and design of a platformer are easy (relatively speaking) to process by an AI. Once you know the max jump length and height, you can give those restrictions to the AI to build the levels around.

However, when we start talking about unique mechanics, this is when any attempt at procedural design falls apart. You can’t program an AI to make interesting levels using the time mechanics of Braid for instance, or the portals of Portal 1 and 2.

An AI at this point cannot be programmed around lateral thinking like that. Someday this could change when we have emergent AI, but that’s still a long time coming for game development. Going back to point one, this is why so many procedurally generated games’ complexity are built into the environment and not on the player’s interaction.

![The Swapper procedural](../../assets/b2c982cbad73b5b5.jpg)


![The Swapper procedural](../../assets/b2c982cbad73b5b5.jpg)

The more unique your game mechanics are, the less likely the engine can generate a level to make full use of it

In a game like Rimworld, Clockwork Empires or Dwarf Fortress, you give generalized orders to your people who will then perform them based on the operation devised by the developer. Your means of interaction are locked to these orders.

Instead of adding in brand new systems or design, the developers can extrapolate out the base systems with new things to interact with: Giving more depth to the game, while not adding more control or systems to the player.

Minecraft is the other major example. The developers have added in tons of content from alpha to release, but not much that changes how the player interacts with things. The majority of content in the game is built off of the base foundation; keeping the player’s control the same throughout the experience.

You can tell me that your game has limitless environments and levels, but if I’m just doing the exact same thing every time, then all that is just window dressing.

## 3: Mass-Produced vs. Handcrafted

Another point and the biggie for a lot of people who don’t like procedurally generated content is the fact that procedurally generated content is always lacking behind handcrafted content.

A discerning eye can easily spot a procedurally generated level compared to a handcrafted one. Handcrafted levels by their very nature have a personality to them. There’s a reason why we still remember Mario world 1-1 after all this time. Handcrafted design allows the designer to create an experience exactly how they want it and test the player.

Anyone who has played games with procedurally generated levels can see how they’re usually filled with areas of dead space where nothing happens. In less quality games, the procedural engine can screw up and place objects in weird arrangements. You can have corridors that don’t lead anywhere, enemies stuck in walls, and the worst: A level that is literally unsolvable.

![Dark Souls 3 procedural](../../assets/5270673febb6e80d.jpg)


![Dark Souls 3 procedural](../../assets/5270673febb6e80d.jpg)

Handcrafted levels can have a sense of personality and place to them; something procedurally-generated levels lack

This is a huge far cry from games like the Souls series: Where Every. Single. Piece of environment was meticulously placed and designed. Returning to that point on personality, the Souls series has that in spades and is a crowning example of the advantage of handcrafted design.

Looking at how most games handle procedurally generated levels, despite the variety of possible designs, there’s always this sameness that you can see. In handcrafted levels its okay, because you have the personality and uniqueness of the design to keep you engaged. In procedurally generated levels, it starts to become very repetitive to play through.

There is one major exception to this and when procedurally generated levels are better than handcrafted. That is when we’re talking about games where the environment is built around affecting the player’s options in-game. Typically seen in tactical and strategy games, linear environments can lead to repetitive play. In XCOM 2, Firaxis designed each level to be built out of the AI procedurally generating environmental obstacles and details from basic templates.

This way, the player’s available options and tactics were always changing based on the level design they got; a huge improvement from XCOM EU and having preset maps. Another example would be the tactical game Invisible Inc: Where the stealth play was impacted by the environment generation.

## The Sky’s the Limit:

At this point, I’m sure you’re wondering what procedurally-generated games I enjoy, and there aren’t many. Besides Spelunky and the Binding of Isaac, I’ve liked the ARPGs from Soldak Entertainment for the complexity and replayability of their designs.

The big game that’s coming out by the time of this post would be No Man’s Sky. The game has been in development for a long time and the developers have been promising big things with the game.

From planet-side to space, the game will supposedly give a procedurally generated universe to explore.

If there’s any game that will either truly show the merits of procedurally-generated content or fail it the most, it will be No Man’s Sky. And while I don’t have much interest in playing it as of right now, I’m still keeping an eye on it to see where things will go with procedurally generated design.

**If you enjoyed this post, please consider donating to the Game-Wisdom Patreon campaign. Your donations can help to keep the site going and allow me to produce more great content. Follow me on Twitter @GWBycer, and you can find daily video content on the Game-Wisdom YouTube channel.**