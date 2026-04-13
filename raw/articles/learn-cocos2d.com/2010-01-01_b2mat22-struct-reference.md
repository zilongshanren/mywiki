---
title: b2Mat22 Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_mat22/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A 2-by-2 matrix. Stored in column-major order.
[More...](http://www.learn-cocos2d.com#_details)

`#include <`

[b2Math.h](http://www.learn-cocos2d.com/box2d-api-reference/API/b2_math_8h_source/)>

## Public Member Functions | |
|

A 2-by-2 matrix. Stored in column-major order.

| b2Mat22::b2Mat22 | ( | ) | ` [inline]` |

The default constructor does nothing (for performance).

Construct this matrix using columns.

Construct this matrix using scalars.

Construct this matrix using an angle. This matrix becomes an orthonormal rotation matrix.

Extract the angle from this matrix (assumed to be a rotation matrix).

Initialize this matrix using an angle. This matrix becomes an orthonormal rotation matrix.

Initialize this matrix using columns.

| void b2Mat22::SetIdentity | ( | ) | ` [inline]` |

Set this to the identity matrix.

| void b2Mat22::SetZero | ( | ) | ` [inline]` |

Set this matrix to all zeros.

Solve A * x = b, where b is a column vector. This is more efficient than computing the inverse in one-shot cases.