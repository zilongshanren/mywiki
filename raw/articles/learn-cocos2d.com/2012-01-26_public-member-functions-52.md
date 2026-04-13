---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_vec3/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A 2D column vector with 3 elements.
[More...](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#details)

`#include <b2Math.h>`


[List of all members.](/)

Public Member Functions
|
| | [b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#a837423f66d6fb72d815e7390c09938b9) () |
| | Default constructor does nothing (for performance).
|
| | [b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#a47df55b26ab254dcf42a16638c7feeeb) (float32 x, float32 y, float32 z) |
| | Construct using coordinates.
|
| void | [SetZero](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#a5a459ed49f1910a347ca247f848a2dd8) () |
| | Set this vector to all zeros.
|
| void | [Set](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#a12a1bc14bbe722dfb175a492d2d00a79) (float32 x_, float32 y_, float32 z_) |
| | Set this vector to some specified coordinates.
|
[b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/) | [operator-](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#a246cb7ed59d3e758989939ed4e30e5ec) () const |
| | Negate this vector.
|
| void | [operator+=](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#a2aaeed3f5308aad85d19c5f0efc72641) (const [b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/) &v) |
| | Add a vector to this vector.
|
| void | [operator-=](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#a9e5b535548e1c5dfc0dc258d08f5ca32) (const [b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/) &v) |
| | Subtract a vector from this vector.
|
| void | [operator*=](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/#aaa9aa20195cd0ee53c7176a9a9b02389) (float32 s) |
| | Multiply this vector by a scalar.
|
Public Attributes
|
float32 | **x** |
float32 | **y** |
float32 | **z** |


## Detailed Description

A 2D column vector with 3 elements.


## Constructor & Destructor Documentation

| b2Vec3::b2Vec3 |
( |
| ) |
` [inline]` |

Default constructor does nothing (for performance).

| b2Vec3::b2Vec3 |
( |
float32 |
*x*, |
|
|
float32 |
*y*, |
|
|
float32 |
*z* |
|
) |
| ` [inline]` |

Construct using coordinates.


## Member Function Documentation

| void b2Vec3::operator*= |
( |
float32 |
*s* | ) |
` [inline]` |

Multiply this vector by a scalar.

| void b2Vec3::operator+= |
( |
const [b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/) & |
*v* | ) |
` [inline]` |

Add a vector to this vector.

[b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/) b2Vec3::operator- |
( |
| ) |
const` [inline]` |

| void b2Vec3::operator-= |
( |
const [b2Vec3](../../../../../api-ref/1.0/Box2D/html/structb2_vec3/) & |
*v* | ) |
` [inline]` |

Subtract a vector from this vector.

| void b2Vec3::Set |
( |
float32 |
*x_*, |
|
|
float32 |
*y_*, |
|
|
float32 |
*z_* |
|
) |
| ` [inline]` |

Set this vector to some specified coordinates.

| void b2Vec3::SetZero |
( |
| ) |
` [inline]` |

Set this vector to all zeros.


The documentation for this struct was generated from the following file: