---
title: Random Thoughts on Randomization in Game Design. - Game Wisdom
url: https://game-wisdom.com/critical/random-thoughts-on-randomization-in-game-design
author: Josh Bycer
published: '2011-09-06'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

When it comes to game design, randomization is one of my favorite words. When used properly, it enhances a game’s replay-ability dramatically. Classic titles like X-Com and Diablo 2 make excellent use of randomization to keep gamers playing, and the rogue-like genre is famous for its use of randomization. Recent indie titles: Dungeons of Dredmor, Din’s Curse and Space Pirates And Zombies each use randomization and are examples of the pros and cons of it.

Before we talk about the pros and cons of randomization, it’s important to define the degrees of randomization that can be implemented in a game. The degrees are not ranked in terms of preference, but just the ways that a designer can have randomization.

**Low**: Just equipment placement and probability of finding them. Action RPGs usually have this degree of randomization. Note, you can still have important items in set locations and have common items and equipment randomized.

**Medium:** Enemy placement along with the low category. There are two ways of implementing this, first is with having “unique” enemies. In Diablo 2, there was a chance of running across an enemy who had a name, these enemies looked different from their cohorts and had a unique modifier such as: increase damage, fire resistance, etc, and the other way is randomizing enemy positions as well.

**High:** Everything in the last two categories, along with world randomization. Rogue-likes fit the bill here, but this category is not mutually exclusive to rogue-likes. Space Pirates And Zombies allows players to create a random Universe from the get-go. TBS games like Civilization also allow players a chance to play on a randomized world, or preset map conditions.

With that out of the way, let’s move on to the pros of randomization. First, is that randomization is a great way to have replay-ability in your game. You’ll never know what that treasure chest will have, or what is behind the next door, and that can be an excellent motivator to keep playing. The more elements that are randomized in the game, the longer the experience will stay fresh.

While talking to a friend about Rogue-likes he told me that to him, they were like a slot-machine. In a way he is right with that analogy, you never know if you’re going to get lucky and get all the equipment you need and blaze through the game, or if the odds are going to be stacked against you.

Randomization can also be used as a difficulty modifier, allowing the game to generate a smaller or easier world for newcomers, or a larger more challenging world for experts. This is something that Din’s Curse does well, as players can choose the levels of the enemies, how big the world is, among other factors.

With that said, there are some cons to randomization. Going back to the slot machine analogy, while the lure of a jackpot can be motivating, losing thirty times before you get there can be demoralizing. In Dungeons of Dredmor, playing the game at the hardest difficulty setting, it felt like 9 out of my 10 runs ended before I even got off the first floor due to unlucky enemy and equipment placement.

Depending on the degree of randomization, it’s very easy to generate maps that completely screw the player. Going back to Din’s Curse, there were plenty of times that the game spawns hordes of enemies at the entrance to the dungeon that overwhelmed me or having a boss appearing on the very first floor with the hardest modifiers attached to it. Din’s Curse also features modifiers to the world that makes things harder; getting stuck with the worse modifiers at the beginning can be a big hole for the player to crawl out of.

Next, is that when it comes to randomized levels, most often quality takes a hit. Creating a randomize level using functions and basic assets is easy, creating a level that not only looks aesthetically pleasing and is crafted well is another story.

The perfect example of this would be Demon’s Souls, while you could argue that randomized levels would have helped the game, no one can say that the levels weren’t carefully designed. Each level was developed with a specific challenge in mind to the point that each level had its own mood and style. From the vertigo inducing heights of stage 3-2, to the poison gauntlet of 5-2, you could tell that the designers went to great effort to design the levels.

The first poor example that I had with randomized levels was with Phantasy Star Online for the Dreamcast. In the game, every dungeon’s layout was randomized, but the game only had a few room assets per world. What this meant was that every floor had maybe 4 different room models and that’s it. The level design had a very “Frankenstein” feel, in the way that the level design felt like it was just stitched together from various elements. That is also something you want to avoid when creating randomized levels as there should be a sense of cohesion in how the world is set up. The first retail build for Dungeons of Dredmor had door assets show up where rooms were supposed to be, and it brought the quality down somewhat.

The second problem is that the more game mechanics you have in mind, the harder it will be to create a decent system. The reason is that, the more mechanics the player has access to, the more variables will have to be programmed and implemented into the engine. In Mine Craft, on each new game, the world is randomly generated for scratch and it works because the only interactions the player has is putting a block down, interacting with objects and attacking.

Let’s say that someone designs a randomized level for Deus Ex: Human Revolution, in order for that level to work, the engine must be able to create a randomized setting that must also allow for the variations in play-style, meaning it must have breakable walls, vents, areas to reach and terminals to hack. If it doesn’t have all these elements and have them presented in a way that allows progress, then players will become very frustrated if the game gives them a level with a solution that is impossible for their build.

To create a randomized system that works, it has to be built on top of a layer of linearity. What that means, is that for every random element, there must be something guaranteed. For example, in Dungeons of Dredmor, while the world is randomized each time, enemy types are limited for the most part, to specific floors. You will never see an enemy who appears on floor 5, on floor 1 and vice versa.

Same goes for Din’s Curse, on every floor no matter what; there will be a way up, along with a portal back to town. In terms of enemies, the enemies will progressively get stronger the further the player descends into the dungeon based on what level the player set as the starting level at world generation.

Going back to Mine Craft, while the world is completely randomized at creation, the same basic rules apply to each new world: better materials are found deeper underground, enemies spawn in darkness and the player has complete freedom of where to go. With these three constants, the player still experiences the world fresh each time due to the scale of the randomization.

For one of my game ideas I envisioned the game taking place in a randomized world. Where ever the player is placed, the world will be built in a sense around that position. Incredibly dangerous areas would be further away, while easier areas will be closer. The majority of the buildings will be randomized, while special buildings that act more like dungeons are linear in their design. This will allow players to experience the game differently each time, but still have a sense of progression that they can base their play through on.

A well designed randomization system can be the cherry on top for your game design, giving players added value. However, like all good mechanics, it must be properly designed and implemented.

Josh Bycer