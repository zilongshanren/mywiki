---
title: Rusher 2.1 – Introduction & Migrating from 2.0 | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/07/rusher-2-1-introduction/
author: Allen Chou
published: '2012-07-09'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

By merging into [Rusher](https://allenchou.net/rusher.googlecode.com) what I’ve learned at [DigiPen](https://www.digipen.edu/), mostly from Game Engine Architecture Club lectures, I’ve secretly marked it version 2.1 a while ago.

For convenience, here’s a quick list of what’s new and what’s removed in version 2.1:

- A brand new engine-system and entity-component framework. The concept is the same, but the interface is much more polished and consistent. The core part of the engine still makes use of
[SwiftSuspenders](https://github.com/tschneidereit/SwiftSuspenders/)for dependency injection and management. - A simplified
**Renderer2D**system has taken over the old camera-layer based one. I think it makes more sense for the developers to decide what type of systems they want to use themselves. - An extension for
[Starling](http://gamua.com/starling/)is available. It’s pretty much the mirrored version of the new**Renderer2D**system and**RenderTarget**component class. - The new
**Action List**framework replaced the old**command**and**state machine**framework. I’ll write a dedicated post on action lists later. - Components no longer “update” themselves. They are pretty much “passive” in version 2.1. If you want to have an “active components” that update themselves, then you’d need to create a system to update them. More on this topic later.

Now I’ll cover some of the immediately important topics in detail.


### Reference Management & Dependency Injection

The `[Inject]`

metadata tag still works in the same way. But if you choose to obtain an object reference later on in the game instead of at the time of injection, you may make use of the newly-added `getInstance(Type:Class, name:String="")`

method that is conveniently available in almost every scope. This method makes use of the underlying injector to obtain object reference and thus takes what you’d expect as arguments: a class type and an option name string for further differentiation.

var transform:Transform2D = getInstance(Transform2D);

The mapping rule to obtain object reference is the same:

- The name is not required for systems, since there can only be on instance for each system class.

### Component Updates

One major change in version 2.1 is the update sequence management. Previously, all components are updated, which is not necessary since some components are just for holding data. In Rusher 2.1, if an object is to be updated, then the class should define an update method like `udpate(dt:Number)`

, and add itself to some other object that is able to update it. For instance, the `RenderTarget2D`

component class overrides the `Component.init()`

method, which is invoked when the component is added to an entity, to register itself to the related `Renderer2D`

system through the `Renderer2D.register(component:RenderTarget2D)`

method. It is the client’s responsibility to define a component update method and a system register method.

//RenderTarget2D component class override public function init():void { getInstance(Renderer2D).register(this); }

The class also overrides the `Component.dispose()`

method, which is invoked when the component is removed from an entity, to unregister itself from the renderer system through the `Renderer2D.unregister(component:RenderTarget2D)`

method. It’s also the client’s responsibility to define a system unregister method.

//RenderTarget2D class override public function dispose():void { if (displayObject_ && displayObject_.parent) { displayObject_.parent.removeChild(displayObject_); } Renderer2D(getInstance(Renderer2D)).unregister(this); }

The `Renderer2D`

system class internally has an `InList`

(intrusively linked list) object that keeps the chain of registered components, where the `RenderTarget2D`

component class ultimately extends the `InListNode`

class for this to work.

//Renderer2D system class override public function update(dt:Number):void { var iter:InListIterator = targets_.getIterator(); var target:RenderTarget2D; while (target = iter.data()) { var displayObject:DisplayObject = target.displayObject; if (displayObject) { var transform:Transform2D = target.getInstance(Transform2D); var displayTransform:Transform = displayObject.transform; displayTransform.matrix = transform.calculateMatrix(); displayObject.transform = displayTransform; } iter.next(); } }

This is just an example of how you can manage an internal update list in a system; you can of course implement one in your own way.