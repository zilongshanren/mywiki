---
title: How Modern Roguelikes are Becoming Accessible - Game Wisdom
url: https://game-wisdom.com/critical/modern-roguelikes-becoming-accessible
author: Josh Bycer
published: '2020-07-13'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

The last three years have seen multiple roguelikes being released to stellar reviews, and more importantly, being recognized among mainstream consumers. What we’ve seen is a new approach to both difficulty and playability that I want to talk about today.


**Progressive Difficulty**

The philosophy of progressive difficulty in roguelikes goes back to the concept of “ascension mode” coined by Slay the Spire. An ascension mode provides players with an ever-escalating set of difficulty modifiers that become available once the player wins at their current highest level.

Unlike traditional difficulty settings, progressive difficulty is not about “one size fits all” difficulty modifiers. Here, each level of difficulty will tweak an aspect of the game to make things more challenging. In Slay the Spire, while you do get levels that raise enemy attack values, you’ll also have a level that introduces “trash cards” to your deck, or changes how the shops operate.

Playing the game at the baseline setting should be capable for most players, with the progressive levels designed to take the game to its absolute hardest variant. There should be a monumental difference in terms of the challenge at level 0 vs. the game’s max.

The beauty of progressive difficulty is that it allows for the philosophy and implementation of player-controlled difficulty.

**Player Controlled Difficulty**

When I last spoke about [playability in game design](https://game-wisdom.com/analysis/pillars-of-playability-part-2-dynamic-difficulty), we discussed this idea of letting the player decide the difficulty of the game beyond just blanket settings. By putting the player in control over the difficulty, it allows developers to make their titles more approachable for new and existing fans.

We saw a similar concept with The Binding of Isaac that unlocked new challenges and situations the more someone managed to beat the game. There was Way of the Passive Fist that allowed for multiple tweaks of their gameplay to create different difficulties.

As we’ve talked about, the problem with blanket settings for the difficulty is that they don’t often get at what makes a game too easy or too difficult. It’s very easy to design a game to be at either end of the difficulty spectrum, but making something that is fair and *perceived to be fair* by the player is another matter.

The beauty of progressive difficulty provides players with the means of setting a limit for themselves, while still having goals to achieve. It also allows the developer to look at the difficulty of their game differently compared to games in the past. Again, you’re not choosing the different levels just in terms of raw stat changes, but figuring out what aspects of your game can be made harder or different, but still providing a game experience *that is beatable*.

As mentioned, this opens your game to a larger audience of players who might have been put off by the higher difficulty of older roguelikes. To reiterate, the base version of your game should be easy enough for most people to win once they’ve learned the rules. Progressive difficulty acts as both a gatekeeper to the harder modes and a mountain for expert players to climb.

With that said, I want to talk about one of my favorite examples of this kind of design.

**A Hellish Buffet of Difficulty**

Hades by Supergiant Games has been my favorite title from the company and one of my most anticipated games of 2020. Besides having three starting difficulties of easy, normal, and hellish, the game features one of my favorite forms of progressive-styled difficulty.

Every time you beat the game with a different weapon, you unlock rewards, or bounties, for that weapon. From then on, the game introduces the “pact of punishment” as a way of unlocking more rewards and making the game harder.

This works by having the player “raise the heat” of the play to different thresholds that will then unlock more rewards for beating the bosses (and the game). To raise the heat, players have to metaphorically choose the rope that they want to be hung with by selecting which difficulty modifiers to turn on for that run.

The modifiers will affect the game in different ways and have different heat boosters to go with them. You can do things such as turn on a timer for each part of the game, make traps do more damage, even require yourself to give up a precious buff before completing a biome. Some modifiers are hard enough as is, let alone when combined with the rest of the list. This is not new to Super Giant Games, as Bastion also featured a similar system of rewards and difficulty.

By letting the player choose how hard to make the game, it gives them more control over the playthrough beyond just static difficulty settings.

With all that said, the progressive difficulty does present a problem when it comes to balancing a game and its many options.

**Tightening the Gameplay**

Progressive difficulty is not the same as directly adding content to a title. As a designer, you are effectively “layering” on the difficulty of the base experience. This creates a problem when it comes to balancing games built on multiple builds or options — the higher the difficulty grows; the amount of viable choices shrinks.

Fun or weird builds that could work in a pinch lose their viability. Any time the game increases the stats of the enemies or weakens the player, it’s going to dramatically affect what the player can do.

Here’s an example: let’s say we have an attack that does 10 points of damage. The base health of an enemy is 20, meaning that the player can kill an enemy with two uses of that attack. Now, let’s raise the progressive level and increase enemy health by 15, that same enemy will now take four hits to kill and is now a lot harder to fight.

This is an issue I ran into with Monster Train. While I enjoyed the game for its variety of builds and options, the higher I go up its covenant system, the harder it is to make suboptimal builds work. For any game that gives the player random equipment or options, the RNG (random number generation) at play becomes stricter.

With both Slay the Spire and Monster Train, I’m at the point with their progressive difficulty that if I can’t create a suitable build within the first floor (or first couple of battles respectively), then I know my chances for victory are going to be next to zero.

For action-focused titles, higher progressive difficulty levels act like pushing yourself to the limit while lifting weights. Eventually, you’re going to hit the limit of your skill and won’t be able to make any more progress with the progressive difficulty. With Dead Cells, I found that as the game limited your ability to heal and recover, I could not get far into its mode due to my playstyle.

You may be thinking that the solution is to just rebalance options, but therein lies the problem with progressive difficulty. The very options that aren’t working at the higher difficulties are still very much viable at the base level. You could end up making things worse for players by presenting them with something powerful to pull the rug from out from under them later on.

Therefore it’s okay to introduce new systems or rules with your difficulty, but you need to be very mindful of changing stats. If the final level of your progressive difficulty is so difficult that there’s only a 10% chance of everything lining up for a win, then you may want to tone things down. And finally, we have an obvious point — always work from the bottom to the top when looking at balancing your levels. You don’t want to be balancing #15 and then come to the realization that it’s #8 that is causing the difficulty spikes.

**Opening the Doors**

Progressive Difficulty, along with persistent systems, is some of the more popular ways of opening up roguelikes to a larger audience. Not everyone is going to be able (or want) to play your game at the highest setting, but it allows your design to be more accommodating to a larger audience.

*For more thoughts on roguelike design and its implementation, be sure to check out my next book Game Design Deep Dive: Roguelikes coming at the end of this year, acknowledgments are **available over on my Patreon*

*If you enjoyed my post, consider joining the **Game-Wisdom discord channel** open to everyone.*