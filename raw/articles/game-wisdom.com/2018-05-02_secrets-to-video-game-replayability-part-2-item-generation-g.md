---
title: 'Secrets to Video Game Replayability Part 2: Item Generation - Game Wisdom'
url: https://game-wisdom.com/critical/replayability-game-design-item-generation
author: Josh Bycer
published: '2018-05-02'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

Continuing our talk [about replayability in game design](http://wp.me/p2OOw3-5Bn), we’re going to talk about item generation. The ability to either create new items, or use set items randomly, can do a lot to create variance and replayability. Just like biomes however, there is more to understand than just having the game randomly drop things in the player’s lap.


## The Item Pool:

Before we talk about loot tables and their implications, I want to focus on a simpler, but still vital system. For games that want to create huge swings with their items or gear, some developers opt for an item pool system.

The item pool refers to the game randomly giving the player set items from a massive pool. These items are hard coded in their design and typically appear at fixed locations or events in the game. Some major examples would be The Binding of Isaac, Enter the Gungeon and FTL.

As the player, you have a good idea as to what could show up, but you don’t know what you’re going to get. For games built around player skill, an item pool is typically used as there is less abstraction impacting things. A good Binding of Isaac player can make due with a bad draw if their skill can carry them.

When designing and balancing an item pool, there are several considerations to take into play. The first one is obvious: The larger the group of items means that there is a lesser chance of the player getting the same things. Because the game is not procedurally generating equipment, any game that goes with an item pool design must come with a large pool. The size is going to depend on how much you can impact the mechanics and the length of a play.

Balancing an item pool can be tough. Not every item can be an all powerful game winning option, but you want to avoid having legitimately amazing and horrible items. With the Binding of Isaac, there are items that are just amazing with no downsides, but they are only a handful compared to all the items in the game.

You need to go into balancing with the understanding that the player is never going to get everything in a single run. If you do your job right in terms of balance and item pool size, the chance of the player getting a game breaking build every time should be minimal.

That is also why you want to avoid having legitimately bad options: Items that no combination will ever work for the player. The beauty of these games is when crazy builds can come together through the combining of items, but they should still have value by themselves.

One of the problems that I had with Enter the Gungeon was the fact that so many guns were simply “joke weapons”, and the ones that were run winners were few and far between.

With that said, let’s move on to when games create the items during play.

## Loot Table Design:

A loot table is an essential part of any game where the design requires procedurally generated items to drop. The concept behind a loot table is building an algorithm that will generate an item based on hardcoded attributes defined by the developer. Typically, the loot table will start with the most general details and then work its way towards specific ones.

The loot table’s purpose is simple: To provide a way to generate an endless amount of items for the player to find. Unlike the item pool, the items generated via a table are not as deep in terms of what they do. Whatever “item type” the table chooses typically has the most impact on how the item will impact the gameplay. This is important, because it would be easy to throw all balance out the window if the game could just generate new mechanics and modifiers to attach to the items.

Loot tables are more popular in RPG-styled games, where there is abstraction at the heart of progress. Loot tables are an essential part of the ARPG gameplay loop of Fight – Get Loot – Grow Stronger, and it’s easy to see why.

When loot tables work, they can keep people coming back for more, and as long as you don’t run out of numbers, the experience can be extended indefinitely. However, from our talk about biomes, just having randomized elements is not enough to produce replayability.

## Slot Machine Power:

The first big point about loot table design is that you are throwing out any chance of accurately knowing the player’s strength at any given point of the game. That means you need to be careful when balancing enemy encounters, as you’ll have some players who have gotten lucky with good generation and some who didn’t.

This is why contemporary developers make use of a gear rating system as an abstract measurement of the gear’s power. That affords a little more leeway when it comes to defining enemy attributes and provides a rough idea of how strong the player is.

Another point is that with so much gear being generated while playing, you need to make it easy for the player to determine if they should replace what they’re wearing. I can’t tell you the number of times when I play ARPGS that I just stop because I can’t decide what gear to wear. Diablo 3 did this by condensing all stats down into three categories: Power, Health, and Defense, for someone to look at.

But perhaps the biggest issue with loot tables compared to loot pools is that they have very little impact on the actual gameplay. No matter what game design we’re talking about, there will always come a point when the player is not changing anything they’re doing, and the only form of progress is numerical.

Swinging a sword that does 5 or 5 million points of damage doesn’t change the act of actually swinging it. Eventually, the push for higher numbers will no longer motivate the player. Like-wise, if the only thing you’re doing to the enemies is raising their attributes, then the player will not have anything new to fight on their endless progression.

One final point before we wrap up for this post, when we talk about a loot table, that doesn’t mean you’re just creating one for the entire game. Typically, developers will create multiple loot tables based on the character’s level that will scale the attributes up. This is important, because it helps to make sure that the player will continue to find gear comparative to their level and grow in power.

## Up Next: Finding Friends

For our next topic on replayability in game design, we’re going to focus on why multiplayer is not just a popular request, but a huge element for making a game replayable.