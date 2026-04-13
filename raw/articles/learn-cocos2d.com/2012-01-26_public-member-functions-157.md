---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3World.h>`


[CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is a [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) that manages a 3D scene.

[CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) has the following responsibilities:

When creating a 3D application, you will almost always create a subclass of [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) to define the control, features, and behaviour of your 3D world suitable to your application. In your [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) subclass, your will typically override one or more of the following template methods:

In these methods, you can manipulate most nodes by setting their properties. You can move and orient nodes using the node's location, rotation and scale properties, and can show or hide nodes with the node's visible property.

You should override the updateBeforeTransform: method if you need to make changes to the transform properties (location, rotation, scale), of any node. These changes will them automatically be applied to the transformMatrix of the node and its child nodes.

You should override the updateAfterTransform: method if you need access to the global transform properties (globalLocation, globalRotation, globalScale), of a node since these properties are only valid after the transformMatrix has been recalculated. An example of where access to the global transform properties would be useful is in the execution of collision detection algorithms.

To access nodes in your world, you can use the method getNodeNamed: on the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) (or any node). However, if you need to access the same node repeatedly, for example to update it on every frame, it's highly recommended that you retrieve it once and then cache it in an instance variable in your [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance.

By default, the initializeWorld, updateBeforeTransform:, and updateAfterTransform: methods do nothing. Subclasses do not need to invoke this default superclass implementations in the overridden methods. The updateBeforeTransform: and updateAfterTransform: methods are defined in the [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) class. See the documentation there.

If you change the contents of the world outside of the normal update mechanism, for instance, as a result of a user event, you may find that the next frame is rendered without the updated content. Depending on the degree of change to your world (for instance, if you have removed and added many nodes), you may notice a flicker. To avoid this, you can use the updateWorld method to force your updates to be processed immediately, without waiting for the next update interval.

You must add at least one [CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) to your 3D world to make it viewable. This camera may be added directly, or it may be added as part of a larger node assembly. Regardless of the technique used to add cameras, the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) will take the first camera added and automatically make it the activeCamera.

The camera can also be used to project global locations within the 3D world onto a 2D point on the screen view, and can be used to project 2D screen points onto a ray or plane intersection within the 3D world. See the class notes of [CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) for more information on mapping between 3D and 2D locations.

You can add fog to your world using the fog property. Fog has a color and blends with the display of objects within the world. Objects farther away from the camera are affected by the fog more than objects that are closer to the camera.

During drawing, the nodes can be traversed in the hierarchical order of the node structural assembly, starting at the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance that forms the root node of the node assembly. Alternately, and preferrably, the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) can use a [CC3NodeSequencer](http://www.learn-cocos2d.com/) instance to arrange the nodes into a linear sequence, ordered and grouped based on definable sorting priorities. This is beneficial, because it allows the application to order and group drawing operations in ways that reduce the number and scope of state changes within the GL engine, thereby improving performance and throughput.

For example, when drawing, nodes could be grouped by the drawing sequencer so that opaque objects are drawn prior to blended objects, and an application with many objects that use the same material or mesh can be sorted so that nodes with like materials or meshes are grouped together. It is highly recommended that you use a [CC3NodeSequencer](http://www.learn-cocos2d.com/), and this is the default configuration for [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instances.

The [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) maintains this drawing sequence separately from the hierarchical node assembly. This allows the maintenance of the hierarchical parent-child relationships for operations such as movement and transformations, while simultaneously enabling more efficient drawing operations through node drawing sequencing.

An instance of [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) is held by an instance of [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), which is a subclass of the cocos2d CCLayer class, and can participate with other cocos2d layers and CCNodes in an overall cocos2d scene. During drawing, the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) delegates all 3D operations to its [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance. You will also typically create a subclass of [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) that is customized for your application. In most cases, you will add methods and state to both your [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) and [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) subclasses to facilitate user interaction.

The [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) and [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) can process touch events. To enable touch event handling, set the isTouchEnabled property of your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to YES. Touch events are forwarded from the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to the touchEvent:at: method of your [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) for handling by your [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/).

Since the touch-move events are both voluminous and seldom used, the implementation of ccTouchMoved:withEvent: has been left out of the default [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) implementation. To receive and handle touch-move events for object picking, copy the commented-out ccTouchMoved:withEvent: template method implementation in [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) subclass.

The default implementation of the touchEvent:at: method forwards all touch events to the node picker held in the touchedNodePicker property. The node picker determines which 3D node is under the touch point. Object picking is handled asynchronously, and once the node is retrieved, the nodeSelected:byTouchEvent:at: callback method will be invoked on your customized [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance. You indicate which nodes in your world should respond to touch events by setting the isTouchEnabled property on those nodes that you want to trigger a touch event callback to the nodeSelected:byTouchEvent:at: method. See the description of the nodeSelected:byTouchEvent:at: method and the [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) isTouchEnabled property for useful hints about choosing which nodes to enable for touch selection.

Be aware that node picking from touch events is expensive, and you should override the touchEvent:at: method to forward to the node picker only those touch events that you actually intend to select a node. By default, all touch events are forwarded from the touchEvent:at: method. You should override this implementation, handle touch events that are not used for selection directly in this method, and forward only those events for which you want a node picked, to the touchedNodePicker.

The node picker uses a colorization algorithm to determine which node is under the touch point. When a touch event occurs and has been forwarded to the node picker, the node picker draws the scene in solid colors, with each node a different color, and then reads the color of the pixel under the touch point to identify the object under the touch point. This is performed under the covers, and the scene is immediately redrawn in true colors and textures before being presented to the screen, so the user is never aware that the scene was drawn twice. However, be aware that, if a translucent or transparent object has nothing but the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) background color behind it, AND that [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) background color is also translucent or transparent, you might notice an unavoidable flicker of the translucent node. To avoid this, you can use a backdrop or skybox in your 3D world. This issue only occurs during node picking, and only when BOTH the node and the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) background colors are translucent or transparent, and the backgound color is directly behind the node.

Depending on the complexity of the application, it may instantiate a single [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/), instance, or multiple instances if the application progresses from scene to scene. Similarly, the application may have a single [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), or multiple CC3Layers. Each [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) may have its own [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance, or may share a single instance.

To maximize GL throughput, all OpenGL ES 1.1 state is tracked by the singleton instance [[CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) engine]. [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) only sends state change calls to the GL engine if GL state really is changing. It is critical that all changes to GL state are made through the [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton. When adding or overriding functionality in this framework, do NOT make gl* function calls directly if there is a corresponding state change tracker in the [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton. Route the state change request through the [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton instead.

You can collect statistics about the performance of your cocos3d application by setting the performanceStatistics property to an appropriate instance of a statistics collector. By default, no statistics are collected. See the notes of the performanceStatistics property for more information.

Instantiates an instance of [CC3PODResourceNode](http://www.learn-cocos2d.com/), loads it from the POD file at the specified path, which must be an absolute path, and adds the [CC3PODResourceNode](http://www.learn-cocos2d.com/) instance as a child node to this [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance.

The name of the resource node will be that of the file.

| void
|

` [virtual]`

Instantiates an instance of [CC3PODResourceNode](http://www.learn-cocos2d.com/) with the specified name, loads it from the POD file at the specified path, which must be an absolute path, and adds the [CC3PODResourceNode](http://www.learn-cocos2d.com/) instance as a child node to this [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance.

Instantiates an instance of [CC3PODResourceNode](http://www.learn-cocos2d.com/), loads it from the POD file at the specified resource path, and adds the [CC3PODResourceNode](http://www.learn-cocos2d.com/) instance as a child node to this [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance.

The name of the resource node will be that of the file.

The specified file path is a path relative to the resource directory. Typically this means that the specified path can just be the name of the file, with no path information.

| void
|

` [virtual]`

Instantiates an instance of [CC3PODResourceNode](http://www.learn-cocos2d.com/) with the specified name, loads it from the POD file at the specified resource path, and adds the [CC3PODResourceNode](http://www.learn-cocos2d.com/) instance as a child node to this [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance.

The specified file path is a path relative to the resource directory. Typically this means that the specified path can just be the name of the file, with no path information.

| id CC3World::drawVisitorClass | ( | ) | ` [virtual]` |

Returns the class of visitor that will automatically be instantiated into the drawVisitor property.

The returned class must be a subclass of [CC3NodeDrawingVisitor](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_drawing_visitor/). This implementation returns [CC3NodeDrawingVisitor](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node_drawing_visitor/). Subclasses may override to customize the behaviour of the drawing visits.

| void CC3World::drawWorld | ( | ) | ` [virtual]` |

This method is invoked periodically when the objects in the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) are to be drawn.

Typcially this method is invoked automatically from the draw method of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) instance. This method is invoked asynchronously to the model updating loop, to keep the processing of OpenGL ES drawing separate from model updates.

To maximize GL throughput, all OpenGL ES 1.1 state is tracked by the singleton instance [[CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) engine]. [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) only sends state change calls to the GL engine if GL state really is changing. It is critical that all changes to GL state are made through the [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton. When overriding this method, or any other 3D drawing features, do NOT make gl* function calls directly if there is a corresponding state change tracker in the [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton. Route the state change request through the [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton instead.

This method is invoked automatically during each rendering frame. Usually, the application never needs to invoke this method directly.

| void CC3World::initializeWorld | ( | ) | ` [virtual]` |

This template method is where a subclass should populate the 3D world models.

This can be accomplished through a combination of instantiting model objects directly and loading them from model data files exported from a 3D editor.

This [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance forms the base of a structural tree of nodes. Model objects are added as nodes to this root node instance using the addChild: method.

When loading from files, or adding large node assemblies, you can access individual nodes using the getNodeNamed: method, if you need to set futher initial state.

If you will need to access the same node repeatedly, for example to update it on every frame, it's highly recommended that you retrieve it once in this method, and cache it in an instance variable in your [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) subclass instance.

You must add at least one [CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) to your 3D world to make it viewable. This can be instantiated directly, or loaded from a file as part of a node assembly.

By default, this method does nothing. Subclasses do not need to invoke this default superclass implementation in the overridden method.

| void CC3World::nodeSelected:byTouchEvent:at: | ( |
|

` [virtual]`

This callback template method is invoked automatically from the touchedNodePicker when a node has been picked as a result of a touch event.

The specified node will be one of the visible nodes whose isTouchable property returns YES, or will be nil if the touch event occurred in an area under which there is no 3D node that is touch enabled.

For node assemblies, the specified node will not necessarily be the individual component or leaf node that was touched. The specified node will be the closest structural ancestor of the leaf node that has the isTouchEnabled property set to YES.

For example, if the node representing a wheel of a car is touched, it may be more desireable to identify the car as being the object of interest to be selected, instead of the wheel. In this case, setting the isTouchEnabled property to YES on the car, but to NO on the wheel, will allow the wheel to be touched, but the node received by this callback will be the car structural node.

The touchType is one of the enumerated touch types: kCCTouchBegan, kCCTouchMoved, kCCTouchEnded, or kCCTouchCancelled. The touchPoint is the location in 2D coordinate system of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) where the touch occurred.

This callback is received as part of the update processing loop, and is invoked before the invocation of either the updateBeforeTransform: and updateAfterTransform: methods. This callback is invoked only once per event.

To enable touch events, set the isTouchEnabled property of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/).

Since the touch-move events are both voluminous and seldom used, the handling of ccTouchMoved:withEvent: has been left out of the default [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) implementation. To receive and handle touch-move events for object picking, copy the commented-out ccTouchMoved:withEvent: template method implementation in [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) subclass.

In addition, node selection is expensive, and you should only propagate touch events from touchEvent:at: that actually intend to select a node. By default, all touch events are propagated from touchEvent:at:, but in practice, you should override that method and handle touch events that are not used for selection in that method.

For example, if you want to let a user touch an object and move it around with their finger, only the initial touch-down event needs to select a node. Once the node is selected, you can cache the node, and move it and release it by capturing the touch-move and touch-up events in the touchEvent:at: method, and avoid propagating them to the selection mechanism.

To enable a node to be selectable by touching, set the isTouchEnabled property of that node, or an ancestor node to YES.

This implementation does nothing. Subclasses that are interested in node picking will override.

Usually, you would not invoke this method directly. This method is invoked automatically whenever a touch event occurs and is processed by the touchEvent:at: method. If you are handling touch events, multi-touch events, or gestures within your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), invoke the touchEvent:at: method to initiate node selection, and implement this callback method to determine what to do with selected nodes.

| void CC3World::pause | ( | ) | ` [virtual]` |

Pauses the dynamics of the 3D world model, including internal updates and CCActions, by setting the isRunning property to NO.

The world will automatically start playing when added to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), and will automatically pause when removed from the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/). During typical use, you will not need to invoke this method directly.

| id CC3World::pickVisitorClass | ( | ) | ` [virtual]` |

Returns the class of visitor that will be instantiated in the touchedNodePicker pickTouchedNode method, in order to paint each node a unique color so that the node under the touched pixel can be identified.

The returned class must be a subclass of [CC3NodePickingVisitor](http://www.learn-cocos2d.com/). This implementation returns [CC3NodePickingVisitor](http://www.learn-cocos2d.com/). Subclasses may override to customized the behaviour of the drawing visits.

| void CC3World::play | ( | ) | ` [virtual]` |

Starts the dynamics of the 3D world model, including internal updates and CCActions, by setting the isRunning property to YES.

The world will automatically start playing when added to a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), and will automatically pause when removed from the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/). During typical use, you will not need to invoke this method directly.

| void CC3World::touchEvent:at: | ( | uint | touchType, |
| [at] CGPoint | touchPoint |
||
| ) | ` [virtual]` |

This method is invoked from the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) whenever a touch event occurs, if that layer has indicated that it is interested in receiving touch events, and is handling them.

The touchType is one of the enumerated touch types: kCCTouchBegan, kCCTouchMoved, kCCTouchEnded, or kCCTouchCancelled, and may have originated as a single-touch event, a multi-touch event, or a gesture event.

To enable touch events, set the isTouchEnabled property of the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/). Once the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) is touch-enabled, this method is invoked automatically whenever a single-touch event occurs.

Since the touch-move events are both voluminous and seldom used, the handling of ccTouchMoved:withEvent: has been left out of the default [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) implementation. To receive and handle touch-move events for object picking, copy the commented-out ccTouchMoved:withEvent: template method implementation in [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) to your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) subclass.

This default implementation forwards touch-down events to the node picker held in the touchedNodePicker property, which determines which 3D node is under the touch point, and does nothing with touch-move and touch-up events. For the touch-down events, object picking is handled asynchronously, and once the node is retrieved, the nodeSelected:byTouchEvent:at: callback method will be invoked on this instance.

Node picking from touch events is somewhat expensive. If you do not require node picking, you should override this implementation and avoid forwarding the touch-down events to the node picker. You can also override this method to enhance the touch interaction, such as swipe detection, or dragging & dropping objects. You can use the implementation of this method as a template for enhancements.

For example, if you want to let a user touch an object and move it around with their finger, only the initial touch-down event needs to select a node. Once the node is selected, you can cache the node, and move it and release it by capturing the touch-move and touch-up events in this method.

To support multi-touch events or gestures, add event-handing behaviour to your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), as you would for any cocos2d application, and invoke this method from your customized [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) when interaction with 3D objects, such as node-picking, is required.

| id CC3World::updateVisitorClass | ( | ) | ` [virtual]` |

Returns the class of visitor that will automatically be instantiated into the updateVisitor property.

The returned class must be a subclass of [CC3NodeUpdatingVisitor](http://www.learn-cocos2d.com/). This implementation returns [CC3NodeUpdatingVisitor](http://www.learn-cocos2d.com/). Subclasses may override to customize the behaviour of the updating visits.

| void CC3World::updateWorld | ( | ) | ` [virtual]` |

Invokes the udpateWorld: method with the value of the minUpdateInterval property.

This method temporarily ensures that the isRunning property is set to YES internally, to ensure that the updateWorld: method will run successfully.

You can use this method if you change the contents of the world outside of the normal update mechanism, for instance, as a result of a user event, and need the update to be processed immediately, without waiting for the next update interval, and even if the world has not been set running yet via the play method, or isRunning property.

This method is automatically invoked when a the world is assigned to the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), and when the world is added to a running [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), to ensure that transforms have been processed before the first rendering frame draws the contents of the world.

| void CC3World::updateWorld: | ( | ccTime | dt | ) | ` [virtual]` |

This method is invoked periodically when the components in the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) are to be updated.

Typcially this method is invoked automatically from a [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) instance via a scheduled update, but may also be invoked by some other periodic operation, or even directly by the application.

This method is invoked asynchronously to the frame rendering animation loop, to keep the processing of model updates separate from OpenGL ES drawing.

The dt argument gives the interval, in seconds, since the previous update. This value can be used to create realistic real-time motion that is independent of specific frame or update rates. If either of the minUpdateInterval or maxUpdateInterval properties have been set, this method will clamp dt to those limits. See the description of minUpdateInterval and maxUpdateInterval for more information about clamping the update interval.

If this instance is not running, as indicated by the isRunning property, this method does nothing.

As implemented, this method performs the following processing steps, in order:

Sublcasses should not override this updateWorld: method. To customize the behaviour of the 3D model world, sublcasses should override the updateBeforeTransform: or updateAfterTransform: methods. Those two methods are defined and documented in the [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/) class. Please refer there for more documentation.

This method is invoked automatically at each scheduled update. Usually, the application never needs to invoke this method directly.

| id CC3World::world | ( | ) | ` [static, virtual]` |

Allocates and initializes an autoreleased unnamed instance with an automatically generated unique tag value.

The tag value is generated using a call to nextTag.

The 3D camera that is currently displaying the scene of this world.

You can set this property directly, or if this property is not set directly, it will be set automatically to the first [CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) added to this world via the addChild: method, including cameras contained somewhere in a structural assembly of nodes whose root node was added to this instance via addChild:. In this way, adding the root node of a node assembly loaded from a file will set the activeCamera property to the first camera found in the assembly, if the property was not already set.

The converse occurs when a camera is removed from the world using the removeChild: method. The camera will be removed as the activeCamera, and the second camera that was previously added (assuming more than one was added) will automatically be set as the activeCamera. Again, this is true even if the root node of a large assembly containing the active camera is removed from the world using the removeChild: method.

The initial value is nil. You must add at least one [CC3Camera](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_camera/) to your 3D world to make it viewable.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a6c93e6c1c60cf0757df9bd33cdc09fbb).

ccColor4F CC3World::ambientLight` [read, write, assign]` |

The color of the ambient light of the world.

This is independent of any [CC3Light](http://www.learn-cocos2d.com/) nodes that are added as child nodes. You can use this to provide general flat lighting in your world without having to add light nodes.

The initial value is set to kCC3DefaultLightColorAmbientWorld.

The node sequencer being used by this instance to order the drawing of child nodes.

During drawing, the nodes can be traversed in the hierarchical order of the node structural assembly, starting at the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance that forms the root node of the node assembly. Alternately, and preferrably, the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) can use a [CC3NodeSequencer](http://www.learn-cocos2d.com/) instance to arrange the nodes into a linear sequence, ordered and grouped based on definable sorting priorities. This is beneficial, because it allows the application to order and group drawing operations in ways that reduce the number and scope of state changes within the GL engine, thereby improving performance and throughput.

For example, when drawing, nodes could be grouped by the drawing sequencer so that opaque objects are drawn prior to blended objects, and an application with many objects that use the same material or mesh can be sorted so that nodes with like materials or meshes are grouped together. It is highly recommended that you use a [CC3NodeSequencer](http://www.learn-cocos2d.com/).

The default drawing sequencer includes only nodes with local content, and groups them so that opaque nodes are drawn first, then nodes with blending.

The sequencer visitor used to visit the drawing sequencer during operations on the drawing sequencer, such as adding or removing individual nodes.

This property defaults to an instance of the [CC3NodeSequencerVisitor](http://www.learn-cocos2d.com/) class. The application can set a different visitor if desired.

The visitor that is used to visit the nodes to draw them to the GL engine.

This property defaults to an instance of the class returned by the drawVisitorClass method. The application can set a different visitor if desired.

If set, creates fog within the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/).

Fog has a color and blends with the display of objects within the world. Objects farther away from the camera are affected by the fog more than objects that are closer to the camera.

The initial value is nil, indicating that the world will contain no fog.

BOOL CC3World::isUsingDrawingSequence` [read, assign]` |

Returns whether this instance is using a drawing sequencer.

ccTime CC3World::maxUpdateInterval` [read, write, assign]` |

If the value of this property is greater than zero, it will be used as the upper limit accepted by the updateWorld: method.

Values sent to the updateWorld: method that are larger than this maximum will be clamped to this limit. If the value of this property is zero (or negative), the updateWorld: method will use the value that is passed to it unchanged.

Resource limitations, and activities around start-up and shut-down, can sometimes cause an occasional large interval between consecutive updates. These large intervals can sometimes cause object in the world to appear to jump around, and if you are using physics simulation, might cause collisions to be missed.

Setting a maximum update interval can help eliminate both concerns, but the trade-off may be less realistic real-time behaviour. With a limit in place, larger intervals between updates will make the world appear to run in slow motion, rather than jump around.

The initial value of this property is set to kCC3DefaultMaximumUpdateInterval.

The behaviour described here does not apply to nodes controlled by CCActionIntervals, which are not affected by the time between updates, or the value of this property.

ccTime CC3World::minUpdateInterval` [read, write, assign]` |

The value of this property is used as the lower limit accepted by the updateWorld: method.

Values sent to the updateWorld: method that are smaller than this maximum will be clamped to this limit. If the value of this property is zero (or negative), the updateWorld: method will use the value that is passed to it unchanged.

You can set this value if your custom world cannot work with a zero interval, or with an interval that is too small. For instance, if the logic of your world uses the update interval as the denominator in a division calculation, you would want to set this property to a value slightly above zero.

The initial value of this property is set to kCC3DefaultMinimumUpdateInterval.

The behaviour described here does not apply to nodes controlled by CCActionIntervals, which are not affected by the time between updates, or the value of this property.

If set, collects statistics about the updating and drawing performance of the 3D world.

By default, this property is nil, and no statistics are accumulated. To accumulate statistics, set this property with an appropriate instance. Subclasses of [CC3PerformanceStatistics](http://www.learn-cocos2d.com/) can customize the statistics that are collected.

To allow flexibility in accumulating statistics, the statistics collector does not automatically clear the accumulated statistics. If you set this property with a statistic collector, it is your responsibility to read the values, and reset the performanceStatistics instance periodically, using the [CC3PerformanceStatistics](http://www.learn-cocos2d.com/) reset method, to ensure that the counters do not overflow. Depending on the complexity and capabilities of your application, you should reset the performance statistics at least every few seconds.

Implements [CC3Node](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_node/#a968396edac85926dcd809809220f0489).

BOOL CC3World::shouldClearDepthBufferBefore2D` [read, write, assign]` |

Indicates whether the OpenGL depth buffer should be cleared before reverting back to the 2D world.

If 2D content will be drawn on top of the 3D content, AND it is being drawn with depth testing enabled, then this property should be set to YES.

However, if this is not the case, then this property can be set to NO to skip the overhead of clearing of the depth buffer when transitioning from 3D back to 2D.

Clearing the depth buffer is a relatively expensive operation, and avoiding it when it is not necessary can result in a performance improvement. Because of this, it is recommended that this property be set to NO, and turn depth testing off during drawing of the 2D content on top of the 3D world.

You can turn depth testing off for the 2D content by invoking the following code once during the initialization of your application after the EAGLView has been created:

[[CCDirector sharedDirector] setDepthTest: NO];

By doing so, you will then be able to set this property to NO and still be able to draw 2D content on top of the 3D world, while avoiding an unnecessary clearing of the depth buffer.

The initial value of this property is YES. Set this property to NO to improve performance if depth-testing 2D content is not being drawn on top of 3D content.

BOOL CC3World::shouldClearDepthBufferBefore3D` [read, write, assign]` |

Indicates whether the OpenGL depth buffer should be cleared before drawing the 3D world.

If the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/), or other 2D nodes that the [CC3Layer](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_layer/) may be contained within, have drawn 2D content on which the 3D world is to be drawn on top of, AND is using depth testing, then this property should be set to YES to ensure that the 3D content will not conflict with the previously drawn 2D content, and will be drawn on top of that 2D content.

However, if this is not the case, then this property can be set to NO to skip the overhead of clearing of the depth buffer when transitioning from 2D to 3D.

Clearing the depth buffer is a relatively expensive operation, and avoiding it when it is not necessary can result in a performance improvement. Because of this, it is recommended that this property be set to NO unless conflicts arise when drawing 3D content over previously drawn 2D content.

The initial value of this property is YES. Set this property to NO to improve performance if 3D content is not being drawn on top of 2D content.

The touchedNodePicker picks the node under the point at which a touch event occurred.

Touch events are forwarded to the touchedNodePicker from the touchEvent:at: method when a node is to be picked from a particular touch event.

The visitor that is used to visit the nodes when transforming them without updating.

This property defaults to an instance of the class returned by the transformVisitorClass method. The application can set a different visitor if desired.

The visitor that is used to visit the nodes to update and transform them during scheduled updates.

This property defaults to an instance of the class returned by the updateVisitorClass method. The application can set a different visitor if desired.

The viewport manager manages the viewport and device orientation, including handling coordinate rotation based on the device orientation, and conversion of locations and points between the 3D and 2D coordinate systems.