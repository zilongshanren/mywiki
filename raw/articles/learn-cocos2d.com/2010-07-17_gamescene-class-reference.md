---
title: GameScene Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_scene/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

The scene (CCLayer) where the game takes place.
[More...](#_details)

`#import <`[GameScene.h](../../../line-drawing-game-starterkit-documentation/html/_game_scene_8h_source/)>


Inherits [PauseDelegateProtocol-p](../../../line-drawing-game-starterkit-documentation/html/protocol_pause_delegate_protocol-p/).

[List of all members.](../../../line-drawing-game-starterkit-documentation/html/class_game_scene-members/)


## Detailed Description

The scene (CCLayer) where the game takes place.

It contains all game objects, paths as well as HUD and GUI.


## Member Function Documentation

| - (BOOL) ccTouchBegan: |
|
(UITouch*) |
*touch* |
| withEvent: |
|
(UIEvent*) |
*event* | |
|
|
| | ` [implementation]` |


| - (void) ccTouchCancelled: |
|
(UITouch*) |
*touch* |
| withEvent: |
|
(UIEvent*) |
*event* | |
|
|
| | ` [implementation]` |


| - (void) ccTouchEnded: |
|
(UITouch*) |
*touch* |
| withEvent: |
|
(UIEvent*) |
*event* | |
|
|
| | ` [implementation]` |


| - (void) ccTouchMoved: |
|
(UITouch*) |
*touch* |
| withEvent: |
|
(UIEvent*) |
*event* | |
|
|
| | ` [implementation]` |


| - (void) dealloc |
|
|
|
` [implementation]` |


should not be called by you - use [[GameScene](../../../line-drawing-game-starterkit-documentation/html/interface_game_scene/) scene] instead!

instance of [GameScene](../../../line-drawing-game-starterkit-documentation/html/interface_game_scene/), only valid as long as the scene is running (caution: it's not a proper Singleton!).

It's meant for quick access to it from child nodes.

returns true if the game is running, false if it is paused either because of the pause menu being shown or the game being over

pauses the scene for a moment, then resets

| - (void) onCrashTimeOut: |
|
(ccTime) |
*delta* |
|
` [implementation]` |


| - (void) onPauseButton: |
|
(id) |
*sender* |
|
|


resumes the game when it is paused, otherwise does nothing

| - (void) registerWithTouchDispatcher |
|
|
|
` [implementation]` |

We want to use a targeted touch dispatcher because then we don't need to deal with the user drawing a path and moving over a UI button by accident.

Using a Targeted touch handler avoids the button being "touched" accidentally.

creates the scene, returns an autoreleased object

| - (void) setIsPaused: |
|
(bool) |
*isPaused* |
|
` [implementation]` |


| - (void) setIsPlaying: |
|
(bool) |
*isPlaying* |
|
` [implementation]` |



## Member Data Documentation


## Property Documentation

- (unsigned int) currentScore` [read, write, assign]` |



The documentation for this class was generated from the following files: