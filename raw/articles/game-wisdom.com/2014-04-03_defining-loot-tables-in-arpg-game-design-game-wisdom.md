---
title: Defining Loot Tables in ARPG Game Design - Game Wisdom
url: https://game-wisdom.com/critical/loot-tables-game-design
author: Josh Bycer
published: '2014-04-03'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

If you’ve read or listened to any critical examination of ARPG design, you should have heard the term “loot table” thrown around. A loot table both determines the probability and attributes of an item and is an important concept both for regular ARPG game design and understanding how game mechanics and systems work.


## The Item Roulette Wheel:

*(The following post explores the low level design of loot tables and there are several ways for this to be implemented. If any designers who have previous experience with designing loot tables would like to go over their procedure or basic philosophy, please leave a comment below.)*

For this post, we’re going to talk about loot tables briefly in games with set loot and then spend more time on randomly or procedurally generated loot.

Set loot means that every piece of equipment in the game is hard coded by the designer and meant to either drop from specific enemies or be found in chests and an example would be *Dark Souls*. The designers and programmers of the game first sat down and created a spreadsheet usually of every piece of equipment that could be found in the game. From generic swords to legendary items, they all get placed on the spreadsheet and are usually categorized by their rarity.

When the player kills an enemy or opens a chest, the game does a behind the scenes calculation to determine if an item should drop. In traditional set loot design, each enemy has their own loot table based on what items it could drop. For this post we’re going to use a scale of 1 to 100 to help explain the concepts of loot tables. Please note that any numbers mentioned in this post are abstracted and used for example purposes.

After the player kills a monster, the game picks a random number between 1 and 100. If the number is less than 40, then nothing drops, 41-60 a regular item drops, 61- 80 a magic item, 81-93 a rare item and finally 94-100 a legendary item. After the number has been determined, the game will go to the spreadsheet and choose a random item from the specific category to generate and give to the player.

With set loot design, the loot table stays condense as each enemy may only have the chance to drop one of two or three different items.

To give the player a better shot at rarer items, designers may make certain actions weighted towards specific qualities. For instance, let’s say that anytime a player finds and opens a treasure chest they are guaranteed a rare item.

To do that, the designer can simply skip the number generation and just have the game use a 93 so that it will just generate a rare item from the spreadsheet.

When a game talks about items or buffs that improve the chance at finding items, which is also an example of a weighted action. So if something gives you a +5 chance at finding a better item when the game rolls the number to determine the item drop, it will add +5 to the roll and therefore increase your chance at getting an item.

For a set loot design, loot tables don’t have to be that complex. However, when you’re designing something like *Diablo 3* or modern ARPGs, procedurally generated loot adds several wrinkles to the proceedings.

## Mixing Things up:

We can use the same principle of set loot design and rolling for items with procedurally generated loot. But there is a lot more work and calculations that need to be done when generating your own loot. Instead of hard coding all your loot on the loot table, you’ll need two loot tables. First, one that holds any and all possible items that can be dropped and another to hold the affixes or modifying variables that can affect an item.

The first table essentially holds the basic blueprint of an item like sword, shield, rare axe, etc. We then go one step further and for each item, there are stats that are either hard coded like attack damage, attack speed, etc, or they exist within a scale. So that a sword could spawn that does anywhere from five points of damage to ten points.

When you start generating rarer loot, beyond just deciding what type of item within the category is spawned, the game also determines what affixes to add. Affixes as mentioned are the passive modifiers and can mean just about anything that your imagination can come up with: Increase damage, movement speed, spawn flying monkeys upon strike, whatever.

These affixes are placed into their own table with usually scales associated to any numerical based affix. Some designers may group affixes based on rarity, so that the better ones will only show up on a rare item and so on. Putting it all together, the game has to make five calculations regarding loot: Does an item drop, what’s the rarity of the item, what type of item will drop, what affixes will be associated and what are the actual numerical variables for the affixes?

![Diablo 3 Game Design](../../assets/e9a178325682e6c1.jpg)


![Diablo 3 Game Design](../../assets/e9a178325682e6c1.jpg)

The completed item with all of its affixes and stats. This is the extent of what a player will see of loot generation most of the time.

Those calculations are happening in milliseconds every time the player kills a monster, opens a chest or some other event. Once you understand the basics of how a loot table is designed and functions, we can easily extrapolate that out for other designs and functionality.

For instance, *Diablo 3’s* “smart loot” system in which the player finds items related to their chosen character more often can easily be explained. Once the system decides whether or not to drop an item, it will check for what class the player is and then give related attributes and item types an added weight when the game is deciding the rest of the choices.

Progressively increasing the power curve of items is done simply by having multiple loot tables based on the level of the character and just switching to a higher table when the player reaches the respective level.

With Diablo 3’s legendary and set items, while they are hard coded in terms of having set affixes or abilities, they also featured random affixes that are attached, so that no two legendary items are 100% the same.

## Controlling the Dice Roll:

While this next topic is a bit big to talk about in this post, it’s important to understand both as a designer and as a player that a good loot table is about controlled randomization. In the sense that the player should not have any idea what loot they’re going to find only that they know when it’s going to happen. The anticipation is as important as the actual reveal of the item and this is a part of that “one more turn” feel to ARPGs.

Understanding how loot tables are designed and works is a great step in building your knowledge base on game design and low level thinking. The concept of building a foundation for procedurally generated loot can also be applied to other areas of designing a game like creating monsters for the player to fight.

As you can probably guess by now, creating a loot table is a lot of work both in the initial design and implementation. But good loot design hinges on having a well designed loot table and is important for understanding the basics of game design.