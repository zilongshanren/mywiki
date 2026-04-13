---
title: Breaking the RogueLike Wall - Roguelikes vs Rogue-lites - Game Wisdom
url: https://game-wisdom.com/critical/roguelikes-vs-rogue-lites
author: Josh Bycer
published: '2019-11-21'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

This decade has done a lot for the rogue-like genre among indie and mainstream developers. Building on the success of Spelunky and the Binding of Isaac, roguelikes, souls-likes, rogue-lites, and possibly more connotations have sprung up. The subgenre has become immensely popular with indie devs all trying to make the next big success, and it has caused a hotly debated discussion for every new game: what’s the difference between a rogue-like and a rogue-lite?

While some use this to troll, there is an actual game design discussion to be had here, and what we’re going to break down today.


## A Rogue’s Rogue

As always, let’s begin with a brief history. The rogue-like genre is named that in honor of the game Rogue, released in 1980, the first game to popularize the aspects that would go on to define roguelikes, despite there being older examples. With Rogue, players had to explore a dungeon to find a magical amulet, with the layouts, monster placements, and treasure location randomly generated. If the player dies, their progress is wiped, and they must restart from the top.

Rogue would go on to inspire the game Hack which in turn was re-released and updated as Nethack in 1987. Nethack is considered one of the finest roguelikes ever made, and is still being updated to this day.

Throughout the 90’s we saw more titles on the PC that were based off Nethack, as well as console titles with their own designs; such as the Shiren the Wanderer series. Despite that, there were titles like Toejam and Earl that despite not having any RPG elements to them, did show signs of rogue-like design.

The rogue-like genre had a dedicated niche of fans for over 20 years, but it wasn’t until this decade that we saw it burst onto the mainstream.

## The Rogue-like Arrival:

If you were to ask a modern fan today the game that got them into roguelikes, chances are they would namedrop one of the following games: The Binding of Isaac, FTL, or Spelunky. All three titles embodied the basic ideas of the classical rogue-like: procedurally generated game spaces, permadeath difficulty, and variance between runs.

There’s just one big difference that all of them share, none of them would be considered RPGs in the same sense as older roguelikes. Each game used the rogue-like formula, but applied it to a different genre. We could spend entire articles talking about each one of these games, and I’ve written about both Spelunky and the Binding of Isaac in my first book “20 Essential Games to Study” and they’ll be a part of my hopefully fourth book on design.

This is where we began to see the loosening of the term “rogue-like” among developers, and being inspired to take those elements into other genres. At this point, I’ve forgotten more roguelikes than most people have played this decade. And with that, the idea of a rogue-like began to get muddy among fans and consumers. There are still people who say that none of the games released this decade should be called a rogue-like because they’re not RPG in nature.

In turn, this created the other term “rogue-lite,” whose definition as per this article is hotly debated. What makes this a difficult topic is that many people will immediately designate a title a rogue-like or a rogue-lite without digging into it, and many developers have purposely tagged or defined their game as either genre to try and get people interested in them.

But it’s finally time to earn some internet hate and make an official definition for these terms.

## What’s a Rogue-Like?

A Rogue-Like by my definition is a game with randomly or procedurally generated game spaces, hardcore (or semi-hardcore difficulty) and able to create a lot of variance between runs. While that part is nothing new to fans of the genre, there is one other factor that I feel is critical for a game to be called a rogue-like — the game’s focus and gameplay loop is on the runs and not on reaching the end.

Obviously, every rogue-like (and of course every game) has an endpoint for the player to reach, but roguelikes are not about reaching it, but seeing what happens on the next run. There’s a reason why roguelikes typically give players a score at the end of a run so that they have something to compare the next one too.

The best roguelikes are designed around variance as opposed to hard elements. Getting the proc gen (procedural generation) correct is beyond the scope of this piece, but it’s required to create the variance needed to make each run play differently.

Persistence elements are typically not the focus of a rogue-like. The only exception is using persistence to add more to the proc gen on future runs, such as in the Binding of Isaac, or new ships in FTL. The player is always focused on the run at hand and there should not be any carryover from one run to the next.

With that said, let’s turn our attention to the rogue-lite genre.

## What’s a Rogue-Lite

Rogue-lite are typically designed around random or procedurally generated spaces with the same concept of hardcore or semi-hardcore difficulty, but the focus of playing them is reaching the end and not on the run itself.

Unlike roguelikes, rogue-lites have a heavy focus on persistence and carryover between runs. In fact, a key difference between a rogue-like and a rogue-lite is that you typically are not able to beat a rogue-lite with your early runs.

That last point needs to be clarified, as you’re not going to be beating a rogue-like on your early runs either. The differing factor is that a rogue-like is designed so that it is possible to beat a run depending on the skill of the player. With a rogue-lite however, the abstraction and persistence elements prevent a player from winning until the abstraction matches the player’s skill.

Playing games like Rogue Legacy, Hades, among many others, I still need to grind the persistence systems, but not as much compared to someone with lesser skill than I. With rogue-lites, given enough time any player should be able to win once the persistence elements are stacked in their favor.

Unlike roguelikes, rogue-lites have a finite end for the player to reach and there isn’t enough variance between the runs to keep someone invested after they reach it. Despite having procedurally generated environments, the basic run through in each rogue-lite does not change or provide variance on repeated plays. When playing a game like FTL, even though new ships unlock through play, the player is always starting back at 0 with each new run. The design of a rogue-lite will determine how much carry-over there is, but the player will typically lose common items and keep some kind of currency or persistent element.

The problem with replaying rogue-lites is that without the variance to generate different runs, the persistent systems will override any sense of challenge given enough time. As a case in point, when playing Hades in its current version, I could beat the game fully starting at 0 in about 4 runs of play thanks to my knowledge of the game and the persistent elements.

## What Does This All Mean?

At the start I said that this kind of question has been used to troll many developers, but it’s important to understand the focus for your design. If you’re trying to make a rogue-like, then you need to invest heavily into the proc gen of your game, and designing elements that can lead to variance. That means differing options for the player, just as having different enemies and events that can change the path of a run. If the player is having the same experience from one run to the next, then you are in trouble.

For a rogue-lite, you need to think about the progression curve that is carrying through from one run to the next. While you are focusing on replayabilty such as a rogue-like, it’s coming from a different direction. You want the player to feel like every run is moving the needle forward; whether it’s by inches or miles.

Both sub-genres have tremendous potential in terms of their gameplay loops, and the proof is in the number of games that have been released. The next time we should add more fuel to the fire and talk about the souls-like genre.

*For more talks about game design, be sure to check out my **discord channel** now open to everyone.*