---
title: Motivationals Class Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/interface_motivationals/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

manages motivational labels when landing, praising the player so he wants to see more of them .
[More...](#_details)

`#import <`[Motivationals.h](/)>


[List of all members.](/)

Public Member Functions
|
| (id) | - [init](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/#a786d3517474ff589dcd9659b63a06f9a) |
| | initializes [Motivationals](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/) class and returns an instance of the class, you must take care of allocating the object yourself
|
| (void) | - [dealloc](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/#a1653fa7b8e796b5e259f103ac350b566)` [implementation]` |
| (void) | - [createLabels](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/#a5c94943d76c9618bb942e2068fec17b2)` [implementation]` |
| (void) | - [onLabelHide:](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/#a4cb2c8ffc171c5123f91c4cafd962c7d)` [implementation]` |
Static Public Member Functions
|
| (id) | + [motivationals](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/#a93be17b4ee6d875d23a3196740bb5308) |
| | initializes [Motivationals](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/) class and returns an autoreleased instance of the class
|
| (void) | + [showLabelAt:](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/#a1ee5b40f3c6537c5aff4e6ffffc2b25a) |
| | show one of the motivational labels at this position
|
Protected Attributes
|
| int | [currentLabel](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/#a5b9ea510d1d123941876391b3a6515e8) |


## Detailed Description

manages motivational labels when landing, praising the player so he wants to see more of them .

. so many more ..


## Member Function Documentation

| - (void) createLabels |
|
|
|
` [implementation]` |


| - (void) dealloc |
|
|
|
` [implementation]` |


initializes [Motivationals](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/) class and returns an instance of the class, you must take care of allocating the object yourself

initializes [Motivationals](../../../line-drawing-game-starterkit-documentation/html/interface_motivationals/) class and returns an autoreleased instance of the class

| - (void) onLabelHide: |
|
(CCNode*) |
*sender* |
|
` [implementation]` |


| + (void) showLabelAt: |
|
(CGPoint) |
*pos* |
|
|

show one of the motivational labels at this position


## Member Data Documentation


The documentation for this class was generated from the following files: