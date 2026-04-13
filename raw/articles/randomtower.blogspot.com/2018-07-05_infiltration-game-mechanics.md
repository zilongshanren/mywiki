---
title: Infiltration game mechanics
url: https://randomtower.blogspot.com/2018/07/infiltration-game-mechanics.html
author: Pubblicato da Marte
published: '2018-07-05'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**TLTR**: I was on vacation and doing some work at home, but I'm back on design side for this experience, after reading an amazing book.

Last month was a little bit "strange": first work at home, then I was on vacations (yahoo!).

So I had a lot of time relaxing, thinking and reading a book about game design. I've read some books in topic during years and found them a little bit too much abstract or too much in a specific "angle" to be useful. This time, however, I found a nice mix, in

*Designing Games: A Guide to Engineering Experiences, by Tynan Sylvester*.

In my first post on this thread, I've put in a single line my vision for this project as follow:

*"a turn based single player asymmetric game where player take control of an agent and manipulate actors and organizations to obtain victory"*

(sorry for my English btw!)

and I need to focus more this vision to answer two simple questions:

1) which mechanics my game does it have ?

2) what are the core mechanics?

After think a little bit, I'm trying this "design exercise" and I'm thinking could be valuable to anyone want to start and build a game.. so let's start:

**Mechanics**

To formalize and think on the right track, I want to write down what is a mechanics (see

[https://en.wikipedia.org/wiki/Game_mechanics](https://en.wikipedia.org/wiki/Game_mechanics)for some reference about this huge topics): "a set of rules designed for interactions on game state" and more important an emphasis on "

**mechanics is the way game create events**" and events are what players wants.

A reasoned list for my Infiltration test could be:

poi = point of interest in the map

characters = not playable characters, agents, etc..

challenges= contest between characters statistic or environment

- characters can move between different pois: characters interactions could be during travel or in pois and found new hidden poi

- characters gain experience, levels and tags: winning challenges, found hidden pois, solving quests will provide experience and on each level unlock tags. Like in promised feature on TWS, characters can reason on tags presence (for example hate an archimage? love a warrior full of scars?). Base statistics will be also increased and characters will be more powerful and able to solve more difficult challenges and quests

- characters can solve quests thought challenges: solve a quest could provide effect also in a poi, for example, raid merchant guild could provoke panic on a poi

- specific triggers in pois unlock new quests: some specific events (killed character, solved quest, character with specific tag) could trigger new quests in a poi

- player corrupt characters and force them to do what he want, leaving clues around: player can move to a specific poi, to a specific quest or challenge, to get a specific bonus and broke sigils and win

- organizations give bonuses to characters : organizations can give new tags or bonuses to organization's characters

- organizations could make war/peace with other organizations: events, quests, challenges can change organization's view on other organizations and trigger war or peace, so organization's member start to fight

- player can grow ancient one in power and unlock new abilities: new abilities can create quests, triggers or give tags to characters, or event create poi

- characters can follow clues and uncover player presence: corrupted characters can find and hide these clues and characters can unlock a "clue quest" and reason on clues, make a challenge and increase "ancient one awarness" in the world

During this writing I've realized that many ideas are already put into my prototype, but also mixed together, so it's hard to change a part of the software without move everything My bad about this!

**Core mechanics**

Core mechanics are important because will provide the foundation for the game. An example I've found on the book is for Starcraft 2: core mechanics here is to control scv, build a barracks, train marines and kill enemies. All other units, mechanics, etc.. are build on top of that.

For my game the most important think is for the player:

player corrupt characters and force them to do what he want, leaving clues around

But is the core mechanic? I've found this question hard to answer, because if you think to build a house, this seems to be like a nice door for the player, not foundation to build on it.

So I've tried to build them in order, trying to visualize dependencies between them:

![](../../assets/9c57a1c8623d9b62.png)


![](../../assets/9c57a1c8623d9b62.png)

In this diagram what I need to see are dependencies (thanks Tynan Sylvester!) between mechanics. I have mixed up a little bit mechanics with "general concept", like "game world" but I think this should display how this kind of prototype should be made: from bottom to top, for example:

1) corrupt a character without any character available is not possible

2) organizations are mostly independent from what characters do or even from ancient one

3) poi triggers does not involve organizations diplomacy

In green you can see what it's already implemented so far.

Looking at this diagram, my choose for core mechanics are the following:

1) game world / character definition / character action

2) characters move between pois, following internal logic

3) character solve quests

4) ancient one / player action / corrupt characters: now player can move a character to a poi and solve quests

These mechanics are the foundation for the game, what do you think ?

So my next steps are:

1) answer these design questions

2) work on core mechanics, don't waste time on other stuff for next release

## No comments:

## Post a Comment