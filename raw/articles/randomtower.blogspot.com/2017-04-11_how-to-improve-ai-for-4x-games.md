---
title: How to improve AI for 4x games
url: https://randomtower.blogspot.com/2017/04/how-to-improve-ai-for-4x-games.html
author: Pubblicato da Marte
published: '2017-04-11'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

This time I'm here to share with you a really nice article

[9 Ways that 4X AIs disappoint us](https://remnantsoftheprecursors.com/2017/03/01/9-ways-that-4x-ais-disappoint-us/)from the creator of

[Remnant of the Precursors](https://remnantsoftheprecursors.com/)a remake of the original Master of Orion with Java and some improvement on the interface

![]() |

In the article in particular the following points are really important for me:

**AI don't know how to play the game**

I've made some prototype on that side and for sure, if you design a game where the player vs player component is crucial, this point is not so central. But for games like any kind of strategy game there is a need of specify and make understandable for the AI the basic actions. I think is better to have some kind of atomic actions (move an unit, evolve your character, attack another unit) and use them.. from AIs and from players. So for example you can specify a basic action like move and use it when player decide to move using keyboard or also from AI because it's better to move an unit using a simple influence map (take a look to my experiment,

[Wargame](https://randomtower.blogspot.it/2015/11/wargame-simple-ai-experiment.html), about that!


**Personality**

Players want a challenge on most of the game and a personalized challenge is the top. But ofter AIs are the same. Even AAA titles can have the same problem! For example in Starcraft 2, if you player against an AI does not matter if you choose zerg, protoss or terran. In the end, the strategy will be always the same: create a large enough group of unit as fast as possible and attack you.

What if an AI can use different strategies based on situation and personal attitudes ? It's something related to game like Civilization V, where opponent AIs can have different attitudes on different actions.

Using the example above, personality A prefer attack move, instead personality B prefer to scout enemy units, retreat and form a much larger force to attack you. This could be end in a really nice match, no ?

What do you think about different way to personalizes AIs ?

## No comments:

## Post a Comment