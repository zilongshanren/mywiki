---
title: Infiltration 0.0.7 Challenges and tag system
url: https://randomtower.blogspot.com/2018/09/infiltration-007-challenges-and-tag.html
author: Pubblicato da Marte
published: '2018-09-26'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[some info on bay12 forums](http://www.bay12forums.com/smf/index.php?topic=169949.0)), called Infiltration, and my vision is:

*a turn based single player asymmetric game where player take control of an agent and manipulate actors and organizations to obtain victory*





You can see a preview of current status of the game in this video:You are not dead, you are not living.. yet.

Aeons ago, in a time before mith, your enemies sigil you in a realm far from reality. Weakened and far from your power, your will simply.. disappear.

One echo, from time to time, hit your dreams. Something called humanity is playing with arcane power and forgotten knowledge, part of you.

You simply awaken and take a look into the world. These "humans" will serve you as puppets in your quest to become powerful, again.

In this release 0.0.7 for my prototype, Infiltration, I've worked to add a new fundamental system, tagging, that interact with various elements in the game. This tagging system refers to a simple concept: actors in the game (npc, not playable characters) can have tags, like for example "strong" or "ignorant" and these tags will affect how npc can interact with game world through quests and player actions, challenges.

Tags can be good, with an active bonus (+20% on physical challenges) for npc or really bad, with a malus (-50% on mental challenges) and are added randomly from a customizable pool of tags on actor creation and after a particular quests are solved or failed.

In this version you will find following tags:

- generous, +20% social challenges
- greedy -20% social challenges
- ignorant -20% mental challenges
- intelligent +20% mental challenges
- strong +20% physical challenges
- weak -20% physical challenges
- scarred -30% social challenges
- anathema -30% social challenges
- falseGod -30% mental challenges
- renowned +10% social challenges
- integrity +50% resist focus player action
- willpower +50% resist calling player action
- determination +50% resist manipulation player action

As you can see from the list there are two big types of tags: one related to challenges (related to quests and actor interaction with game world) and player action resist bonuses.

Thanks to awesome platelayers I've found a nice way to filter living cities simulation behind the scenes in the quest log and with a filter by city on the left of quest log, now the player can be informed on a very specific city and not all together!

Like always any feedback is welcome!

## No comments:

## Post a Comment