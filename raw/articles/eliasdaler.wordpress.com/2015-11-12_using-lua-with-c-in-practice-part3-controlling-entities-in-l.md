---
title: Using Lua with C++ in Practice. Part3. Controlling entities in Lua by calling
  C++ functions.
url: https://eliasdaler.wordpress.com/2015/11/12/using-lua-with-cpp-in-practice-part-3/
published: '2015-11-12'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Part 1**. Intro to ECS and basic principles**Part 2**. Implementing the basics**Part 3. Controlling entities in Lua by calling C++ functions.**

If you haven’t read the first part of the tutorial, I suggest you to read it, so you have a clear idea what’s going on. See the second part for the implementation details.

This article uses **LuaBridge** and if you’re not familiar with it, I suggest you to check out my tutorials about it. ([Pt1](https://eliasdaler.wordpress.com/2014/07/18/using-lua-with-cpp-luabridge/), [Pt2](https://eliasdaler.wordpress.com/2014/11/01/using-lua-with-c-luabridge-part-2-using-scripts-for-object-behaviour/)). If you’re using another Lua/C++ binding: that’s fine, you can totally implement everything I’m talking about with other bindings.

#### Intro

One of the coolest things in Lua is that you can call C++ functions from it. You can even register your own classes and call their member functions!

![](../../assets/3b7f6133d07d4908.png)


Suppose you have an entity class which contains a list of components:

class Entity { ... private: std::vector<std::unique_ptr<Component>> components; };

Suppose that you have a function which lets you get a component by its name.

What if you want to change animations in some Lua script? You can do it like this:

function someLuaFunction(entity) ... local graphics = entity:getComponent("Graphics") if(graphics) then graphics:setAnimation("someAnimation") end ... end

I believe that this is not a greatest way to do things, because exposing components to Lua is not really necessary. Woudn’t it be nice to hide all the implementation details in C++? Here’s how the code above may look:

function someLuaFunction(entity) ... entity:setAnimation("someAnimation") ... end


Much better! And here’s why:

- This code is easier to read, especially for non-programmers. If you’re working in a team which has non-programmers, this is very handy for game designers, level designers, artists, etc. They can much easily create scripts without knowing how the code which they call works. Even if you are a programmer, this is still a huge win, because you are less likely to make errors and don’t have to remember lots of stuff you have to check.
- If you expose lots of stuff to Lua, you have to do lots of error checking in scripts which is not very great. It’s much easier to do it in C++ because then you can safely use simple functions in your scripts.

Here’s an example. Let’s make our setAnimation safer.

void Entity::setAnimation(const std::string& animationName) { auto graphics = get<GraphicsComponent>(); if (graphics) { if(graphics->animationExists(animationName)) { graphics->setAnimation(animationName); } else { log("Entity doesn't have animation named " + animationName); } } else { log("Entity doesn't have a GraphicsComponent"); } }

Here’s how we can call this function from the script once it’s registered:

entity:setAnimation("someAnimation");

- Sometimes you need to do more complicated stuff and it’s nice to have C++ functions which do it for you, so you just call one function in Lua and you’re done! A huge function in C++ may be called from C++ with just one line of code. Scripts are becoming shorter while you still can achieve a lot with them.

#### LuaEntityHandle

Suppose we have Entity class which looks like this:

class Entity { public: ... // C++ only stuff // Lua bindings void setAnimation(const std::string& name); int getAnimationFrame() const; ... // etc. private: ... }

As you create more and more functions, the Entity class will become pretty hard to maintain. You may have hundreds of functions and this will make your Entity class very hard to read.

And by the way, passing the reference to Entity or pointer to Entity into Lua is not very safe. What if something goes wrong with the script and the Entity’s state is corrupted?

Here’s a better way to do stuff. Let’s make a LuaEntityHandle class. Here’s how it looks:

class LuaEntityHandle { public: ... // Lua bindings void setAnimation(const std::string& name); int getAnimationFrame(); ... // etc. private: Entity* e; }

Each entity has a LuaEntity handle which contains a pointer to the entity. Functions can be implemented like this:

void LuaEntityHandle::setAnimation(const std::string& animationName) { auto graphics = e->get<GraphicsComponent>(); if(graphics) { graphics->setAnimation(animationName); } else { ... // print error or something } }

And you register the class like this:

getGlobalNamespace(L) .beginClass<LuaEntityHandle>("LuaEntityHandle") .addFunction("setAnimation", &LuaEntityHandle::setAnimation) ... // etc .endClass();

Now, all you need to do is to pass these LuaEntityHandle’s inside some functions and use them as if they were entities.

For example, suppose you have a function which does some stuff to entity:

function doSomething(e) e:doSomeStuff() end

Here’s how you can call it from C++:

auto doSomething = getGlobal(L, "doSomething") doSomething(LuaEntityHandle(&entity));

Awesome, now all of the Lua/C++ binding code is in one place and you don’t have to worry about it too much.

Is there something we can improve? Of course! Take a look at this function call:

addFunction("setAnimation", &LuaEntityHandle::setAnimation)

We need to do this for each member function inside LuaEntityHandle. The first argument is the name which this function gets inside Lua. Most of the time you want this name to be exactly the same as in C++. Doing this by hand is not very good, because:

- You may write the function name wrong
- The function name may change and you’ll have something like this:

addFunction("setAnimation", &LuaEntityHandle::setCurrentAnimation)

This has some pros: you don’t have to change scripts when you change names in C++, but it also has cons: you need to keep C++ function name and corresponding Lua function name in your head.

So, let’s create a macro which will do all this stuff for us:

#define ADD_FUNCTION(x) addFunction(#x, &LuaEntityHandle::x)

And now you can do stuff like this:

getGlobalNamespace(L) .beginClass("LuaEntityHandle") .ADD_FUNCTION(setAnimation) .ADD_FUNCTION(getAnimationName) ... // etc

The main trick here is that I use preprocessor stringfication operator (#) which turns a macro parameter into a string constant. So, the preprocessor does half the job for us, neat.

#### Next part?

And that’s it for now.

Next time I’ll tell you about managing entity declarations in scripts and getting list of global names in Lua scripts, so you can easily load every entity template by loading a script file and processing it.

Subscribe to my blog or to [my twitter](https://twitter.com/EliasDaler) to not miss the next part of the tutorial.

Thanks for reading!

I have a question, how to register lua callbacks in C++?

if I have a lua function XXX and I want something like CPPManager.RegisterCallback(XXX)

how do I declare and store this in C++ for a later call?

Can’t find any info on the internet for luabridge.

Thanks

You can store luabridge::LuaRef to a function and then call it.

Write me an e-mail if you have more questions. I eventually plan to write a part about event management between Lua and C++.

Check this out for now:

http://en.sfml-dev.org/forums/index.php?topic=18062.msg139016#msg139016

I was right along with you through all of these tutorial, right up until the end of this one where you pass the entity reference to doSomething. I am unsure what LuaRefWrapper is in this instance and trying to pass a reference as in doSomething(&e) gives me the error `Assertion failed: (lua_istable (L, -1)), function push, file /Users/da5id/Projects/tutorials/cpp-lua-ecs/lib/luabridge/Source/LuaBridge/detail/Userdata.h, line 412.` Any insight would be much appreciated.

After poking around in the LuaBridge source and reading what you say very careful during the last section. I think that you might have a typo in the last part where you pass the LuaRefWrapper into doSomething. I believe you meant to pass in a LuaEntityHandle to the function, correct? This is the only way I could get this code working.

You’re correct! I’ll fix that, thanks. :)

I was wondering how to implement a GetComponent function? atm I’m passing a string a returning a base class but that doesn’t seem to be working as I can’t figure out a way to cast the base class pointer back into a subclass.

Component* getComponentByType(std::string type)

{

if (type == “Transform”)

return GetComponentByType();

return nullptr;

}

.addFunction(“getComponent”, &GameObject::getComponentByType)

Huh, I didn’t think of that, when I was doing the tutorial. Implementing such function wouldn’t be possible, I think. You should register functions like getGraphicsComponent, getCollisionComponent, etc.

If you have generic getComponent() function in C++, you will do this with LuaBridge:

.addFunction(“getGraphicsComponent”, &GameObject::getComponent)

.addFunction(“getCollisionComponent”, &GameObject::getComponent);

etc.

Hi !! Have you ever encountered this ?

https://stackoverflow.com/questions/20227690/luabridge-and-inheritance/20229241#20229241

// c++

class Entity

{

Component* getComponent(const std::string &name);

};

— lua

local cmp = entity:getComponent(“Transform”) — cmp is consider Component*

cmp:pos —

luabridge seemingly doesn’t support downcast automatically !!! how to solve it ?

I don’t work with LuaBridge anymore and I didn’t use inheritance with it. I recommend to use sol2 as the Lua/C++ wrapper now.