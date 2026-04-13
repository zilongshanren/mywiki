---
title: New maps, new weapon, new money system, new game mode!
url: https://etodd.io/2010/04/09/new-maps-new-weapon-new-money-system-new-game-mode/
published: '2010-04-09'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# New maps, new weapon, new money system, new game mode!

I've been silent here for a while, but that's just because I've been busy getting some glamorous new features in! Things are really starting to shape up.

First things first. Bobpoblo has joined the team as a mapper/tester! He's been working hard on some new maps made in Hammer, textures courtesy of [-B-]. The original maps will likely be remade as well. Unfortunately the content pipeline is a little convoluted: I open the Source map in Crafty, export it to Wavefront OBJ format, and import it into Blender. From there I fix import errors, remove degenerate triangles, apply lightmaps, etc. before exporting to .egg format.

But! It's all worth it in the end. Here are some screens:

There's also screens of the molotov cocktail, the latest addition to A3P weaponry. It bounces around like a grenade, catching enemies on fire for a few seconds and slowly lowering the health. It's most effective when used to weaken a group of enemies before finishing them off with another weapon.

The new purchasing UI is also shown. Instead of re-purchasing weapons and special abilities every round, the new system lets you keep items from round to round, and store them in inventory if you want to save them for later. And it's based on drag and drop, which makes it easier to understand, even though it lets you do a lot more. Also, when you mouse over any of the items, it displays a popup with the price and some useful information about the item. This really helps people like me who don't read instructions and can't be bothered to remember all the details of each item.

Finally, a new game mode is in progress, which pits up to four players against an army of AI bots (called "zombies") which spawn around the edges of a circular map and assail the players in the center. Currently, there's a simple wave system which spawns AI bots with different loadouts every wave. Nothing happens when you get past 6 waves or so, it just crashes. But still, it's a first step! Look for more news on survival mode soon.

In fact, I'm pondering a whole new gameplay idea for the main game. It may or may not involve the return of drop pods, performing a different task.

Also, sorry for the "play" page being continuously down for a while. Everything is operational, it's just that I have to have a terminal session open on the lobby server in order to keep it running. Hopefully I can figure that out soon.

Anyway, stay tuned! Big things are goin' down.