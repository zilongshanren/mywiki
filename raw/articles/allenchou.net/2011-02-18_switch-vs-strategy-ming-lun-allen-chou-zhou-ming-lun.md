---
title: Switch vs Strategy | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/02/switch-vs-strategy/
author: Allen Chou
published: '2011-02-18'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Recently, I’ve been working with the blend mode feature for Bunnyhill, my upcoming 2D rending engine based on Molehill. And I’ve used strategy objects to replace what could have been written in a switch statement. I think this could be a nice example for replacing switch statements with strategies, so I’ll share some of the details here.

**The Switch Appraoch**

First let’s take a look at the naive switch appraoch to set the blend mode of a render engine. Say we have a render engine that implements the interface below.

interface IRenderEngine { function setBlendMode(value:String):void; }

And the `BlendMode`

class provides static constants representing different blend modes.

class BlendMode { public static const ADD:String = "add"; public static const ALPHA:String = "alpha"; public static const NORMAL:String = "normal"; }

A possible render engine implementation for the switch approach is shown below.

class RenderEngine implements IRenderEngine { public function setBlendMode(value:String):void { switch (value) { case BlendMode.ADD: //use add blend mode break; case BlendMode.ALPHA: //use alpha blend mode break; case BlendMode.NORMAL: //use normal blend mode break; } } }

In our main program, we could set the blend mode of the render engine like this.

renderEngine.blendMode = BlendMode.ADD;

The use of switch seems quite reasonable at the first glance, but is identified as “coding bad smell” in **Refactoring**, by Martin Fowler. If we were to add more blend modes to the render engine, this means we have to add an extra constant in the `BlendMode`

class and an extra case in the switch statement. One feature change results in changes in two places, no good!

This is when the use of strategy objects should be considered.

**The Strategy Approach**

We could define an interface for strategy objects.

interface IBlendMode { function setupBlendMode(engine:IRenderEngine):void; }

And the new `BlendMode`

class looks like this.

class BlendMode { public static const ADD:IBlendMode = new Add(); public static const ALPHA:IBlendMode = new Alpha(); public static const NORMAL:IBlendMode = new Normal(); } class Add implements IBlendMode { public function setupBlendMode(engine:IRenderEngine):void { //use add blend mode } } class Alpha implements IBlendMode { public function setupBlendMode(engine:IRenderEngine):void { //use alpha blend mode } } class Normal implements IBlendMode { public function setupBlendMode(engine:IRenderEngine):void { //use normal blend mode } }

Now the implementation of the render engine is as follows.

class RenderEngine implements IRenderEngine { public function setBlendMode(value:IBlendMode):void { value.setupBlendMode(value); } }

And in the main program, the code to set the blend mode of a render engine is, surprisingly, exactly the same. However, the underlying implementation has switched from switch statements to strategy objects.

renderEngine.blendMode = BlendMode.ADD;

If you want to create new blend modes, all you have to do is create a new `IBlendMode`

strategy class, and you don ‘t have to add any code in the `RenderEngine`

class. This is pretty much the essence of the Strategy Pattern, adding new features and functionalities to a system by simply extending the strategy base class, or implementing a common strategy interface.

good approach! old blendMode API instead of setBlendFactors and keep extendable

Ah yes the classic “Replace type code with State/Strategy”. Its one of the many code refactorings from Martin Fowler’s Refactoring: Improving the Design of Existing Code. You should check it out.

I just used your idea (and gave it credit in comments) and made it generic:

https://github.com/puppetMaster3/Gamina-Core/tree/master/asSrc/org/gamina/api/logic/fsm

I tested it, example will be in npm in a few weeks.

thx!

Vic

Cool. Be sure to send me the link 🙂

Nice example but isn’t there always a trade-off? I mean, which approach is faster to execute, faster to code, uses less memory/resources, more scalable, easier to understand and maintain, etc.? Is one of the two better in all aspects?

Yes, there’s always a trade-ff. Using the strategy pattern doesn’t necessarily give better performance than switch statements. It’s all about whether the code causes performance bottleneck (run once vs 10000 times per frame). If using strategy pattern does not slow your program down, but can greatly make your code cleaner and easier to maintain, then just use it.