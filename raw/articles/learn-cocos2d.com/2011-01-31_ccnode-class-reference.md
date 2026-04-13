---
title: CCNode Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCNode.h](http://www.learn-cocos2d.com/)"

Inherited by [CCAtlasNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_atlas_node/), [CCLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/), [CCMenuItem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu_item/), [CCMotionStreak](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_motion_streak/), [CCParallaxNode](http://www.learn-cocos2d.com/), [CCParticleSystem](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_particle_system/), [CCProgressTimer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_progress_timer/), [CCRenderTexture](http://www.learn-cocos2d.com/), [CCRibbon](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_ribbon/), [CCScene](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_scene/), [CCSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite/), [CCSpriteBatchNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite_batch_node/), and [CCTMXTiledMap](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_t_m_x_tiled_map/).

[CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) is the main element. Anything thats gets drawn or contains things that get drawn is a [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/). The most popular CCNodes are: [CCScene](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_scene/), [CCLayer](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_layer/), [CCSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite/), [CCMenu](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_menu/).

The main features of a [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) are:

Some [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) nodes provide extra functionality for them or their children.

Subclassing a [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) usually means (one/all) of:

Features of [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/):

Default values:

Limitations:

Order in transformations with grid disabled

Order in transformations with grid enabled

Camera:

Adds a child to the container with z-order as 0. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with a z-order. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with z order and tag. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

| - (CGRect) boundingBox |

returns a "local" axis aligned bounding box of the node in points. The returned box is relative only to its parent. The returned box is in Points.

| - (CGRect) boundingBoxInPixels |

returns a "local" axis aligned bounding box of the node in pixels. The returned box is relative only to its parent. The returned box is in Points.

| - (void) cleanup |

Stops all running actions and schedulers. IMPORTANT: if you override this method in your class you MUST call [super cleanup] otherwise actions/schedulers may not be deallocated, causing the whole node to be leaked!

| - (CGPoint) convertToNodeSpace: | (CGPoint) | worldPoint |

Converts a Point to node (local) space coordinates. The result is in Points.

| - (CGPoint) convertToNodeSpaceAR: | (CGPoint) | worldPoint |

Converts a Point to node (local) space coordinates. The result is in Points. treating the returned/received node point as anchor relative.

| - (CGPoint) convertTouchToNodeSpace: | (UITouch *) | touch |

Converts a UITouch to node (local) space coordinates. The result is in Points.

| - (CGPoint) convertTouchToNodeSpaceAR: | (UITouch *) | touch |

Converts a UITouch to node (local) space coordinates. The result is in Points. This method is AR (Anchor Relative)..

| - (CGPoint) convertToWorldSpace: | (CGPoint) | nodePoint |

Converts a Point to world space coordinates. The result is in Points.

| - (CGPoint) convertToWorldSpaceAR: | (CGPoint) | nodePoint |

Converts a local Point to world space coordinates.The result is in Points. treating the returned/received node point as anchor relative.

| - (void) draw |

Override this method to draw your own node. The following GL states will be enabled by default:

AND YOU SHOULD NOT DISABLE THEM AFTER DRAWING YOUR NODE

But if you enable any other GL state, you should disable it after drawing your node.

IMPORTANT: you should always call [super draw] if you override this method out of "good OOP manners", even if it normally doesn't draw itself (eg. [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/)).

Gets an action from the running action list given its tag

| - (id) init |

Default initializer.

| + (id) node |

Default autorelease initializer. Allocates and initializes a node and sends the autorelease message to it.

| - (CGAffineTransform) nodeToParentTransform |

Returns the matrix that transform the node's (local) space coordinates into the parent's space coordinates. The matrix is in Pixels.

| - (CGAffineTransform) nodeToWorldTransform |

Retrusn the world affine transform matrix. The matrix is in Pixels.

| - (int) numberOfRunningActions |

Returns the numbers of actions that are running plus the ones that are schedule to run (actions in actionsToAdd and actions arrays). Composable actions are counted as 1 action. Example: If you are running 1 Sequence of 7 actions, it will return 1. If you are running 7 Sequences of 2 actions, it will return 7.

| - (void) onEnter |

Called every time the [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) becomes active in the node hierarchy, for example by adding it as child or when transitioning to a new scene. If the [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) enters the 'stage' with a transition, this callback is called when the transition starts. IMPORTANT: Within this method you must not modify the [[self parent] children] array. IMPORTANT: If you override this method in your class you MUST call [super onEnter] to make sure the node is fully initialized!

| - (void) onEnterTransitionDidFinish |

Same as onEnter, except it is called when the transition has finished. If there is no transition it will be called right after onEnter. IMPORTANT: Within this method you must not modify the [[self parent] children] array. IMPORTANT: if you override this method in your class you MUST call [super onEnter] to make sure the node is fully initialized!

| - (void) onExit |

Called every time the [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) becomes inactive in the node hierarchy, for example by removing it from its parent or when transitioning to a different scene. If the [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) leaves the 'stage' with a transition, this callback is called when the transition finishes. IMPORTANT: Within this method you must not modify the [[self parent] children] array. IMPORTANT: if you override this method in your class you MUST call [super onEnter] to make sure the node is fully initialized!

| - (CGAffineTransform) parentToNodeTransform |

Returns the matrix that transform parent's space coordinates to the node's (local) space coordinates. The matrix is in Pixels.

| - (void) pauseSchedulerAndActions |

pauses all scheduled selectors and actions. Called internally by onExit

| - (void) removeAllChildrenWithCleanup: | (BOOL) | cleanup |

Removes all children from the container and do a cleanup all running actions depending on the cleanup parameter.

Removes a child from the container. It will also cleanup all running actions depending on the cleanup parameter.

| - (void) removeChildByTag: | (int) | tag |
||
| cleanup: | (BOOL) | cleanup | ||

Removes a child from the container by tag value. It will also cleanup all running actions depending on the cleanup parameter

| - (void) removeFromParentAndCleanup: | (BOOL) | cleanup |

Remove itself from its parent node. If cleanup is YES, then also remove all actions and callbacks. If the node orphan, then nothing happens.

Reorders a child according to a new z value. The child MUST be already added. Keep in mind that this method removes and inserts the child to the children array which can be a costly operation if there are many (hundreds) of children. If you need to reorder Z often consider switching to 2D Projection with Depth Buffer and using the vertexZ property to change the z order of nodes.

| - (void) resumeSchedulerAndActions |

resumes all scheduled selectors and actions. Called internally by onEnter

Executes an action, and returns the action that is executed. The node becomes the action's target.

| - (void) schedule: | (SEL) | s |

schedules a selector. The scheduled selector will be called every frame. The first call will be in the frame after the selector was scheduled, so you can use this method to delay execution of a method by one frame.

schedules a custom selector with an interval time in seconds. If time is 0 it will be ticked every frame. If time is 0, it is recommended to use 'scheduleUpdate' instead.

If the selector is already scheduled, then the interval parameter will be updated without scheduling it again.

| - (void) scheduleUpdate |

check whether a selector is scheduled. schedules the "update" method. It will use the order number 0. This method will be called every frame. Scheduled methods with a lower order value will be called before the ones that have a higher order value. Only one "udpate" method could be scheduled per node.

| - (void) scheduleUpdateWithPriority: | (int) | priority |

schedules the "update" selector with a custom priority. This selector will be called every frame. Scheduled selectors with a lower priority will be called before the ones that have a higher value. Only one "udpate" selector could be scheduled per node (You can't have 2 'update' selectors).

| - (void) stopActionByTag: | (int) | tag |

Removes an action from the running action list given its tag

| - (void) stopAllActions |

Removes all actions from the running action list

| - (void) transform |

performs OpenGL view-matrix transformation based on position, scale, rotation and other attributes.

| - (void) transformAncestors |

performs OpenGL view-matrix transformation of it's ancestors. Generally the ancestors are already transformed, but in certain cases (eg: attaching a FBO) it's necessary to transform the ancestors again.

| - (void) unschedule: | (SEL) | s |

unschedules a custom selector. Use [self unschedule:_cmd] within a scheduled selector to unschedule that specific selector without having to refer to it by name.

| - (void) unscheduleAllSelectors |

unschedule all scheduled selectors: custom selectors, and the 'update' selector. Actions are not affected by this method.

| - (void) visit |

Recursive method that visit its children and draw them.

| - (CGAffineTransform) worldToNodeTransform |

Returns the inverse world affine transform matrix. The matrix is in Pixels.

- (CGPoint) anchorPoint` [read, write, assign]` |

anchorPoint is the point around which all transformations and positioning manipulations take place. It's like a pin in the node where it is "attached" to its parent. The anchorPoint is normalized, like a percentage. (0,0) means the bottom-left corner and (1,1) means the top-right corner. But you can use values higher than (1,1) and lower than (0,0) too. The default anchorPoint for [CCNode](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_node/) is (0, 0). [CCSprite](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite/) and other subclasses have a different default anchorPoint, usually (0.5f, 0.5f).

- (CGPoint) anchorPointInPixels` [read, assign]` |

The anchorPoint in absolute pixels. Since v0.8 you can only read it. If you wish to modify it, use anchorPoint instead

A [CCCamera](http://www.learn-cocos2d.com/) object that lets you move the node using a gluLookAt. Note: an often made misconception is that you have to work with the camera in order to implement scrolling worlds. Instead, prefer to move the layer where the world objects are added to instead.

- (CGSize) contentSize` [read, write, assign]` |

The untransformed size of the node in Points The contentSize remains the same no matter the node is scaled or rotated. All nodes has a size. Layer and Scene has the same size of the screen.

- (CGSize) contentSizeInPixels` [read, write, assign]` |

The untransformed size of the node in Pixels The contentSize remains the same no matter the node is scaled or rotated. All nodes has a size. Layer and Scene has the same size of the screen.

A CCGrid object that is used when applying effects. You don't normally use this yourself.

- (BOOL) isRelativeAnchorPoint` [read, write, assign]` |

If YES the transformtions will be relative to it's anchor point. Sprites, Labels and any other sizeble object use it have it enabled by default. Scenes, Layers and other "whole screen" object don't use it, have it disabled by default.

- (BOOL) isRunning` [read, assign]` |

whether or not the node is running

- (CGPoint) position` [read, write, assign]` |

Position (x,y) of the node in points. (0, 0) is the left-bottom corner in all device orientations contrary to what you may be used to from other game engines or UIKit. On standard iPhone/iPod and Retina iPhone/iPod the upper right corner is 320x480 in portrait and 480x320 in landscape orientations. On the iPad it's 1024x768 respectively 768x1024. It is highly recommend to design your game to use points (position) and refrain from using pixels (positionInPixels) unless you have a very good reason to do so.

- (CGPoint) positionInPixels` [read, write, assign]` |

Position (x,y) of the node in pixels. (0, 0) is the left-bottom corner, on standard iPhone/iPod the upper right corner is 320x480 (480x320 in landscape) but on Retina devices it's 640x960 (960x640 in landscape).

- (float) rotation` [read, write, assign]` |

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node clockwise.

- (float) scale` [read, write, assign]` |

The scale factor of the node. 1.0 is the default scale factor. It modifies the X and Y scale at the same time. Note that scaling is done by the CPU. Scaling up (scale > 1) will also increase the fillrate and scaling in any direction will decrease image quality. It is strongly recommended to design your game's graphics in a way that they can be used with scale of 1.0 at all times and to use scaling only in rare and justified circumstances with small sprites.

- (float) scaleX` [read, write, assign]` |

The scale factor of the node. 1.0 is the default scale factor. It only modifies the X scale factor. Please also see the notes for the scale property.

- (float) scaleY` [read, write, assign]` |

The scale factor of the node. 1.0 is the default scale factor. It only modifies the Y scale factor. Please also see the notes for the scale property.

- (NSInteger) tag` [read, write, assign]` |

A tag used to identify the node easily. Prefer to use an enum to name each tag value.

- (void*) userData` [read, write, assign]` |

A custom user data pointer. Note that this pointer is NOT retained.

- (float) vertexZ` [read, write, assign]` |

The real openGL Z vertex. Differences between openGL Z vertex and cocos2d Z order:

- (BOOL) visible` [read, write, assign]` |

Whether of not the node is visible. Default is YES. If NO, the node is not drawn which saves performance. This is especially important to keep in mind when you fade out (change opacity to 0) of nodes that support opacity. With opacity 0 but visible = YES the node would technically still be drawn and strain the fillrate/GPU.

- (NSInteger) zOrder` [read, assign]` |

The z order of the node relative to it's "brothers": children of the same parent