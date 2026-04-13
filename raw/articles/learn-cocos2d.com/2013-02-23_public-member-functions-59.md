---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_action_manager/
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

`#import <CCActionManager.h>`


| (void) | -
|

[CCActionManager](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_action_manager/) the object that manages all the actions. Normally you won't need to use this API directly. 99% of the cases you will use the [CCNode](http://www.learn-cocos2d.com/api-ref/latest_2.x/cocos2d-iphone/html/interface_c_c_node/) interface, which uses this object. But there are some cases where you might need to use this API directly: Examples:

Adds an action with a target. If the target is already present, then the action will be added to the existing target. If the target is not present, a new instance of this target will be created either paused or paused, and the action will be added to the newly created target. When the target is paused, the queued actions won't be 'ticked'.

Gets an action given its tag an a target

Returns the numbers of actions that are running in a certain target Composable actions are counted as 1 action. Example: If you are running 1 Sequence of 7 actions, it will return 1. If you are running 7 Sequences of 2 actions, it will return 7.

Pauses all running actions, returning a list of targets whose actions were paused.

Pauses the target: all running actions and newly added actions will be paused.

| - (void) removeActionByTag: | (NSInteger) | tag |
|
| target: | (id) | target |
|

Removes an action given its tag and the target

Removes all actions from a certain target. All the actions that belongs to the target will be removed.

Resume a set of targets (convenience function to reverse a pauseAllRunningActions call)