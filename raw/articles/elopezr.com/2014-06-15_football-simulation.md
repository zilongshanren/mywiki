---
title: Football Simulation
url: https://www.elopezr.com/football-simulation/
author: Redorav
published: '2014-06-15'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

![RFM14_Ingame](../../assets/9bb618362261487d.png)

Real Football Manager prototype

One of the first prototypes at Gameloft was a football manager, for which the main focus was a match simulation. The development lasted two months, in which we were able to have a basic implementation of the game AI for the players. The agents were able to score goals, tackle other players, pass according to a specified strategy, unmark themselves to receive a good pass, chase and intercept other players, etc. We were not able to include other football rules like offside, throw-ins, or corners since the prototype was halted.

**AI**

The AI was designed to be predictable, so we stored random seeds and set them as appropriate, which helped debugging. Players were represented by a complex state machine that would constantly query the surroundings and decide to support a player, or rather unmark and try to kick to goal, or defend, etc.

**Debugging**

Almost from the beginning, we included very visual debugging features. Data like player kick and pass distance, tackle distance, ball height (at the top of the field, in a side view), player objective, player role, enabling/disabling behaviors for specific roles to debug, etc. were all represented on the football field for commodity.

Debugging individual behaviors was tricky, since they depended on the environment and other players’ actions and specific situations (not the same to be alone in the field than to have several teammates supporting), which is why predictability was of importance.

**UI and Engine**

The game kicked off right after Christmas, but before starting I took two weeks to revamp the whole UI system. The game moved from a very primitive data system to GUI elements, each represented by their own class, which took the needed data from the UI editor. These GUI elements are then handled by GUI layers in a very convenient and easy to use UI system. This system is currently used in all Java projects in Madrid.