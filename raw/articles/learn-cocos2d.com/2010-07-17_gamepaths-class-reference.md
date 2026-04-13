---
title: GamePaths Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_game_paths/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Contains, manages and creates all Paths.
[More...](#_details)

`#import <`[GamePaths.h](../../../line-drawing-game-starterkit-documentation/html/_game_paths_8h_source/)>


[List of all members.](/)

Public Member Functions
|
| (id) | - [init](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#a9cbf3d6208c432296ccca04a9035187a) |
| | initializes class and returns an instance of the class, you must take care of allocating the object yourself
|
| (void) | - [startPathForObject:touchLocation:](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#aa7881effb0349d6ca673f45f76ff0638) |
| | begins drawing a path and assigns that path to the [MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/) once at least one more path points has been drawn
|
| (void) | - [addPathPointsFromTouch:targets:](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#afba15729c1b50c7721edd71e80707866) |
| | tries to add a new path point, if the new path point is not far enough from the last point's position it will be ignored
|
| (void) | - [endPath](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#a1fc40c30fd0316f1a8d9b5eeadc1517c) |
| | ends drawing the path, releases the object we're drawing the path for, changes line style if necessary
|
| (void) | - [dealloc](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#af6e5ea60532f333a924b291abb3488ac)` [implementation]` |
| (void) | - [splitLineFrom:toPoint:pointArray:](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#aea5ee10f62ae79afb6f24814f3d9a533)` [implementation]` |
| | this splits the line into smaller segments so that target points are not easily missed if the player draws a line quickly
|
| (void) | - [addPathPointsForLineFrom:toPoint:targets:](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#ac87036cc8e7c48ccaad0a4e03c156be6)` [implementation]` |
Static Public Member Functions
|
| (id) | + [paths](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#a124b1716a20185c449846587bc094946) |
| | initializes class and returns an autoreleased instance of the class
|
Protected Attributes
|
[Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) * | [drawingPath](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#ab230ccb1cea26b1d480983cc75725d99) |
| | this is the [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) we're currently drawing
|
[MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/) * | [pathFollowObject](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#a880a4cca0abd4484303c2bc8220d3d2e) |
| | only valid for the time a path is drawn, needed to check object states
|
| CGPoint | [touchBeganLocation](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#a95389c1a7e4576d57b70b9bb264e3757) |
| | location where touch began, we need this as starting point for our path
|
| bool | [isDrawingPath](../../../line-drawing-game-starterkit-documentation/html/interface_game_paths/#a029c18d1e2dd036e0ac561c783fb6741) |
| | true if we're currently drawing a path
|


## Detailed Description

Contains, manages and creates all Paths.

Creates a new [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) and adds points to path as the player moves his finger. Ends or aborts path drawing as needed, eg. touch ended, path drawn is illegal (hit a collision) or path was drawn over endpoint (eg. landing strip or dock). Paths are drawn just above the [GameHUD](../../../line-drawing-game-starterkit-documentation/html/interface_game_h_u_d/) and below all [GameObjects](../../../line-drawing-game-starterkit-documentation/html/interface_game_objects/).


## Member Function Documentation

| - (void) addPathPointsForLineFrom: |
|
(CGPoint) |
*startPoint* |
| toPoint: |
|
(CGPoint) |
*endPoint* |
| targets: |
|
([TargetObjects](../../../line-drawing-game-starterkit-documentation/html/interface_target_objects/)*) |
*targets* | |
|
|
| | ` [implementation]` |


| - (void) addPathPointsFromTouch: |
|
(CGPoint) |
*touchLocation* |
| targets: |
|
([TargetObjects](../../../line-drawing-game-starterkit-documentation/html/interface_target_objects/)*) |
*targets* | |
|
|
| | |

tries to add a new path point, if the new path point is not far enough from the last point's position it will be ignored

| - (void) dealloc |
|
|
|
` [implementation]` |


ends drawing the path, releases the object we're drawing the path for, changes line style if necessary

initializes class and returns an instance of the class, you must take care of allocating the object yourself

initializes class and returns an autoreleased instance of the class

| - (void) splitLineFrom: |
|
(CGPoint) |
*startPoint* |
| toPoint: |
|
(CGPoint) |
*endPoint* |
| pointArray: |
|
(NSMutableArray*) |
*points* | |
|
|
| | ` [implementation]` |

this splits the line into smaller segments so that target points are not easily missed if the player draws a line quickly

| - (void) startPathForObject: |
|
([MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/)*) |
*object* |
| touchLocation: |
|
(CGPoint) |
*touchLocation* | |
|
|
| | |

begins drawing a path and assigns that path to the [MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/) once at least one more path points has been drawn


## Member Data Documentation

this is the [Path](../../../line-drawing-game-starterkit-documentation/html/interface_path/) we're currently drawing

true if we're currently drawing a path

only valid for the time a path is drawn, needed to check object states

location where touch began, we need this as starting point for our path


The documentation for this class was generated from the following files: