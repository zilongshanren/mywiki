---
title: Instance Methods
url: http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/
published: '2013-06-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.koboldtouch.com developers
|

`#import <CCNode.h>`


| (id) | +
|

|

| NSInteger |
|

[CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/) is the main element. Anything thats gets drawn or contains things that get drawn is a [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/). The most popular CCNodes are: [CCScene](http://www.learn-cocos2d.com/), [CCLayer](http://www.learn-cocos2d.com/), [CCSprite](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_sprite/), [CCMenu](http://www.learn-cocos2d.com/).

The main features of a [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/) are:

Some [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/) nodes provide extra functionality for them or their children.

Subclassing a [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/) usually means (one/all) of:

Features of [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/):

Default values:

Limitations:

Order in transformations with grid disabled

Order in transformations with grid enabled

Camera:

Adds a child to the container with z-order as 0. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with a z-order. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with z order and tag. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Implemented in [CCTMXLayer](http://www.learn-cocos2d.com/#a898f8a54b02cc7cdfc9236177d93a2c0).

| - (CGRect) boundingBox |

returns a "local" axis aligned bounding box of the node in points. The returned box is relative only to its parent. The returned box is in Points.

| - (void) cleanup |

Event that is called when the running node is no longer running (eg: its [CCScene](http://www.learn-cocos2d.com/) is being removed from the "stage" ). On cleanup you should break any possible circular references. [CCNode](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_node/)'s cleanup removes any possible scheduled timer and/or any possible action. If you override cleanup, you shall call [super cleanup]

Implemented in [CCMenuItem](http://www.learn-cocos2d.com/#a9dacc63a07fd86adb30bd6c4ee28d47b).

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

Override this method to draw your own node. You should use cocos2d's GL API to enable/disable the GL state / shaders. For further info, please see ccGLstate.h. You shall NOT call [super draw];

Gets an action from the running action list given its tag

| - (id) init |

initializes the node

Implemented in [CCTransitionCrossFade](http://www.learn-cocos2d.com/#a84e566a9c1ef713de1deaf006b6dbd0f), [CCTransitionTurnOffTiles](http://www.learn-cocos2d.com/#a002e9740f8487af7afd9fe157e99dfcc), [CCScene](http://www.learn-cocos2d.com/#a6ced7d1397204cb5dc2a5579e547ed0c), [CCTransitionRotoZoom](http://www.learn-cocos2d.com/#a588b1d67980b94489bed54922ae3eb2a), [CCTransitionJumpZoom](http://www.learn-cocos2d.com/#a520ada27cbde20c1b27c81d2bfbcd74a), [CCTransitionShrinkGrow](http://www.learn-cocos2d.com/#aaa4d30491aec84748cf226918abd2987), [CCTransitionFlipX](http://www.learn-cocos2d.com/#a826655c1f01b1edf2aaa7663544bc69c), [CCTransitionFlipY](http://www.learn-cocos2d.com/#a89a277a0795c44498c0dcdd0d15ffd78), [CCTransitionFlipAngular](http://www.learn-cocos2d.com/#acfbd2cd5d83cccb25e8566f39502df7e), [CCTransitionZoomFlipX](http://www.learn-cocos2d.com/#a29c33d700630ff1e7b83ad4ba501935b), [CCTransitionZoomFlipY](http://www.learn-cocos2d.com/#a5ca9edd127622a0d25322dde9daf7447), [CCTransitionZoomFlipAngular](http://www.learn-cocos2d.com/#aff9352d756a5f4688bac73395eed9c90), [CCParticleFire](http://www.learn-cocos2d.com/#a9f025d19086e736df8df05426338a7ba), [CCParticleFireworks](http://www.learn-cocos2d.com/#abbfff416ef6ab06eff1c36a229593fab), [CCParticleSun](http://www.learn-cocos2d.com/#ab84fe32e5cf6e091faa2dbdf43446683), [CCParticleGalaxy](http://www.learn-cocos2d.com/#a02d1d1e4ddbaf7986763f593dd70db84), [CCParticleFlower](http://www.learn-cocos2d.com/#a99aac34cc21adf80dfe6adc53025eb7b), [CCParticleMeteor](http://www.learn-cocos2d.com/#ad7402ac21d287939ed1252ad9a92b318), [CCParticleSpiral](http://www.learn-cocos2d.com/#aa7607aa26814c372db7e96b413597f7b), [CCParticleExplosion](http://www.learn-cocos2d.com/#a23096de235891ce9328d019444294a27), [CCParticleSmoke](http://www.learn-cocos2d.com/#ae9c86fd3c3dacf114ce6b6e2bf8f3e36), [CCParticleSnow](http://www.learn-cocos2d.com/#a02c1c36b330a938b7acdc04e81bfdca9), [CCParticleRain](http://www.learn-cocos2d.com/#ac95df79d70f3f82eb60056b770ba463a), and [CCClippingNode](http://www.learn-cocos2d.com/#a20a68e2646b7659063e58aa4d4b6de1f).

| + (id) node |

allocates and initializes a node. The node will be created as "autorelease".

| - (CGAffineTransform) nodeToParentTransform |

Returns the matrix that transform the node's (local) space coordinates into the parent's space coordinates. The matrix is in Pixels.

| - (CGAffineTransform) nodeToWorldTransform |

Returns the world affine transform matrix. The matrix is in Pixels.

| - (NSUInteger) numberOfRunningActions |

Returns the numbers of actions that are running plus the ones that are schedule to run (actions in actionsToAdd and actions arrays). Composable actions are counted as 1 action. Example: If you are running 1 Sequence of 7 actions, it will return 1. If you are running 7 Sequences of 2 actions, it will return 7.

| - (void) onEnter |

| - (void) onEnterTransitionDidFinish |

| - (void) onExit |

| - (void) onExitTransitionDidStart |

| - (CGAffineTransform) parentToNodeTransform |

Returns the matrix that transform parent's space coordinates to the node's (local) space coordinates. The matrix is in Pixels.

| - (void) pauseSchedulerAndActions |

pauses all scheduled selectors and actions. Called internally by onExit

| - (void) removeAllChildren |

Removes all children from the container forcing a cleanup.

| - (void) removeAllChildrenWithCleanup: | (BOOL) | cleanup |

Removes all children from the container and do a cleanup all running actions depending on the cleanup parameter.

Removes a child from the container forcing a cleanup

Removes a child from the container. It will also cleanup all running actions depending on the cleanup parameter.

| - (void) removeChildByTag: | (NSInteger) | tag |

Removes a child from the container by tag value forcing a cleanup.

Removes a child from the container by tag value. It will also cleanup all running actions depending on the cleanup parameter

| - (void) removeFromParent |

Remove itself from its parent node forcing a cleanup. If the node orphan, then nothing happens.

| - (void) removeFromParentAndCleanup: | (BOOL) | cleanup |

Remove itself from its parent node. If cleanup is YES, then also remove all actions and callbacks. If the node orphan, then nothing happens.

Reorders a child according to a new z value. The child MUST be already added.

| - (void) resumeSchedulerAndActions |

resumes all scheduled selectors and actions. Called internally by onEnter

Executes an action, and returns the action that is executed. The node becomes the action's target.

| - (void) schedule: | (SEL) | s |

schedules a selector. The scheduled selector will be ticked every frame

schedules a custom selector with an interval time in seconds. If time is 0 it will be ticked every frame. If time is 0, it is recommended to use 'scheduleUpdate' instead.

If the selector is already scheduled, then the interval parameter will be updated without scheduling it again.

| - (void)
|

repeat will execute the action repeat + 1 times, for a continues action use kCCRepeatForever delay is the amount of time the action will wait before execution

Schedules a selector that runs only once, with a delay of 0 or larger

| - (void) scheduleUpdate |

check whether a selector is scheduled. schedules the "update" method. It will use the order number 0. This method will be called every frame. Scheduled methods with a lower order value will be called before the ones that have a higher order value. Only one "update" method could be scheduled per node.

| - (void) scheduleUpdateWithPriority: | (NSInteger) | priority |

schedules the "update" selector with a custom priority. This selector will be called every frame. Scheduled selectors with a lower priority will be called before the ones that have a higher value. Only one "update" selector could be scheduled per node (You can't have 2 'update' selectors).

| - (void) sortAllChildren |

performance improvement, Sort the children array once before drawing, instead of every time when a child is added or reordered don't call this manually unless a child added needs to be removed in the same frame

| - (void) stopActionByTag: | (NSInteger) | tag |

Removes an action from the running action list given its tag

| - (void) stopAllActions |

Removes all actions from the running action list

| - (void) transform |

performs OpenGL view-matrix transformation based on position, scale, rotation and other attributes.

| - (void) transformAncestors |

performs OpenGL view-matrix transformation of its ancestors. Generally the ancestors are already transformed, but in certain cases (eg: attaching a FBO) it is necessary to transform the ancestors again.

| - (void) unschedule: | (SEL) | s |

unschedules a custom selector.

| - (void) unscheduleAllSelectors |

unschedule all scheduled selectors: custom selectors, and the 'update' selector. Actions are not affected by this method.

| - (void) visit |

recursive method that visit its children and draw them

| - (CGAffineTransform) worldToNodeTransform |

Returns the inverse world affine transform matrix. The matrix is in Pixels.

|
readwritenonatomicassign |

anchorPoint is the point around which all transformations and positioning manipulations take place. It's like a pin in the node where it is "attached" to its parent. The anchorPoint is normalized, like a percentage. (0,0) means the bottom-left corner and (1,1) means the top-right corner. But you can use values higher than (1,1) and lower than (0,0) too. The default anchorPoint is (0,0). It starts in the bottom-left corner. [CCSprite](http://www.learn-cocos2d.com/api-ref/KoboldTouch/6.2/cocos2d-iphone/html/interface_c_c_sprite/) and other subclasses have a different default anchorPoint.

|
readnonatomicassign |

The anchorPoint in absolute pixels. Since v0.8 you can only read it. If you wish to modify it, use anchorPoint instead

|
readwritenonatomicassign |

The untransformed size of the node in Points The contentSize remains the same no matter the node is scaled or rotated. All nodes has a size. Layer and Scene has the same size of the screen.

|
readwritenonatomicassign |

|
readnonatomicassign |

whether or not the node is running

|
readwritenonatomicassign |

used internally for zOrder sorting, don't change this manually

|
readwritenonatomicassign |

Position (x,y) of the node in points. (0,0) is the left-bottom corner.

|
readwritenonatomicassign |

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node CW.

|
readwritenonatomicassign |

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node CW. It only modifies the X rotation performing a horizontal rotational skew .

|
readwritenonatomicassign |

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node CW. It only modifies the Y rotation performing a vertical rotational skew .

|
readwritenonatomicassign |

The scale factor of the node. 1.0 is the default scale factor. It modifies the X and Y scale at the same time.

|
readwritenonatomicassign |

The scale factor of the node. 1.0 is the default scale factor. It only modifies the X scale factor.

|
readwritenonatomicassign |

The scale factor of the node. 1.0 is the default scale factor. It only modifies the Y scale factor.

|
readwritenonatomicassign |

The X skew angle of the node in degrees. This angle describes the shear distortion in the X direction. Thus, it is the angle between the Y axis and the left edge of the shape The default skewX angle is 0. Positive values distort the node in a CW direction.

|
readwritenonatomicassign |

The Y skew angle of the node in degrees. This angle describes the shear distortion in the Y direction. Thus, it is the angle between the X axis and the bottom edge of the shape The default skewY angle is 0. Positive values distort the node in a CCW direction.

|
readwritenonatomicassign |

A tag used to identify the node easily

|
readwritenonatomicassign |

A custom user data pointer

|
readwritenonatomicretain |

Similar to userData, but instead of holding a void* it holds an id

|
readwritenonatomicassign |

The real openGL Z vertex. Differences between openGL Z vertex and cocos2d Z order:

|
readwritenonatomicassign |

Whether of not the node is visible. Default is YES

|
readwritenonatomicassign |

The z order of the node relative to its "siblings": children of the same parent