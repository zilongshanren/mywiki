---
title: Rusher 2 – Renderer2D | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2011/10/rusher-2-renderer2d/
author: Allen Chou
published: '2011-10-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

[Go to Rusher 2 project homepage](http://code.google.com/p/rusher/)

[Rusher 2 tutorial list](http://www.cjcat.net/rusher-2-tutorials/)

[View Renderer2D example](http://rusher.googlecode.com/svn/trunk/examples/Renderer2D/bin/index.html)

[Example source](http://rusher.googlecode.com/svn/trunk/examples/)

There is a built-in 2D camera-layer-based renderer system in Rusher 2, which is based on the 2D renderer in Rusher and the rendering system in [DigiPen ProjectFUN](http://projectfun.digipen.edu). You have other options than this, however. As you have already seen, you can implement your own 2D renderer like the `DisplayObjectUpdater`

system in previous examples.

**Cameras & Layers**

The `Renderer2D`

system models the scene as a camera, a HUD (heads-up display), and layers. The HUD is a sprite you can add display objects to that will be displayed on top of the entire scene and will not be distorted whatsoever. This is useful for displaying HUD elements such as character health, timer, and scores. Layers, on the other hand, will be displaced, rotated, scaled according to their relative position to the camera.

The `Renderer2D`

system uses right-handed coordinate system, meaning the positive z axis is pointing into the screen. The camera’s z position would be its negative focal length. Any layer having a z value smaller than the negative focal length would not be visible, since it is “behind” the camera. The position of every layer is updated every frame according to its relative position to the camera, which you may make use of to create a parallax effect. In addition, setting the `Layer.usePerspectiveScale`

property of a layer to true makes it scale according to the perspective projection equation:

//(x, y, z) is the point to be projected (projectedX, projectedY) = (x, y) * (focalLength / (z - cameraZ));


Here’s a visual representation of the relation between the camera and the layers.

![camera and layers](../../assets/fcabf9fd29ba6c2f.png)


**The Example**

This time we’re not creating an `EntityCreator`

system like we did in previous examples, which serves as a “one shot” system that creates and sets up everything and does nothing afterwards. We’re going to add a state machine system to the engine, and create an initial state. We’ll override the `State.onSet()`

method and write our “one shot” action inside.

Again, we’re extending the `BasicEngine`

class, so that we don’t have to add the clock and mouse system. A state machine system is added to the engine and the initial state is set to an `InitState`

object.

public class Renderer2DExampleEngine extends BasicEngine { private var _canvas:Sprite; public function Renderer2DExampleEngine(canvas:Sprite) { _canvas = canvas; } override protected function addSystems ( systemManager:ISystemManager ):void { super.addSystems(systemManager); var renderer:Renderer2D = new Renderer2D(); renderer.canvas.x = 400; renderer.canvas.y = 300; _canvas.addChild(renderer.canvas); systemManager.addSystem(renderer); systemManager.addSystem(new StateSystem(new InitState())); } }

In the `InitState.onSet()`

method, we invoke `createCamera()`

and `createLayers()`

.

public class InitState extends State { [Inject] public var renderer:Renderer2D; [Inject] public var entityManager:IEntityManager; override public function onSet():void { createCamera(); createLayers(); } private function createCamera():void { var camera:IEntity = entityManager.createEntity(); camera.addComponent(renderer.camera); camera.addComponent(new CameraController()); } private function createLayers():void { for (var i:int = 0; i < 8; ++i) { var layer:Layer = new Layer(); var gray:uint = 0x20 + i * 0x10; layer.addChild ( new WindowPane(gray << 16 | gray << 8 | gray) ); layer.z = i * 20; layer.usePerspectiveScale = true; renderer.addLayer(layer); } } }

The `Camera`

class actually implements the `IComponent`

interface and can be used as an ordinary component of an entity. We create an entity that holds a reference to the default camera object as a component, and we add a `CameraController`

component to the entity. This controller will alter the camera position and focal length in reaction to the mouse.

public class CameraController implements IComponent { [Inject] public var camera:Camera; [Inject] public var mouse:Mouse; [Inject] public var clock:Clock; [Inject] public var commandManager:CommandManager; [PostConstruct] public function listenToClock():void { clock.add(update); } private function update(dt:Number):void { camera.x = mouse.x - 400; camera.y = mouse.y - 300; if (mouse.isPressed()) { commandManager.execute ( new TweenNanoTo ( camera, 0.2, { focalLength: 100, overwrite: true } ) ); } else if (mouse.isReleased()) { commandManager.execute ( new TweenNanoTo ( camera, 0.2, { focalLength: 200, overwrite: true } ) ); } } }

It’s all done. Run the example and you can see how the renderer creates the effect of moving the camera with the mouse, and how it “zooms” in and out by altering the camera focal length.

cool