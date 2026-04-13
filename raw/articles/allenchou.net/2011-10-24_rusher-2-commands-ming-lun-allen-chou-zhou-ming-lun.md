---
title: Rusher 2 – Commands | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/10/rusher-2-commands/
author: Allen Chou
published: '2011-10-24'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

[View Commands example](http://rusher.googlecode.com/svn/trunk/examples/Commands/bin/index.html)

This tutorial will be a short and easy one, since it’s based on the [Keybaord example](http://rusher.googlecode.com/svn/trunk/examples/) in the [previous tutorial](http://www.cjcat.net/2011/10/rusher-2-getting-started/).

**The **`CommandManager`

System

`CommandManager`

SystemRusher 2 has a built-in command manager system, which is automatically added to the `BasicEngine`

. What is a command? It’s basically an object with encapsulated actions. In this way, it’s very easy to customly build your own commands and have them executed through a central system, the command manager system.

For more information on commands, you may refer to my tutorials on [ActiveTuts+](http://active.tutsplus.com/): Thinking in Commands [part 1](http://active.tutsplus.com/tutorials/actionscript/thinking-in-commands-part-1-of-2/) and [part 2](http://active.tutsplus.com/tutorials/actionscript/thinking-in-commands-part-2-of-2/).

If you have read about the Thinking in Commands tutorials and are excited about the serial and parallel commands, then you’ll get even more excited to know that Rusher 2 has them! Rusher 2 has a fully integrated command manager system that can execute serial and parallel commands in addition to simple commands. It’s okay if you have no idea what a serial and parallel command are. I’ll cover those special type of **composite commands** in later tutorials.

First thing’s first. Let’s have a quick flashback on what we have done in the `KeyController`

component class in the previous tutorial.


public class KeyboardController implements IComponent { [Inject] public var clock:Clock; [Inject] public var position:Position; [Inject] public var keyboard:Keyboard; public function KeyboardController() { } [PostConstruct] public function listenToClock():void { clock.add(update); } //400 pixels per second private const SPEED:Number = 400; private function update(dt:Number):void { var dx:Number = 0; var dy:Number = 0; if (keyboard.isDown(Key.RIGHT)) dx += SPEED; if (keyboard.isDown(Key.LEFT)) dx -= SPEED; if (keyboard.isDown(Key.UP)) dy -= SPEED; if (keyboard.isDown(Key.DOWN)) dy += SPEED; //one of dx and dy is not zero if (dx || dy) { //both dx and dy are not zero if (dx && dy) { //normalize dx *= Math.SQRT1_2; dy *= Math.SQRT1_2; } //update position position.x += dx * dt; position.y += dy * dt; position.x = RusherMath.clamp(position.x, 20, 780); position.y = RusherMath.clamp(position.y, 70, 530); } } public function dispose():void { clock.remove(update); clock = null; position = null; keyboard = null; } }

We need the `CommandManager`

system, so we’ll use dependency injection to obtain a reference to it. Add the two lines of code below in the `KeyboardController`

class:

[Inject] public var commandManager:CommandManager;

Now we’re going to swap out the two lines of code that actually “does something” to another component with commands.

Change the following two lines:

position.x = RusherMath.clamp(position.x, 20, 780); position.y = RusherMath.clamp(position.y, 70, 530);

to the following:

commandManager.execute ( new MovePosition ( position, RusherMath.clamp(position.x, 20, 780), RusherMath.clamp(position.y, 70, 530) ) );

The `CommandManager.execute()`

method will invoke the `execute()`

method of the `MovePosition`

command object, which is defined as follows:

public class MovePosition extends Command { private var _position:Position; private var _x:Number; private var _y:Number; public function MovePosition ( position:Position, x:Number, y:Number ) { _position = position; _x = x; _y = y; } override public function execute():void { _position.x = _x; _position.y = _y; complete(); } override public function dispose():void { _position = null; } }

Note that you must invoke the `complete()`

method in the command object, otherwise the command manager will not know if the command execution is complete. The consequence might not be obvious for this example. However, if you forget to invoke the `complete()`

method in a subcommand of a larger composite command, the entire composite command will “freeze”, waiting for your command to complete.

Run the game and you’ll see the exact same result as the Keyboard example, since we were just refactoring out game logics into command objects. However, it’s important that you should encapsulate inter-component data manipulation in commands. This way, your code is cleaner, your game flow is more visually self-explanatory, and most important of all, classes are more decoupled and class responsibilities are assigned more correctly.

Coming up next, composite commands.