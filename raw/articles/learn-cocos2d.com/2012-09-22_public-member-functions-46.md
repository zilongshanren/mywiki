---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_mat33/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

|
Box2D
2.2
Box2D API Reference for www.kobold2d.com developers
|

A 3-by-3 matrix. Stored in column-major order.
[More...](http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_mat33/#details)

`#include <b2Math.h>`


|

A 3-by-3 matrix. Stored in column-major order.

Construct this matrix using columns.

Get the inverse of this matrix as a 2-by-2. Returns the zero matrix if singular.

Get the symmetric inverse of this matrix as a 3-by-3. Returns the zero matrix if singular.

Solve A * x = b, where b is a column vector. This is more efficient than computing the inverse in one-shot cases. Solve only the upper 2-by-2 matrix equation.

Solve A * x = b, where b is a column vector. This is more efficient than computing the inverse in one-shot cases.