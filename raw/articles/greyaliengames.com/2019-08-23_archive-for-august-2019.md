---
title: Archive for August, 2019
url: http://greyaliengames.com/blog/2019/08/
published: '2019-08-23'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

We often talk about tasks we are working on such as ‘adding enemies to the game’ but thought it might be interesting to break that down and tell you a bit more about what steps are involved.

Part of the process for adding enemies to [Ancient Enemy](http://bit.ly/AncientEnemy) involves aligning everything first in photoshop so that the stances make sense, then adding in attack lines.

![](../../assets/3386fa2be05027cf.jpg)

Then I export all the frames and load them into the game and have to do these things:

– Add to correct levels

– Set correct music

– Set player melee position

– Give correct weapons/magic and test

– Set enemy melee and magic impact positions

– Give enemies bombs or potions if applicable

– Set enemy throw coords if applicable

– Set enemy magic start position if using a fireball/dark orb

– Test player using throwing knives/bombs/magic arrows, etc., and adjust impact X coord accordingly.

– Add enemy VO

![](../../assets/0fd4cb5a451aef4a.jpg)

Here’s an example of enemy setup code:

![](../../assets/ecc617808c21d8f4.png)

Later, during the balancing phase I’ll set their health, resistances, intelligence and attack/defense values.

Basically, it’s a lot of work!

But the end results in-game are worth it:

![](../../assets/a5cc1570b898fa95.jpg)

Don’t forget that you can find out more about the game and wishlist it here: