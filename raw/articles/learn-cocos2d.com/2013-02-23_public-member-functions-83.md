---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_director/
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

`#import <CCDirector.h>`


| (CGSize) | -
|

Class that creates and handle the main Window and manages how and when to execute the Scenes.

The [CCDirector](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_director/) is also responsible for:

Since the [CCDirector](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_director/) is a singleton, the standard way to use it is by calling:

The [CCDirector](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_director/) also sets the default OpenGL context:

converts a UIKit coordinate to an OpenGL coordinate Useful to convert (multi) touch coordinates to the current layout (portrait or landscape)

converts an OpenGL coordinate to a UIKit coordinate Useful to convert node points to window points for calls such as glScissor

Will enable Retina Display on devices that supports it. It will enable Retina Display on iPhone4 and iPod Touch 4. It will return YES, if it could enabled it, otherwise it will return NO.

This is the recommended way to enable Retina Display.

Ends the execution, releases the running scene. It doesn't remove the OpenGL view from its parent. You have to do it manually.

Pauses the running scene. The running scene will be *drawed* but all scheduled timers will be paused While paused, the draw rate will be 4 FPS to reduce CPU consumption

Pops out a scene from the queue. This scene will replace the running one. The running scene will be deleted. If there are no more scenes in the stack the execution is terminated. ONLY call it if there is a running scene.

Pops out all scenes from the queue until the root scene in the queue. This scene will replace the running one. The running scene will be deleted. If there are no more scenes in the stack the execution is terminated. ONLY call it if there is a running scene.

Removes all the cocos2d data that was cached automatically. It will purge the [CCTextureCache](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_texture_cache/), [CCLabelBMFont](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_label_b_m_font/) cache. IMPORTANT: The [CCSpriteFrameCache](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_sprite_frame_cache/) won't be purged. If you want to purge it, you have to purge it manually.

Suspends the execution of the running scene, pushing it on the stack of suspended scenes. The new scene will be executed. Try to avoid big stacks of pushed scenes to reduce memory allocation. ONLY call it if there is a running scene.

Replaces the running scene with a new one. The running scene is terminated. ONLY call it if there is a running scene.

Resumes the paused scene The scheduled timers will be activated again. The "delta time" will be 0 (as if the game wasn't paused)

Enters the Director's main loop with the given Scene. Call it to run only your FIRST scene. Don't call it if there is already a running scene.

It will call pushScene: and then it will call startAnimation

The size in pixels of the surface. It could be different than the screen size. High-res devices might have a higher surface size than the screen size. In non High-res device the contentScale will be emulated.

The recommend way to enable Retina Display is by using the "enableRetinaDisplay:(BOOL)enabled" method.

The main loop is triggered again. Call this function only if [stopAnimation] was called earlier

Stops the animation. Nothing will be drawn. The main loop won't be triggered anymore. If you want to pause your animation call [pause] instead.

returns the size of the OpenGL view in pixels. On Mac winSize and winSizeInPixels return the same value.

This object will be visited after the main scene is visited. This object MUST implement the "visit" selector. Useful to hook a notification object, like CCNotifications ([http://github.com/manucorporat/CCNotifications](https://github.com/manucorporat/CCNotifications))

The current running Scene. Director can only run one Scene at the time

returns the cocos2d thread. If you want to run any cocos2d task, run it in this thread. On iOS usually it is the main thread.

Whether or not the replaced scene will receive the cleanup message. If the new scene is pushed, then the old scene won't receive the "cleanup" message. If the new scene replaces the old one, the it will receive the "cleanup" message.