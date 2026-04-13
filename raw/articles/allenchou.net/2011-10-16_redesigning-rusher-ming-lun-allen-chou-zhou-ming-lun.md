---
title: Redesigning Rusher | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/10/redesigning-rusher/
author: Allen Chou
published: '2011-10-16'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

The current version of [Rusher](http://code.google.com/p/rusher/) was based on the component-based architecture of [PushButton Engine](http://pushbuttonengine.com/). I’ve used Rusher with a couple of personal experiments, and I soon found out the fact that Rusher is simply “too fat”. Too much code is required to build even a simple game; lots of code was dedicated to reference passing and maintenance. I couldn’t find a way to solve this, so I kind of stopped working with Rusher at all for quite a while.

Lately I stumbled upon [Richard Lord](http://www.richardlord.net/blog)‘s [Asteroids](https://github.com/richardlord/Ember/tree/master/examples/asteroids) example based on the [Ember](https://github.com/tdavies/Ember) game framework. The classes in the engine are very loosely coupled with the use of [SwiftSuspenders](https://github.com/tschneidereit/SwiftSuspenders), a [Dependency Injection](http://en.wikipedia.org/wiki/Dependency_injection) library. SwiftSuspenders makes use of the [reflective](http://en.wikipedia.org/wiki/Reflection_(computer_programming)) nature of ActionScript 3.0 and enables developers to easily create loosely coupled classes. SwiftSuspenders is most famous for its use in [Robotlegs](http://www.robotlegs.org/), a [Model-View-Controller](http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) framework.


I’ve studied Ember’s source code and have drawn some inspiration from it. Now I’m trying to perform a complete redesign on Rusher; basically, I’m rewriting Rusher from the ground up. This time I make use of SwiftSuspenders for inter-component reference passing.

Originally in Rusher, a component reference must be obtained through a string query system.

class RendererComponent implements IActiveComponent { function onTick(dt:Number):void { var spatialComponent:Spatial2D = entity.getComponentByName("spatial2D"); displayObject.x = spatialComponent.x; displayObject.y = spatialComponent.y; } }

This might not seem to be a lot of code to write. However, behind the scene in Rusher, there is a central process manager that calls the onTick() method of all active objects every frame. When an active component is added to an entity, the entity makes sure this component is an active component and adds it to the process manager. Too much of checking and reference passing is going around, and this has made it quite difficult for me to maintain Rusher.

In the new Rusher architecture, the engine is initially “empty”. Developers can add Rusher’s built-in or customly built **systems** to the engine as they see fit. The most basic engine class only has a clock system, which essentially is working as the process manager. What is different, though, is with the use of SwiftSuspenders, the clock no longer has to keep references to active objects. Every component can obtain a reference to the clock by Dependency Injection (mostly through Constructor Injection), and it can listen to the “clock ticks” dispatched with [Robert Penner](http://robertpenner.com/)‘s [AS3 Signals](https://github.com/robertpenner/as3-signals), an [Observer](http://en.wikipedia.org/wiki/Observer_pattern) system.

Without me having to write code in Rusher to handle active components, a component listens to clock ticks as shown below.

[Inject] class RenderComponent { private var _spatialCopmonent:Spatial2D; //code omitted for the "displayObject" property public function RenderComponent ( clock:Clock, spatialComponent:Spatial2D ) function onTick(dt):void { displayObject.x = spatialComponent.x; displayObject.y = spatialComponent.y; } }

You can see how a reference of the spatial component is also obtained through Constructor Injection, all done with the awesome SwiftSuspenders 🙂

Also, previously in Rusher, each component needs a name string for reference purpose. Now all you have to do is write out the component classes you want an entity to have.

var spaceShip:IEntity = createEntity("ship"); spaceShip.addComponent(Position); spaceShip.addComponent(Controller); spaceShip.addComponent(View);

The component classes now needn’t to extend a base class. Almost everything in the new Rusher works with interfaces. This conforms to one of the OOP design principles: “Favor composition over inheritance.”

I have less school work at [DigiPen](https://www.digipen.edu/) next week, so I hope I can at least finish the basic features in the new Rusher and create some tests and examples.