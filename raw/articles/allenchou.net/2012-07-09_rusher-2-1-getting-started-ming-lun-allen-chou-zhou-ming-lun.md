---
title: Rusher 2.1 – Getting Started | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/07/rusher-2-1-getting-started/
author: Allen Chou
published: '2012-07-09'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

Rusher is a **component-based game engine**, which means everything is treated equally as an **entity** (a.k.a **game object**) that owns **components** making up the overall behavior of the entity. **Systems** are like components for the engine itself, where each system is in charge of an engine-scale behavior. For instance, the `Input`

system manages all user input states that can be queried by components, and the `Renderer2D`

system updates all `RenderTarget2D`

components in the engine.

### Systems & Components

Each engine can only have one instance of each system type, and each entity can have only one instance of each component type. You add systems to an engine and add components to an entity by passing in class object references:


//add systems to engine engine.addSystem(Input); engine.addSystem(Renderer2D); //craete an entity of name "hero" var entity:Entity = engine.createEntity("hero"); //add components to entity //extra constructor arguments can be passed in entity.addComopnent(Transform2D, 10, 20); entity.addComponent(RenderTarget2D, new HeroShape());

To keep the engine running, the `Engine.update(dt:Number)`

method must be called repeatedly. This is referred to as the **game loop**.

private function init():void { //some other initialization code //... addEventListener(Event.ENTER_FRAME, gameLoop); } //The gameLoop method private var oldTime:int = 0; private function gameLoop(e:Event):void { var newTime:int = getTimer(); //dt is in seconds var dt:Number = 0.001 * (newTime - oldTime); //update engine engine.update(dt); oldTime = newTime; }

### The `getInstance()`

Method

Remember the code snippet in the `Renderer2D`

class from the [introduction](http://allenchou.net/2012/07/rusher-2-1-introduction/)?

//Renderer2D class override public function update(dt:Number):void { var iter:InListIterator = targets_.getIterator(); var target:RenderTarget2D; while (target = iter.data()) { var displayObject:DisplayObject = target.displayObject; if (displayObject) { var transform:Transform2D = target.getInstance(Transform2D); var displayTransform:Transform = displayObject.transform; displayTransform.matrix = transform.calculateMatrix(); displayObject.transform = displayTransform; } iter.next(); } }

You might wonder what object the call to `getInstance()`

returns reference to, and how Rusher knows which reference to return. It’s based on the **reference mapping rules** Rusher uses under the hood; I’ll write a dedicated post on this topic later. For now, all you need to remember is:

- If you pass in a system class reference, since there can only be one instance of each system type, the one system instance reference is returned.
- If you pass in a component class reference, a reference to the component object belonging to
**the same owner entity**, i.e. the**sibling**of that type, is returned. - If the component class reference passed in is followed by a name (string), then the method returns a reference to the component instance of that type belonging to the entity of the name.

With the `getInstance()`

method that is available in almost every scope, you can literally obtain references to all systems, entities, and components everywhere in your client code.