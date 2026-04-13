---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

![]() |
cocos2d-iphone
2.1
Improved Cocos2D API Reference (iOS version) for www.kobold2d.com developers
|

`#import <CCNode.h>`


| (id) | -
|

[CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) is the main element. Anything thats gets drawn or contains things that get drawn is a [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/). The most popular CCNodes are: [CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/), [CCLayer](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_layer/), [CCSprite](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite/), [CCMenu](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu/).

The main features of a [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) are:

Some [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) nodes provide extra functionality for them or their children.

Subclassing a [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) usually means (one/all) of:

Features of [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/):

Default values:

Limitations:

Order in transformations with grid disabled

Order in transformations with grid enabled

Camera:

Adds a child to the container with z-order as 0. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with a z-order. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Adds a child to the container with z order and tag. If the child is added to a 'running' node, then 'onEnter' and 'onEnterTransitionDidFinish' will be called immediately.

Implemented in [CCTMXLayer](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_t_m_x_layer/#a898f8a54b02cc7cdfc9236177d93a2c0).

returns a "local" axis aligned bounding box of the node in points. The returned box is relative only to its parent. The returned box is in Points.

Event that is called when the running node is no longer running (eg: its [CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/) is being removed from the "stage" ). On cleanup you should break any possible circular references. [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/)'s cleanup removes any possible scheduled timer and/or any possible action. If you override cleanup, you shall call [super cleanup]

Implemented in [CCMenuItem](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_menu_item/#a9dacc63a07fd86adb30bd6c4ee28d47b).

Converts a Point to node (local) space coordinates. The result is in Points.

Converts a Point to node (local) space coordinates. The result is in Points. treating the returned/received node point as anchor relative.

Converts a UITouch to node (local) space coordinates. The result is in Points.

Converts a UITouch to node (local) space coordinates. The result is in Points. This method is AR (Anchor Relative)..

Converts a Point to world space coordinates. The result is in Points.

Converts a local Point to world space coordinates.The result is in Points. treating the returned/received node point as anchor relative.

Override this method to draw your own node. You should use cocos2d's GL API to enable/disable the GL state / shaders. For further info, please see ccGLstate.h. You shall NOT call [super draw];

Gets an action from the running action list given its tag

initializes the node

Implemented in [CCTransitionTurnOffTiles](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_turn_off_tiles/#a002e9740f8487af7afd9fe157e99dfcc), [CCTransitionCrossFade](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_cross_fade/#a84e566a9c1ef713de1deaf006b6dbd0f), [CCTransitionZoomFlipAngular](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_zoom_flip_angular/#aff9352d756a5f4688bac73395eed9c90), [CCTransitionZoomFlipY](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_zoom_flip_y/#a5ca9edd127622a0d25322dde9daf7447), [CCTransitionZoomFlipX](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_zoom_flip_x/#a29c33d700630ff1e7b83ad4ba501935b), [CCTransitionFlipAngular](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_flip_angular/#acfbd2cd5d83cccb25e8566f39502df7e), [CCTransitionFlipY](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_flip_y/#a89a277a0795c44498c0dcdd0d15ffd78), [CCTransitionFlipX](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_flip_x/#a826655c1f01b1edf2aaa7663544bc69c), [CCTransitionShrinkGrow](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_shrink_grow/#aaa4d30491aec84748cf226918abd2987), [CCParticleRain](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_rain/#ac95df79d70f3f82eb60056b770ba463a), [CCTransitionJumpZoom](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_jump_zoom/#a520ada27cbde20c1b27c81d2bfbcd74a), [CCParticleSnow](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_snow/#a02c1c36b330a938b7acdc04e81bfdca9), [CCTransitionRotoZoom](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_transition_roto_zoom/#a588b1d67980b94489bed54922ae3eb2a), [CCParticleSmoke](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_smoke/#ae9c86fd3c3dacf114ce6b6e2bf8f3e36), [CCParticleExplosion](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_explosion/#a23096de235891ce9328d019444294a27), [CCParticleSpiral](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_spiral/#aa7607aa26814c372db7e96b413597f7b), [CCParticleMeteor](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_meteor/#ad7402ac21d287939ed1252ad9a92b318), [CCClippingNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_clipping_node/#a20a68e2646b7659063e58aa4d4b6de1f), [CCParticleFlower](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_flower/#a99aac34cc21adf80dfe6adc53025eb7b), [CCParticleGalaxy](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_galaxy/#a02d1d1e4ddbaf7986763f593dd70db84), [CCParticleSun](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_sun/#ab84fe32e5cf6e091faa2dbdf43446683), [CCScene](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_scene/#a6ced7d1397204cb5dc2a5579e547ed0c), [CCParticleFireworks](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_fireworks/#abbfff416ef6ab06eff1c36a229593fab), and [CCParticleFire](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_particle_fire/#a9f025d19086e736df8df05426338a7ba).

Returns the matrix that transform the node's (local) space coordinates into the parent's space coordinates. The matrix is in Pixels.

Returns the world affine transform matrix. The matrix is in Pixels.

Returns the numbers of actions that are running plus the ones that are schedule to run (actions in actionsToAdd and actions arrays). Composable actions are counted as 1 action. Example: If you are running 1 Sequence of 7 actions, it will return 1. If you are running 7 Sequences of 2 actions, it will return 7.

Returns the matrix that transform parent's space coordinates to the node's (local) space coordinates. The matrix is in Pixels.

pauses all scheduled selectors and actions. Called internally by onExit

Removes all children from the container and do a cleanup all running actions depending on the cleanup parameter.

Removes a child from the container forcing a cleanup

Removes a child from the container. It will also cleanup all running actions depending on the cleanup parameter.

Removes a child from the container by tag value forcing a cleanup.

Removes a child from the container by tag value. It will also cleanup all running actions depending on the cleanup parameter

Remove itself from its parent node forcing a cleanup. If the node orphan, then nothing happens.

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

check whether a selector is scheduled. schedules the "update" method. It will use the order number 0. This method will be called every frame. Scheduled methods with a lower order value will be called before the ones that have a higher order value. Only one "update" method could be scheduled per node.

schedules the "update" selector with a custom priority. This selector will be called every frame. Scheduled selectors with a lower priority will be called before the ones that have a higher value. Only one "update" selector could be scheduled per node (You can't have 2 'update' selectors).

performance improvement, Sort the children array once before drawing, instead of every time when a child is added or reordered don't call this manually unless a child added needs to be removed in the same frame

Removes an action from the running action list given its tag

performs OpenGL view-matrix transformation based on position, scale, rotation and other attributes.

performs OpenGL view-matrix transformation of its ancestors. Generally the ancestors are already transformed, but in certain cases (eg: attaching a FBO) it is necessary to transform the ancestors again.

unschedule all scheduled selectors: custom selectors, and the 'update' selector. Actions are not affected by this method.

Returns the inverse world affine transform matrix. The matrix is in Pixels.

anchorPoint is the point around which all transformations and positioning manipulations take place. It's like a pin in the node where it is "attached" to its parent. The anchorPoint is normalized, like a percentage. (0,0) means the bottom-left corner and (1,1) means the top-right corner. But you can use values higher than (1,1) and lower than (0,0) too. The default anchorPoint is (0,0). It starts in the bottom-left corner. [CCSprite](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite/) and other subclasses have a different default anchorPoint.

The anchorPoint in absolute pixels. Since v0.8 you can only read it. If you wish to modify it, use anchorPoint instead

The untransformed size of the node in Points The contentSize remains the same no matter the node is scaled or rotated. All nodes has a size. Layer and Scene has the same size of the screen.

used internally for zOrder sorting, don't change this manually

Position (x,y) of the node in points. (0,0) is the left-bottom corner.

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node CW.

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node CW. It only modifies the X rotation performing a horizontal rotational skew .

The rotation (angle) of the node in degrees. 0 is the default rotation angle. Positive values rotate node CW. It only modifies the Y rotation performing a vertical rotational skew .

The scale factor of the node. 1.0 is the default scale factor. It modifies the X and Y scale at the same time.

The scale factor of the node. 1.0 is the default scale factor. It only modifies the X scale factor.

The scale factor of the node. 1.0 is the default scale factor. It only modifies the Y scale factor.

The X skew angle of the node in degrees. This angle describes the shear distortion in the X direction. Thus, it is the angle between the Y axis and the left edge of the shape The default skewX angle is 0. Positive values distort the node in a CW direction.

The Y skew angle of the node in degrees. This angle describes the shear distortion in the Y direction. Thus, it is the angle between the X axis and the bottom edge of the shape The default skewY angle is 0. Positive values distort the node in a CCW direction.

Similar to userData, but instead of holding a void* it holds an id

The real openGL Z vertex. Differences between openGL Z vertex and cocos2d Z order:

The z order of the node relative to its "siblings": children of the same parent