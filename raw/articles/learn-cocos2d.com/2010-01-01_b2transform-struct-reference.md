---
title: b2Transform Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_transform/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Math.h](http://www.learn-cocos2d.com/box2d-api-reference/API/b2_math_8h_source/)>

## Public Member Functions | |
|

A transform contains translation and rotation. It is used to represent the position and orientation of rigid frames.

| b2Transform::b2Transform | ( | ) | ` [inline]` |

The default constructor does nothing (for performance).

Initialize using a position vector and a rotation matrix.

Calculate the angle that the rotation matrix represents.

Set this based on the position and angle.

| void b2Transform::SetIdentity | ( | ) | ` [inline]` |

Set this to the identity transform.