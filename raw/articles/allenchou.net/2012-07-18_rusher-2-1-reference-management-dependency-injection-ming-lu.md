---
title: Rusher 2.1 – Reference Management & Dependency Injection | Ming-Lun "Allen"
  Chou | 周明倫
url: https://allenchou.net/2012/07/rusher-2-1-dependency-injection/
author: Allen Chou
published: '2012-07-18'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

Rusher uses [SwiftSuspenders](https://github.com/tschneidereit/SwiftSuspenders/) for reference management and dependency injection. Reference management refers to the part of the engine that keeps track of all objects (including systems, entities, components, etc.) and exposes to client an interface to easily obtain references to any object. Dependency injection is a powerful feature where an **injector** automatically assigns references to objects through public properties and methods marked with the `[Inject]`

metadata tags.

In this post I’m going to talk about Rusher’s **reference mapping rules** that the `getInstance()`

method uses to determine which object’s reference is returned.


### Reference Management

Internally, Rusher uses the `Injector`

class from SwiftSuspenders to manage references. Think of an **injector** as a black box, where you tell the injector what **type** of instance reference you want, and provide an additional **name string** to distinguish between different instances of that type if there are more than one instances, and the injector would give back a reference to an instance of the given type, based on the **reference mapping rules**.

Rusher’s `getInstance()`

method is a wrapper around this mechanism, and not surprisingly, it takes two arguments: a **class reference** for type specification, and a **name string** (defaulted to empty string) to further distinguish instances if there are more than one instance of that type.

```
getInstance(TypeOfInstanceYouWant, "optionalNameString");
```

In Rusher, an engine instance holds an `engine injector`

that is the top-level injector of the entire engine. It uses the following reference mapping rule:

- A
**system class reference**is passed in: since there can only be one instance per system type, there is no need to provided an additional name string (therefore the default empty string is used). A reference to the only one instance of the given system type is returned. By the way, if a non-empty name string is provided, the mapping rule look-up would actually fail. - A
is passed in: as stated in previous tutorials, an engine can have multiple entities, so an additional`Entity`

class reference**name string**is required for the mapping process. The name string is the name used to create the entity through the`Engine.createEntity(name)`

method. - A
**component class reference**is passed in: an additional**name string**is required for mapping. A reference to a component instance of the given type, belonging to the entity of the given name, is returned.

The rules above are sufficient to obtain references to all systems, entities, and components. However, Rusher makes sibling reference acquisition even more convenient by creating an **entity injector** for each entity (components of the same entity are called **siblings**). Instead of the engine injector, the entity injector is used when a component of an entity calls the `getInstance()`

method. An entity injector **inherits all mapping rules** from the engine injector and defines an additional mapping rule:

- A
**component class reference**is passed in: if**no name string**is given, a reference to the**sibling**of the given component type is returned.

Now that you know the reference mapping rules in Rusher, let’s take a look at a slightly more advanced topic: dependency injection. You may make use of dependency injection to write cleaner code and acquire references more efficiently than using the `getInstance()`

method.

### Dependency Injection

Let’s say you have an **active component**, which is updated in every game loop. It’s called `CharacterController`

, and uses the `Input`

system to listen for user input to manipulate the `Transform2D`

sibling component. Remember that only systems are updated in each game loop iteration by the engine, not components, so we have to register the `ControllerController`

component in some system, say a system called `ControllerUpdater`

, and update the component through that system’s update method.

Somewhere in the engine initialization code, we add the `Input`

and `ControllerUpdater`

systems to the engine and create an entity with `Transform2D`

and `CharacterController`

components:

```
engine.addSystem(Input);
engine.addSystem(CharacterUpdater);
var character:Entity = engine.createEntity("character");
character.addComponent(Transform2D);
character.addComponent(CharacterController);
```

The purpose of the `CharacterUpdater`

system is to accept character controllers and update them. In this example, there’s only one character controller instance. This is how we’d design our system:

```
interface IController
{
function update(dt:Number):void;
}
class ControllerUpdater extends System
{
//an intrusively linked list
private var controllers_:InList = new InList();
public function
register(controller:IController):void
{
controllers_.add(controller);
}
public function
unregister(controller:IController):void
{
controllers_.remove(controller);
}
overtide public function update(dt:Number):void
{
var iter:InListIterator
= controllers_.getIterator();
//iterate through all registered controllers
//in this case, there's only one
var controller:IController;
while (controller = iter.data())
{
controller.update(dt);
iter.next();
}
}
}
```

And our `CharacterController`

component may look like this:

```
class CharacterController implements IController
{
private static const SPEED:Number = 10;
//invoked when added to entity
override public function init():void
{
//get the ControllerUpdater system
var updater:ControllerUpdater =
getInstance(ControllerUpdater);
updater.register(this);
}
//invoked when removed from entity
//or when the entity is destroyed
override public function dispose():void
{
//get the ControllerUpdater system
var updater:ControllerUpdater =
getInstance(ControllerUpdater);
updater.unregister(this);
}
public function update(dt:Number):void
{
//get the Input system
var input:Input = getInstance(Input);
//get the Transform2D sibling
var transform:Transform2D
= getInstance(Transform2D);
//move transform left and right
//based on the keyboard input
if (input.isDown(Key.LEFT))
{
transform.x -= SPEED * dt;
}
if (input.isDown(Key.RIGHT))
{
transform.x += SPEED * dt;
}
}
}
```

It looks all well and good, but notice how we invoke the `getInstance()`

method in the `CharacterController.update()`

method. The injector is used to look up to get the correct reference in every single game loop, and every time it returns the exact same reference. Doesn’t it sound inefficient? This brings us to `dependency injection`

. You might have been wondering why injectors are called injectors. Well, it’s because they are used for dependency injection. This mechanism is making use of ActionScript 3.0’s built-in [reflection](http://en.wikipedia.org/wiki/Reflection_(computer_programming)) feature. Not only can you look up what properties and methods an object has at run-time by using the [describeType()](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/utils/package.html#describeType()) function, you can also annotate properties and methods with custom metadata tags, which would be reflected at run-time on `describeType()`

calls.

If you annotate a **public property** with the `[Inject]`

metadata tag, at some point in the engine code, it would **inject** into objects by assigning correct reference to this public property, typically before the object starts to carry out its duty. We call this **dependency injection**. The same reference mapping rules are used while injecting dependencies.

For systems and components, before the `init()`

method is called, the dependencies are injected into the instance. So if you’re making use of dependency injection, make sure to access the injected properties (a.k.a. **injection points**) after the `init()`

method is invoked.

Now let’s modify our `CharacterController`

class so that it makes use of this one-time injection instead of calling `getInstance()`

in the `update()`

method.

```
class CharacterController implements Controller
{
//injection points
//--------------------------------------------
[Inject]
public var updater:ControllerUpdater;
[Inject]
public var input:Input;
[Inject]
public var transform:Transform2D;
//--------------------------------------------
//end of injection points
private static const SPEED:Number = 10;
override public function init():void
{
updater.register(this);
}
override public function dispose():void
{
updater.unregister(this);
}
public function update(dt:Number):void
{
if (input.isDown(Key.LEFT))
{
transform.x -= SPEED * dt;
}
if (input.isDown(Key.RIGHT))
{
transform.x += SPEED * dt;
}
}
}
```

See how clean the code has become? All calls to `getInstance()`

scattered throughout the code have been replaced by injection points. Also the code is more efficient since we only ask the injector to give a reference to the `Transform2D`

sibling once during the dependency injection, instead of calling `getInstance()`

in `udpate()`

that is called in every game loop.

The only drawback of this type of dependency injection is that we have to make injection points public, which some programmers might not like. This approach is called **property injection**; we actually have another option called `method injection`

. This pretty much does the same thing, except that dependencies are injected into the object through **public methods**:

```
class CharacterController implements Controller
{
[Inject]
public function inject
(
updater :ControllerUpdater,
input :Input,
transform :Transform
)
{
this.updater = updater;
this.input = input;
this.transform = transform;
}
private var updater:ControllerUpdater;
private var input:Input;
private var transform:Transform2D;
//the rest of the class omitted for clarity
//...
}
```

You may use the same dependency injection technique in your systems.

One last note on this example: systems and components are only added to the injector’s reference mapping table when they are added to an engine or entity, so we’d want to add the `Transform2D`

component to the entity before adding the `CharacterController`

component; otherwise, the injector would not be able to find the correct `Transform2D`

reference during dependency injection.