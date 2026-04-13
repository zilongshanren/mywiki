---
title: ClassesLineDrawingStarterkit/ObjectDef.h File Reference
url: http://www.learn-cocos2d.com/line-drawing-game-starterkit-documentation/html/_object_def_8h/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

# ClassesLineDrawingStarterkit/ObjectDef.h File Reference

`#import "`[AssetHelper.h](_asset_helper_8h_source.html)"

[Go to the source code of this file.](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h_source/)

## Classes |
| struct | [ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/) |
| | Contains all configurable gameplay parameters of any [MovingObject](../../../line-drawing-game-starterkit-documentation/html/interface_moving_object/). [More...](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/#_details)
|
## Enumerations |
| enum | [ObjectTypes](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#aeb594bb7008341c7b10ecf8e8ef84f94) {
[ObjectTypeDefaultPlane](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#aeb594bb7008341c7b10ecf8e8ef84f94a4a60e9451f6500c603de9cbd8d49bdde),
[ObjectTypes_MAX](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#aeb594bb7008341c7b10ecf8e8ef84f94a37fe6e7d7513fe3b375b25198d66b652)
} |
| | list of all ObjectTypes that are defined
[More...](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#aeb594bb7008341c7b10ecf8e8ef84f94)
|
| enum | [ImageOrientations](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894) {
[ImageOrientationRight](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894a5c59483c5ccc6a1354a8f35291d4929d) = 0,
[ImageOrientationUp](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894a00f9025c873066bb11a66f7d31a992e4) = -90,
[ImageOrientationLeft](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894a4ad73e7f3538476fc4b537b97408e25e) = -180,
[ImageOrientationDown](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894aa9a55818f9fc9fe2ccc41e35b95e538a) = -270
} |
## Functions |
static __inline__ [ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/) | [ObjectDefMake](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#ab872f260012c9dac703796f944f56a72) ([ObjectTypes](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#aeb594bb7008341c7b10ecf8e8ef84f94) type, NSString *imageFileName, NSString *proximityWarningFileName, [ImageOrientations](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894) imageOrientation, float speed, float rotationSpeed, float touchRadius, float collisionRadius) |
| | Convenience method to create and initialize an [ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/) struct.
|


## Enumeration Type Documentation

**Enumerator: **
ImageOrientationRight |
|
ImageOrientationUp |
|
ImageOrientationLeft |
|
ImageOrientationDown |
|


list of all ObjectTypes that are defined

**Enumerator: **
ObjectTypeDefaultPlane |
my dull test planes
|
ObjectTypes_MAX |
this many ObjectTypes are defined
|



## Function Documentation

static __inline__ [ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/) ObjectDefMake |
( |
[ObjectTypes](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#aeb594bb7008341c7b10ecf8e8ef84f94) |
*type*, |
|
|
NSString * |
*imageFileName*, |
|
|
NSString * |
*proximityWarningFileName*, |
|
|
[ImageOrientations](../../../line-drawing-game-starterkit-documentation/html/_object_def_8h/#a19aa37bc70f0e4af0074353c5c375894) |
*imageOrientation*, |
|
|
float |
*speed*, |
|
|
float |
*rotationSpeed*, |
|
|
float |
*touchRadius*, |
|
|
float |
*collisionRadius* | |
|
) |
| | ` [static]` |

Convenience method to create and initialize an [ObjectDef](../../../line-drawing-game-starterkit-documentation/html/struct_object_def/) struct.

Used to define properties of individual MovingObjects.