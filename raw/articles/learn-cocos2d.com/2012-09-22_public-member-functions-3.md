---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
1.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCNode.h>`


| (id) | -
|

[CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/) is the main element. Anything thats gets drawn or contains things that get drawn is a [CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/). The most popular CCNodes are: [CCScene](http://www.learn-cocos2d.com/), [CCLayer](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_layer/), [CCSprite](http://www.learn-cocos2d.com/), [CCMenu](http://www.learn-cocos2d.com/).

The main features of a [CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/) are:

Some [CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/) nodes provide extra functionality for them or their children.

Subclassing a [CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/) usually means (one/all) of:

Features of [CCNode](http://www.learn-cocos2d.com/api-ref/1.1/cocos2d-iphone/html/interface_c_c_node/):

Default values:

Limitations:

Order in transformations with grid disabled

Order in transformations with grid enabled

Camera:

Adds a child to the container with z-order as 0. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with a z-order. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with z order and tag. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Implemented in [CCTMXLayer](http://www.learn-cocos2d.com/#a898f8a54b02cc7cdfc9236177d93a2c0).

returns a "local" axis aligned bounding box of the node in points. The returned box is relative only to its parent. The returned box is in Points.

returns a "local" axis aligned bounding box of the node in pixels. The returned box is relative only to its parent. The returned box is in Points.

Converts a Point to node (local) space coordinates. The result is in Points.

Converts a Point to node (local) space coordinates. The result is in Points. treating the returned/received node point as anchor relative.

Converts a UITouch to node (local) space coordinates. The result is in Points.

Converts a UITouch to node (local) space coordinates. The result is in Points. This method is AR (Anchor Relative)..

Converts a Point to world space coordinates. The result is in Points.

Converts a local Point to world space coordinates.The result is in Points. treating the returned/received node point as anchor relative.

Override this method to draw your own node. The following GL states will be enabled by default:

AND YOU SHOULD NOT DISABLE THEM AFTER DRAWING YOUR NODE

But if you enable any other GL state, you should disable it after drawing your node.

Gets an action from the running action list given its tag

Returns the matrix that transform the node's (local) space coordinates into the parent's space coordinates. The matrix is in Pixels.

Retrusn the world affine transform matrix. The matrix is in Pixels.

Returns the numbers of actions that are running plus the ones that are schedule to run (actions in actionsToAdd and actions arrays). Composable actions are counted as 1 action. Example: If you are running 1 Sequence of 7 actions, it will return 1. If you are running 7 Sequences of 2 actions, it will return 7.

Returns the matrix that transform parent's space coordinates to the node's (local) space coordinates. The matrix is in Pixels.

pauses all scheduled selectors and actions. Called internally by onExit

Removes all children from the container and do a cleanup all running actions depending on the cleanup parameter.

Removes a child from the container. It will also cleanup all running actions depending on the cleanup parameter.

| - (void) removeChildByTag: | (NSInteger) | tag |
|
| cleanup: | (BOOL) | cleanup |
|

Removes a child from the container by tag value. It will also cleanup all running actions depending on the cleanup parameter

Remove itself from its parent node. If cleanup is YES, then also remove all actions and callbacks. If the node orphan, then nothing happens.

Reorders a child according to a new z value. The child MUST be already added.

resumes all scheduled selectors and actions. Called internally by onEnter

Executes an action, and returns the action that is executed. The node becomes the action's target.

schedules a custom selector with an interval time in seconds. If time is 0 it will be ticked every frame. If time is 0, it is recommended to use 'scheduleUpdate' instead.

If the selector is already scheduled, then the interval parameter will be updated without scheduling it again.

| - (void)
|

repeat will execute the action repeat + 1 times, for a continues action use kCCRepeatForever delay is the amount of time the action will wait before execution

Schedules a selector that runs only once, with a delay of 0 or larger

check whether a selector is scheduled. schedules the "update" method. It will use the order number 0. This method will be called every frame. Scheduled methods with a lower order value will be called before the ones that have a higher order value. Only one "udpate" method could be scheduled per node.

schedules the "update" selector with a custom priority. This selector will be called every frame. Scheduled selectors with a lower priority will be called before the ones that have a higher value. Only one "udpate" selector could be scheduled per node (You can't have 2 'update' selectors).

performance improvement, Sort the children array once before drawing, instead of every time when a child is added or reordered don't call this manually unless a child added needs to be removed in the same frame

Removes an action from the running action list given its tag

performs OpenGL view-matrix transformation based on position, scale, rotation and other attributes.

performs OpenGL view-matrix transformation of it's ancestors. Generally the ancestors are already transformed, but in certain cases (eg: attaching a FBO) it's necessary to transform the ancestors again.

unschedule all scheduled selectors: custom selectors, and the 'update' selector. Actions are not affected by this method.

Returns the inverse world affine transform matrix. The matrix is in Pixels.

anchorPoint is the point around which all transformations and positioning manipulations take place. It's like a pin in the node where it is "attached" to its parent. The anchorPoint is normalized, like a percentage. (0,0) means the bottom-left corner and (1,1) means the top-right corner. But you can use values higher than (1,1) and lower than (0,0) too. The default anchorPoint is (0,0). It starts in the bottom-left corner. [CCSprite](http://www.learn-cocos2d.com/) and other subclasses have a different default anchorPoint.

The anchorPoint in absolute pixels. Since v0.8 you can only read it. If you wish to modify it, use anchorPoint instead

The untransformed size of the node in Points The contentSize remains the same no matter the node is scaled or rotated. All nodes has a size. Layer and Scene has the same size of the screen.

The untransformed size of the node in Pixels The contentSize remains the same no matter the node is scaled or rotated. All nodes has a size. Layer and Scene has the same size of the screen.

If YES the transformtions will be relative to it's anchor point. Sprites, Labels and any other sizeble object use it have it enabled by default. Scenes, Layers and other "whole screen" object don't use it, have it disabled by default.

used internally for zOrder sorting, don't change this manually

Position (x,y) of the node in points. (0,0) is the left-bottom corner.

Position (x,y) of the node in points. (0,0) is the left-bottom corner.

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node CW.

The scale factor of the node. 1.0 is the default scale factor. It modifies the X and Y scale at the same time.

The scale factor of the node. 1.0 is the default scale factor. It only modifies the X scale factor.

The scale factor of the node. 1.0 is the default scale factor. It only modifies the Y scale factor.

The X skew angle of the node in degrees. This angle describes the shear distortion in the X direction. Thus, it is the angle between the Y axis and the left edge of the shape The default skewX angle is 0. Positive values distort the node in a CW direction.

The Y skew angle of the node in degrees. This angle describes the shear distortion in the Y direction. Thus, it is the angle between the X axis and the bottom edge of the shape The default skewY angle is 0. Positive values distort the node in a CCW direction.

The real openGL Z vertex. Differences between openGL Z vertex and cocos2d Z order:

The z order of the node relative to it's "brothers": children of the same parent