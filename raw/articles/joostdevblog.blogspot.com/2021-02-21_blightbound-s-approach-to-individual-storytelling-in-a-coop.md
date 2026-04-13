---
title: Blightbound's approach to individual storytelling in a coop game
url: http://joostdevblog.blogspot.com/2021/02/individual-storytelling-in-coop-game.html
author: Joost van Dongen
published: '2021-02-21'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

An interesting design challenge during development of [Blightbound](https://www.blightbound.com/) was how to combine personal storytelling with coop gameplay. In Blightbound three players play together, but they might be at different spots in the stories of their respective characters. How to make room for storytelling without spoiling stories for other players who might not be there yet, and without making players wait for each other? Today I’d like to dissect the approach we’ve used to solve this problem.

*Before I continue, note that this blogpost will spoil some story moments. However, I’ve made sure to only take examples from early in each character’s story, so the videos in this post will only be a minor spoiler to the game.*

Blightbound is a coop dungeon crawler, but unlike games like Diablo it doesn’t have a linear campaign. Instead, the player repeatedly plays a number of dungeons while learning each character’s story and gathering loot and more characters. In that sense it’s structured more like the end-game of Diablo, or like a looter shooter.

![](../../assets/c647de3be7657f65.jpg)

*Blightbound is a 3 player game, with both online and local coop.*

Another important aspect of Blightbound is that it has a lot of heroes. Instead of maxing out one hero for dozens of hours, the player gets to unlock a bunch and is invited to try them all. We would like players to vary what character they play. For this reason we wanted to tell a lot of small stories, interweaved with gameplay, instead of telling one big story. Each character has their own little story they go through.

Each hero in Blightbound has an individual story that’s told through the dungeon runs with that character. When 3 players play together, they each play a different character so they’re supposed to get different stories. This is where the issues that I’m discussing today arise. Players shouldn’t see the stories that the other players are getting, because they might not have progressed to that point with that character yet (spoilers!), or might have seen that bit already. Also, Blightbound is a fast-paced game so we don’t want players waiting for each other’s cutscenes.

The solution we came up with is that the storytelling is entirely private. When one player gets a bit of story for their character, other players don’t notice this at all. They might even simultaneously be getting different stories for different characters!

Now how do we make that work without letting players wait for an invisible cutscene? The simplest solution is used a lot in Blightbound: dialogue while gameplay continues. The player gets served portraits, speech bubbles and voice acting while the gameplay continues. So there’s no need to stand still and watch a cutscene.

*Two examples of basic story beats during gameplay.*

This does introduce a problem: getting extensive dialogue during combat is going to be very distracting and the player likely won’t be able to follow the text while focussing on the fight. Luckily, we needed some pacing anyway. A dungeon that’s 15 minutes of constant combat is both too intense and boring. So we should introduce some quieter moments anyway, and we make dialogue happen during such moments as much as possible. This way players can keep exploring but also have the mindspace to digest the storytelling.

If the player keeps moving, who is that dialogue with then? Here we’ve tried to vary it as much as possible. The simplest ‘dialogues’ are inner monologues of the hero. In other cases there’s a dialogue with an an NPC who’s standing in the level. Here too the other players can’t see this non-player character. To avoid waiting, the player can just keep walking: the dialogue starts when interacting with the NPC, but after that the player can run away and the dialogue will continue.

*Gameplay continues during dialogues, so teammates don't have to wait for you.*

To spice things up, we’ve added a fun trick here. The player is playing with two others who are random other heroes. To make the dialogues more dynamic, these other heroes will actually respond to it. But 21 characters all responding to all the story moments of all 21 other characters is way too many combinations. So instead we’ve defined a bunch of standard responses that each character has unique versions of. These are referred to in the dialogue scripts and then inserted dynamically during gameplay.

We have a total of 11 types of such standard responses and each character has their own line for each type. This way the responses can fit their personality. For example, these three lines show how different characters fill in the symphathy response:

- "
*I feel your pain.*" - "
*You have the clan's sympathy.*" - "
*Would a moisturizing salve help?*" (lol wut)

![](../../assets/3e5a4f3aa9b6362d.gif)

*All eleven types of responses for one of the playable heroes.*

What we have so far is cool, but still rather basic: all storytelling is done through dialogues and monologues and that’s it. From there we’ve looked into how we could spice things up without adding pauses. We should also not introduce too much work: Blightbound has more than 100 such story moments so efficiency is important.

The first element that adds some variation is how story beats are triggered. In some cases it’s simple: enter an area that’s marked and the storytelling starts. Some story events can trigger in any such area, while others need to take place in specific dungeons since they’re linked to that setting.

The more interesting ones require some form of interaction. For example, the mage Korrus looks for vases to investigate, so you need to spot them and interact with them. Other characters see someone standing in the dungeon and need to interact with the character, or see a hallucination. When there’s a hallucination hanging in the level, it’s only visible to the player who’s story beat this is for. To their teammates, it’s just a regular spot in a dungeon. Again we’ve made sure that we only use short and simple interactions, so that your teammates don’t need to wait for you.

One of the more fun types of story events are elite enemies. Some heroes need to fight specific characters to progress their story. To make this work, we’ve made special elite versions of some enemies that only trigger as part of someone’s story. The party of 3 players fight the elite enemy together. The nice thing here is that to your teammates, it’s just another elite enemy with some special skills (we have plenty of those outside story moments as well), while to you this specific enemy is a story moment and triggers dialogue. So this is a coop battle that is also a single player story moment. Quit neat, I think!

*An example of a story beat in which we encounter an elite enemy.*

Unlocking new heroes to play is a big part of Blightbound’s progression system. Here too a goal was to add some variation. Many heroes are simply found and rescued from a dungeon, but some others can only be unlocked by paying the merchant, by making your village prosper, or by finishing the story of another character.

For the simplest case, where a hero is rescued from a dungeon, we again ran into the problem of this being a coop game. My teammate might already have saved the hero that I’m rescuing, how does that work? To solve this problem, we’ve introduced the concept of survivors. These are basic characters that you can’t play. When you rescue a survivor, you get a little prosperity bonus to your village and that’s it. Now whenever one player is unlocking a hero by rescuing them in a dungeon, the other players see this as rescuing a generic survivor. This way it never looks like a teammate is reviving thin air: there’s always someone lying on the ground, ready to be saved. It might just happen to be a different character for each player.

*Unlocking a hero compared to rescuing an anymous survivor.*

One more nice trick that I would like to mention is one that we’ve so far unfortunately not finished implementing (Blightbound is still in Early Access on Steam). Since levels have these areas that are ideal for triggering story beats (no combat, some space for exploration), it would be nice to do something with that even when there’s no story beat for your specific character triggering in that run. So Roderick (the writer on Blightbound) has written a bunch of dialogues and banter that add some world building and personality building, but aren’t tied to any moment in the story. This way we can always trigger something. Since this is really a non-essential bonus feature we haven’t gotten around to actually implementing these lines yet, but I really like this feature so I can only hope that we’ll find the time to add this at some point.

Before concluding this blogpost I’d like to also have a short look at the implementation. With 21 heroes all having story moments and shouts and banter, Blightbound has a LOT of voice lines. There are more than 100 story events and over 6,000 voice files, ranging from short barks to several sentences. Working efficiently with such large volumes requires some proper tools, so [Ronimo](https://www.ronimo-games.com/) programmer Jeroen Stout (known for having made [Dinner Date](https://store.steampowered.com/app/94000/Dinner_Date/) before joining Ronimo) implemented a system he calls Voice-A-Tron.

Voice-A-Tron was tailor-made for Blightbound and it’s a very neat tool that provides a bunch of features, including:

- A spreadsheet that automatically presents all lines in two formats: per character and as it appears in dialogue (so alternating between lines of different characters).
- Some simple scripting rules that allow defining dialogues, what portrait to use, where to trigger context-sensitive responses, triggering animations and even triggering related achievements and unlocks.
- A system that automatically executes these scripts in-game, so that our game designers need to do less work to implement story beats.
- Special objects that can be placed in levels to control where and when story beats are triggered.

Using Jeroen’s Voice-A-Tron system, [Roderick Leeuwenhart](https://twitter.com/HeerRood) wrote and defined all the story beats. Roderick is the writer for all Blightbound dialogues, as well as a series of [short stories set in the Blightbound universe](https://www.blightbound.com/stories/). The next step was that Ronimo game designer Thomas van der Klis did the actual implementation, for example defining where story events can trigger and creating special items and elite enemies.

The result of all this work is that in Blightbound, each character has their own story beats and these are told without interrupting the flow of gameplay and without spoiling teammates. At the same time the system is simple enough that it was doable to implement for all 21 heroes in Blightbound. While Blightbound isn't a storytelling game at its core, I feel this adds a lot of personality and purpose to the experience.

## No comments:

## Post a Comment