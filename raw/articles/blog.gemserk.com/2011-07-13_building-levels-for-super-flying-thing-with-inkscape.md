---
title: Building levels for Super Flying Thing with Inkscape
url: https://blog.gemserk.com/2011/07/13/building-levels-for-super-flying-thing-with-inkscape/
published: '2011-07-13'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As we did for [Archers Vs Zombies](https://blog.gemserk.com/2011/05/03/using-inkscape-as-scene-editor/) and [Taken](https://blog.gemserk.com/games/codename-taken/), we are using Inkscape for building Super Flying Thing levels too.

On SFT, levels are defined by the following information:

- The position of the starting planet
- The position of the destination planet
- The obstacles, specified by a collection of vertices and if they are dynamic or not
- The items, specified by their position
- For dynamic obstacles, a list of vertices specifying the path they follow

To declare this stuff on Inkscape, we are using three layers: World, Paths and Obstacles.

World layer is used to declare starting positions like start and destination planets and items.

Paths layer is used to define paths to use for dynamic obstacles (and probably for other stuff too).

Obstacles layer is used to define the shapes of the obstacles of the level. If the obstacles are dynamic we could link them with a defined path to make them follow it in the game. To link it we are using, for now, a custom xml field named movementPath with the id of the path we want.

We also have a templates layer, used to define templates for stuff we want to replicate later in other layer, for example, premade obstacles. That layer is not being processed when the level is loaded.

Here is a screenshot of one level being edited:

Using Inkscape as level editor for Super Flying Thing works great, however, we believe it could be an interesting feature to have an in-game easy to use level editor, to let players create their own levels and probably share them with other players.

Hope you like it.