---
title: Using Lua with C++ in practice. Part 1. Intro to ECS and basic principles
url: https://eliasdaler.wordpress.com/2015/08/10/using-lua-and-cpp-in-practice/
published: '2015-08-10'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Part 1**. Intro to ECS and basic principles**Part 2**. Implementing the basics**Part 3.**Controlling entities in Lua by calling C++ functions.

There are many reasons to use Lua with C++. One of them is that you can put some of the logic from C++ code into scripts, so you can easily change them without the need or recompilation. You can also write some good interfaces, so the scripts are easy enough for even non-coders to write them. Lua is free, Lua is fast, Lua is used in game development quite often.

While there are plenty of good articles about using Lua with C++, I think there are not enough articles about how to use Lua in real projects.

This article is one of the many articles I plan to write. Here are some topics which my articles will cover:

- Entity creation and other basic stuff (you’re reading this now)
- How to implement entity creation
- Managing Lua state and cleaning up
- Scriptable state machines
- Events and callbacks

The stuff described in the articles was mostly discovered during the development of my game called **Re:creation**.

I don’t think the methods here are perfect, but they’re good enough, fast and work well for me. So, your feedback is welcome. Feel free to leave comments and write e-mails to me about the stuff I can do better. I’m interested in hearing about your Lua/C++ usage!

While this is a C++ article, I think you can implement most of the things mentioned here in your favourite language. I’ll use Lua C API and LuaBridge for examples, so I recommend to read the following articles if you’re not familiar with them:


# Entity creation

My game’s engine is build around entity/component/system (ECS) model. Because there are lots of different ways to implement ECS. I’ll explain my approach.

**Entity** is every object you see (and don’t see, e.g. collision boxes, triggers, etc.) in the game: rocks, tress, NPC’s, etc. Each entity has a number of components which are stored in **std::vector<Component*>**.

**Component** is a data about a particular aspect of an entity. There are a number of different components: **GraphicsComponent** (contains info about sprite, texture, animations, etc.), **CollisionComponent** (information about bounding box, collision response function, etc.), **HealthComponent**, etc.

**Systems** are where logic lives. They store a list of pointers to components of currently active entities which they iterate through. They don’t care which entity the component belongs to. For example, **RenderingSystem** iterates through **GraphicsComponent**‘s and renders them in a particular order. **CollisionSystem** checks collisions between entities using their **CollisionComponent**‘s , etc.

What’s cool about ECS is that there is no complex inheritance tree and this solves lots of problems (blob-classes, deadly diamond problem, etc.).

Entities are created by creating components with different parameters and adding them to entity’s component list. Here’s a simple example of how it looks in C++ code:

Entity e; auto gc = new GraphicsComponent; gc->setSprite(entitySprite); ... // setting component properties e.addComponent(gc); ...

Here’s how I can get components by the class name (**get** function uses **dynamic_cast** to do this):

auto gc = e->get<GraphicsComponent>(); // gc is nullptr if entity doesn't have GraphicsComponent

Okay, pretty cool. But how do you create specific entities, like an NPC or a house? A [Factory pattern](https://en.wikipedia.org/wiki/Factory_method_pattern) may be used, but eventually you’ll have lots of different types of entities and customizing entity definitions would cause recompilation which is not very good. It will also be impossible for non-coders to create new entities or modify existing ones.

This is where Lua helps a lot.

Here’s an example of a simple Lua script:

![](../../assets/896e1394072ec5b6.png)


Note, that this script doesn’t create an entity. It’s simply used to obtain data to set different components parameters and then create Entity in C++. I create template entity using information from the script and then create instances of this entity class by copying. Here’s how the entity creation process works in general:

When loading template entity:

- Get entity table from script
- Get table keys list (this gives us a list of components to create)
- Create each component, passing corresponding table to component constructor (you’ll need to create an instance of class by class name. I’ll show one cool way to do that in the next article)

When creating other entities of this type

- Copy every component from template entity
- Assign unique properties of this entity (position, state, etc.)

# Why didn’t I expose component classes to Lua?

You can easily create C++ objects in Lua with LuaBridge (or a binding of your choice) like this:

someObject = SomeClass()

So why do I use tables and create components in C++ instead of creating them in Lua? There’s a number of reasons for this:

- Scripts look simpler this way

Imagine if the script looked something like this:

tree = function() gc = GraphicsComponent() gc.setFilename("res/images/tree.png") gc.setZ(0) gc.setAnimated(false) gc.setFrame(64, 0, 64, 74) cc = CollisionComponent() cc.setType("Solid") cc.setBoundingBox(14, 60, 32, 10) tree = Entity() tree.addComponent(gc) tree.addComponent(cc) return tree end

I don’t think that this script looks easier than the one I’ve shown before. And it may be difficult to read, understand and change for non-programmers.

- There’s no need for Lua to know about components at all. It’s better to hide implementation details in C++

Here’s an example of how I can set animation in a Lua script in my game:

setAnimation(entity, "some_animation")

This calls this function in C++:

void setAnimation(Entity* e, const std::string& animationName) { auto gc = e->get<GraphicsComponent>(); if(gc) { gc->setAnimation(animationName); } else { ... // write about error in a log! } }

Imagine if I had to do it like this in Lua each time I wanted to set some animation:

gc = entity.get("GraphicsComponent") if(gc ~= nil) then gc.setAnimation("some_animation") else ... -- print about error end

Not that easy anymore. And I have to do error checking in Lua. I think it’s a lot better to do it in C++ and hide implementation details there. Some functions may be even more complex in C++ but look very simple in Lua. Writing error checking in Lua would make scripts confusing and error-prone.

- You can optimize entity creation by moving some entity declarations into JSON/XML/binary files

You may notice that the Lua table presented before doesn’t hold any information which cannot be stored in JSON or XML. And this is true. If you create every component and entity in C++, you can easily move entity descriptions from Lua to JSON or XML to speed things up.

So what’s the point of using Lua then? Lua is used for adding different functions to entities and this makes scripting very enjoyable and lets me put lots of code in Lua instead of C++. This is very awesome, because it lets me easily change entity behaviour with no recompilation and hardcore a lot less. I can even change entity properties and functions **while the game is still running**! Isn’t this great?

# Scripting entity behaviour with Lua

Here’s an example when Lua functions are used to provide different entity behaviour.

For example, different entities may react differently to collisions.

Suppose I want to create a cute ghost which blushes when it collides with some entity (it also damages it. This is absurd, but hey, it’s just an example!). Here’s how it would look in the script:

![](../../assets/3e588fb40f2bfb88.png)


Here’s how it works: when **CollisionSystem** finds a collision between two entities, it calls a **collide** function which is stored in entity’s **CollisionComponent**. It also passes two arguments to the function: **this** – a pointer to the entity of the type which this function belongs to, **second** – a pointer to the entity which collided with **this** (**this** is a name of a variable I use, not a Lua keyword!)

# Conclusion

This article got pretty big so I’ve decided to explain implementation details in [the next part](https://eliasdaler.wordpress.com/2015/09/08/using-lua-with-cpp-in-practice-part-2/). You’ll learn some cool patterns and Lua stuff along the way. The next article will cover:

- Entity creation process
- Getting list of table keys
- Creating components by their names in C++
- Adding and using simple Lua callbacks to common events (collision, damage, etc.)

I hope that this article sparkled your interest in Lua. If you want to learn more, you can read my Lua articles on this blog (especially [this one](https://eliasdaler.wordpress.com/2014/07/18/using-lua-with-cpp-luabridge/) which will help you to configure Lua for the next article) to learn more about Lua or read [some of my dev logs](https://eliasdaler.wordpress.com/tag/devlog/) to see how I use Lua to solve problems during the development. Stay tuned, the next article will cover lots of stuff!

Hi,

Awesome article! I’m also trying to make my own game engine for learning purpose and I’d like to integrate Lua as scripting language. I found your articles about Lua are very helpful!

After I read this article,what I’m getting is that you have vector of Component in your Entity class, and you also have System class to create the desired Component object.

Ex: You have RenderingSystem class that also holds any GraphicsComponent that Entity has. I’d like to ask how you implement RenderingSystem class since I’m new to ECS pattern.

Sorry for bad english.

Thank you.

Thanks!

No, systems don’t create components, they simply have pointers to components they’re interested in.

For example, you can have this function:

And then you simply iterate over pointers in this system like this:

Hello

I am trying to implement lua into my game engine.

When loading scripts, should I create new lua_State for every script or use one global state for all scripts ?

Great article bdw :) Can’t wait for next part.

Hi.

I use one lua_State for every script because it lets me bind some C++ functions in this lua_State and use them in every script I want. If you use several lua_States, you have to bind those functions to each of them which is not good.

Thanks. Working on it. :D

Hello

I am currently trying to implement an ECS on my own and I would really like to know how you solved the communication between Systems. I am particularly interested in the RenderingSystem. It needs to know the location of the Entity to render the sprite/animation at the correct position on the screen. Where does it get this information from?

Michalis

Great work on the game btw, the re:creation mechanic is one of the most creative puzzle mechanics I have seen in a while :)

Hello. There are two solutions. One is to have systems which operate on multiple components, so RenderingSystem may have two lists of pointers: pointers to GraphicsComponent and pointers to PositionComponent. All components can have id of the entity they belong to, so you can easily find a corresponding PositionComponent by GraphicsComponent’s parent id. Or, you can just store pointers to a parent entity inside the component (this is what I currently do) and get PositionComponent from it.

Another way to do it is store position data and graphics data together. But then you’ll see that you need position data and collision data together too. Some people may suggest to duplicate data, which makes sense if you store components contiguously. This may lead to great perfomance, because cache misses are minimized, but this is harder to implement and properly maintain.

And thanks!

What about creating new components and systems in Lua? Did you try to implement something like that?

Didn’t try that out yet. But this is definitely possible with tables and metatables. Would be a cool thing to have, but I feel I don’t need it at the moment.

For now I have around 12 components and don’t think I’ll need much more, but who knows!

Lots of stuff is just easily scriptable. You don’t need DoorComponent, for example, you can just create DoorOpenState and DoorCloseState and write some script logic for those states. Same goes for other components which don’t need to have their own components.

As for systems… same thing. Maybe it’s because my game is so simple, but I didn’t add new systems and components for like a year and I’ve made a lot of progress this year. :)

RE: “you can easily move entity descriptions from Lua to JSON or XML to speed things up.”

I’m not sure about this claim. _Maybe_ you can find JSON/XML parsers that happen to be faster than eg. LuaJIT’s parser, but those are still extremely slow representations of data to load (in the context of a video game). A better argument for performance might be creating a custom binary representation. In that case, you can memory map the binary file and read the data directly with little to no parsing.

Yeah, binary representation is probably the fastest you can get, but I’ve noticed that decent JSON parsers are ~3 times faster compared to Lua (not LuaJIT, this one can probably be as fast or even faster).

Another argument for not using Lua for all data is that you can easily load stuff in another thread without having to create another Lua state or trying to properly handle multi-threading with one Lua state which can be painful.

I think all these formats and features (XML/JSON/binary and multi-threaded loading) break the ability to add Lua functions within your data. At the end of the day I guess you have to think about your specific use case to do any optimizations.

Yeah, it totally depends on the use case. If the data you load is going to be used on Lua side, then it’s easier and better to store them in Lua and maybe even load it on Lua’s side.

If the data is going to be used on C++ side only, then using Lua is not so necessary. (But still, I find data stored in Lua tables a lot more visually appealing and easier to write compared to JSON and XML).

also, interesting to hear about Lua vs JSON parsing speed. I wonder how LuaJIT compares.

Have you seen this way of storing data in Lua? I think it’s pretty elegant. https://www.lua.org/pil/12.html

Yeah, it’s very nice way of doing things. I’m currently doing something similar, but with a more OOP approach using middleclass: https://github.com/kikito/middleclass

nice article you wrote, beautiful, could you kindly post more about Lua,LuaBridge and C++

Thank you! I plan on writing more, but currently very busy, so can’t tell exactly when new articles are going to come out, but they’ll be on my new blog: https://eliasdaler.github.io/

Hello ! Very interesting article ; interesting and inspiring ;-)

But, I’ve a question… Today, we are in 2021. Is there new way to do what you tell ? Is Lua still on-trend (in term of performance) ? Is there new way of binding c++ and Lua ? Would you still use the same tools today if you were building a new game ?

Maybe it is a message in a bottle, but, we never know, thank you for your answer ;-)

Have a nice day !

Hello.

> Is there new way to do what you tell ?

Yes, for example you can see that I’ve started to use data/script separation for initializing entities as explained here: https://eliasdaler.github.io/tomb-painter-first-dev-log/#data–script-separation

You can also check out how Don’t Starve does ECS and Lua scripts (the scripts are in the open once you install the game)

> Is Lua still on-trend (in term of performance) ?

Yes. As far as I’m aware, there’s no new languages which are as fast as Lua in terms in performance (especially LuaJIT). A lot of engines seem to use C# and even JavaScript for scripting/game logic, so that’s a valid alternative, but it’s not as easy to set-up.

> Is there new way of binding c++ and Lua

The best way to bind Lua and C++ these days is sol2 (https://github.com/ThePhD/sol2) – you should definitely use it as it’s the best in every regard (speed, API, feature support…)

> Would you still use the same tools today if you were building a new game ?

If you’re talking about the choice of scripting language – yes, I still like Lua the best.

ECS architecture is also nice (but I don’t bother much with strict ECS definition where every bit of logic is defined in systems and all components are laid down contigiously in the memory.

As for ECS I’d probably try entt (https://github.com/skypjack/entt) instead of implementing my own ECS. But I did it, so it works the best for me, but is it worth doing for everyone? Not really, probably.