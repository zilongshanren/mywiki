---
title: TargetObject Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_target_object/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Defines the position, radius and type of places where your objects can land, dock, etc.
[More...](#_details)

`#import <`[TargetObject.h](../../../line-drawing-game-starterkit-documentation/html/_target_object_8h_source/)>


[List of all members.](/)

Public Member Functions
|
| (id) | - [initWithRadius:](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/#a17d0b7895957b43bdd8e3e4c63389748) |
| | initializes [TargetObject](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/) class and returns an instance of the class, you must take care of allocating the object yourself
|
| (void) | - [dealloc](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/#adcde1b9e42af9bb3d789cd64238d4dda)` [implementation]` |
| (void) | - [draw](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/#a1f2eb5effdcf01bc042c6ccb26b5cf32)` [implementation]` |
Static Public Member Functions
|
| (id) | + [targetObjectWithRadius:](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/#af846925534f12ae05c3de93b62ffb2d5) |
| | initializes [TargetObject](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/) class and returns an autoreleased instance of the class
|
Protected Attributes
|
| float | [radius_](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/#ac5c43b476a0ae5ff16632355296d1f71) |
Properties
|
| float | [radius](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/#a57f34ad8302d67cc46fc8030f0a1767b) |


## Detailed Description

Defines the position, radius and type of places where your objects can land, dock, etc.

Extend as needed.


## Member Function Documentation

| - (void) dealloc |
|
|
|
` [implementation]` |


| - (void) draw |
|
|
|
` [implementation]` |


| - (id) initWithRadius: |
|
(float) |
*radius* |
|
|

initializes [TargetObject](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/) class and returns an instance of the class, you must take care of allocating the object yourself

| + (id) targetObjectWithRadius: |
|
(float) |
*radius* |
|
|

initializes [TargetObject](../../../line-drawing-game-starterkit-documentation/html/interface_target_object/) class and returns an autoreleased instance of the class


## Member Data Documentation


## Property Documentation

- (float) radius` [read, write, assign]` |



The documentation for this class was generated from the following files: