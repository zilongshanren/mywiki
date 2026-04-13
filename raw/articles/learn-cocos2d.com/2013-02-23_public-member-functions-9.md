---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/structb2_vec2/
published: '2013-02-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A 2D column vector.
[More...](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#details)

`#include <b2Math.h>`


[List of all members.](/)

Public Member Functions
|
| | [b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a9171b31deb83af96872f99689939a12f) () |
| | Default constructor does nothing (for performance).
|
| | [b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#aa8a2f026420a84bbbc62f3a3de2041d6) (float32 x, float32 y) |
| | Construct using coordinates.
|
| void | [SetZero](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a5c6cbe27cfb29c6dbb29b9a3285b88d0) () |
| | Set this vector to all zeros.
|
| void | [Set](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a4d61640a645e470a50b451307d8e94c3) (float32 x_, float32 y_) |
| | Set this vector to some specified coordinates.
|
[b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/) | [operator-](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#ab1f648091d3cba00b4c132758fcf4450) () const |
| | Negate this vector.
|
| float32 | [operator()](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a9cb67b5f755b82d40673337a3652d81f) (int32 i) const |
| | Read from and indexed element.
|
| float32 & | [operator()](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a50b39580d9f479e17b23ce3cb8efbac6) (int32 i) |
| | Write to an indexed element.
|
| void | [operator+=](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a590789342e22ac1e7f9c1a63a2778b6d) (const [b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/) &v) |
| | Add a vector to this vector.
|
| void | [operator-=](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a6b48cab4695a979ae40b7613aedc8b17) (const [b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/) &v) |
| | Subtract a vector from this vector.
|
| void | [operator*=](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a7097696dce578322928f4535b34f1c6b) (float32 a) |
| | Multiply this vector by a scalar.
|
| float32 | [Length](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#afb1c498214b88874fcb07eb6322374da) () const |
| | Get the length of this vector (the norm).
|
| float32 | [LengthSquared](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#af66641b887488490e2168bfafc5a7e36) () const |
| float32 | [Normalize](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#adda78c92f318fe53d8a53f9b5cfd8e41) () |
| | Convert this vector into a unit vector. Returns the length.
|
| bool | [IsValid](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#aafb971cf7cc726f91fc3a8215fb0aa17) () const |
| | Does this vector contain finite coordinates?
|
[b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/) | [Skew](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#a8f2c6e60cb5898bc239801bd19e2d619) () const |
| | Get the skew vector such that dot(skew_vec, other) == cross(vec, other)
|
Public Attributes
|
float32 | **x** |
float32 | **y** |


## Detailed Description


## Constructor & Destructor Documentation

Default constructor does nothing (for performance).

Construct using coordinates.


## Member Function Documentation

Does this vector contain finite coordinates?

Get the length of this vector (the norm).

Get the length squared. For performance, use this instead of [b2Vec2::Length](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/#afb1c498214b88874fcb07eb6322374da) (if possible).

Convert this vector into a unit vector. Returns the length.

| float32 b2Vec2::operator() |
( |
int32 |
*i* | ) |
const` [inline]` |

Read from and indexed element.

| float32& b2Vec2::operator() |
( |
int32 |
*i* | ) |
` [inline]` |

Write to an indexed element.

| void b2Vec2::operator*= |
( |
float32 |
*a* | ) |
` [inline]` |

Multiply this vector by a scalar.

| void b2Vec2::operator+= |
( |
const [b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/) & |
*v* | ) |
` [inline]` |

Add a vector to this vector.

[b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/) b2Vec2::operator- |
( |
| ) |
const` [inline]` |

| void b2Vec2::operator-= |
( |
const [b2Vec2](../../../../../api-ref/2.1/Box2D/html/structb2_vec2/) & |
*v* | ) |
` [inline]` |

Subtract a vector from this vector.

Set this vector to some specified coordinates.

Set this vector to all zeros.

Get the skew vector such that dot(skew_vec, other) == cross(vec, other)


The documentation for this struct was generated from the following file: