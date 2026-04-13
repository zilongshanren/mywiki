---
title: 'Infiltration: open design points'
url: https://randomtower.blogspot.com/2018/09/infiltration-open-design-points.html
author: Pubblicato da Marte
published: '2018-09-12'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

Inspired
by tag discussions on

[bay12forum](http://www.bay12forums.com/smf/index.php?topic=169949.0), I want to share some thoughts about future directions for this prototype.
I've
written before that scope for this project is only to be a prototype,
and like other prototypes, should answer questions. In this case,
questions are about game mechanics and how they interact each other
to form player experience.

Current
status about mechanics is the following (see




[this msg about mechanics discussion](http://www.bay12forums.com/smf/index.php?topic=169949.msg7800030#msg7800030))![]() |
| gameplay mechanics tree, green: completed, yellow to be done |

*Note*s:

- pois: point of interest

- TBC: to be completed

-

**game world**: game world generation on this stage is mostly completed. For sure I can add variation, more procedural content, procedural generated map, better graphics.. but is out of scope right now. Have a group of pois (cities for now) is enough, or I want to say, the minimum foundation for start to play. For me this side is completed!
-

**point of interest**: now pois are completed: with districts cities are now a stage for npc confrontations, battles and so on. I want to stop now on this side, because I can add more special pois (dungeons, crypts, villages, battle fields..) but is only variation on the same idea. What will bring more, in term of gameplay, is add new special mechanics for particular pois. For example, add "unlockable" pois, after some events are triggered (see below)
-

**poi triggers**: (TBC) one of the "core" feature I've identified for this prototype is possibility to add some triggers on a poi. A trigger in my mind should be defined as a series of condition on poi variables and some actions on poi. One example I've come in mind is to create some hidden poi, like a dungeon.
This
dungeon will provide unique quests for npc ( and also tags!) and some
kind of tag (bonus) for player too (for example bonus on manipulation
action, but is only an example). So player will unlock this poi after
first rebellion in another city, with an event. I think that this
kind of triggers, if used correctly, will provide more options for
gameplay and my reference model are Xcom games, where player complete
missions and acquire more experience and this advancement trigger
tier 2 mission and so on.

-

**characters**: on this side I'm on maintenance mode right now. This means that my focus is to fix bugs. I'm satisfied with "city simulations" and characters interaction. Maybe I will work on relation side, bug always to add more possibility for players
-
ancient one: inspired from TWS, I have considered a lot of specific
ancient one power, instead of "generic one" (like corrupt),
but I want to keep it simple. How it's possible to design ancient
one's power without know which elements can be modified by player ?

-

**ancient one level up**: (TBC) for now this is covered knowledge unlock and special "tags" for ancient one, maybe after a manipulated npc complete a particular quest. After observing how paradox games are made (EU4 or HoI4 for example), seems that add a lot of small bonuses, unlocked often are a good way to keep player busy. I don't know right now how this fit in my prototype, this is one of my research questions. I don't want achievements, but something player can have influence on. For this I'm thinking about ancient one religion. Because player take role of ancient god, what fit best of a religion? After first unlock of player power, this mechanics will be unlocked and with a new dedicated interface, with more and more corrupted npc (and many followers!) you can build on top of this base your cult. My idea is to use npc followers in the good old sacrifice way and in this way unlock new tags. These bonuses or tags will provide bonuses for player challenges or can be used for power-up and npc ?
-

**player action**: here I've done for now. I have a lot, I mean a list of dozen and dozen of possible actions, but I want to KISS (keep it simple stupid!). Focus to corrupt (maybe is better corrupt?), calling for doing stuff in a poi and manipulate for interact between two different npcs. Of course actions could be complicated, but.. not for this prototype!
-

**corrupt character**s: see above
-

**character actions**: (TBC) npc fight for poi dominance, but I think is not right choice. Dominance is not the only way npc could be, so my idea is to add a "nature" or "destiny" for every npc. For example good old Uzbar, the barbarian, will be violent by nature and every interaction or challenge will be solved with a physical challenge or a fight. Of course with madness this will be worse, but I think that different natures will provide more variability for each character when they interact each other, for fight in a poi or not. Why all npc should fight? Maybe some npc can start to study, connect the dots, or improve abilities. I want to be KISS even here and just try little variation, not too much
-

**follow clues/ uncover ancient one**: I know from various reports that this is a simplified version and most of the runs npc cannot find player hidden in the world. This is fine. I mean is a matter of balance right now and even if I have some ideas (like chosen one from TWS.. keep it simple!)
-

**move characters**: (TBC) This is something I want! For example bobby2hands made a great work in Shadows behind the throne ([see here](https://bobbytwohands.itch.io/shadows-behind-the-throne)) with a lot of characters moving on the map. Keep in mind that for this prototype graphics, animations and so on are not a focus, so I want to implement very basic movement: and action that characters can do on some triggers (to escape death after a manipulation, for example!) or after a calling from player. This an important point: right now cities are islands with no interaction. If characters can move around, they can start to mess with internal city equilibrium and of course player with it. But instead of TWS, based on direct control on few key adepts, I want to experiment some indirect control over npcs, like force them to leave a city, move to another city and start to search knowledge there
-

**solve quests**: completed!
-

**character experience**: with tag system is completed, at least for this prototype. Experience could be much more (xp, levels, items, powerful followers and so on..) but KISS again!
-
organization: guilds are simplified right now, again for scope. I
have ideas on this side too, for example a guild could hide a piece
of forgotten knowledge somewhere (a hidden poi, see triggers ) and as
player to uncover this secret you should help your corrupted agent to
climb the ranks inside the organization. This could add some
variation on the main formula, but not for this prototype

-

**organization bonuses**: originally this idea comes from "rank" inside a guild for a npc. If a guild is powerful, win wars, get more points and provide more assistance on npc with higher rank. A simple formula.. but is something connected to organization rank and want to keep it out from this prototype, maybe in the future
-

**organization diplomacy**: this is also out of the scope. Right now guild can start wars each others.. and this is a mess caused by player too! For example if a manipulated npc kill another npc in a city.. this will cause problems between guilds. I don't understand if this is something that players can see right now, maybe with a proper guild's relations window, this could be more easy to follow
So far
my points on design side are the following:

1) work
on unlockable pois, using triggers to add more variation and more re
playability for the game

2)
design and think ancient one religion, to unlock bonuses, based on
number of corrupted npcs and followers

3)
destiny types for npc, this will guide actions and reactions to a
changing world

4)
moveable characters between pois

On next
builds I will focus in find my way to solve these points and like
always, any comment, feedback, critique are welcome!

## No comments:

## Post a Comment