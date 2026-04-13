---
title: KoboldScript Koolness, Part 1
url: http://www.learn-cocos2d.com/2012/02/koboldscript-koolness-part-1/
author: Jorge says
published: '2012-02-18'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I thought I’d post a very early result of the KoboldScript scene setup. This scene was scripted entirely with KoboldScript with about 50 lines of code:

Below you’ll see the part of the Lua script that created this scene. In fact it’s not so much code as it is defining data, which behind the scenes calls the node functions like setPosition and setColor for you.


```
Scene
{
Name = "My first KoboldScript'ed scene!",
Sprite
{
Name = "FirstSprite",
FrameName = "alien.png",
Position = {60, 60},
Sprite
{
Name = "SubSprite",
FrameName = "spider.png",
Position = {100, 20},
};
Sprite
{
Tag = 12345,
FrameName = "bitmapfont.png",
Position = {120, 120},
Color = {0, 255, 55},
};
Sprite
{
FrameName = "spider.png",
Position = {140, 20},
Color = {155, 100, 100},
Sprite
{
FrameName = "fps_images.png",
Position = {210, 99},
Color = {255, 0, 255},
DrawOrder = 3,
};
Sprite
{
FrameName = "fps_images.png",
Position = {210, 88},
Color = {255, 255, 0},
DrawOrder = 2,
};
Sprite
{
FrameName = "fps_images.png",
Position = {210, 77},
Color = {0, 255, 255},
DrawOrder = 1,
};
};
};
};
RunSceneByName("My first KoboldScript'ed scene!")
```


The table layout is very natural since each level of hierarchy in the table matches the resulting node hierarchy. Furthermore you can use Lua logic to create (parts of) the scene, for example to create dozens of similar-but-not-identical sprites. You could even define parts of the scene in a different script, for example your HUD layer. Then you can insert the HUD layer to each scene that needs it by simply running **dofile(“HUDLayer.lua”)**.

Once the scene was loaded (of course transitions will be supported) you will be able to access each node in the hierarchy at runtime by using its tag or name, like so:

```
doSomethingWithNode(runningScene.FirstSprite)
doSomethingWithNode(runningScene.FirstSprite.SubSprite)
doSomethingWithNode(runningScene.FirstSprite[12345])
```


As you can see you will be able to easily access the child nodes of a node. This is particularly awkward to program in Cocos2D but in KoboldScript it’s just writing each node’s name or tag separated by a dot: **runningScene.FirstNode.ChildNode.AnotherChildNode**. The runningScene is simply the currently running scene itself.

There’s a lot more kool stuff coming, stay tüned! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Awesome!

Looks really awesome. Do you nest a group of sprites into a top-level sprite?

Not sure what you mean exactly. The table hierarchy reflects the node hierarchy. So if you put a Sprite B inside another Sprite A, it will be a child of A. The top level is always the scene, but you can define parts of the hierarchy in a seperate file and only return the top level node of that file, for example you could have a script file that only returns a Layer with all kinds of child nodes. Then you could simply dofile this script to insert it in any scene, at the desired location in the hierarchy.

The separate script would be something like this:

return Layer

{

Sprite

{

};

— more nodes here…

};

And in some other scene you can do:

Scene

{

dofile(“statusbar.lua”),

dofile(“HUDLayer.lua”),

dofile(“pause-menu.lua”),

Sprite

{

};

— more nodes here …

}

It makes constructing scenes and reusing parts of other scenes very easy.

Need to get my hands on this.

I was wondering about the hierarchy “Scene > Sprite > Sprite” and so on, but it makes absolutely sense. Great work.