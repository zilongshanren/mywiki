---
title: Rusher 2 – Getting Started | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/10/rusher-2-getting-started/
author: Allen Chou
published: '2011-10-24'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

[View Cursor example](http://rusher.googlecode.com/svn/trunk/examples/Cursor/bin/index.html)

[View Keyboard example](http://rusher.googlecode.com/svn/trunk/examples/Keyboard/bin/index.html)

[Example source](http://rusher.googlecode.com/svn/trunk/examples/)

In this tutorial I’ll show you how to put together two minimalistic games, or two very simple applications in particular, one with mouse control, and one with keyboard control.

**Extending The Engine**

First, you’ll need to extend either the `Engine`

class or `BasicEngine`

class. The `Engine`

class is the most abstract game engine, without any systems added to it. The `BasicEngine`

extends the `Engine`

class and already has some basic systems added to it, including the `Clock`

system, the `Mouse`

system, and the `Keyboard`

system (not all of the added systems are listed here).

You override the `addSystem()`

method and add new systems here. The system manager is passed in as an argument for you to add systems to. Here we add two systems to the engine, which we will write later. The `DisplayObjectUpdater`

is the system that updates every entity’s view with their position data, although we’ll pretty much create only one entity in this example. The `EntityCreator`

system gives our game a “kick start” by creating an entity and adding several components to it.

Our document class looks like this. It passes a sprite to the engine constructor, where the sprite is intended to be the main container.

public class Main extends Sprite { public function Main() { var canvas:Sprite = new Sprite(); addChild(canvas); var engine:IEngine = new CursorExampleEngine(canvas); engine.start(stage); } }


And this is what our engine extension looks like. Note that you must first call the `addSystems()`

method defined in the superclass, otherwise the aforementioned systems will not be added first.

public class CursorExampleEngine extends BasicEngine { private var _canvas:Sprite; public function CursorExampleEngine(canvas:Sprite) { _canvas = canvas; } override protected function addSystems ( systemManager:ISystemManager ):void { super.addSystems(systemManager); systemManager.addSystem(new DisplayObjectUpdater(_canvas)); systemManager.addSystem(new CursorCreator()); } }

**The **`Position`

and `View`

Components

`Position`

and `View`

ComponentsWe are going to write a component class that stores an entity’s spacial data, the 2D (x, y) coordinate. It’s as simple as declaring two variables named `x`

and `y`

. Also, you’ll need to implement the `IComponent`

interface for this to be added to an entity. This interface required that a `dispose()`

method be implemented. In this method you should clean up any resource that is no longer needed. Since this component only has two primitive properties, it’s okay to just leave this method blank.

public class Position implements IComponent { public var x:Number; public var y:Number; public function Position(x:Number = 0, y:Number = 0):void { this.x = x; this.y = y; } public function dispose():void { } }

Next, the `View`

component. This component is for holding a reference to an entity’s corresponding display object. The code looks pretty much straightforward and similar to the `Position`

component.

public class View implements IComponent { public var display:DisplayObject; public function View(display:DisplayObject) { this.display = display; } public function dispose():void { } }

**The **`CursorController`

Component

`CursorController`

ComponentThis component listens to the `Clock`

system and updates every frame. When it updates, it assigns the current mouse position to the `Position`

component of the same entity. Thus this component needs three references: the `Clock`

system, the `Mouse`

system, and the `Position`

component. We’ll use Dependency Injection to obtain these references.

After the dependencies are injected, we’ll need to listen to the clock, so we mark a method with the `[PostConstruct]`

metadata tag, so this method will be invoked right after the dependencies are injected.

Also note that in the implemented `dispose()`

method we actually are going to write something. We need to remove the listener function from the clock and dispose of all the references at hand.

public class CursorController implements IComponent { [Inject] public var clock:Clock; [Inject] public var position:Position; [Inject] public var mouse:Mouse; public function CursorController() { } [PostConstruct] public function listenToClock():void { clock.add(update); } private function update(dt:Number):void { position.x = mouse.x; position.y = mouse.y; } public function dispose():void { clock.remove(update); clock = null; position = null; mouse = null; } }

**The **`DisplayObjectUpdater`

System

`DisplayObjectUpdater`

SystemNow it’s time to write the system that updates the position of display objects according to the `Position`

component of the same entities.

This time let’s take a look at the final code first, and I’ll explain it afterwards.

public class DisplayObjectUpdater implements ISystem { [Inject] public var clock:Clock; [Inject] public var entityManager:IEntityManager; private var _canvas:Sprite; public function DisplayObjectUpdater(canvas:Sprite) { _canvas = canvas; } private var entities:IEntityCollection; public function onAdd():void { clock.add(update); entities = entityManager.getEntityCollection(RenderNode); entities.onAdd.add(addChild); entities.onRemove.add(removeChild); } private function addChild(node:RenderNode):void { _canvas.addChild(node.view.display); } private function removeChild(node:RenderNode):void { _canvas.removeChild(node.view.display); } private function update(dt:Number):void { var iter:IEntityIterator = entities.getIterator(); var node:RenderNode; while (node = iter.current()) { var display:DisplayObject = node.view.display; var position:Position = node.position; display.x = position.x; display.y = position.y; iter.next(); } } public function dispose():void { clock.remove(update); clock = null; entities.onAdd.remove(addChild); entities.onRemove.remove(removeChild); entities = null; entityManager.disposeEntityCollection(RenderNode); entityManager = null; } }

Similar to the components, a system class has to implement an interface, the `ISystem`

interface, which requires the implementation of two methods: `onAdd()`

and `dispose()`

. The `onAdd()`

method will be invoked after a system is added to the engine and the dependency injection is finished. The `dispose()`

is for resource clean-up, which will be invoked after the system is removed from the engine.

How does the system obtain every single reference of every entity that has both a `Position`

component and a `View`

component? Don’t worry, the entity manager takes care that for you. All you have to do it use the `IEntityManager.getEntityCollection()`

method. You pass a class reference to this method, which should extend the `EntityNode`

class and should specify that it needs both the `Position`

component and the `View`

component. We’ll see the code for the `RenderNode`

class later.

The entity collection has two signals we need to listen to, the `onAdd`

and `onRemove`

. They are dispatched when a new entity with the two desired components are added to the collection. So, we simply add the display object of the new entity to the display list, and we remove it from the display list, respectively.

In the `update`

method, we generate an **iterator** that allows you to **traverse** through the collection by invoking the `IEntityCollection.getIterator()`

method. A fresh iterator should point to the first node in the collection. The `IEntityIterator.current()`

method returns a reference to the current node it’s pointing to, if the iterator is pointing past the last node, the method returns a null value. The code>IEntityIterator.next() method makes the iterator to point to the next node in the collection. We make use of these two methods to pull out information about each of the entities in the collection, again, although there is only one entity in this example.

Now it’s time to take a look at this mysterious `RenderNode`

class. It’s quite simple, actually. You override the `getNeededComponents()`

method and return an array of class references of the components you need, and you pull out the information in the overridden `pullComponents()`

method. A `Dictionary`

is used here. The key is the component class reference, and the value would be the actual component object of the entity.

public class RenderNode extends EntityNode { public var position:Position; public var view:View; override protected function getNeededComponents():Array { return [Position, View]; } override protected function pullComponents ( components:Dictionary ):void { position = components[Position]; view = components[View]; } }

**The **`EntityCreator`

System

`EntityCreator`

SystemThis is in fact a “one shot” system, which creates entities we need and does nothing afterward. This isn’t what a system is supposed to do, but for convenience, we’ll use a system this way. In later tutorials, I’ll show you how to perform “one shot” actions using the Command system.

Here’s the code for the system class.

public class CursorCreator implements ISystem { [Inject] public var entityManager:IEntityManager; public function CursorCreator() { } public function onAdd():void { Mouse.hide(); var cursor:IEntity = entityManager.createEntity(); cursor.addComponent(new Position()); cursor.addComponent(new View(new CursorGraphics())); cursor.addComponent(new CursorController()); } public function dispose():void { } }

We only need to focus on the `onAdd()`

method. An entity is created using the `IEntityManager.createEntity()`

method, and components are added to the entity using the `IEntity.addComponent()`

method. The `CursorGraphics`

class is just a display object subclass for the cursor appearance.

That’s it! Our game is finished. Isn’t it fantastic that all you need to focus on is the game logic instead of the architecture concerning reference management? All thanks to [SwiftSuspenders](https://github.com/tschneidereit/SwiftSuspenders)!

**The Keyboard Example**

Wait! I mentioned this tutorial has two examples, right? The other example is similar to this one, only that it uses a keyboard to control the entity. So, I’ll just show you the code worth mentioning, the `KeyController`

component class.

Instead of adding a `CursorController`

component in the `EntityCreator`

system, you add the `KeyController`

component instead.

public class KeyboardController implements IComponent { [Inject] public var clock:Clock; [Inject] public var position:Position; [Inject] public var keyboard:Keyboard; public function KeyboardController() { } [PostConstruct] public function listenToClock():void { clock.add(update); } //400 pixels per second private const SPEED:Number = 400; private function update(dt:Number):void { var dx:Number = 0; var dy:Number = 0; if (keyboard.isDown(Key.RIGHT)) dx += SPEED; if (keyboard.isDown(Key.LEFT)) dx -= SPEED; if (keyboard.isDown(Key.UP)) dy -= SPEED; if (keyboard.isDown(Key.DOWN)) dy += SPEED; //one of dx and dy is not zero if (dx || dy) { //both dx and dy are not zero if (dx && dy) { //normalize dx *= Math.SQRT1_2; dy *= Math.SQRT1_2; } //update position position.x += dx * dt; position.y += dy * dt; position.x = RusherMath.clamp(position.x, 20, 780); position.y = RusherMath.clamp(position.y, 70, 530); } } public function dispose():void { clock.remove(update); clock = null; position = null; keyboard = null; } }

I won’t go through the code in the `update()`

method, because I know you’re clever enough to figure that out yourself 🙂

The complete source code for these two examples with proper imports can be found on Rusher 2’s [example repository](http://rusher.googlecode.com/svn/trunk/examples/).

Hvae fun 🙂