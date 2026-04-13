---
title: Re:creation dev log. March-June 2016. Part one. Game stuff and and some awesome
  Lua scripting
url: https://eliasdaler.wordpress.com/2016/07/04/recreation-dev-log-march-june-2016-part-one/
published: '2016-07-04'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

The last few months I was very busy finishing my bachelor’s degree (it’s over, I got an “A”!). But still, I’ve managed to do some cool stuff and improve the engine structure and tools in the last couple of months.

This dev log will be released in two parts. In this part I’m going to talk about game stuff I did and stuff I changed about Lua/C++ integration. In the second part I’ll talk about engine tools I’ve made with ImGui and different refactoring I’ve done.

## Game stuff

Here’s one of the latest screenshots of the game. Houses were previously just big sprites, but right now they’re composed out of tiles which lets me reuse them for other houses and build new buildings more quickly.

![i2yn8x4](../../assets/0aaa94616fdf1b19.png)



The main character got some graphics improvements!

![xqtlpud](../../assets/b681fb9b753603c6.png)


Now he looks a lot more undeadly and has some awesome confidence in him! You’ll still sometimes see old character sprite occasionally because I haven’t redrawn all character animations yet.

![s1kfulv](../../assets/21cca5ba7c1b9a10.gif)


And here’s some fun little cutscene I’ve made for testing new Action List system (see below for more details about action lists)

There’s some awesome ideas and prototype stuff I have done but don’t want to show yet. :)

## Lua changes

My scripting approach changed a lot during the last few months. One of the reasons for that change was the observation that calling Lua from C++ takes a really long time compared to calling C++ from Lua. I wrote about it in the last dev log, but now I’ll write a bit more about that.

#### Remaking event manager in Lua

I’ve previously implemented a simple event manager in C++ and it worked great. You registered callbacks for event types, you queued events and then event manager looped over event queue by calling registered callbacks.

But what about Lua? I’ve approached this in straightforward way at first: by storing references to Lua functions and calling them on particular event.

This worked well, but wasn’t quite as fast as I expected. I realized that the approach must differ depending on type of callback:

- What if callbacks are C++ functions?

Easy, I just used**std::function**for them. C++ being called from C++, what can be better? - What if callbacks are Lua functions?

Basically, I had a situation like this:for(auto& event : eventQueue) { ... // call Lua callbacks }

See the problem? If

**eventQueue**is big or there are lots of callbacks to be called, Lua is going to be called a lot from C++ and that’s slow. There’s a better way to do this: pass array of events in Lua function and then call all Lua callbacks there:luaProcessEvents(eventQueueLuaTable); // in C++

-- in Lua function EventManager:processEvents(events) for _, event in ipairs(events) do ... -- call Lua callback end end


Interestingly enough, this made a huge difference in performance! That’s because if I had to call 20 Lua callbacks with old approach, I’ll do it in 20 C++ -> Lua calls, but now it’ll just be one Lua call to **EventManager:processEvents** and every callback will be called from there, and now there’s no need to store Lua callbacks in C++ and no need to call Lua from C++ for each callback. Neat!

Of course, now I had to store Lua callbacks in Lua. It makes sense, doesn’t it? That’s why there’s now two event managers: C++ event manager and Lua event manager. They work quite well together.

#### Remaking entity states in Lua

Previously some entity states (states as in state machines) were hard coded in C++.

This wasn’t quite what I wanted, so I’ve managed to create script states for new states which I didn’t want to write in C++ (See **Advanced Script Machines** section [here](https://eliasdaler.wordpress.com/2015/03/30/recreation-dev-log-march-2015/)). But then came the old problem: lots of C++ -> Lua calls, because sometimes state has to do something in each frame.

The answer came naturally: I just implemented Entity State Machine in Lua! But then I realized that I could just move **all** entity states in Lua to make my life easier. And now there’s only a tiny bit of game logic left in C++! Most of it is in Lua and it’s great: this allows me to write stuff more quickly and create as much states as I want without recompiling.

#### Action Lists in Lua

Action lists were a great addition to scripting in my game. This allowed me to easily create sequences of actions which are meant to be done one after another. It’s not as easy as it may seems at first.

Quick recap of what action lists do. Suppose you want to do some cutscene like this:

- Hero goes to a point on the map
- Breaks the door
- Says “hello”
- Sits on the chair

You can’t just do it like this:

-- inside some Lua function hero:goTo(somePoint) hero:break(theDoor) hero:say("Hello") hero:sit(theChair)

That’s because some actions will take more than one frame so you can’t just call one function after another. You can do that only when the action is finished. And that’s where Action Lists are used. You create a list of events and then the first action starts to execute. Action list manager repeatedly checks if the action is finished.

For example, **GoToAction** checks if the entity arrived at the destination. If it did, the action is considered to be finished and the next one executes.

Previously all actions were implemented in C++, but I could provide some Lua functions to be called at the beginning or at the end of the action. Action lists were created in Lua as tables which were then converted to C++ instances of Actions.

But then I realized: why do I need C++ here? What if I implement all Actions in Lua and then call each Action List’s execute function inside some **ActionListManager:update**? And that’s what I did! Now all actions and action lists are implemented, created and stored in Lua! The implementation is much easier to modify, expand and use.

At one point I needed some Lua OOP lib for implementing stuff and I used [middleclass](https://github.com/kikito/middleclass) for that.

Here’s an example of **DelayAction** in Lua:

local Action = require("action") local DelayAction = class("DelayAction", Action) function DelayAction:initialize(params) Action.initialize(self, params) self.time = params.time self.currentTime = 0 end function DelayAction:update(dt) self.currentTime = self.currentTime + dt if self.currentTime >= self.time then self.isFinished = true end end return DelayAction

This action just waits for specified amount of time and then is marked as finished when the time passes. It can be created like this:

local action = DelayAction { time = 500 } -- wait for 500 ms

**Note**: DelayAction{…} is equal to this function call: DelayAction({…}) just in case you’re confused. I didn’t know about that Lua allowed this for a long time.

And [here](http://pastebin.com/nWVkUG7D)‘s another, more complex example with lots of different actions being done.

The gif below shows how each action of this ActionList are executed in a cutscene:

![lgaocuw](../../assets/97643290cb906968.gif)


What’s great is that new action types can easily be added in Lua which allows fast iteration for me and some great modding capabilities in the future!

#### Writing Lua is easy and relaxing

Rewriting stuff from C++ to Lua and writing new stuff purely in Lua was a great experience. In the past I’ve used Lua mostly just for calling C++ stuff, but now I’ve realized that I can actually do a lot more in Lua. And writing pure Lua code is amazingly fast compared to C++. It’s more compact too sometimes. Just by rewriting C++ stuff in Lua, I’ve got rid of ~1.5k lines of code!

It’s hard to explain what makes Lua so easy to write compared to C++, probably it has to do something with dynamic typing (imagine if **auto** and function templates were everywhere), heterogeneous containers (tables), awesome arrays and really cool dictionaries (tables again!).

Someone said that writing Lua is pretty close to writing pseudo-code and I fully agree. Sometimes I just write some pseudo-code which is close to Lua and then I realize that I can easily transform it into valid Lua code just by doing some small modifications. Isn’t that amazing?

#### Burning bridges and praising the Sun

![cmb0ifbxeaeeewb](../../assets/474bfeb5181e2c54.jpg)


[LuaBridge](https://github.com/vinniefalco/LuaBridge) was a Lua/C++ binding library I’ve used for a very long time. It was pretty great, but certainly wasn’t perfect and had some pretty serious faults. Recently I’ve come across amazing library called [sol2](https://github.com/ThePhD/sol2) and it amazed me right away.

It has everything I ever wanted from Lua/C++ binding library and even more! It isn’t perfect, but it does everything that I need and it does it pretty fast.

There’s a lot of stuff to be said about sol2, but I think I’ll devote an entire article to it.

Still, here are some things I like about it:

- Written in modern C++, no crazy macros needed
- Currently maintained and expands very quickly
- Has lots of features which lots of libraries don’t have
- Very fast!
- Has very clean and simple interface. Lua stack is completely hidden from you
- Works with Lua 5.1-5.3. and LuaJIT without noticeable differences

Right now I’m helping [The PhD](https://github.com/ThePhD) (the creator of sol2) to make the library better. The amount of work being done on the project by him is just incredible and there are some changes I’ve proposed that already became part of the library.

Sol2 is pretty close to being the best Lua/C++ library ever.

I’ve managed to port all my Lua/C++ code from LuaBridge to sol2 in a couple of hours thanks to wrappers I’ve made around LuaBridge. I’ll show how they work and why you should make them in the next **Using Lua with C++ in Practice** article.

## End of part 1

That’s it for now, thanks for reading!

The next part as I said will be about in-game dev tools and some major C++ refactorings I’ve done. See ya!

Don’t miss the second part by following me: [@EliasDaler](https://twitter.com/EliasDaler)