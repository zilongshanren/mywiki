---
title: Game designers need instant feedback
url: https://dewitters.com/game-designers-need-instant-feedback/
published: '2014-04-14'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

When I started programming games, I had the same workflow as most game developers: Program the game logic in a programming language, compile it, and then playtest the game. Once you stumble upon an issue, the whole cycle starts again.

I did the same for resources. So when a graphic needed updating, you stop the game, edit the resource, and start the game to test it.

This process seems fast and easy on paper, but most of the time it’s pretty tedious. The part you want to see might be at end of a level, so you first need to reach that point (again). You can work with cheat codes, but it still remains pretty annoying.

## Real-time updating of resources

When modifying resources, it quickly becomes frustrating to have to restart the game again to see the result. So a first thing I implemented in my game engine was ingame reloading of resources.

The poor mans’ solution is to do a reload when a certain button is pressed, and the more fancy one keeps track of file changes, and reloads accordingly. This functionality should only make it in debug builds, and not in release builds of course.

![Tiled tilemap editor Tiled tilemap editor](../../assets/cc1009d6385f30a5.png)

Tiled tilemap editor


It can work for resources, but for compiled source code, such a solution is impossible. But then again, not everything that is part of your game source code should be in there.

## Move configuration from code to data

Most game programmer that I know do configuration inside their source code. The reason is because its easy and fast.

Whether or not you do configuration inside code is easily spotted. Every time you write a ‘magic value’, it probably doesn’t really belong in your code, but in a configuration file. It takes a bit more work to store these numbers inside a configuration file, and load them in your code, but it is well worth the effort. It enables real-time updating of these values in your game.

Going from code, to compilation to starting your game and going to the correct location, only to find out it’s still not the preferred value, can be a real time waster. So configuring values in a resource file can be a real time saver.

## From issue to updating the game

So I already explained how you can get fast feedback on the resources you adapted, but the other way around might also be a burden.

Assume you’re playtesting your game, and you find an issue in a certain tilemap or sprite. You will have to locate that file, open it in your favorite editor, locate the position of the error and adapt it. For configuration files this also means finding that specific configuration inside the file. Once adapted and saved, as I explained above, that result can be instantly seen inside your running game.

So how to speed up locating your resources for editing? Well, unfortunately, that’s not easy. If you want instant editing of your game, you will need an ingame editor. Some projects have an ingame level editor (my game [Mystic Mine](http://www.mysticmine.com) had one), but it’s probably not worth the effort if your tilemaps can be made with a tool like [Mappy](http://tilemap.co.uk/mappy.php) or [Tiled](http://www.mapeditor.org/).

For example Civilization 5 has an ingame editor:

## Real-time reloading of game code

Although compiled source code can’t be adapted at run time, there are some ways to still pull this off. Game logic can be written in scripting language, which can be reloaded while running your game. But this is not as easy as it sounds, because that code might be in some sort of state. And the question is how this state will be transferred to the new scripting code.

Programming languages like Erlang for example, support so called [Dynamic Software Updating](https://en.wikipedia.org/wiki/Dynamic_Software_Updating), where a module can be hot-swapped. I don’t think this is practical for now, but the concept can definitely bring added value for game development.

If you use C++, there is a [runtime compiled C++ library](https://github.com/RuntimeCompiledCPlusPlus/RuntimeCompiledCPlusPlus) that allows you to make changes in your code at runtime and see the results immediately.

Bret Victor has a nice presentation on how to do game programming with real time feedback. Also not practical for real life projects, but the concept is definitely very cool. You can see his presentation at [vimeo](http://vimeo.com/36579366) and fast forward to 10:40.

## Putting all of this into my RPG Playground game editor

All of the above evolved in to the main philosophy of my [RPG Playground game editor](http://rpgplayground.com). I want to play my game, and once I notice something, open up the editor, do the modification, and continue playing. Both the modification and feedback should be done as easy and fast as possible. Kind of keeping the editing latency low. I think this can only be done by integrating the editor into the game.

An extra benefit that you get with such an integrated editor is that you work straight into your game. So when creating your level for example, you’re not editing each individual part like the tilemap, the entities, the position of the entities, etc. You see the complete whole, and see how each component interacts with others. When doing changes, you immediately see the end result, including interaction with other game objects, visual effects, etc. Associated animations and sounds are also available while editing.

In my opinion, such an editor that allows instand feedback is the best tool for any game designer. It saves time, easy to tweak things, and fun to work with. The challenge with RPG Playground is of course to keep everything generic, so it doesn’t turn out as just a ‘level editor’, but a real ‘game editor’.

So why don’t you give RPG Playground a try at [http://rpgplayground.com](http://rpgplayground.com), and let me know what you think of it.

## 0 Comments