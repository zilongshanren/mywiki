---
title: What goes into a game engine? A long list.
url: http://www.learn-cocos2d.com/2013/06/game-engine-long-list/
author: Daniel Marques says
published: '2013-06-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Cocos2D is a *rendering* engine. Note the emphasis. 90% of what it does is draw stuff onto the screen and animate it. It adds some input processing and scheduling and the rest is up to you.

A game engine is to cocos2d what cocos2d is to OpenGL. The list of things I want in an actual **game** engine is long.

The iOS mobile platform has advanced far enough that a pure rendering engine just isn’t that much of a help anymore. We’re effectively moving back towards where we were back in 2008 if we don’t start pushing the boundaries, hard.

Here are some ideas I have for and would like to see in a 2D **game** engine, in no particular order. It is not a feature list for Kobold Kit, but it does reflect what I *want to make possible with / encourage for* Kobold Kit.


#### Behaviors (Plug-in Components)

Any good game engine these days offers a game component system. Consider Unity. You want an object to have physics? You attach the physics component to the object. That’s the extreme case.

On a smaller level, components can be as tiny like actions and make a character jump. Or turn a label into a clickable button. Or allow an actor to follow another actor that follows another actor following the player. All using the same component.

Components are any code you can and want to reuse but can’t implement as an action, and has some game-relevant attribute. There is no “flying” action, is there? That’s what a component brings to the table.

#### Template-Based Actors (NSCopying)

You define an actor, for example a tree, by adding branches to the stem, leaves and fruits to the branches. Then you copy the entire actor and place it multiple times in your world. While doing so you can change or randomize or combine multiple variants of the same actor template.

The same goes for any stats an actor may have, like walk speed, armor, health, spells, weapons, including behaviors like the ability to fly. You design the actor once, save it, and then make copies of it in your game.

This really comes to shine when you have an editor to build these templates. Even if not, copying a template beats re-running the same alloc, init and property tweaking code over and over again to create copies of the same object.

#### Autocoding Variables (NSCoding)

Implementing NSCoding is tedious, error prone task. It’s very easy to forget to encode or decode a variable or make any other mistake. Yet NSCoding is so important for savegames, and editors too.

While we have NSUserDefaults, what developers really need are per-node variables that will be encoded and decoded automatically. No subclassing needed to add “ivars” to a node.

Multiple classes can share this pool of variables to exchange data between them without knowing about each other. If a variable doesn’t exist, it is created transparently and initialized to 0 so accessing an undefined variable is not an error. Many scripting languages use this approach.

#### Game Specific But Still Generic Code

Consider things like a homing missile. Relatively easy to create but still takes time to program and test. Though not used in every game, if you need it, something like that is great to have available. Like the builtin transitions in cocos2d.

Or more complex stuff like the contour tracing to create physics collision shapes for a tilemap. These are the things that open up a whole new level of games for a lot more developers.

Virtual Joypads and of course support for controllers like iCade and GameDock are just as important. Used only by some but great to have and doesn’t get in the way when you don’t use it.

#### Debugging Helpers

Box2D debug rendering is nice. Why not extend that to all nodes? Draw their bounding boxes, positions, anchor points. Add labels for tag, name, exact position coords and other things. Allow the user to enter a mode where he can tap anywhere on the screen to bring up detailed info about the node. See what went wrong right then and there.

Or imagine profiling graphs. You enclose a section of code, give it a name, and it will print a graph with time in ms onto the screen. You can see in realtime which sections of your code use up the most time, and where the peaks are.

Or enable an edit mode with a gesture, where you start dragging individual nodes around on the screen to fine-tune the layout, or see what’s behind that sprite.

#### Camera and Scrolling

Hooking up the game world’s scrolling to the accelerometer should take no more than 3 lines of code. Scrolling the world should be as easy as setting the position of a node.

In addition we need to get rid of the rigidity. I want automatic and configurable camera easing, so that the camera follows a character faster the further the character has moved from the center. Perhaps with a deadzone around the center where the camera doesn’t move at all.

Parallaxing any two nodes would be a natural result of this. Parallaxing is very simple: one node gets the position of another (moving) node every frame, multiplies it with a parallax factor and applies the result to its own position. The result is a node that follows the target either faster or slower, but always synchronous.

#### Screen Templates

Every game we build starts as a prototype. Every time most of us start entirely from scratch. We need at least the standard screens for the standard things, either as templates or at least to plug them in for prototyping and have them ready in 5 minutes.

What am I talking about?

The settings screen: Audio volume sliders, music on/off toggles, difficulty settings. Just connect object and property name and type of control and the slider will adjust the value in the given range.

The controller screen: shows the game controller and allows you to re-map buttons and sticks to actions and movement. Similar for keyboard and mouse. For the accelerometer this would be a calibration screen.

Selection screen: Take an array of strings or sprites, generate a (scrollable) list of items. Click one and you receive a notification with the index. Use it for quick & dirty level, character or music track selection.

The back and forth: Frequently we need a “back” button, or else entering the settings screen leaves us deadlocked. So some “install wizard” type system similar to how Storyboard works would be dandy. Just plug it in and the navigation buttons remain available in every other scene until you explicitly remove it, and the back button always knows automatically what “back” means.

The HUD: connect a property to a HUD item and player.health is displayed as a health bar on screen. KVO may not be the fastest thing, but just being able to enable something like that right away is really going to boost preproduction productivity.

#### Frame Animation Statemachines

I almost forgot. You rarely play an animation by its own and then you’re done. In some games it can be a lot more complex.

So much so that you want metadata associated with each frame. Send a delegate message when a specific frame is displayed or play a sound effect. Change the delay between individual frames. Allow portions of the animation to run endlessly until interrupted, while ensuring the currently running animation runs to its predefined end before the next animation starts.

The best way to deal with that complexity is through statemachines. Incidentally statemachines are also a great tool to write game logic, provided you add enough custom conditions and actions.

#### Enumerate Actors

So what if you want to have an explosion that affects all enemies in an area? You could really use an enumerator that gives you all nodes in a radius or rectangle and enumerates each one. Perhaps with additional filters like the actor’s class, or it’s “type”.

Or you may want to find a spot that’s comfortably away from all the action to spawn an actor to. And what about disabling actors that aren’t visible on the screen anymore? Including a threshold to avoid them from popping out of existence the second they leave the screen.

#### Pathfinding

With a known data format for tilemaps it is possible to implement generic A* and other pathfinding methods right in the engine.

Even clever approaches that return a series of points to start walking right away, while completing the rest of the path in the background, on another thread, feeding the actor walking the path in time with new path points.

#### Input Mapping

Code not the keys or buttons which then run more code. Define and name an action (target/selector or notification) and add the input actions to the input mapper.

This way we can use a common or customized input mapping screen to reassign which button or key or click performs what action. Sure the system has its limits, a accelerometer won’t map to an analog stick, nor would a swipe map to a button action.

But there’s merit in this too, in particular for Mac games and games using game controllers.

#### Great, Outstanding Tools!

Last but not least, we need better development tools. Specifically those tools that allow you to design screens and worlds. The Interface Builder for 2D games unfortunately isn’t out there yet, and what I’ve seen just isn’t good enough.

A good game editor needs to treat everything like a game object that has a visual representation, not the other way around. You can add and edit behavior right in the editor, and make the links with code with ease. This is what’s really important, not the scale or the color of the sprite.

It needs to help you build a template of things you need often, characters, parts of the scenery, screens, user interfaces, everything. It has your entire game in a single project, every scene.

An excellent game editor lets you run the game within the editor itself, and is able to connect with and deploy directly to your device while the game is running and allows you to modify it in realtime, perhaps sending a new level so you can play that instantly.

Of course for the teams out there it must be multi-user capable and source control friendly, so you can’t accidentally overwrite each other’s changes.

#### These are…

… just some of the things I want to see in a moderately decent 2D game engine.

Tighter integration of related technologies. Simplify code through sensible defaults and configuration. More prefabricated code to use as templates. And native, well engineered, usable tools that use NSCoding & NSCopying.

More functionality, more out-of-the-box features, more quick & dirty solutions for faster prototyping, more of these smaller game-specific but popular features we’re currently re-inventing over and over again.

We need to make systemic progress towards a higher standard for 2D game development. I used to be working with many of these things well over 10 years ago. The iPhone is far more advanced than the Gameboy Color I used to develop for, yet back in the day I had better tools and engines (built by a very small team) at my disposal.

I miss them dearly. I want them back, now!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen,

First of all, I read your cocos2d books since the first publication, helped me a lot, thanks!

I feel the same about our current game engines. Do you know any good 2d game engine available right now that let us do less redo code and help us more? I didnt mean only for iphone, but cross platform like cocos2d-js.

I heard about Game Maker and ImpactJS and would like to study them a bit sometime.

Sorry for my english!

Game Maker is one of my favorite tools but I haven’t used it in years. Definitely worth checking out though I can’t say anything about its porting capabilities and performance, I used it when there was only a Windows version. There are also several open source projects aiming to clone GM and be compatible with its file format.

Here’s a list of game making tools: http://www.pixelprospector.com/the-big-list-of-game-making-tools/

Game Editor http://game-editor.com/Main_Page and OGM2D http://sourceforge.net/projects/ogm2d/ also look promising.

[…] To understand the differences read my game engine wishlist post. […]

Sounds like you want unity3D and a few assets from asset store![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Yes, in a certain way. Specific to 2D game development, native to Apple’s platforms. That would be it.