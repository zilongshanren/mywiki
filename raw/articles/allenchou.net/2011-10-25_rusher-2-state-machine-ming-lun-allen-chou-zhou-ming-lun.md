---
title: Rusher 2 – State Machine | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/10/rusher-2-state-machine/
author: Allen Chou
published: '2011-10-25'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

[View State Machine example](http://rusher.googlecode.com/svn/trunk/examples/State Machine/bin/index.html)

[Example source](http://rusher.googlecode.com/svn/trunk/examples/)

This tutorial introduces the `StateMachine`

system in Rusher 2.

**States and State Machines**

In Rusher 2, the `StateMachine`

class is used as a component class, where its subclass `StateSystem`

is a state machine system that can be added to a game engine. No matter you’re using a state machine component or a state machine system, the `State`

class can be extended and used in both cases.

The `Command`

class defines the following methods (not all are listed):

public function onSet():void; public function getEnterCommand():Command; public function getExitCommand():Command; public function update(dt:Number):void; protected final function goto(state:State):void;


The `onSet()`

method is invoked when the state is set as the current state of the state machine.

The `getEnterCommand()`

should return a command which will be executed when the state machine is about to enter this state. The `onSet()`

method is invoked after the enter command is completed.

The `getExitCommand()`

should return a command to be executed when the state machine is leaving this state, when the `StateMachine.setState()`

method or the `State.goto()`

method is called. After the exit command is completed, the state machine will start executing the enter command of the new state.

The `update()`

method is invoked in each game loop. You can make use of this method to query the game state and determine whether you want to enter a new state by invoking the `goto()`

method.

Note that due to the use of commands, the`CommandManager`

system must be added to the engine prior to any state machine system.

**State Machine Example**

Again, we’re going to base our example on the previous [Keybaord example](http://rusher.googlecode.com/svn/trunk/examples/).

Instead of using the `KeyboardController`

component to control the circle on the screen, we’re going to use the `StateMachine`

component.

So in the `EntityCreator`

system, we swap the line below:

circle.addComponent(new KeyboardController());

with this:

circle.addComponent(new StateMachine(new CenterState()));

The `StateMachine`

constructor takes one optional argument, which is the initial state object.

Here’s what the `CenterState`

class looks like. Basically the enter command tweens the circle position to the center of the screen, and the `update()`

method queries the `Keyboard`

system and enter to other four states accordingly.

public class CenterState extends State { [Inject] public var position:Position; [Inject] public var keyboard:Keyboard; override public function getEnterCommand():Command { return new TweenNanoTo ( position, 0.2, { x: 400, y: 300 } ); } override public function update(dt:Number):void { if (keyboard.isDown(Key.UP)) { goto(new UpState()); } else if (keyboard.isDown(Key.DOWN)) { goto(new DownState()); } else if (keyboard.isDown(Key.LEFT)) { goto(new LeftState()); } else if (keyboard.isDown(Key.RIGHT)) { goto(new RightState()); } } }

The four other states all look similar, so I’ll just show the `UpState`

here. Note it only queries the down key, since the other three directions would not be a valid input for this state.

public class UpState extends State { [Inject] public var position:Position; [Inject] public var keyboard:Keyboard; public function UpState() { } override public function getEnterCommand():Command { return new TweenNanoTo ( position, 0.2, { x: 400, y: 200 } ); } override public function update(dt:Number):void { if (keyboard.isDown(Key.DOWN)) { goto(new CenterState()); } } }

All set. If you run the example, you can see a circle in the center of the screen that can be moved along a cross with the keyboard.