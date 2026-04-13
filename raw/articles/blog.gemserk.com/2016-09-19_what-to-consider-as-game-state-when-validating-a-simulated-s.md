---
title: What to consider as game state when validating a simulated synchronization.
url: https://blog.gemserk.com/2016/09/19/what-to-consider-as-game-state-when-validating-a-simulated-synchronization/
published: '2016-09-19'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

One really important thing when performing a synchronized simulation is having a way to check if all clients have the same simulation state. In order to do that, it must be clear which parts of the game state are important for the synchronized simulation and which parts aren’t. Obviously, this depends a lot on the game.

The idea of this blog post is to talk briefly about what is normally an important value for a game, and what isn’t.

### What is not important for the game state

Let’s talk first about what is not important for your game. Even though it depends on the game, there are some common things that shouldn’t be considered as part of the important game state.

These things are normally all the stuff that doesn’t affect the game outcome, in other words, all the stuff that could be removed from the game and the game will be the same. For example, the smoke particles coming out from a bonfire, or even the current playtime of fire sound effect.

Also, things that could be derived from important gamestate even though they could affect the outcome in some way. For example, the units health bar current fill percentage could be derived from the unit health, that value could be used by the game logic but since it is directly derived from other values, it is not considered important.

### What is important for the game state

All the things that could affect directly the game outcome are important for the game state. If you have a way to restore the game from a saved state, you have to be able to finish the game the same way each time you restore it.

For example, in a game like Doom, if you save and load you have to have the same health, armor, weapons and ammo, you should be in the same world position you were and enemies too, with same health, etc.

In Starcraft, what is important is your current vespene gas and your minerals since that decide what you can build or not, your current units with their health, your structures and their queued orders, the revealed map, etc. Things that are not so important include the blood in the ground when your units die (if you are playing Terran of course), your current units selection, the exact frame of a unit animation (unless the game depends on that to fire a skill).

If you are just saving the game state to be restored locally, you may want to store more stuff that you need since that shouldn’t matter. However, in the case of checking state synchronization between machines, having stuff that could differ and doesn’t affect the game outcome is not a good thing to have since you are not only wasting bandwidth but also risking the synchronization check.

### Next time

Currently I am working on a way to represent the game state of a game I am working on and I want to have both features, a way to check synchronization between machines as well as having a way to save and restore the game state. I hope to talk about the benefits and problems of those features in the next posts, as well as having a more detailed information on the concepts of this blog post too.

Even though this blog post was a bit basic, I hope you liked it. I just wanted to talk a bit about the challenges I am dealing with right now.