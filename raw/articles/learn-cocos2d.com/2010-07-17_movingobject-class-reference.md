---
title: MovingObject Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_moving_object/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Moving objects are the objects the player can touch to draw a [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) for them.
[More...](#_details)

`#import <`[MovingObject.h](../../../line-drawing-game-starterkit-documentation/html/_moving_object_8h_source/)>


[List of all members.](../../../line-drawing-game-starterkit-documentation/html/class_moving_object-members/)


## Detailed Description

Moving objects are the objects the player can touch to draw a [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) for them.

They have common attributes like movement speed, rotation speed, collision radius and bounding box (a CGRect) which are mostly determined by using a specific [ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/). [MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/) can also have children like the collision warning sprites, touch highlights and it plays sounds as appropriate.


## Member Function Documentation

returns true if the object can collide with others, otherwise false

returns false if the object for whatever reason is out of the game, eg.

it crashed, left the screen, or landed

| - (bool) canShowProximityWarning |
|
|
|
` [implementation]` |


| - (void) continueMovingInSameDirection |
|
|
|
` [implementation]` |


| - (void) dealloc |
|
|
|
` [implementation]` |


| - (id) initMovingObjectWithDef: |
|
([ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/)) |
*objectDef* |
|
|

initializes class and returns an instance of the class, you must take care of allocating the object yourself

returns true for the duration that the object is assigned to a path as pathFollowObject

| - (void) moveInDirectionOfLocation: |
|
(CGPoint) |
*location* |
|
` [implementation]` |


called when object is spawned outside screen to have it move into the screen area

| - (void) moveTo: |
|
(CGPoint) |
*location* |
|
|

move the object to a certain location and fixed speed

| - (void) moveTo: |
|
(CGPoint) |
*location* |
| target: |
|
(id) |
*target* |
| selector: |
|
(SEL) |
*selector* | |
|
|
| | |

move the object to a certain location and fixed speed, will perform selector when it arrived

| - (void) moveToNextPathPoint |
|
|
|
` [implementation]` |


| - (void) moveToScreenBorder: |
|
(float) |
*direction* |
|
|

object will move to the nearest screenborder in the given direction

| + (id) movingObjectWithDef: |
|
([ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/)) |
*objectDef* |
|
|

initializes class and returns an autoreleased instance of the class

| - (void) onArrivedAtPathPoint |
|
|
|
` [implementation]` |


| - (void) onArrivedAtTarget |
|
|
|
` [implementation]` |


| - (void) onFadeOutDone |
|
|
|
` [implementation]` |


| - (void) onPathPointAdded |
|
|
|
|

signals the object that another path point has been added, may trigger it to start moving

| - (void) onProximityWarningTimeOut |
|
|
|
` [implementation]` |


signals the object that it has been touched (selected), usesful to play a sound or animation or change state.

enables the proximity warning and keeps it visible for longer

| - (void) setProximityWarningEnabled: |
|
(bool) |
*enabled* |
|
|

enables or disables the proximity warning image and plays sound

sets the ObjectState of the object unless the object is already set to kStateInactive

| - (void) setStateInactive |
|
|
|
` [implementation]` |


| - (void) startPathFollow: |
|
([Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/)*) |
*followPath* |
|
|

assigns this object a path that it will follow from now on

| - (void) stopPathFollow |
|
|
|
` [implementation]` |


| - (void) turnAroundAtScreenBorder |
|
|
|
` [implementation]` |

checks if the object is too close to the screen border and if so, it will turn the object around (it bounces back)

| - (void) update: |
|
(ccTime) |
*delta* |
|
` [implementation]` |



## Member Data Documentation

holds the pointer to a [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) object as long as the object is following that path


## Property Documentation

give access to this object's [ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/) which defines the object's type and other parameters

an object can only be in one state at a time (StateMachine concept)

returns the current object state


The documentation for this class was generated from the following files: