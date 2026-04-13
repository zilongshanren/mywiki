---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/structb2_mat33/
published: '2011-10-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A 3-by-3 matrix. Stored in column-major order.
[More...](http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/structb2_mat33/#details)

`#include <b2Math.h>`


|

A 3-by-3 matrix. Stored in column-major order.

| b2Mat33::b2Mat33 | ( | ) | ` [inline]` |

The default constructor does nothing (for performance).

Construct this matrix using columns.

Get the inverse of this matrix as a 2-by-2. Returns the zero matrix if singular.

Get the symmetric inverse of this matrix as a 3-by-3. Returns the zero matrix if singular.

| void b2Mat33::SetZero | ( | ) | ` [inline]` |

Set this matrix to all zeros.

Solve A * x = b, where b is a column vector. This is more efficient than computing the inverse in one-shot cases. Solve only the upper 2-by-2 matrix equation.

Solve A * x = b, where b is a column vector. This is more efficient than computing the inverse in one-shot cases.