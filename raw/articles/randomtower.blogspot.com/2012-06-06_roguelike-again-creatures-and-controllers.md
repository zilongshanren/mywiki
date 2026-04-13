---
title: 'Roguelike again: creatures and controllers'
url: https://randomtower.blogspot.com/2012/06/roguelike-again-creatures-and.html
author: Pubblicato da Marte
published: '2012-06-06'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[MarteEngine roguelike tutorial series](http://randomtower.blogspot.it/search/label/rougelike%20tutorial)(thanks!) so I've decided to add this little post as bonus for fans.

Is not MarteEngine related , but build on top of

[AsciiPanel from Trystan](https://github.com/trystan/AsciiPanel).

**Introduction**

This post assume you already know what is a roguelike, a minimal introduction to AsciiPanel (se for example

[Twelve Hours](https://github.com/trystan/latestart7DRL)). I'm not a roguelike expert, but I'd like to share what I've learned so far.

**What is a creature ?**

In a tipical roguelike a creature is something is moving around the map, trying to kill player or doing something else. In my

[MarteEngine roguelike tutorial 9](http://randomtower.blogspot.it/2012/05/marte-engine-graphic-rogue-like_09.html)I've introduced wander AI for bats. A simple solution for a monster: just wander around, with no goal and behaviour.

If you search around net about this, realize soon this kind of topic is a BIG topic: Artificial Intelligence is hard and I've found many many and again many links about this.

My idea is that a Creature is just something, like a puppet, someone control. From here idea of Controller: a bunch of line that decide what Creature must do (in my MarteEngine tutorial I've named this Creature and CreatureAI, it's the same).

**Some initial toughts**

Think about last AAA title: what is behaviour of enemies? Attack on sight player, cover sometims, not too much. In this roguelike is more active: many good roguelike have interesting behaviours and I've decided to have something more than just wander (see my first experiment,

[Goblin Invasion](http://randomtower.blogspot.it/2011/07/goblin-invasion.html)). Mainly ideas come from this

[article on roguebasin](http://roguebasin.roguelikedevelopment.org/index.php/Plug-In_Monster_AI)

To do this I've implemented basic stuff: map, enemies, hp and even groups with some allies for player.

**Behaviours**

Following this approach and inspired from Trystan works, I've defined some behaviours:

**Wander**: move in a random direction if possible**Attack Player**: wander around, but if can see player, compute a path to move next to it and attack**Flee**: if see player, move to opposite direction (not at every step) otherwise flee**Gravedigger**: seeks dead bodies and eat them if see no enemy, otherwise flee**Healer**: move to ally if on sight and then heal it and if see enemy, flee**Nest**: wander inside an area (nest) and attack enemy on sight until inside nest**Random Point**: move to a random point inside map, then iterate. If see player attacks it**Scaravenger**: attack wounded enemies (30% of hp), otherwise flee

[Slick library](http://slick.cokeandcode.com/)for A star: I love opensources!)

Final result is here

[Java](http://www.java.com/)to play it!

Suggestion: click with your mouse on game area to get focus

Legend (name - behaviour - color letter)

Bat - attack player - red b

Skeleton - random point - white s

Hyena - gravedigger - orange h

Kobold - flee - red k

Scaravenger - scaravennger - yellow s

Healer - healer - white h

Villager - wander - white v

Wolf - nest - gray w

**Conclusions**

Roguelike could be without too much pain a nice way to experiment basic behaviour without need of complicated frameworks. Adding features like levelling for creatures (even monsters!), more groups (not only heroes vs monsters), more complicated behaviours is easy and fun.

In this experience I've learned a lot and found a huge limit: when you need more than "if I see player, attack it, otherwise wander", you must start thinking of a finite state machine and in particular behaviour trees. You cannot simply use my approach to get a more complicated exaple, without huge refactoring of code.

## No comments:

## Post a Comment