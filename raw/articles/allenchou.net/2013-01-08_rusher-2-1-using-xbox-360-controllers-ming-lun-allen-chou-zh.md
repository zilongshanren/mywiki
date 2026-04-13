---
title: Rusher 2.1 – Using Xbox 360 Controllers | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2013/01/rusher-2-1-using-xbox-360-controllers/
author: Allen Chou
published: '2013-01-08'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

[Rusher 2 repository](https://code.google.com/p/rusher/) ([Mercurial](http://en.wikipedia.org/wiki/Mercurial) client required to checkout)

I was excited when I found out about [Airxbc](http://rhuno.com/flashblog/airxbc/). It is a [native extension for Adobe AIR](http://www.adobe.com/devnet/air/native-extensions-for-air.html) that allows AIR applications on Windows platforms to access Xbox 360 controllers. What a big plus for games! I started working on integrating Airxbc into Rusher right away. And now the latest Rusher supports Xbox 360 controllers through the new

system.[X360Input](https://rusher.googlecode.com/hg/docs/index.html?rusher/extension/airxbc/X360Input.html&rusher/extension/airxbc/class-list.html)

The system is capable of the following:

- Query number of connected controllers.
- Query whether a controller of a specific ID is connected.
- Dispatch connection and disconnection signals for controllers, which can be used to display custom message.
- Query button down/pressed/released status as Boolean values, including: D-Pad, A, B, X, Y, LB, RB, LT, RT, LS, RS, Back, and Start (triggers’ status is measured by a reasonable threshold).
- Query analog input as percentage: LS and RS in the range [-1.0, 1.0]; LT and RT in the range [0.0, 1.0].
- Set vibration amount for the low- and high-frequency rumblers.

Below are some code snippets that demonstrate how to use the `X360Input`

system. The source code for the entire example can be found in the repository. You’ll need a Mercurial client to checkout the entire repository. I recommend [TortoiseHg](http://tortoisehg.bitbucket.org/). The entire repository is required in order for the example projects to build.


### Adding The System

In order to use a system, we need to add it to the engine at the engine initialization stage.

//engine initialization engine = new Engine(stage); engine.addSystem(X360Input); engine.addSystem(ActionSystem, new StartUp()); engine.addSystem(Renderer2D, canvas);

### Obtaining System Reference through Injection

Anywhere in another system, a component, or an action, a reference to the `X360Input`

system can be obtained through dependency injection:

[Inject] public var input:X360Input;

or the `getInstance`

method inherited from the

class:[RusherObject](https://rusher.googlecode.com/hg/docs/index.html?rusher/engine/RusherObject.html&rusher/engine/class-list.html)

input = getInstance(X360Input);

### Connection Status

The `isConnected`

method allows client code to query whether a controller of a specific ID (0-3) is connected. The ID is defaulted to 0 if no ID is provided. This applies to many other methods as well.

if (!input.isConnected(1)) { trace("Controller 2 is not connected."); }

There’s also an alternative for determining the connection status, which is listening to the `onConnected`

and `onDisconnected`

signals.

private function init():void { input.onConnected.add(connected); input.onDisconnected.add(disconnected); } private function connected(controllerID:uint):void { trace ( "Controller" + (controllerID + 1).toString() + "is connected." ); } private function disconnected(controllerID:uint):void { trace ( "Controller" + (controllerID + 1).toString() + "is disconnected." ); }

### Button Status

Similar to the

system, the [Input](https://rusher.googlecode.com/hg/docs/index.html?rusher/input/Input.html&rusher/input/class-list.html)`X360Input`

system provides methods such as `isDown`

, `isPressed`

, and `isReleased`

for button status query.

if (input.isDown(X360Input.A)) { trace("Button A is down."); }

If the client code just needs to determine whether the left or right trigger is pressed down, where the analog value is not important, the client can just use the `isDown`

method as well. A reasonable threshold is used internally to determine whether a trigger is being pressed down.

if (input.isDown(X360Input.LT)) { trace("Left Trigger is down."); }

### Analog Input Status

The analog values of the left and right sticks (from -1.0 to 1.0), as well as the left and right triggers (from 0.0 to 1.0), can be queried through the `leftStickX`

, code>leftStickY, code>rightStickX, code>rightStickY, `leftTrigger`

, and `rightTrigger`

methods.

const THRESHOLD:Number = 0.3; if (leftStickX() < -THRESHOLD) { trace("Moving left."); } if (leftStickX() > THRESHOLD) { trace("Moving right."); }

### Vibration

The `setVibration`

method sets the low- and high-frequency vibration amount at the same time, while the `setVibrationLow`

and `setVibrationHigh`

can set them separately.

input.setVibrationLow(0.3); input.setVibrationHigh(1.0);

There are also some utility actions that are convenient for generating a fix-timed burst of vibration:

, [X360Vibrate](https://rusher.googlecode.com/hg/docs/index.html?rusher/extension/airxbc/X360Vibrate.html&rusher/extension/airxbc/class-list.html)

, and [X360VibrateLow](https://rusher.googlecode.com/hg/docs/index.html?rusher/extension/airxbc/X360VibrateHigh.html&rusher/extension/airxbc/class-list.html)

.[X360VibrateHigh](https://rusher.googlecode.com/hg/docs/index.html?rusher/extension/airxbc/X360VibrateLow.html&rusher/extension/airxbc/class-list.html)

var actions:ActionSystem = getInstance(ActionSystem); actions.pushback(new X360Vibrate(VIBRATION_AMOUNT));

### Full Examples

This concludes the introduction to the new `X360Input`

system that supports Xbox 360 controllers for AIR applications on Windows platforms. You can check out the full source code for examples from the [repository](https://code.google.com/p/rusher/). You’ll need to checkout the entire repository in order to build the examples.

thanks for sharing this!! very nice !!