---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_mat22/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A 2-by-2 matrix. Stored in column-major order.
[More...](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#details)

`#include <b2Math.h>`



[List of all members.](/)

Public Member Functions
|
| | [b2Mat22](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#ac3e10f6d457c8dab9062ba378f66bc4d) () |
| | The default constructor does nothing (for performance).
|
| | [b2Mat22](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#abd674c6d92e26962977f34bcd92ff24d) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &c1, const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &c2) |
| | Construct this matrix using columns.
|
| | [b2Mat22](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#a41d5d8743bda32cb8c6e212528934810) (float32 a11, float32 a12, float32 a21, float32 a22) |
| | Construct this matrix using scalars.
|
| void | [Set](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#aed3bee1de38a0b3f36e21c90faa24112) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &c1, const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &c2) |
| | Initialize this matrix using columns.
|
| void | [SetIdentity](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#a7192f063b771ac9ded060e41df890509) () |
| | Set this to the identity matrix.
|
| void | [SetZero](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#aaeae95f61cf3171ffb94703980e3594b) () |
| | Set this matrix to all zeros.
|
[b2Mat22](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/) | **GetInverse** () const |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | [Solve](../../../../../api-ref/1.0/Box2D/html/structb2_mat22/#ab511ad33f5abf87351581842628a9dc3) (const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) &b) const |
Public Attributes
|
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **ex** |
[b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) | **ey** |


## Detailed Description

A 2-by-2 matrix. Stored in column-major order.


## Constructor & Destructor Documentation

| b2Mat22::b2Mat22 |
( |
| ) |
` [inline]` |

The default constructor does nothing (for performance).

| b2Mat22::b2Mat22 |
( |
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*c1*, |
|
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*c2* |
|
) |
| ` [inline]` |

Construct this matrix using columns.

| b2Mat22::b2Mat22 |
( |
float32 |
*a11*, |
|
|
float32 |
*a12*, |
|
|
float32 |
*a21*, |
|
|
float32 |
*a22* |
|
) |
| ` [inline]` |

Construct this matrix using scalars.


## Member Function Documentation

| void b2Mat22::Set |
( |
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*c1*, |
|
|
const [b2Vec2](../../../../../api-ref/1.0/Box2D/html/structb2_vec2/) & |
*c2* |
|
) |
| ` [inline]` |

Initialize this matrix using columns.

| void b2Mat22::SetIdentity |
( |
| ) |
` [inline]` |

Set this to the identity matrix.

| void b2Mat22::SetZero |
( |
| ) |
` [inline]` |

Set this matrix to all zeros.

Solve A * x = b, where b is a column vector. This is more efficient than computing the inverse in one-shot cases.


The documentation for this struct was generated from the following file: