---
title: CCDirector Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCDirector.h](http://www.learn-cocos2d.com/)"

Inherited by [CCDirectorIOS](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_i_o_s/), and [CCDirectorMac](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director_mac/).

Class that creates and handle the main Window and manages how and when to execute the Scenes.

The [CCDirector](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director/) is also resposible for:

Since the [CCDirector](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director/) is a singleton, the standard way to use it is by calling:

The [CCDirector](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_director/) also sets the default OpenGL context:

| - (CGFloat) contentScaleFactor |

returns the content scale factor

| - (CGPoint) convertEventToGL: | (NSEvent *) | event |

converts an NSEvent to GL coordinates

| - (CGPoint) convertToGL: | (CGPoint) | p |

converts a UIKit coordinate to an OpenGL coordinate Useful to convert (multi) touchs coordinates to the current layout (portrait or landscape)

| - (CGPoint) convertToUI: | (CGPoint) | p |

converts an OpenGL coordinate to a UIKit coordinate Useful to convert node points to window points for calls such as glScissor

| - (ccDeviceOrientation) deviceOrientation |

returns the device orientation

| - (CGSize) displaySizeInPixels |

returns the display size of the OpenGL view in pixels. It doesn't take into account any possible rotation of the window.

| - (void) drawScene |

Draw the scene. This method is called every frame. Don't call it manually.

| - (BOOL) enableRetinaDisplay: | (BOOL) | yes |

Will enable Retina Display on devices that supports it. It will enable Retina Display on iPhone4 and iPod Touch 4. It will return YES, if it could enabled it, otherwise it will return NO.

This is the recommened way to enable Retina Display.

| - (void) end |

Ends the execution, releases the running scene. It doesn't remove the OpenGL view from its parent. You have to do it manually.

| - (float) getZEye |

XXX: missing description.

| - (void) pause |

Pauses the running scene. The running scene will be _drawed_ but all scheduled timers will be paused While paused, the draw rate will be 4 FPS to reduce CPU consuption

| - (void) popScene |

Pops out a scene from the queue. This scene will replace the running one. The running scene will be deleted. If there are no more scenes in the stack the execution is terminated. ONLY call it if there is a running scene.

| - (void) purgeCachedData |

Removes all the cocos2d data that was cached automatically. It will purge the [CCTextureCache](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_texture_cache/), CCBitmapFont cache. IMPORTANT: The [CCSpriteFrameCache](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_sprite_frame_cache/) won't be purged. If you want to purge it, you have to purge it manually.

Suspends the execution of the running scene, pushing it on the stack of suspended scenes. The new scene will be executed. Try to avoid big stacks of pushed scenes to reduce memory allocation. ONLY call it if there is a running scene.

Replaces the running scene with a new one. The running scene is terminated. ONLY call it if there is a running scene.

| - (void) reshapeProjection: | (CGSize) | newWindowSize |

changes the projection size

| - (void) resume |

Resumes the paused scene The scheduled timers will be activated again. The "delta time" will be 0 (as if the game wasn't paused)

Enters the Director's main loop with the given Scene. Call it to run only your FIRST scene. Don't call it if there is already a running scene.

| - (void) setAlphaBlending: | (BOOL) | on |

enables/disables OpenGL alpha blending

| - (void) setContentScaleFactor: | (CGFloat) | scaleFactor |

The size in pixels of the surface. It could be different than the screen size. High-res devices might have a higher surface size than the screen size. In non High-res device the contentScale will be emulated.

The recommend way to enable Retina Display is by using the "enableRetinaDisplay:(BOOL)enabled" method.

| - (void) setDepthTest: | (BOOL) | on |

enables/disables OpenGL depth test

| - (void) setDeviceOrientation: | (ccDeviceOrientation) | orientation |

Sets the device orientation. If the orientation is going to be controlled by an UIViewController, then the orientation should be Portrait

| + (BOOL) setDirectorType: | (ccDirectorType) | directorType |

There are 4 types of Director.

Each Director has it's own benefits, limitations. If you are using SDK 3.1 or newer it is recommed to use the DisplayLink director

This method should be called before any other call to the director.

It will return NO if the director type is kCCDirectorTypeDisplayLink and the running SDK is < 3.1. Otherwise it will return YES.

| - (void) setGLDefaultValues |

sets the OpenGL default values

| - (void) startAnimation |

The main loop is triggered again. Call this function only if [stopAnimation] was called earlier

| - (void) stopAnimation |

Stops the animation. Nothing will be drawn. The main loop won't be triggered anymore. If you wan't to pause your animation call [pause] instead.

| - (CGSize) winSize |

returns the size of the OpenGL view in points. It takes into account any possible rotation (device orientation) of the window

| - (CGSize) winSizeInPixels |

returns the size of the OpenGL view in pixels. It takes into account any possible rotation (device orientation) of the window. On Mac winSize and winSizeInPixels return the same value.

- (NSTimeInterval) animationInterval` [read, write, assign]` |

The FPS value

- (BOOL) displayFPS` [read, write, assign]` |

Whether or not to display the FPS on the bottom-left corner

- (BOOL) isPaused` [read, assign]` |

Whether or not the Director is paused

- (BOOL) nextDeltaTimeZero` [read, write, assign]` |

whether or not the next delta time will be zero

- (id) notificationNode` [read, write, retain]` |

This object will be visited after the main scene is visited. This object MUST implement the "visit" selector. Useful to hook a notification object, like CCNotifications ([http://github.com/manucorporat/CCNotifications](https://github.com/manucorporat/CCNotifications))

- (CC_GLVIEW*) openGLView` [read, write, retain]` |

The OpenGLView, where everything is rendered

- (ccDirectorProjection) projection` [read, write, assign]` |

Sets an OpenGL projection

This object will be called when the OpenGL projection is udpated and only when the kCCDirectorProjectionCustom projection is used.

The current running Scene. Director can only run one Scene at the time

- (NSThread*) runningThread` [read, assign]` |

returns the cocos2d thread. If you want to run any cocos2d task, run it in this thread. On iOS usually it is the main thread.

- (BOOL) sendCleanupToScene` [read, assign]` |

Whether or not the replaced scene will receive the cleanup message. If the new scene is pushed, then the old scene won't receive the "cleanup" message. If the new scene replaces the old one, the it will receive the "cleanup" message.