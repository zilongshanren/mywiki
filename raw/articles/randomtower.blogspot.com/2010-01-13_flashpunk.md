---
title: Flashpunk
url: https://randomtower.blogspot.com/2010/01/flashpunk-seems-to-be-jung-good.html
author: Pubblicato da Marte
published: '2010-01-13'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/b3a81ff51ece6cf1.gif)


![](../../assets/b3a81ff51ece6cf1.gif)

[FlashPunk](http://flashpunk.net/)seems to be a young good framework to build game with ActionScript 3. I've read first tutorial and is clear for all that have seen ActionScript 3 like me (see

[ninja experiment](http://gamejolt.com/online/games/action/randomtower-ninja-test/962/)).

[First tutorial](http://flashpunk.net/forums/index.php?topic=22.msg148#msg148)is short, good and clear: all things that i really desire in this kind of thing.

Reading source code, I've some rapid observation about it: i think that everyone have ever coded a videogame with AS3 can share some thoughts about it (as always IMHO):

- good use of classes, finally: i really don't like AS2, I'm old Object Oriented programmer, welcome Chevy Ray Johnston to this side of programming (dark side?)

- no release notes: this is bad. FlashPunk is young, but without a little help how can someone decide what version is better? How much change from version 0.x to 0.y ? How much to experiment with?

- no bug tracker: only forum. I don't like forum for this, but seems that for someone is working well (

[Slick](http://slick.cokeandcode.com/)too). A good bug tracker (like

[Track](http://trac.edgewall.org/)(used at work in really no-videogame-life)) can help to keep things organized, setting priorities and favorite new developers into young projects,

- Core.as with:

Basic overridable method of update, render and addAlarm (all in AS3 in based on events, keep it in mind): this is good, because force developers to keep logic separated from display things (like in Slick ). Don't waste your time think about it, is ALWAYS a good choice, remember

[KISS](http://en.wikipedia.org/wiki/KISS_principle)principle?

I don't understand why have here drawSprite, drawRectangle and drawLine in this class: maybe an external class can help?

Note: Core.as depends from only core packages, no external library, this is good

- Entity.as is as creator have define it "Basic game object which can be added to Worlds. They have an x/y position and functions for collision.", with:

x,y in the world (see below), depth of painting on screen.. basic stuff, but wait! There is collision stuff: some brute force method (check against all entities in the world), but also grid approach (see

[Anotherearlymorning](http://www.anotherearlymorning.com/2009/03/revisiting-the-grid-data-structure/)example): this is really good for performance, maybe some test can help to explain power of this approach.

An interesting thing to mention is search-type for collision: coder behind FlashPunk think that search collision with only certain type (player vs enemies, not enemies vs enemies, for example), can help. Good point!

Another good point is Collision Mask support, good to see it!

This class have good idea, but i don't like idea to mix basic information about an entity with collision detection: maybe a different class?

- Actor.as is "A game Entity able to display and switch between animated sprites.", so a little more than an entity that support animated sprite: maybe an Animation class (like in Slick) can help coders, but i like idea to give to everyone a tool to use, without force to use it. Do you want to code your animation framework, lets do it! I see SpriteMap.as that seems to be a sort of Spritesheet support :D

A small bad thing is that i've found into package two Actor.as class file: a bugfix can help :D

- World.as is "A Playing stage that game Entities can be added to. Used for organization, example worlds: "Menu", "Level1", etc.": game state support, with some good ideas: adding a vector to a particular entity, perform a Function to all Entity of a particular Class (Actor for example), get mouseCoordinate. World have is own update and render thing, so all within it is updated and rendered. World.as is a strange object: seems to be a bottle where all entities can go, but have some manipulation methods. I don't like this idea, is not so

[MVC](http://en.wikipedia.org/wiki/Model_view_controller)(that is one of the main pattern for AS3 itself): is better to keep separated bottle from tools, so coders can use any of them.. and this can reduce confusion,

- Acrobat.as is an Actor class with advanced draw capabilities: alpha, scaling, rotating and so on. I don't like this approach: again mixing together render with update. Why not add some Transformation classes with special effects that actor can use?

- TileMap.as is an embrional classes to give support to tilemap. Not linked with any particular format, is just a class to support this kind of things: maybe can be mixed to Grid.as to give a sort of TileMap + Grid collision things? Maybe with quadtree? Ok, it's only an idea :D

- Grid.as: remember collision stuff? Here you have Grid collision support: i like this idea!

- In general comments are enough to understand all, and this is a really good point! Otherwise, there aren't so much logging info about what is going on and no game console (like in Flixel): in this area FlashPunk can do really much more.

I think that FlashPunk is not ready yet to be THE AS3 framework for videogames (not on version 0_73), but is intersting: interestings, good points. Always the same. But much important, documentations!!

First tutorial explain all in a clear way: this can be right start.

Nice article about this young framework.

ReplyDeleteSome other frameworks I know about are

Flixel: http://www.flixel.org

and

PushButton: http://www.pushbuttonengine.com

I've build "basic" app with Flixel, but never with pushbotton, have you ever done something with it?

ReplyDeleteGreat article! I'm just on my second day with FP.


ReplyDeleteJust a note your MVC link doesn't work. It should be http://en.wikipedia.org/wiki/Model_view_controller

Thanks, like now is working :D

ReplyDeleteAnd now flashpunk is evolving .. now at version 0.83 with new features :D

I, of course, a newcomer to this blog, but the author does not agree

ReplyDeletesorry?

ReplyDelete