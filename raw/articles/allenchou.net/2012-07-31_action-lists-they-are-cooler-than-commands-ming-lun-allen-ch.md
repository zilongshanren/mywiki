---
title: Action Lists – They Are Cooler than Commands | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/07/action-lists-they-are-cooler-than-commands/
author: Allen Chou
published: '2012-07-31'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

I have written several articles on how to make use of the [commands](http://code.tutsplus.com/tutorials/thinking-in-commands-part-1-of-2--active-3383) in game engines in order to manage different multi-frame and asynchronous tasks effectively. From the Game Engine Architecture Club at [DigiPen](https://www.digipen.edu/), I learned about action lists, which provide all the advantages commands have and more cool features.

### Actions

An **action** object is like a **command** object, which carries out a modular action, such as tweening a property, loading an asset, and printing out a message, which leads to an interface that is not hard to expect:

(For clarity, I’m not using standard AS3 syntax.)

class Action { //basic functionalities function update(dt:Number):void; function complete():void; function isComplete():Boolean; }

An **action list** is a container of actions (or a composite action), which has multiple **lanes** that child actions can run on. Lanes are sorted by **lane IDs** and are processed in this order. When a lane is processed, the action list goes through the child actions on that lane and **updates** them until it encounters a **blocking action**. When that happens, the action list simply moves to the next lane without checking if there’s any other child action following the blocking action on the current lane.

We need a way to specify whether an action is blocking or not, the parent (action list) of and action, and which lane the action runs on. This leads to this new interface:


class Action { //blocking & unblocking function block():void; function unblock():void; //blocking query function isBlocking():Boolean; //parent and lane ID accessors function getParent():ActionList; function laneID():int; //...what we had before }

Someone once asked me if I could show him how to implement a command framework that supports **pausing** and **cancelling**. I never gave it a try until I was building the action list framework in [Rusher](https://allenchou.net/rusher.googlecode.com), which replaced the original command framework. I implemented these features using Robert Penner’s [AS3 Signals](https://github.com/robertpenner/as3-signals/) framework. I made it so that a signal is dispatched whenever an action is **started**, **paused**, **resumed**, **completed**, **cancelled**, and **finished (either completed or paused)**, so the client code can listen to these signals and hook up different listeners:

class Action { //signals function get onStarted ():ISignal; function get onPaused ():ISignal; function get onResumed ():ISignal; function get onCompleted():ISignal; function get onCancelled():ISignal; function get onFinished ():ISignal; //pausing, resuming, and cancelling function pause ():void; function resume():void; function cancel():void; //queries function isStarted ():Boolean; function isPuased ():Boolean; function isFinished():Boolean; //...what we had before }

### Action Lists

As you might have guessed, we are using the [Composite Pattern](http://en.wikipedia.org/wiki/Composite_pattern) to make the action list class. An action list contains multiple actions and is an action itself:

class ActionList extends Action { function ActionList(autoComplete:Boolean); //pushes a child action onto an action lane function push(action:Action, laneID:int):void; //updates child actions override function update(dt:Number):void; }

If `autoComplete`

is true, then the action list automatically calls its `complete()`

method when all child actions are finished. Of course, it also listens to the `onCancelled`

signal to call the `cancel()`

method on all non-finished child actions.

### Serial & Parallel Actions

One of the power features from common command frameworks is being able to assemble **serial** and **parallel** composite commands. Yes, you can do the same thing with actions. With blocking and non-blocking actions, you can create serial and parallel actions extremely easily:

function serial(...actions):Action { var list:ActionList = new ActionList(true); for ( var i:int = 0, len:int = actions.length; i < len; ++i ) { //make all child actions blocking actions[i].block(); list.push(actions[i], 0); } return list; } function parallel(...actions):Action { var list:ActionList = new ActionList(true); for ( var i:int = 0, len:int = actions.length; i < len; ++i ) { //make all child actions non-blocking actions[i].unblock(); list.push(actions[i], 0); } return list; }

We can still have the same clean syntax for creating complex nested actions as commands:

var intro:Action = serial ( new Wait(WAIT_TIME), new TweenTo(logo, TWEEN_TIME, { alpha: 1.0 }), new Wait(WAIT_TIME), parallel ( new TweenTo(button1, TWEEN_TIME, { y: 100 }), new TweenTo(button2, TWEEN_TIME, { y: 200 }), new TweenTo(button3, TWEEN_TIME, { y: 300 }) ) );

### Action Lists Drivers

In order to use the action list framework, you’ll need a **driver** somewhere in your client code that holds a **root action list** and keeps calling its `update()`

method. That action list should have a false `autoComplete`

property, so that it never completes itself and keeps on accepting new child actions.

In Rusher, the two classes that act as drivers are the

class and the [ActionSystem](https://code.google.com/p/rusher/source/browse/src/rusher/action/ActionSystem.as)

class. Each of the driver classes updates the action list on its own update call.[ActionComponent](https://code.google.com/p/rusher/source/browse/src/rusher/action/ActionComponent.as)

### Rusher’s Implementation

For simplicity, I’ve only provided the interface of the framework and skipped the implementation. If you’re interested, here’s the implementation of the action list framework in Rusher:

[Action implementation](https://code.google.com/p/rusher/source/browse/src/rusher/action/Action.as)

[ActionList implementation](https://code.google.com/p/rusher/source/browse/src/rusher/action/ActionList.as)

You may ignore any code related to [dependency injection](http://allenchou.net/2012/07/rusher-2-1-dependency-injection/) if it confuses you.

### Action Lists as State Machines

I have removed the state machine framework in Rusher since version 2.1, because it was entirely replaced by the action list framework. Yes, the action list framework can also serve as a full-blown state machine framework.

Think of it this way: an action’s `update()`

method is equivalent to a state update. When the state changes, the state simply **completes itself** so that it gets removed from the parent action list, and **pushes** the next state (action) onto the same lane. Here’s a possible idle state implementation that does nothing and transitions to the active state when the space key is pressed:

class IdleState extends Action { override public function udpate(dt:Number):void { if (input.isDown(Key.SPACE)) { complete(); getParent().push(new ActiveState(), 0); } } }

Aren’t action lists cooler than commands or what?

I feel i didn’t understand almost nothing… :S can u help me with some links to start before this?

Update your blog more! 😛

I like reading your posts, especially the ones like on delegates.

I feel the code is harder to read than Commands…

Please tell me which part confuses you.

I can try to elaborate on that in future posts 🙂

I can’t understand the concept of ActionList. Would you provide some graphic expression?

and the update() method in your implementation looks a bit heavy 😛

The concept is that you have a list of actions to perform in sequence. There’s a single update functions that updates the first action in the list. If this first action is “blocking”, then updating is stopped until the next call to update. If the first action is “non-blocking”, the next action in the list has update called on it, and so on. This way you can easily create complex behavior or algorithms on-the-fly, as opposed to writing annoying state machines, or some other method.

Wow. Thanks for the explanation, Randy.

I guess I assumed people are already familiar with the concept of commands, so I didn’t explain the concept of action lists thoroughly enough.