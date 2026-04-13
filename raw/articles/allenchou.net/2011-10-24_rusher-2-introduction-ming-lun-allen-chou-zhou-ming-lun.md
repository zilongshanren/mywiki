---
title: Rusher 2 – Introduction | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/10/rusher-2-introduction/
author: Allen Chou
published: '2011-10-24'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

Here I’ll give a very brief introduction to Rusher 2, my next version of my component-based game engine for ActionScript 3.0.

**Component-Based Game Engine**

First off, what is a component-based game engine? In a component-based game engine, everything, literally everything, from physical information to AI behavior are represented as individual **component**. The most elemental unit in a component-based game engine is an **entity**, say the hero character, an enemy, or a collectable object in the game world. Each entity can have multiple components attached to it, fulfilling the entity’s logical purpose in the game. For instance, a hero character controlled by a player in the game can have: a physical data component, which contains the current position of the character; a view component, which holds a reference to a display object representing the appearance of the character in the game; and a controller component, which listens to player input from the player (keyboard, mouse, etc.) and then updates the physical data component by altering its underlying coordinate data.


![Hero Entity](../../assets/7cef66533a361183.png)


**Systems**

Much like entities, the engine itself also contains multiple components with different responsibilities, which are known as **systems**. The most basic game engine generally consists of four systems: a clock system, which “ticks” every frame in order to keep the engine up and running (basically the clock invokes the **main loop** every frame); an input system, which listens for player input; an update system, which listens to the input system and update the game logic accordingly; and a rendering system, which draws the game onto the screen based on the current game state.

**Dependency Injection**

In generally, maintaining the intertwining references in a game engine is a daunting task. For instance, an engine needs to know what systems are added to it, an entity keeps track of its own components as well as needs to access components of other entities sometimes, and a command object needs to hold a reference to the game engine that its command manager belongs to. All this could result in tons of code dedicated to reference management. Making sure every single reference required is passed around correctly and removed as necessary is not easy. Hence, Rusher 2 makes use of [SwiftSuspenders](https://github.com/tschneidereit/SwiftSuspenders), a [Dependency Injection](http://en.wikipedia.org/wiki/Dependency_injection) framework known for playing an important role in [Robotlegs](http://www.robotlegs.org/), one of the most popular [MVC](http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) frameworks.

SwiftSuspenders allows Rusher 2 to manage references in a very robost way. In any component class or system class, users can simply declare a public variable or a public function marked with the `[Inject]`

metadata tag, and Rusher 2 would use SwiftSuspenders to inject, or assign, the correct reference to the variable or to the arguments of the function.

For example, suppose we have a `Mover`

component class. Inside this class we want to listen to the keyboard input and alter the `Position`

component according. Of course, all these components belong to the same entity.

You need three references: one for the keyboard input system, from which you can query keyboard state; one for the `Position`

component, whose data you want to alter; and one for the clock system, which you listen to and update with each “tick”. So you declare three public properties marked with the `[Inject]`

metadata tag. When this component is added to an entity, Rusher will use an injector to assign the correct references to these properties. After the injection is complete, any public methods marked with a `[PostConstruct]`

metadata tag is invoked. This is what we want to make use of to start listening to the clock ticks. The listener method takes one argument of type `Number`

which is the time between two ticks, or two frames.

```
class Mover
{
[Inject]
public var keyboard:Keyboard;
[Inject]
public var position:Position;
[Inject]
public var clock:Clock;
[PostConstruct]
public function listenToClock():void
{
clock.add(listener);
}
private function listener(dt:Number):void
{
var dx:Number = 0;
var dy:Number = 0;
if (keyboard.isDown(Key.LEFT)) dx -= 10;
if (keyboard.isDown(Key.RIGHT)) dx += 10;
if (keybaord.isDown(Key.UP)) dy -= 10;
if (keyboard.isDown(Key.DOWN)) dy += 10;
position.x += dx;
position.y += dy;
}
}
```

It’s that simple, no extra reference management is required. You just mark the public variables with `[Inject]`

tags, and SwiftSuspenders takes care of the rest, assigning the correct references to the variables.

Adding this component to any entity that already has a `Position`

component will make the entity listen to the keyboard input and move accordingly. Beware, however, that adding this component to any entity that does **not** have a `Position`

component will cause SwiftSuspenders to throw out an error, because it cannot find the proper reference to inject.

```
entity.addComponent(new Mover());
```

Some interfaces that must be implemented are omitted in the sample code for brevity, which I will cover in future posts.

As a side note, in order for Dependency Injection to work properly, SwiftSuspenders requires that the following two compiler options be added while compiling:

```
-keep-as3-metadata+=Inject
-keep-as3-metadata+=PostConstruct
```

Pingback: Developer's Blog » Flex 5 UIComponent should have Behavior Design Pattern [part 2]

Is this a stable release?

Not yet. It’s an alpha release. I’m currently testing Rusher 2 by prototyping my school game projects with it. So far it’s been working fine. The interface, however, might change slightly throughout the testing.

BTW, you might want to pick a more meaningful name and email, because I almost thought your previous comments were spams and nearly deleted them by accident.

love this engine =)

Good Job