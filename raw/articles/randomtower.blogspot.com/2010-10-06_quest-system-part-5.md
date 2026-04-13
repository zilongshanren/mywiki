---
title: Quest System - part 5
url: https://randomtower.blogspot.com/2010/05/quest-system-part-5.html
author: Pubblicato da Marte
published: '2010-10-06'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

As I said before, a modern and interesting quest system has to be like a web, where player moves. Each time he/she touches part of this web, something change in other part. This process of feedback must active to player: no obscure statistics but real consequences. An image of what I mean is following:

![](../../assets/88e9249fa67ffc71.jpg)

Interconnection could be in many dimensions, so image it could be difficult, but image some properties (see

[part2](http://randomtower.blogspot.com/2009/11/quest-system-part-2.html)) of this "matrix":- factions relationship

- npc relations

- object

- places

I realize that these principles could be not so pratical, so I'll build an example on build of it, hoping someone found interesting.

**Example 1**

**Settings**: fantasy with humans, orcs and elves. Orcs have controls on plains, human hide from orc slaver but also work with them. Elves have a kingdom in forests in war with orcs

**Factions**: human mercenari (HM), orcs slave traders (OST) and elves kingdom (EK)

**Story**: Player start as affiliated to HM faction with a starting quest

**Quest1**: protect caravan from point A to B

**Description**: player must protect caravan from bandits from point A to B and during this job meet another John (HM) and this brother Jack (HM). Fight with bandits is fast and bloody and player can do nothing to save John life, but protect caravan. One bandit flee and left some clue that OST faction is involved with bandits

**Consequences**:

- John die.
- Relation with Jack is ruined (don't save his brother isn't a good thing).
- Relation with HM go up (one job done).
- Some objects looted from bandits dead body.
- Jack leave HM faction (He think that player must be punished, not promoted!)
- player can fast move from point A to B (no more bandits), caravan leader notice that to player
- in city A and B people talk about "no more bandits"
- in city A and B guards are interested in player because help to fight bandits
- relation with OST go down, because they are using bandits

**Analysis**: game must present to player in clear way John die and Jack ruined relation (using a dialog for example "

*Your inability killed my brother, I will not forget that!*"). Good relation with HM faction could represented using another npc that give thanks ("

*You done well in protecting caravan, you will do career!*") to player (also with quest log!) and a new mission. Some side effects are in city A and B and fast moving from A to B and good relation with HM faction means better prices for equipment!

This is just an experiment of design a good quest into a "good" quest system, more will follow :D

## No comments:

## Post a Comment