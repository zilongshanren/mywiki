---
title: Re:creation dev log. March 2015. Graphics improvements, entity inheritance,
  improved state machines and more!
url: https://eliasdaler.wordpress.com/2015/03/30/recreation-dev-log-march-2015/
published: '2015-03-30'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This month was great. I finally got in the flow of development and managed to get lots of things done. I worked hard to make game look better and here’s the result. Compare old screens with new screens:

![](../../assets/6a2a15648087e0c7.png)

October 2014


![](../../assets/a0d4b3a23985d041.png)

March 2015


![](../../assets/0ee1d0532bc5e53c.png)

December 2014

![](../../assets/06ac2945f54e875e.png)

March 2015

Quite a difference, right? I was suprised how positively people have reacted. Thanks a lot for the feedback, everyone! My art skills are surely evolving and I’m glad that I can make a game look nice with my own art.


# Shadows

![](../../assets/02010287248dea95.gif)

With old shadows / with new shadows


This feature was actually added today and I didn’t expect it too look so good. It adds lots of depth to the picture which is very awesome. How was this done? Very simple: I attach second sprite to entity which is just its shadow with alpha channel. The shadow is always rendered before the object it belongs to. It also follows the same z-ordering algorithm I’ve described in detail in [this article](https://eliasdaler.wordpress.com/2013/11/20/z-order-in-top-down-2d-games/). And it works well. Check it out in action:

![](../../assets/e8a0e40b25388179.gif)


# Entity inheritance

Well, it’s not actually an inheritance, so let’s look at the example so you can quickly understand what’s going on.

Suppose I want to make a bigger chest which looks different from ordinary chest. They act almost the same, the only things which are different are **GraphicsComponent**, **CollisionComponent** and **InteractionComponent** values.

![](../../assets/0fc397b0234a9828.png)

Tough choice…

Here’s how original chest script looks:

chest = { init = function(this) setScriptState(this, "ChestClosedState") end, GraphicsComponent = { filename = "res/images/chest.png", ... -- other stuff }, CollisionComponent = { type = "Solid", boundingBox = { 0, 0, 16, 16 } }, InteractionComponent = { interactionRect = { -8, 16, 32, 16 }, interact = function (this, second) if(getScriptState(this) ~= "ChestOpenState") then setScriptState(this, "ChestOpeningState") end end }, InventoryComponent = { ... -- so chest can have items in it }, ScriptStateMachineComponent = { ... -- states of chest (Closed, Opening, Open) } }

So, the only things that we need to change is **GraphicsComponent.filename**, **CollisionComponent.boundingBox** and **InteractionComponent.interactionRect**. Other things are the same. So I can write **super_chest** script like this:

super_chest = { template_init = function(this) copyEntity(this, "chest") end, GraphicsComponent = { filename = "res/images/super_chest.png", animations = { closed = { frame = {0, 0, 32, 32}, }, opened = { frame = {32, 0, 32, 32}, } } }, CollisionComponent = { type = "Solid", boundingBox = { 0, 0, 32, 32 } }, InteractionComponent = { interactionRect = { -16, 32, 32, 16 }, interact = function (this, second) if(getScriptState(this) ~= "ChestOpenState") then setScriptState(this, "ChestOpeningState") end end }, }

When the template for entity is created, the **template_init** function is called first. Every component of “**chest**” entity is copied to “**super_chest**“. Then we start to look at what components this new entity has. If the base entity doesn’t have some component, it’s created. But if it has one, then some values are overwriten. I don’t even have to rewrite all parts of the component, only those which change. I’ve always wanted to do this for a long time and finally I’ve succeded!

# Advanced script machines.

I’ll write a big blog post explaining how I’ve implemented script state machines, but I’ll show you how they work for now.

Each state has three functions: **enter**,** execute** and **exit**. **enter** is called when entity goes into the state, **execute** is called each frame and **exit** is called when the entity goes into another state.

This worked fine until I’ve realized that some states need to have some variables in them.

Simple example. Look at the witch in this gif.

![](../../assets/7d2fadf9916299e8.gif)


When she turns five pages, she goes back to the idle state. How was this achieved with scripts?

You can look full script [here](http://pastebin.com/9B3rnyDm) . I’ll focus on the most important parts

Here’s how the init function looks like.

init = function(self) self.flippingPage = false self.flippedPages = 0 end

This function is called when the state is created. Self is the state itself. This creates variables in the table which can later be used

execute = function(self, entity) ... -- some code ommited if(self.flippingPage and currentAnimationFinished(entity)) then -- finished flipping the page, go to reading state setAnimation(entity, "reading") startTimer(entity, "pageFlipTimer") self.flippingPage = false self.flippedPages = self.flippedPages + 1 end end

So, two arguments are passed to this function. The state itself and entity which is in this state.

And that’s it. Pretty easy and shows how awesome for scripting Lua can be. All this stuff could be hard coded, but I’ve chosen a lot more flexible way to do stuff.

# Managing the Lua state

This was a big problem for a long time for me. I didn’t quite get how to manage one big Lua state. It was certainly needed, because I register a lot of binding functions in a state and later call them from scripts.

When levels loads, I load entity templates from scripts. But older templates stay in lua_State which makes **lua_State** grow bigger and bigger as new levels load. This can be prevented by manually removing unneccesary template entity tables from **lua_State**. I’ve made **TemplateEntity** class which counts number of entities created from the template. After the level is reloaded, I check if any template entity has reference count is zero. If it is, it means that some template entities are not needed anymore and can be removed. (there are exceptions to this like entities which can be created level on the level, but I can easily not delete them by setting a special flag when they’re loaded).

Here’s how I do it:

for all unused template entities:

- Assign nil to template entity table
- Call garbage collector

You can do it using Lua C API like this:

std::vector<std::string> entitiesToBeDeleted; ... // find list of entity names for(auto it = entitiesToBeDeleted.begin(); it != entitiesToBeDeleted.end(); ++it) { lua_pushnil(L); lua_setglobal(L, *it); } lua_gc(L, LUA_GCCOLLECT, 0);

Nice and easy.

# Exceptions in component constructors.

Turns out, if I do something like this in LuaBridge):

LuaRef someStringRef = getGlobal(L, "someString") std::string someString = someStringRef.cast<std::string>();

and someString is not a string in Lua, then LuaRef won’t throw an expection, the program would just crash. The crash reason will not be easily found because the only message you get from lua is this:

"PANIC: unprotected error in call to Lua API (attempt to call a nil value)"

(or something like that)

I needed better error messages. They can easily be produced by exception. So now, every component constructor can throw an exception if something goes wrong. Something like this:

if(filenameStringRef.isString()) { filename = filenameStringRef.cast<std::string>(); } else { throw ComponentLoadException("Filename is not a string!"); }

And then I catch it in** Entity::load** function:

void Entity::load(const std::string& entityName) { ... for( ... /* each component */) { try { ... // create a component } catch(ComponentLoadException& e) { debugLog->write("Failed to load component" + componentName + " for " + entityName + ": " + e.what(), LogManager::ERROR); } } }

This approach is a lot better than returning error codes (well, I can’t return anything from a constructor, but I could create some **int Component::init(…)** function, right?) because there may be A LOT of error codes for components. Something is not a string, something is not a number. Some number is not in a valid range, etc.-etc.

So this is pretty cool and may potentially save me lots of time when I write the scripts so any errors would be identified easily.


# Other stuff

My game got it’s first articles which is so awesome!

Check them out:

[http://www.siliconera.com/2015/03/26/some-undead-just-want-to-stop-being-killed-for-loot-and-experience/](http://www.siliconera.com/2015/03/26/some-undead-just-want-to-stop-being-killed-for-loot-and-experience/)[http://www.playm.de/2015/03/recreation-beweist-der-welt-dass-nicht-alle-zombies-boese-sind-220586/](http://www.playm.de/2015/03/recreation-beweist-der-welt-dass-nicht-alle-zombies-boese-sind-220586/)

# Plans

There’s a lot of stuff I’m planning to do. First of all, I’m planning to finish first part of the game. It won’be polished but it would be fully playable and have enough content to show the overall feel of the game I hope to achieve. I also plan on experimenting with recreation mechanic and combat system. I want to try to make short combos and they may make combat a lot better and interesting. I also have to draw lots of graphics but I’m almost done on the engine side so the process of content creation will be very fast.

And that’s all for this dev log. Phew, it’s been a great month! Thanks for reading!

Subscribe to [my twitter](https://twitter.com/eliasdaler) to not miss any updates.

I really like the graphics. It has a nice theme and feel to it.

Thanks! Glad to hear that.

Release date?!? Demo?!?? Trailer/Gameplay??????? Pleeeeeeease

I hope to release a demo somewhere this year (probably by the end of it).

Release date is still unknown.

You can watch some gameplay gifs on my twitter / on this blog :)

Trailer will come out this summer.

i want to play this so bad.

i’ts just like Zelda Without Zelda. I LOVE IT.

Aww, thanks a lot, great to hear that! Stay tuned for new updates on the game. :)

What platforms will you support?

Windows, Mac, Linux.

Why the Lua ‘if’s have parentheses? They’re not needed as Lua has the ‘then’ keyword…

This makes code more readable for me. And it’s a lot easier to switch between C++ and Lua if I do this.