---
title: Rusher 2 – Composite Commands | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/10/rusher-2-composite-commands/
author: Allen Chou
published: '2011-10-24'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

[View Composite Commands example](http://rusher.googlecode.com/svn/trunk/examples/Composite Commands/bin/index.html)

[Example source](http://rusher.googlecode.com/svn/trunk/examples/)

The previous [command tutorial](http://www.cjcat.net/2011/10/rusher-2-commands/) covered the basics of simple command executions in Rusher 2. Here I’m going to show you how to make use of on of the two composite commands, the `SerialCommand`

.

Basically, a serial command does what its name suggests: it executes its **subcommands** in series, one after another. This heavily depends on the `Command.onComplete`

signal dispatched when the `Command.complete()`

method is invoked. Whenever the command’s job is complete, remember to invoke the `Command.complete()`

method; otherwise, things may not work out as you expect.

There is two way of adding subcommands to a serial command. First, pass in commands as constructor arguments in the order desired. Second, use the inherited `CompositeCommand.append()`

method to dynamically add subcommands in the order you’d like.

The example in this tutorial is going to be based on the previous command example. We’re only going to alter the `EntityCreator`

system.


First, we’ll need to mark the systems we need for dependency injection.

[Inject] public var entityManager:IEntityManager; [Inject] public var mouse:Mouse; [Inject] public var commandManager:CommandManager; [Inject] public var clock:Clock;

We’ll need a new array property to hold the `Position`

components of the 5 circles we’re going to control with commands.

private var _circlePositions:Array;

And below is the new `onAdd()`

method. Here we create 5 entities with a `View`

component and a `Position`

component. At the end we listen to the clock signal.

public function onAdd():void { _circlePositions = []; //create 5 circles for (var i:int = 0; i < 5; ++i) { var c:IEntity = entityManager.createEntity(); var p:Position = new Position(400, 300); c.addComponent(new View(new CircleGraphics())); c.addComponent(p); //push position components to array _circlePositions.push(p); } clock.add(update); }

In the clock listener, we constantly inspect the `Mouse.isPressed()`

query. Note this is different from the `Mouse.isDown()`

method, which returns true as long as the mouse button is held down. The `Mouse.isPressed()`

will only return true for one frame, and then it returns false until the next time the mouse button is released and pressed again. This is useful for actions depending on “one shot” mouse clicks.

private function update(dt:Number):void { if (mouse.isPressed()) { var moveCircles:SerialCommand = new SerialCommand(); for (var i:int = 0; i < 5; ++i) { //append tween command to serial command moveCircles.append ( new TweenNanoTo ( _circlePositions[i], 0.5, { x: mouse.x, y: mouse.y, delay: 0.025 * i, overwrite: true } ) ); } //execute the serial command commandManager.execute(moveCircles); } }

And we’re done! You can run the example and see how each circle starts moving after the previous circle is finished moving. These commands are chained together by the serial command.

The `ParallelCommand`

class is pretty much the same, only that all subcommands are executed simultaneously, and the parallel command fires a complete signal only when all the subcommands are complete.

Next up, state machines.