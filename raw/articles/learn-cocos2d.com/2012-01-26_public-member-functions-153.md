---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3Layer.h>`


| void |
|

[CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) is a cocos2d CCLayer that supports full 3D rendering in combination with normal cocos2d 2D rendering.

It forms the bridge between the 2D and 3D drawing environments.

The [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) contains an instance of [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), and delegates all 3D operations, for both updating and drawing 3D models, to the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance.

In addition, like any cocos2d CCLayer, 2D child CCNodes can be added to this layer and will be rendered either over or under the 3D world, based on their individual Z-order. In particular, 2D controls such as menus, sprites, labels, health bars, joysticks, etc, can be overlayed on the 3D world simply by adding them as children of this layer. Similarly, a 2D backdrop could be rendered behind the 3D world by adding an appropriate CCNode as a child with a negative Z-order.

Like other CCNodes, this layer can be added to another 2D node, and given a contentSize, position, and scale. You can even dynamically move and scale the embedded [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) using CCActions.

Changes to the position and scale of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) are propagated to the viewport of the contained [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), and to any child CC3Layers and CC3Worlds.

However, these properties will only be propagated if the node being moved is a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/). If the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) is a child of a regular 2D CCLayer or CCNode, and that node is moved, the resulting changes to the position or scale of the child [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) may not automatically be propagated to the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) viewport. In this case, you can use the updateViewport method of [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to ensure that the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) viewport is aligned with the position and scale of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

[CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) descends from CCLayerColor, and will draw a colored background behind both 2D and 3D content if configured with a background color.

To make use of the standard cocos2d model updatating functionality to update and animate the 3D world, use the scheduleUpdate or schedule:interval: methods of [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to invoke periodic callbacks to the update: method of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) instance. The update: method forwards these callbacks to the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance held by the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

To enable simple single-touch event handling for this layer, set the isTouchEnabled property to YES. Once enabled, single-touch events will automatically be forwarded to the touchEvent:at: method on your customized [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance to support user selection of 3D nodes via touches. For more information on handling 3D node selections, see the description of the method nodeSelected:byTouchEvent:at: of [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/).

Since the touch-move events are both voluminous and seldom used, the implementation of ccTouchMoved:withEvent: has been left out of the default [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) implementation. To receive and handle touch-move events for object picking, copy the commented-out ccTouchMoved:withEvent: template method implementation in [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) subclass.

For more sophisticated touch interfaces, such as multi-touch events or gestures, add event-handing behaviour to your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), as you would for any cocos2d application and, when required, invoke the touchEvent:at: method on your customized [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) to initiate node selection.

Most 3D games will be displayed in full-screen mode, so typically your custom [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) will be sized to cover the entire screen. However, the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) can indeed be set to a contentSize less that the full window size, and may be positioned on the window, or within a parent CCLayer like any other CCNode.

You can even dyanamically move your [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) around within the window, by changing the position property (for example, by using a CCMoveTo action).

[CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) directly descends from [ControllableCCLayer](http://www.learn-cocos2d.com/), which means that it can optionally be controlled by a [CCNodeController](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c_node_controller/) instance. Doing so enables two features:

With the [CCNodeController](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c_node_controller/) attached, either or both of these features can be turned on or off. If neither of these features is required, there is no need to instantiate and attach a [CCNodeController](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c_node_controller/), and the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) can be used without it.

For most applications, you will create subclasses of both [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) and [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/). The customized subclass of [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) manages the behaviour of the 3D resources. The customized subclass of [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) manages the 2D artifacts, such as menus, sprites, labels, health bars, joysticks, etc, that you want to overlay on the 3D scene.

Typically, you will create a separate instance of [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) for each 3D scene. You can also create a distinct [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) for each scene as well or, more typically, reuse a single [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) instance across multiple [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) scenes by simply assigning a differnt [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance to the layer. Any running actions in the old world are automatically paused, and any running actions in the new world are automatically started. For more information on swapping 3D scenes, see the notes on the cc3World property.

To create and use your [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) and [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) pair, follow these steps:

| void CC3Layer::drawBackdrop | ( | ) | ` [virtual]` |

If a background color has been specified, and this layer is not overlaying the device camera, draws the background color over the entire layer.

This method is invoked automatically when this layer is drawn. The application should never need to invoke this method directly.

| void CC3Layer::initializeControls | ( | ) | ` [virtual]` |

Template method that is invoked automatically during initialization, regardless of the actual init* method that was invoked.

Subclasses can override to set up their 2D controls and other initial state without having to override all of the possible superclass init methods.

This default implementation does nothing. It is not necessary to invoke this superclass implementation when overriding in a subclass.

| void CC3Layer::update: | ( | ccTime | dt | ) | ` [virtual]` |

This method is invoked periodically when the components in the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) are to be updated.

The dt argument gives the interval, in seconds, since the previous update.

This implementation forwards this update to the updateWorld: method of the contained [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance. Subclasses can override to perform updates to 2D nodes added to this layer, but should be sure to invoke this superclass implementation, or to invoke updateWorld: on the cc3World directly.

Typcially this method is scheduled to be invoked automatically at a periodic interval by using the scheduleUpdate or schedule:interval: methods of this instance, but may also be invoked by some other periodic operation, or even directly by the application.

This method is invoked asynchronously to the frame rendering animation loop, to keep the processing of model updates separate from OpenGL ES drawing.

| void CC3Layer::updateViewport | ( | ) | ` [virtual]` |

Updates the viewport of the contained [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance with the dimensions of this layer and the device orientation.

This method is invoked automatically when the position, size, scale, or orientation of this layer changes. You do not need to invoke this method when changing the position or scale of the layer. These changes are forwarded to the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) viewport automatically.

Usually, the application should never need to invoke this method directly. However, if your application changes the orientation of this layer in a manner that is not automatically detected, you can use this method to align the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) viewport with the updated layer.

The [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance that maintains the 3D models and draws the 3D content.

If your application contains multiple 3D scenes, you can swap between these scenes by simply setting the value of this property to the new scene. The old [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance is released. So if you want to swap that old world back into this layer at some point in the future, you should cache it somewhere, or recreated it.

When the old world is released, it will clean up after itself, including all the nodes and meshes it contains.

If this layer already has a [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) assigned, the wasRemoved method of the existing [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) to stop and remove any CCActions running on it and the nodes it contains.

You can set the shouldCleanupWhenRemoved of the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) to NO if you want the CCActions attached to the world and its nodes to be paused, but not stopped and removed. Be aware that CCActions that are paused, but not stopped, will retain the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), and could be cause for memory leaks if not managed correctly. Please see the notes of the [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) shouldCleanupWhenRemoved property and the [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) wasRemoved method for more information.

Setting this property automatically invokes the udpateWorld method on the new world to ensure that the transforms are up to date before the next frame is rendered.

BOOL CC3Layer::isOpaque` [read, assign]` |

Returns whether this layer is opaque.

Return YES if the isColored property returns YES and the opacity property returns 255, otherwise returns NO.

BOOL CC3Layer::shouldAlwaysUpdateViewport` [read, write, assign]` |

Indicates whether this layer should update the 3D viewport on each rendering frame.

If the value of this property is YES, the 3D viewport will be updated before each frame is drawn. This is sometimes useful if the layer is changing in a way that is not automatically tracked by the 3D world.

You do not need to set this property when changing the position or scale of the layer. These changes are forwarded to the 3D world automatically.

The initial value of this property is NO. Unless you encounter issues when modifying the layer, leave this property set to NO, to avoid the overhead of calculating an unnecessary transformation matrix on each frame render.

As an alternate to updating the viewport on every frame render, consider invoking the updateViewport method whenever your application changes the orientation of this layer in a manner that is not automatically propagated to the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) viewport.