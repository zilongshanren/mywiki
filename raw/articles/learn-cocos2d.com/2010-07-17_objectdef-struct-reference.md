---
title: ObjectDef Struct Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/struct_object_def/
published: '2010-07-17'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Contains all configurable gameplay parameters of any [MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/).
[More...](#_details)

`#include <`[ObjectDef.h](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h_source/)>


[List of all members.](/)

Public Attributes
|
[ObjectTypes](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#aeb594bb7008341c7b10ecf8e8ef84f94) | [type](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#aaed41574c8002d7c1ad1635611e760ed) |
| | the type of the object, one of the ObjectTypes enum values
|
| NSString * | [imageFileName](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#ab444985740ef0808bb8da92ea2ee4ee6) |
| | the image file for this object
|
| NSString * | [proximityWarningFileName](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#a1eb4198be2c0c64549177b61e7efb746) |
| | the image file for the proximity warning used by this object
|
[ImageOrientations](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894) | [imageOrientation](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#a87cacee641ac66f9af5b84875d33ee71) |
| | define how the image is oriented, Right means the sprite image is oriented to the right, Up to top, etc.
|
| float | [speed](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#a1046183b10719b772d7cc2f0a08f1051) |
| | how fast the object moves, good values are in range 5-40
|
| float | [rotationSpeed](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#a87ffdab94836cfc0a47923dc46db937b) |
| | how fast the object will rotate to face the direction it is moving to, it's in fractions of a second, a good value is 0.5f
|
| float | [touchRadius](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#a755fd4bb2f4c068a5334494e9395cc6f) |
| | how big the touch area of the object is where it recognizes a touch, typically twice the size of the collision radius
|
| float | [collisionRadius](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#a7279c60433f170dee5cbd9f7119b80ee) |
| | how big the collision radius is, if anything gets closer than collisionRadius pixels the object will collide (crash)
|


## Detailed Description

Contains all configurable gameplay parameters of any [MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/).


## Member Data Documentation

how big the collision radius is, if anything gets closer than collisionRadius pixels the object will collide (crash)

the image file for this object

define how the image is oriented, Right means the sprite image is oriented to the right, Up to top, etc.

If you notice that your images are rotated at 90 degrees or backwards compared to the movement direction then you need to adjust this property and set the correct orientation for your images. I assume most images are drawn pointing upwards so the most commonly used value will be ImageOrientationUp.

the image file for the proximity warning used by this object

how fast the object will rotate to face the direction it is moving to, it's in fractions of a second, a good value is 0.5f

how fast the object moves, good values are in range 5-40

how big the touch area of the object is where it recognizes a touch, typically twice the size of the collision radius

the type of the object, one of the ObjectTypes enum values


The documentation for this struct was generated from the following file: