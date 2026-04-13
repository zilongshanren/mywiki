---
title: Unifying Cocos2D and Sprite Kit with OpenGW
url: http://www.learn-cocos2d.com/2013/10/unifying-cocos2d-sprite-kit-opengw/
author: Warmi Says
published: '2013-10-03'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

How to write code that is relevant for both Cocos2D and Sprite Kit, and as an extension to that the Kobold (2D/Touch/Kit) projects?

Because for the past months I shifted my attention to Sprite Kit, in order to create Kobold Kit and an accompanying Starterkit. While it’s obvious that Sprite Kit has everyone’s attention, I don’t want to turn my back on cocos2d-iphone and KoboldTouch. So from that came the need to create as much code as possible in a portable way.

The result is **OpenGW**, the world’s first game world simulation engine available to the public (in Nov/Dec). This is the holy grail I’ve been unknowingly searching for the past couple years!

## What is OpenGW?

OpenGW stands for **Open** **G**ame **W**orld.

It is a data-driven, engine-agnostic, cross-platform **game world simulation engine**.

I’ve set up a stub page where you’ll find [more info on OpenGW](http://opengameworld.com/).

## Why OpenGW?


The gist of game programming - this may come as a surprise to some - has **absolutely nothing** to do with putting things on the screen! What you see on the screen is just the result of the game’s current simulation state. All data and processes, no visuals. That is, if you write it “properly”.

It’s natural for a beginner to take the most direct, magic numbers, global variables, singletons, copy & paste, “add more stuff in whatever class/method you’re currently in” type of approach.

As you gain experience, your code becomes better, more structured, more modular. But you’re always tempted to take shortcuts (and you *will* take them) and do things quickly which you’ll come to regret further down the road.

### How I learned to love the code

For me it was very hard to grasp “separation of concerns”, and even to understand why it’s always important. Programming for a AAA game title was an eye-opener. But I believe where I learned the most from was doing game programming and simultaneously working on a different, almost entirely self-designed internal app.

On the game side we had a clearly modular game and rendering engine, with one big module being responsible for driving the game simulation. It was completely decoupled from audio, visuals and networking. It gave me a framework to work in, providing guidance on how to do things just by looking at existing code. Almost naturally my code became modular, reusable, flexible, extensible.

On the other hand I was tasked to create a database frontend application. In C# using .NET and several 3rd party frameworks for the user interface with Hibernate connecting to a SQL database, while also designing and administering the database. I had nothing to build on - zero, zilch. C#, .NET, Hibernate were new technologies to me, as was designing and writing a User Interface application that needed to satisfy both end users while avoiding the pitfall of having to custom-code each and every new table or data column.

Suffice it to say, this wasn’t my best code despite good intentions. Some good decisions didn’t work so well with the database or user interface layer. Some bad decisions haunted the project for a long time. What’s worse, the design of hibernate and the database and the design of the user interface were diametrically opposed. There are techniques to handle all of this, but having no blueprint and not keeping the different layers cleanly separated made this a very difficult, taxing project with a less than optimal codebase.

This taught me one thing: if you have a good, solid framework to work in that provides plenty of good examples, writing code is not only going to be easier but it will naturally fit much better into the design of the framework. If the framework is designed well, you’re going to write better code as a consequence!

### Your code is only as good as the engine’s code

Yet that means bad engine design leads to bad developer code, or at least greater effort to write good code.

I always disliked cocos2d-iphone’s design because of what it does to and teaches its users. It is an example of not-so-great-but-it-works-ok design from the perspective of the engine. I’m happy Apple cleaned up the mess, I’m disappointed that their design also lends itself towards subclassing rather than encouraging to write code that works on any node (that’s what behaviors do in [Kobold Kit](http://koboldkit.com/) btw).

Bad engine designs teach users the wrong priorities: that it’s okay to subclass specific views to put your game code in it. That it’s okay to use singletons in the first place, and in the worst case to “bridge gaps” (connect nodes) between branches of the node hierarchy. That it’s acceptable that multiple nodes will process the same input events. That actions can be used as a substitute for actual game logic. That code is always tightly coupled with the engine.

Worst of all: that there is no separation of visuals, audio and input from game logic code. This mixing becomes a problem real quick, even for the smallest projects.

I took a different approach with KoboldTouch, building a MVC framework where cocos2d is demoted to the view, controllers create the hierarchy, and models (and/or controllers) host the game logic. One issue was that cocos2d kept fighting back, always trying to penetrate the framework’s design. Ultimately the separation isn’t as clean as I had hoped it to be, but it was an improvement.

Out of necessity Kobold Kit has a slightly altered design, where the view (nodes) form the hierarchy and the controller attaches itself to a node, and is optional. The controller still hosts the model but it also hosts behaviors, which are code plugins to alter the behavior of any node (ie turn a sprite into a button that responds to touches and clicks).

Component based programming is very powerful. Interestingly I didn’t know until I searched for a good article on CBD that I saw Ray Wenderlich has an [introduction to component based development](http://www.raywenderlich.com/24878/introduction-to-component-based-architecture-in-games) that will help you understand what OpenGW does. And here’s a very instructive article that [shows by example how a monolithic class can be refactored to one that uses components](http://gameprogrammingpatterns.com/component.html).

Anyhow, both Kobold Kit behaviors and Kobold Touch controllers are tightly connected to the view, and thus ultimately they would only work with a specific rendering engine. Sharing code between the two projects seemed rather pointless.

### How OpenGW came about

Not sure what exactly triggered the idea to create OpenGW. It definitely came out of writing the Platformer Starterkit for Kobold Kit. Perhaps the whole idea of running a business with a partner, creating multiple games and realizing what we’re creating isn’t exactly going to be a beginner’s starterkit covering the basics with complete tutorials.

What I was producing was game code and workflows that satisfy a professional developer’s needs, with a necessarily higher learning curve. And that learning curve was even higher before I started rewriting what I had in OpenGW exactly because it was so interwoven with the visuals, and no distinction made between code that only serves the user interface and visual layer, and code that runs the game logic.

One area where this lack of separation became a problem was the TMX object model. It is a complete representation of all the aspects of a TMX file: the map, its layers, tiles, tilesets, gids, objects, properties. In itself it is almost perfectly decoupled from anything engine-specific, minus the tileset textures.

But to run a game on the TMX object model meant looking up gids (tiles), cross-referencing them with what a gid does, checking properties of a tileset or object, and all that stuff. On top of that coordinates need to be converted because TMX has its origin in the upper left corner, not in the lower left. This wasn’t just bad for performance, it made the code clunky, bloated, difficult to grasp.

Somewhere in the process I remembered how we did things in the game simulation. I’ve always wanted to work within such a system again, but it never occurred to me that I could just rewrite it and that it would have great benefits.

### How things change

For example regarding the tilemap information spread over tiles, tileset, objects, layers and their properties. What I’m doing now with OpenGW is collecting all the information I need from the tilemap at load time - combining information from gids, objects and properties and creating a single memory buffer that contains bit-coded information for each tile. That becomes the world map in OpenGW.

There’s actually a class named OGWMap that manages a memory buffer as a “map” and enables you to do cool things like [enumerating the tiles in a certain rectangle](http://opengameworld.com/OpenGW/html/Classes/OGWMap.html#//api/name/enumerateElementsInPointRect:usingBlock:). Certainly Sprite Kit was an inspiration there.

While I’m working on and with OpenGW I can actually see my code improving. The Platformer starterkit code that used to be tied with Sprite Kit has shrunk down to under 200 lines of code, with thousands of lines of code now in OpenGW and at least half of it so generic (ie kinematics, collision detection) that it can be used for any type of game. It’s great knowing that this code is now preserved for all eternity - Sprite Kit or Cocos2D may come or go, this code will now remain relevant and useful past those engines and for multiple projects.

It’s things like these that make me believe that I’m on the right path. That OpenGW works with both KoboldTouch, cocos2d-iphone or any Objective-C (and later C++) game engine for that matter will give us the opportunity to provide the same Starterkit for all of these engines.

## When and how?

The goal is to make OpenGW available this year, November or December. It will be a paid product.

The idea is to put everyone in the same boat - one purchase to get access to OpenGW which as a bonus grants you access to KoboldTouch and Kobold Kit Pro. KoboldTouch customers will get OpenGW at no extra cost through their existing subscription. Once OpenGW is released new subscription plans and pricing will come into effect, though I can’t give you details simply because no thought went into that yet.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I am wondering why are you starting out with Objective-C while planning to “port” it to C++ later..

Seems like a wasted effort to me since any Objective-C code can work with C++ frameworks but not the other way around.

Why maintain two code bases while you can only maintain one with the same overall affect on accessibility of your framework?

Good question. I had to fight with myself for a time before I decided to do Objective-C first and port later. Which by the way I’m not sure whether to support 2 different codebases, or to rewrite in C++ with the ObjC API simply accessing the underlying C++ framework.

My rationale for deciding on Objective-C was:

- Objective-C allows me to develop faster. Less code to do the same thing.

- Objective-C gives me automatic memory management - I know C++ has shared_ptr, weak_ptr, etc but it’s still a manual process to actually use them.

- I’m now deeply rooted in Objective-C land. I wanted to worry and fight less with the language and focus mainly on the design rather than implementation details. This would have been difficult if I had to re-learn C++ and grasp the new concepts introduced in the past ~5 years.

- Objective-C enabled me to implement concurrent (multithreaded) updates with ease thanks to GCD.

- Objective-C frameworks get more buy-in from Apple developers who I am addressing first and foremost.

- Objective-C avoids “polluting” the code with .mm (Objective-C++) files necessary to mix ObjC with C++. Ugly.

- Had I done C++ first I’d be tempted to create the ObjC wrapper along with it - slowing development since any refactoring would have to be done twice.

- Oh, big point: Xcode can’t refactor C++ code.

- When I write C++ code I’ll want to do that in Visual Studio with Visual Assist X (plus some other tools) because this is hands down the best environment to develop C++ code in. Nothing gets even remotely close.

- C++ is a lowest common denominator. As such it’s always a compromise compared to higher-level languages like Objective-C but also C#. Unless you absolutely have to, it’s always better to write code in a higher-level language.

- Thought experiment: when I get to porting, I’ll want to try and write an automated ObjC to C++ code converter. That will be an interesting exercise. It might just work. At least getting the bulk of the work automated will be possible, like class header and property setter/getter.

On a separate note.

I think the idea of having sprite framework even having a concept of node (or any hierarchical structures) is a mistake to begin with.

You idea of using composition is a step in right direction but ultimately node transformations and sprite rendering are independent from each other and should not be grouped.

In my code I have a 2d rendering component which is solely concerned with rendering sprites - it has a simple interface in the form of (among other calls):

int drawSprite(const Transform2d &trans, const UvSet &uvSet=UvSet::Normalized, const ColorQuad &colorQuad=ColorQuad::White);

int drawSprites(const Transform2d *transArray, unsigned int transCount, const UvSet *uvSets, unsigned int uvSetCount, const ColorQuad *colorQuads, unsigned int colorCount);

Where Transform2d is a simple struct encapsulating rotation, scaling and translation

If you need hierarchical rendering ( children and parents) , there is a separate class which can maintain a collection of linked Transform2d using its own metadata and can be optimized to store them linearly ( for cache optimized traversal ) for static hierarchies.

The only thing you need to do is to call transform on it and you will get a pointer to Transform2d array which you can then pass to drawSprite.

It gives you everything a node does, but if you don’t care for hierarchical rendering ( say a large collection of flat sprites) you don’t need to pay a price for maintaining linked nodes for every sprite - in fact you can just keep an array of Transform2ds and be done with it (with all benefits of linear and cache friendly access.)

These two classes +a Material class, is all you really need to emulate majority of Cocos2d.

All sprites are always batched and don’t require any special batching code - it is done for you by simply setting current Material ( which encapsulates a texture or multiple textures and blending operations)

The flow is :

Renderer2d->setCurrentMaterial(Material *)

Renderer2d->drawSprite(sprites ..) // new material set , internally a new batch created

Renderer2d->drawSprite(sprites ..)

Renderer2d->drawSprite(sprites ..)

Renderer2d->setCurrentMaterial(Material *)

Renderer2d->drawSprite(sprites ..) // new material set , internal a new batch created etc

And then dump everything from Renderer2d to the screen - one batch for all sprites ( my engine is a 3d engine so 2d component encapsulated by Renderer2d is just another input in a large pipeline)

With this in place I can easily render 25 000 to 30 000 sprites per frame (of course thats on the CPU side/batching side - fill rate on the GPU is another issue ) while still having access , if needs be , to complicated sprite hierarchies.

I can create game specific structs encapsulating the world in any way I wish and the only link to the rendering component is the Transform2d …

I agree, mostly. A node hierarchy is a nice thing initially as a way to group nodes, and make them behave in unison (ie rotate around parent’s center, move parent to move all children, etc). So that can definitely be helpful to write less code.

But it also gets in the way, plenty of questions related to the fact that devs did not consider the parent affecting the child node’s behavior like position, rotation, visibility, etc.

At the end of the day, any collection of visuals is (should be) handled as a unique entity anyway, so a player composed of multiple sprites, labels, effects is a class that keeps these in synch and doing the right thing, using plug-in components (ie follow at offset, rotate around center point, wiggle within threshold) etc.

OTOH a scene hierarchy is often employed by game engines, whether 2D or 3D because it just helps to sort through entities and it’s the most versatile approach for really complex games.