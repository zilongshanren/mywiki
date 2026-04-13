---
title: AppDelegate Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_app_delegate/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

The Application Delegate which receives all the OS callbacks.
[More...](#_details)

`#import <`[AppDelegate.h](../../../line-drawing-game-starterkit-documentation/html/_app_delegate_8h_source/)>


[List of all members.](../../../line-drawing-game-starterkit-documentation/html/class_app_delegate-members/)


## Detailed Description

The Application Delegate which receives all the OS callbacks.


## Member Function Documentation

| - (BOOL) application: |
|
(UIApplication *) |
*application* |
| didFinishLaunchingWithOptions: |
|
(NSDictionary *) |
*launchOptions* | |
|
|
| | ` [implementation]` |

creates the UIWindow and initializes cocos2d

| - (void) applicationDidBecomeActive: |
|
(UIApplication*) |
*application* |
|
` [implementation]` |


| - (void) applicationDidReceiveMemoryWarning: |
|
(UIApplication*) |
*application* |
|
` [implementation]` |


| - (void) applicationSignificantTimeChange: |
|
(UIApplication*) |
*application* |
|
` [implementation]` |


| - (void) applicationWillResignActive: |
|
(UIApplication*) |
*application* |
|
` [implementation]` |


| - (void) applicationWillTerminate: |
|
(UIApplication*) |
*application* |
|
` [implementation]` |


| - (void) dealloc |
|
|
|
` [implementation]` |


| - (void) orientationChanged: |
|
(NSNotification*) |
*notification* |
|
` [implementation]` |

This method allows us to support both landscape orientations and orientation can be changed on the fly.

If you change this you should also modify UISupportedInterfaceOrientations in Info.plist.


## Member Data Documentation


## Property Documentation

- (bool) isPaused` [read, write, assign]` |


- (bool) isPlaying` [read, write, assign]` |


- (UIWindow *) window` [read, write, retain]` |



The documentation for this class was generated from the following files: