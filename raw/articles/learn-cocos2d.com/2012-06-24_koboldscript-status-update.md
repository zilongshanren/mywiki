---
title: KoboldScript Status Update
url: http://www.learn-cocos2d.com/2012/06/koboldscript-status-update/
published: '2012-06-24'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I think it’s about time to issue a KoboldScript status update. KoboldScript is Lua scripting for cocos2d, in case you didn’t know. In the near future it’ll be released as part of the [KoboldScript Game Kit project](http://www.learn-cocos2d.com/2012/05/learn-create-cocos2d-game-lua-scripting-physics-tilemaps-arc/). I showcased KoboldScript before [here](http://www.learn-cocos2d.com/2012/02/learncocostv-6-small-script-man/) and [here](http://www.learn-cocos2d.com/2012/03/learncocostv-7-tic-tac-lua/).

#### Static bindings, manual labor

One big advantage of KoboldScript over other script language solutions available for cocos2d is that the KoboldScript binding is static, ie it is done at compile time. There’s very little runtime overhead to it, thanks to [SWIG](http://www.swig.org/). So in terms of performance it’s miles ahead of [Wax](https://github.com/probablycorey/wax/wiki), [LuaCocoa](http://playcontrol.net/opensource/LuaCocoa/) or other dynamic scripting language bindings like [JSCocoa](http://inexdo.com/JSCocoa). And it is compatible with both Mac OS X and iOS.

The big problem with static bindings is that you have to somehow define each class, each method, each property and write lots of glue code. In the past, I did this manually. It involved writing a C wrapper method for SWIG and usually an Objective-C dispatch function went along with it. On the Lua side the function needed to be registered as well. It’s an error prone, repetitive, boring task. Perfect for code generation!


#### objc2swig to the rescue!

I initially wrote the objc2swig tool to generate only the C wrapper methods for Objective-C function calls. That was easy enough and helpful, but why stop there?

So over the past days I have extended the tool to parse the cocos2d header files, extract all the interfaces, generate both the Objective-C and C wrapper code for methods and properties, and register everything with Lua. The process is configurable through a config file (a Lua script).

This has some interesting benefits, including:

- exposing custom classes is dead simple, automatic for node, statemachine and other classes
- KoboldScript API can be tweaked (ie remove prefixes, suffixes or use alias names)
- KoboldScript API is updated automatically whenever cocos2d API changes
- alias names can help with backward compatibility, ie redirection or just failing gracefully
- optional type checking code for debugging can be inserted as needed
- (future) create the API reference from the processed classes, methods and properties
- (future) better tool support by exposing the API via data files which describe the language in machine-readable format (think: code completion, syntax highlighting, etc)

One other benefit is that the KoboldScript API methods follow strict rules. At the moment they strictly follow the cocos2d Objective-C API. So if you wanted to create a sprite, you’d use one of the available initWith methods on CCSprite and supply the parameters as described in the cocos2d-iphone API reference. All the properties are exposed, too.

Now if you have a favorite CCSprite+Category class, you can just add that file to the objc2swig search path and the methods and properties that the category adds to the CCSprite class will be available in KoboldScript.

#### API Example

For example this code creates a sprite with a label as child:

|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 |
CCSprite { initWith = {file = "image.png", rect = Rect(0, 0, 100, 50)}, position = Point(160, 240), rotation = 90, CCLabelTTF { initWith = {string = "Sprite Label", fontName = "Marker Felt", fontSize = 32}, color = ccc3(255, 150, 200), }; }; |

There are a few points to take away from this code snippet. Rather than removing the named parameters as is a side-effect of so many scripting languages (see [cocos2d Javascript bindings example](http://www.cocos2d-iphone.org/forum/topic/31640/page/2#post-165100)), the named parameters are preserved. You can’t accidentally mix up the label string with the font name, which is quite a common issue in all C-style languages.

Take for example **cc.LabelTTF.create(“Marker Felt”, “Sprite Label”, 200, 40, 32, 80);** and without looking it up in the API reference, can you tell if the parameters are in the correct order, if the total number of parameters is correct, and what each parameter stands for?

If you asked me what I don’t like about Javascript (and similar C-style scripting and programming languages), then that’s my answer.

Next, the creation of nodes allows you to modify properties at the moment the node is created. Instead of having to store the node in a variable, then tweak that variable’s properties you can do this all at once in KoboldScript.

And finally, to remove a common cause of errors and confusion for even seasoned cocos2d developers the node hierarchy is defined as an actual hierarchical table structure. Meaning if you create the CCLabelTTF inside the CCSprite node, the label will automatically be a child node of the sprite. Moreover you can cut, copy and paste the entire CCLabelTTF block to move it someplace else in the node hierarchy, to some other node, which makes it easy to try out different variations of how you layout your scene.

#### Verbosity

I agree this code is a little verbose. But consider that a scripting language should be easy for beginners. A format that feels more like a human-readable data entry format helps a lot. Professional users can still use loops and what not to create multiple nodes at once, or create template functions that return entire reusable layers of the game (ie HUDs or menus).

Another benefit is part is that the format is not just human-readable, it’s also tool-friendly. And being Lua code you can also transform this into a binary bytecode file with luac.

#### Next

Over the next days I intend to complete work on objc2swig. Once that’s done I can get to implementing game logic for our [KoboldScript Game Kit](http://www.learn-cocos2d.com/2012/05/learn-create-cocos2d-game-lua-scripting-physics-tilemaps-arc/).

I’m also planning to create specific folders for scripts and resources which are included in the Xcode project as a folder references, so that added, removed or renamed script and resource files are automatically updated in the bundle. After all I want users to be able to work with KoboldScript without having to work with Xcode - except for pressing the Run button for now.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |