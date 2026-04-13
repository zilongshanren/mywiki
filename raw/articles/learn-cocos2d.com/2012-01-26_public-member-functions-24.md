---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_polygon_shape/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2PolygonShape.h>`


|

A convex polygon. It is assumed that the interior of the polygon is to the left of each edge. Polygons have a maximum number of vertices equal to b2_maxPolygonVertices. In most cases you should not need many vertices for a convex polygon.

| int32 b2PolygonShape::GetChildCount | ( | ) | const` [virtual]` |

| int32 b2PolygonShape::GetVertexCount | ( | ) | const` [inline]` |

Get the vertex count.

Copy vertices. This assumes the vertices define a convex polygon. It is assumed that the exterior is the the right of each edge. The count must be in the range [3, b2_maxPolygonVertices].

| void b2PolygonShape::SetAsBox | ( | float32 | hx, |
| float32 | hy |
||
| ) |

Build vertices to represent an axis-aligned box.

| hx | the half-width. |
| hy | the half-height. |

Build vertices to represent an oriented box.

| hx | the half-width. |
| hy | the half-height. |
| center | the center of the box in local coordinates. |
| angle | the rotation of the box in local coordinates. |