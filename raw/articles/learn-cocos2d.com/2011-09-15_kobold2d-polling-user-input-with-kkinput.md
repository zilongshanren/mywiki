---
title: 'Kobold2D: Polling User Input with KKInput'
url: http://www.learn-cocos2d.com/2011/09/kobold2d-polling-user-input-kkinput/
author: Dogfooding; Learn; Master Cocos
published: '2011-09-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[Kobold2D](http://www.kobold2d.com/) is about solving annoying, recurring problems, or simply making all things Cocos2D more convenient. The new [ KKInput class](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_input/) does both! (*)


(*) **KKInput** is a new feature of Kobold2D Preview 4 which will be released in a few days.

#### Polling the Input State: anywhere, at any time

**KKInput** gets rid of the event-based processing of input events and for the first time in Cocos2D history allows you to poll the input state. At the same time it also gets rid of the misconception that you can only process input events in Cocos2D in CCLayer classes. With KKInput, you can process input at any time from any class in any method. See the [KKInput class reference](http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_k_k_input/) for details.

At this time, KKInput supports keyboard and mouse input. In the next few days I’ll add touch and accelerometer input to the mix before I’ll release it with Kobold2D Preview 4.

#### Getting the Mouse Location

The following code snippets are excerpts from the newly added User Input Template project for Kobold2D. The code should illustrate how easy it is to work with the KKInput API:

[cc lang=”c”]

-(void) update:(ccTime)delta

{

[self moveShipByPollingKeyboard];

[self rotateShipWithMouseButtons];

[self particleFXFollowsMouse];

}

-(void) particleFXFollowsMouse

{

KKInput* input = [KKInput sharedInput];

particleFX.position = [input mouseLocation];

particleFX.gravity = ccpMult([input mouseLocationDelta], 50.0f);

ship.scale += [input scrollWheelDelta].y * 0.1f;

}

[/cc]

The scheduled update method simply calls all the other input processing methods, like **particleFXFollowsMouse**. This is just to illustrate that this code is running outside of any Cocoa input event methods.

You can get the current mouse cursor location in window coordinates via **[[KKInput sharedInput] mouseLocation]**. It wouldn’t be Kobold2D if there weren’t additional convenience methods like **mouseLocationDelta**, which returns a CGPoint with the difference (delta) of the current and previous mouse locations. Of course you can also access the delta positions returned by the most recent scroll wheel event.

The accelerometer input features will work in a similar way, and also allow you to optionally enable and configure high and low pass accelerometer value filtering.

#### Testing for Mouse Buttons

Let’s have a look at how you can work with mouse button states:

[cc lang=”c”]

-(void) rotateShipWithMouseButtons

{

KKInput* input = [KKInput sharedInput];

if ([input isMouseButtonDown:KKMouseButtonLeft])

{

ship.rotation -= 2;

}

if ([input isMouseButtonDown:KKMouseButtonRight])

{

ship.rotation += 2;

}

if ([input isMouseButtonDown:KKMouseButtonLeft

modifierFlags:KKModifierCommandKeyMask] ||

[input isMouseButtonDown:KKMouseButtonLeft

modifierFlags:KKModifierControlKeyMask])

{

ship.rotation -= 10;

}

if ([input isMouseButtonDown:KKMouseButtonRight

modifierFlags:KKModifierCommandKeyMask] ||

[input isMouseButtonDown:KKMouseButtonRight

modifierFlags:KKModifierControlKeyMask])

{

ship.rotation += 10;

}

if ([input isMouseButtonDownThisFrame:KKMouseButtonDoubleClickLeft])

{

ship.flipX = !ship.flipX;

ship.color = ccYELLOW;

}

if ([input isMouseButtonDownThisFrame:KKMouseButtonDoubleClickRight])

{

ship.flipY = !ship.flipY;

ship.color = ccCYAN;

}

if ([input isMouseButtonDownThisFrame:KKMouseButtonDoubleClickOther])

{

ship.flipX = NO;

ship.flipY = NO;

ship.rotation = 0;

ship.color = ccWHITE;

}

}

[/cc]

The method **isMouseButtonDown** and the companion “up” methods allow you to test the mouse button states. In the case of **[input isMouseButtonDown:KKMouseButtonLeft modifierFlags:KKModifierCommandKeyMask]** you can combine mouse button states with modifier keys like Command, Control, Option, Shift, etc. You’ll notice that it’s a bit verbose if you want to provide several options OR’ed together, but this is much less frequently used than AND’ing modifier keys, which you can do in a single line: **[input isMouseButtonDown:KKMouseButtonLeft modifierFlags:KKModifierCommandKeyMask | KKModifierControlKeyMask]**

You can also easily test for mouse button double-clicks with the special keys **KKMouseButtonDoubleClick***:

**[input isMouseButtonDownThisFrame:KKMouseButtonDoubleClickLeft]**

In theory triple and multiple click tests are easily doable, but I decided against them because they don’t play a role in modern user interface design. They may even be considered harmful, besides some obscure (ahem, Logitech) mouse drivers triple clicks are a foreign concept to almost every computer user.

#### Testing for Key Presses

As seen in the [blog post before this one](http://www.learn-cocos2d.com/2011/09/polling-mac-keyboard/), the following code allows you to control the ship with the arrow keys or alternatively with the WASD keys:

[cc lang=”c”]

-(void) moveShipByPollingKeyboard

{

const float kShipSpeed = 3.0f;

KKInput* input = [KKInput sharedInput];

CGPoint shipPosition = ship.position;

if ([input isKeyDown:KKKeyCode_UpArrow] ||

[input isKeyDown:KKKeyCode_W])

{

shipPosition.y += kShipSpeed;

}

if ([input isKeyDown:KKKeyCode_LeftArrow] ||

[input isKeyDown:KKKeyCode_A])

{

shipPosition.x -= kShipSpeed;

}

if ([input isKeyDown:KKKeyCode_DownArrow] ||

[input isKeyDown:KKKeyCode_S])

{

shipPosition.y -= kShipSpeed;

}

if ([input isKeyDown:KKKeyCode_RightArrow] ||

[input isKeyDown:KKKeyCode_D])

{

shipPosition.x += kShipSpeed;

}

if (([input isKeyDown:KKKeyCode_Command] ||

[input isKeyDown:KKKeyCode_Control]) &&

[input isAnyMouseButtonDown])

{

shipPosition = [input mouseLocation];

}

ship.position = shipPosition;

}

[/cc]

The simplified **isAnyMouseButtonDown** and **isAnyKeyDown** methods together with other such simple tests allow you to build quick & dirty “touch to advance” screens with no hassle.

#### #ifdef-less Programming

One goal for **KKInput** is that you should not need to **#ifdef** your code for a particular platform (iOS or Mac OS). Conditional compiling with preprocessor macros is always problematic, because part of your code won’t be compiled while you’re working for one particular platform. When you switch platforms, you’ll notice all the code that doesn’t work in the other platform, so you fix that, only to find that the fixed code now doesn’t work for the first platform anymore. And so on. It can get very tedious quickly trying to maintain two code bases in a working state.

With **KKInput** it’s perfectly legal to use the key and mouse input code and enumerations like **KKKeyCode_Command** in iOS builds. Of course you can’t expect keyboard & mouse methods to return reasonable results (they’ll usually return 0, NO or nil), so you should still use [[CCDirector sharedDirector] currentPlatformIsIOS] and other runtime conditionals provided by Kobold2D to use regular if(..) in order to branch your code.

The big bonus is that the entire code base will always be compiled, and will still compile when you switch platform build schemes.

**Watch this blog and Kobold2D for more exciting new features!**

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[accelerometer](http://www.learn-cocos2d.com/tag/accelerometer/)•

[button](http://www.learn-cocos2d.com/tag/button/)•

[CCLayer](http://www.learn-cocos2d.com/tag/cclayer/)•

[cocos2d](http://www.learn-cocos2d.com/tag/cocos2d/)•

[convenience](http://www.learn-cocos2d.com/tag/convenience/)•

[input event](http://www.learn-cocos2d.com/tag/input-event/)•

[input events](http://www.learn-cocos2d.com/tag/input-events/)•

[input state](http://www.learn-cocos2d.com/tag/input-state/)•

[isMouseButtonDown](http://www.learn-cocos2d.com/tag/ismousebuttondown/)•

[Key](http://www.learn-cocos2d.com/tag/key/)•

[keyboard](http://www.learn-cocos2d.com/tag/keyboard/)•

[keyCode](http://www.learn-cocos2d.com/tag/keycode/)•

[KKInput](http://www.learn-cocos2d.com/tag/kkinput/)•

[Kobold](http://www.learn-cocos2d.com/tag/kobold/)•

[kobold2d](http://www.learn-cocos2d.com/tag/kobold2d-2/)•

[macro](http://www.learn-cocos2d.com/tag/macro/)•

[mouse input](http://www.learn-cocos2d.com/tag/mouse-input/)•

[mouse location](http://www.learn-cocos2d.com/tag/mouse-location/)•

[mouseLocation](http://www.learn-cocos2d.com/tag/mouselocation/)•

[poll](http://www.learn-cocos2d.com/tag/poll/)•

[polling](http://www.learn-cocos2d.com/tag/polling/)•

[position](http://www.learn-cocos2d.com/tag/position/)•

[preview](http://www.learn-cocos2d.com/tag/preview/)•

[Programming](http://www.learn-cocos2d.com/tag/programming/)•

[scroll wheel](http://www.learn-cocos2d.com/tag/scroll-wheel/)•

[scrollWheelDelta](http://www.learn-cocos2d.com/tag/scrollwheeldelta/)•

[template](http://www.learn-cocos2d.com/tag/template/)•

[touch](http://www.learn-cocos2d.com/tag/touch/)

[…] Kobold2D: Polling User Input with KKInput […]

[…] (Class Reference) enables you to poll Mac keyboard & mouse states (Mac) as well as accelerometer, gyroscope and device motion data […]

There are some smaller typos:

kKKKeyCode_* should be KKKeyCode_*

Thanks for pointing that out. I changed the API after writing this post.