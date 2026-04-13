---
title: Infiltration 0.0.2
url: https://randomtower.blogspot.com/2018/04/infiltration-002.html
author: Pubblicato da Marte
published: '2018-04-23'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[some info on bay12 forums](http://www.bay12forums.com/smf/index.php?topic=169949.0)), called Infiltration, and my vision is:

*a turn based single player asymmetric game where player take control of an agent and manipulate actors and organizations to obtain victory*





In version 0.0.2:You are not dead, you are not living.. yet.

Aeons ago, in a time before mith, your enemies sigil you in a realm far from reality. Weakened and far from your power, your will simply.. disappear.

One echo, from time to time, hit your dreams. Something called humanity is playing with arcane power and forgotten knowledge, part of you.

You simply awaken and take a look into the world. These "humans" will serve you as puppets in your quest to become powerful, again.

- added recruitment system: if a poi has less than 3 character, there is a 2% of chance every turn that
- added faction system: now factions can triggered a war with other factions, guided by relations. When there is a war between factions, player action is not possible. After 10 turns, there is a small chance that factions start a peace
- maximum character for every poi 7, random between 3 and 7
- a lot of bugfixes!
- notification system on left side for multiple events
- now high madness actions has negative impact -10 on faction relations
- display population value on poi stats (used when rebels recruit it's army

Let's dig a little bit in this version 0.0.2 with some screenshoots!

And start with events notification system on left side of the screen. Now when an event, triggered by player actions or from other actors, is displayed on left side for three turns and when clicked the event panel is displayed.

It's a basilar implementation, but now is more easy for player to not miss important events!

So move on faction system.Before this update, faction is just a property for characters player could manipulate. With this update, factions are an actor of the game and has relations with other factions, decide to start or stop a war. Of course player action, in particular character's actions on high madness can impact on faction's relations, so be wise when you play these actions!

And example on how relations are handled right now. I'm thinking to add a separate panel with all relations in one place, to simplify player view on factions.

An important outcome of a war between factions is that character of both factions are not available for manipulation, so be aware of that during play. It's fun from my side to plan to focus on a specific character, then move on calling on a city and.. a ware between two factions occur! As player you have to wait and move to new targets, until war ends!

Another little detail I've missed before is to display poi population on poi panel:

In this screen I'm also highlighting rebellion value, in poi panel and remember that a city in chaos (displayed in red on map) is a perfect place to start a manipulation!

Let me know what do you think of this prototype in comments sections!

## No comments:

## Post a Comment