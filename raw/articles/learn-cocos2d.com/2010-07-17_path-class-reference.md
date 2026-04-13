---
title: Path Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_path/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A path is a list of CGPoint with special attributes that are drawn on screen.
[More...](#_details)

`#import <`[Path.h](../../../line-drawing-game-starterkit-documentation/html/_path_8h_source/)>


[List of all members.](../../../line-drawing-game-starterkit-documentation/html/class_path-members/)

Public Member Functions
|
| (id) | - [init](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a633cc2fa44ec5be8e1ab3d0559da0d9c) |
| | initializes class and returns an instance of the class, you must take care of allocating the object yourself
|
| (void) | - [addEndPoint:](../../../line-drawing-game-starterkit-documentation/html/interface_path/#abe4c801384100922869f94ba03ff7355) |
| | adds another point which is an endpoint (harbor, landing strip, etc)
|
| (void) | - [addPoint:](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a12460c5d130db21d4e98f1f7f61556c5) |
| | add a regular point
|
| (void) | - [endPathDrawing](../../../line-drawing-game-starterkit-documentation/html/interface_path/#ab7bc0d382daf633fd322c6fd5a52785d) |
| | disallows adding more points, stops drawing the endPoint and changes lineStyle
|
| (void) | - [removePath](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a8f62052cf942b13207e00b2720ffa80e) |
| | removes [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) from [GamePaths](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/) list and will deallocate the [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/)
|
| (void) | - [removeFirstPoint](../../../line-drawing-game-starterkit-documentation/html/interface_path/#ac5129b9cedc57a5373460463e98e66d5) |
| | remove the first path point from the list (first being the one closest to the object)
|
| (void) | - [removeAllPoints](../../../line-drawing-game-starterkit-documentation/html/interface_path/#af7dc3d4970d49c5c1830327cc013521e) |
| | remove all path points from the list
|
| (int) | - [getNumPoints](../../../line-drawing-game-starterkit-documentation/html/interface_path/#ac50f12de6d160079f9a7a7f2d24502d5) |
| | returns the number of points in the path
|
| (CGPoint) | - [getLastPointLocation](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a3759f8459091feb4f947d25275c58f9c) |
| | returns the location of the current last point of the path
|
([PathPoint](../../../line-drawing-game-starterkit-documentation/html/struct_path_point/)) | - [getFirstPathPoint](../../../line-drawing-game-starterkit-documentation/html/interface_path/#adebaf2d5cb5eb6be954983e6d4abf503) |
| | returns the first path point in the list
|
| (void) | - [dealloc](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a8f079225f0a16a165fcdc50086add1f9)` [implementation]` |
([PathPoint](../../../line-drawing-game-starterkit-documentation/html/struct_path_point/)) | - [getPathPointAtIndex:](../../../line-drawing-game-starterkit-documentation/html/interface_path/#acb6ff4a8c09b814ac4a2200da11db12a)` [implementation]` |
| (void) | - [addPathPoint:](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a29faa7d9e0df62087f46f204835d9eae)` [implementation]` |
| (void) | - [applyLineStyle:](../../../line-drawing-game-starterkit-documentation/html/interface_path/#aca78fd057a540c11a3e5bcfa13d86645)` [implementation]` |
| | sets the OpenGL line style for the current line
|
| (void) | - [resetOpenGL](../../../line-drawing-game-starterkit-documentation/html/interface_path/#ad9df77a6c0412efdf87e5f63ad7d3c12)` [implementation]` |
| (void) | - [draw](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a44c5c139fada63bc08efe1fe28ca264a)` [implementation]` |
| (void) | - [onArrivedAtPoint](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a3573bab6c5a66cff5ee178c153c6a17d) |
Static Public Member Functions
|
| (id) | + [path](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a8f5aadcac2d28180634fed6b9c2e42aa) |
| | initializes class and returns an autoreleased instance of the class
|
Protected Attributes
|
| NSMutableArray * | [pathPoints](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a52d86050cb023adb73783a616cd0dafa) |
| | contains a list of [PathPoint](../../../line-drawing-game-starterkit-documentation/html/struct_path_point/) structs that define the path
|
Properties
|
[EPathLineStyles](../../../line-drawing-game-starterkit-documentation/html/_path_line_styles_8h/#af12954fd7a976563b14079c71752ffa3) | [lineStyle](../../../line-drawing-game-starterkit-documentation/html/interface_path/#ab306623a46f0978a8f3974c4c54cafdc) |
| | set the desired line style for rendering the path after drawing
|
[EPathLineStyles](../../../line-drawing-game-starterkit-documentation/html/_path_line_styles_8h/#af12954fd7a976563b14079c71752ffa3) | [lineStyleWhileDrawing](../../../line-drawing-game-starterkit-documentation/html/interface_path/#aaaa98fc4b1ec8fe4d0d887fff67f1ffa) |
| | set the desired line style for rendering the path while it is still being drawn
|
| CGPoint | [objectPosition](../../../line-drawing-game-starterkit-documentation/html/interface_path/#ab6633efc4f45a9997c703d3dd69d44ea) |
| | the current position of the object following this path, it is pushed (updated) by the object itself
|
| CGPoint | [drawingEndPoint](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a9b1a5c8ac5e8fabc9e3d06008743d697) |
| | set the drawingEndPoint which is rendered only while drawing the path, should be the location where the finger is touching
|
| bool | [isUserStillDrawingThisPath](../../../line-drawing-game-starterkit-documentation/html/interface_path/#a88a2a60e96e823115e27521718134413) |
| | true if the user is currently drawing this path
|


## Detailed Description

A path is a list of CGPoint with special attributes that are drawn on screen.

It knows how to draw itself with various line styles.


## Member Function Documentation

| - (void) addEndPoint: |
|
(CGPoint) |
*point* |
|
|

adds another point which is an endpoint (harbor, landing strip, etc)

| - (void) addPathPoint: |
|
([PathPoint](../../../line-drawing-game-starterkit-documentation/html/struct_path_point/)) |
*pathPoint* |
|
` [implementation]` |


| - (void) addPoint: |
|
(CGPoint) |
*point* |
|
|

sets the OpenGL line style for the current line

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


disallows adding more points, stops drawing the endPoint and changes lineStyle

returns the first path point in the list

| - (CGPoint) getLastPointLocation |
|
|
|
|

returns the location of the current last point of the path

returns the number of points in the path

- ([PathPoint](../../../line-drawing-game-starterkit-documentation/html/struct_path_point/)) getPathPointAtIndex: |
|
(int) |
*index* |
|
` [implementation]` |


initializes class and returns an instance of the class, you must take care of allocating the object yourself

| - (void) onArrivedAtPoint |
|
|
|
|


initializes class and returns an autoreleased instance of the class

remove all path points from the list

| - (void) removeFirstPoint |
|
|
|
|

remove the first path point from the list (first being the one closest to the object)

| - (void) resetOpenGL |
|
|
|
` [implementation]` |



## Member Data Documentation

contains a list of [PathPoint](../../../line-drawing-game-starterkit-documentation/html/struct_path_point/) structs that define the path


## Property Documentation

- (CGPoint) drawingEndPoint` [read, write, assign]` |

set the drawingEndPoint which is rendered only while drawing the path, should be the location where the finger is touching

- (bool) isUserStillDrawingThisPath` [read, assign]` |

true if the user is currently drawing this path

set the desired line style for rendering the path after drawing

set the desired line style for rendering the path while it is still being drawn

- (CGPoint) objectPosition` [read, write, assign]` |

the current position of the object following this path, it is pushed (updated) by the object itself


The documentation for this class was generated from the following files:

- ClassesLineDrawingStarterkit/
[Path.h](../../../line-drawing-game-starterkit-documentation/html/_path_8h_source/)
- ClassesLineDrawingStarterkit/
[Path.m](../../../line-drawing-game-starterkit-documentation/html/_path_8m/)