---
title: Comparison of Lua Scripting with Corona SDK, Wax and Kobold2D
url: http://www.learn-cocos2d.com/2011/08/comparison-lua-scripting-corona-sdk-wax-kobold2d/
author: Ian Chia says
published: '2011-08-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[This Kobold2D FAQ article](http://www.kobold2d.com/pages/viewpage.action?pageId=918741) explains the difference between [Corona SDK](http://www.anscamobile.com/corona/) and [iPhone Wax library](https://github.com/probablycorey/wax/wiki/Overview), and evaluates the existing and future options for Lua scripting in [Kobold2D](http://www.kobold2d.com/).


#### About Corona SDK

The [Corona SDK](http://www.anscamobile.com/corona/) exposes a well designed API in Lua for app and game development. This API is naturally different from the iOS SDK since Corona is also a cross-platform game engine, exposing the same API for all platforms.

For example, when you receive an accelerometer event in Corona you get an event object [with these properties](http://developer.anscamobile.com/reference/index/events/accelerometer). The acceleration parameters are already split into “instant acceleration” and “gravity acceleration”, something that iOS developers have to do manually. At the same time, the event also reports whether it was a shake event. On iOS this is [an entirely different API](http://stackoverflow.com/questions/1170917/how-to-use-shake-api-in-iphone-sdk-3-0) from the accelerometer events.

In one sentence, Corona exposes the functionality that the devices offer in a uniform, simplified way. Corona also condenses information into fewer properties and methods. You deal with [fewer functions] which makes it great for rapid prototyping. But sometimes you’ll have fewer functionality, and in particular you can’t extend Corona with your own Objective-C, C or C++ code since the backend engine is proprietary. Overall, this makes Corona SDK very easy to learn but because it’s not extensible and can impose restrictions, it’s not for everyone.

#### About Wax

The [iPhone Wax library](https://github.com/probablycorey/wax/wiki/Overview) is a dynamic, automatic binding of the Lua language to Objective-C. Wax provides a translation layer that exposes regular Objective-C code to Lua via [Objective-C runtime functions](http://developer.apple.com/library/mac/#documentation/Cocoa/Reference/ObjCRuntimeRef/Reference/reference.html).

Since the binding happens at runtime, it’s a **dynamic binding** — in other words there is no code that says that function X should be exposed to Lua in a particular way. Instead, there’s code that creates the Lua methods and properties by analyzing the existing Objective-C code at runtime, and applying generic conversion mechanisms to translate between the two languages. The **binding is automatic** because that translation is transparent to the user.

Wax in essence allows you to write Objective-C code in the scripting language Lua. This is nice, in particular automatic memory management should be mentioned as a positive feature of Wax. But other than that it’s really hard to justify the use of Wax if you can write the same code in Objective-C. Here are the major drawbacks of writing (scripting) apps with Wax:

- You end up writing almost the exact same code as in Objective-C. It may be a little less code but it’s using a weird and uncommon syntax.
- The dynamic nature of Wax’ Lua binding causes a significant overhead. So much in fact that actual gameplay scripting for realtime (60 fps) games will result in disappointing performance — unless the game is rather simple and/or you target only newer devices (4th generation onward, and iPads).
- You can not properly debug Lua scripts. You can’t set breakpoints, you can’t single-step through script code, you can’t inspect variables.
- Lua is a dynamically typed language. That means the compiler won’t check Lua scripts for errors. Any syntax errors in your script will only surface while your app is already running.
- Lua support in Xcode is non-existent. There’s no syntax highlighting, no auto-completion, no refactoring, no quick help for Lua script files.
- You lose named parameters in Lua code. Lua functions are non-descript like C functions:
`someFunction("myName", 1, true, "triggerMe", false, 100, 0.4)`


In particular not being able to debug your Wax scripts (#3) and not having compile-time syntax checks (#4) will completely offset any time-savings you might get from writing your app entirely in Wax.

Wax doesn’t play into Lua’s strengths, which is that it’s usually used to expose a simplified, [domain-specific API](https://en.wikipedia.org/wiki/Domain-specific_language). Such an API would be less error-prone, is easier to understand and debug. Instead, Wax exposes the full complexity of Objective-C and applies a weird syntax, removes debugging, disables syntax checking and reduces code editing comfort. Not on purpose, mind you, but in effect that’s what you get.

While Corona shares the issues #4 to #6 with Wax, it’s performance and code design is well above that what Wax is able to provide. [Corona also comes with a Lua debugger](http://www.ludicroussoftware.com/blog/2011/08/22/using-the-corona-debugger/), albeit a command-driven one (eg. like Terminal).

#### The Middle-Ground: A Domain-Specific Script API in Lua

Lua is not without its advantages. It’s an excellent language to script games in. But this is only true if the purpose of the language has been determined and an appropriate API has been designed and implemented, exposed to Lua via regular, non-dynamic Lua bindings for optimal performance. That requires a lot of work.

You can bind the exposed API to Lua either by manually writing C functions that manipulate the Lua stack, or via binding libraries such as [tolua](http://www.tecgraf.puc-rio.br/~celes/tolua/tolua-3.2.html). Such an approach can have one of these goals:

- A general purpose game engine API for writing apps in Lua. (
[Corona SDK](http://developer.anscamobile.com/resources/corona-quick-start-guide)) - A domain-specific scripting API to manipulate existing game objects at runtime for a specific purpose. This is often tailored to work only with a particular (type of) game. (
[World of Warcraft UI Scripting](http://www.wowwiki.com/World_of_Warcraft_API)) - A “load-time” API to configure the app and its objects. Reduces the amount of boilerplate code needed for setting up a scene. Can be used by add-ons and tools as a user-editable data format for scenes, levels, etc. (
[Kobold2D](http://www.kobold2d.com/)) - Use Number 3 to configure a domain-specific, runtime
[state machine](https://en.wikipedia.org/wiki/Finite-state_machine). The statemachine is implemented in a high-level language (Objective-C, C, C++) for best performance. The high-level API is exposed through Lua to provide a user-friendly API to designers. The Lua scripts are run once to initialize the statemachine. ([Battleforge](http://www.learn-cocos2d.com/map-editor/mapcustomizations.pdf),[Spellforce](http://www.spellforce.com/forum/showthread.php?t=41320))

Number 3 is already implemented by Kobold2D. Number 2 and/or 4 could be implemented in the future, provided that there’s a common module that the scripts are supposed to control. For example, this could be a scriptable menu system so that menu screens can be designed and programmed entirely in Lua. This is **not** a promise for a feature, just something that *could* be done.

Number 4 is quite powerful, but new developers repeatedly find it confusing to write scripts that are executed exactly once (eg each time the level is restarted) because the scripting API implies a runtime nature that it doesn’t have — it’s only a setup/init script that’s translated to a runtime state-machine.

Number 1 is not compelling — for one users can simply use the Corona SDK if they want to write everything in Lua, and secondly some of the drawbacks for Wax still apply: no debugging, no compile-time error checking, no Xcode support.

In addition, implementing Number 1 on top of Cocos2D means that there will have to be some amount of hacks, compromises and extension code to keep the Lua API clean and simple while making it work with the already existing Cocos2D API. It would make more sense to write an entirely new game engine with a Lua interface, and also make that cross-platform. But wait, that’s what the Corona SDK is! You also get such a Lua interface with [Cocos2D-X](http://www.cocos2d-x.org/).

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

The bit about Corona not having a Lua debugger is wrong. Corona ships with the standard Lua debugger allowing you to set breakpoints, step through code and more. See http://www.ludicroussoftware.com/blog/2011/08/22/using-the-corona-debugger/

Thanks, I corrected that!

Thanks Steffen for the article. Where can I find an example/tutorial of LUA being used for defining the stages or levels of a game. More specifically what are the advantages versus an XML/JSON approach?

Thanks,

Diego

The Kobold2D template projects contain the config.lua file from which the entire setup of cocos2d is performed. It will be explained in more detail here: http://www.kobold2d.com/display/KKDOC/Config.lua+Settings+Reference

The Hello Kobold2D example also shows how to extend config.lua to contain your own settings and how to use them in your class.

The advantage over XML is that Lua is a human-readable text format, whereas XML is a machine-readable text format that can be read by humans if properly formatted. Editing XML manually however is tedious and error prone, Lua is a lot friendlier in that regard. It also allows you to perform algorithms, for example instead of writing a sequence of numbers you could have a loop that generates long lists of parameters, even randomizes them each time the script is run.

Plus with Lua you get automatic syntax checking that tells you where you made a mistake and what kind. With XML error reporting depends on the implementation, and often isn’t very helpful. It can range from silently ignoring any error (possibly reading the file partially, then stopping), to just telling that there was an error but not where or what kind, to actually useful error messages with line numbers and context.

I have some function module written in Objective-c, could i wrap the objective-C by C++, then integrate C/C++ code with Lua using toLua++, then using the lua code in Corona? Could i do that? It seems impossible…

It is impossible because Corona is a closed source project. You can only write Lua scripts with Corona, there is no way to add custom plugin code.

[…] will differ from other Lua game engines like Corona, and Cocos2D’s approach at developing a unified Javascript API. KoboldScript will […]

I really disagree about corona having a well designed api.

When you look at it in detail, you’ll find inconsistencies everywhere.

They took underlying frameworks, crippled them and dangled them together in a way that only the most passionate flash programmers can find sufficient.

It’s so easy, because it has so few possibilities. And even in it’s limitedness it fails to be a great help in situation where it could really condense functionality of underlying apis.