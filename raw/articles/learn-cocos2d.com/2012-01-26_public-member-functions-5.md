---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/classb2_chain_shape/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2ChainShape.h>`


|

A chain shape is a free form sequence of line segments. The chain has two-sided collision, so you can use inside and outside collision. Therefore, you may use any winding order. Since there may be many vertices, they are allocated using b2Alloc. Connectivity information is used to create smooth collisions. WARNING: The chain will not collide properly if there are self-intersections.

| b2ChainShape::~b2ChainShape | ( | ) |

The destructor frees the vertices using b2Free.

Create a chain with isolated end vertices.

| vertices | an array of vertices, these are copied |
| count | the vertex count |

Create a loop. This automatically adjusts connectivity.

| vertices | an array of vertices, these are copied |
| count | the vertex count |

| int32 b2ChainShape::GetChildCount | ( | ) | const` [virtual]` |

Establish connectivity to a vertex that follows the last vertex. Don't call this for loops.

Establish connectivity to a vertex that precedes the first vertex. Don't call this for loops.