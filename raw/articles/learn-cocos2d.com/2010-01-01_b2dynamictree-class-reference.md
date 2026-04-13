---
title: b2DynamicTree Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_dynamic_tree/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2DynamicTree.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

A dynamic tree arranges data in a binary tree to accelerate queries such as volume queries and ray casts. Leafs are proxies with an AABB. In the tree we expand the proxy AABB by b2_fatAABBFactor so that the proxy AABB is bigger than the client object. This allows the client object to move by small amounts without triggering a tree update.

Nodes are pooled and relocatable, so we use node indices rather than pointers.

| b2DynamicTree::b2DynamicTree | ( | ) |

Constructing the tree initializes the node pool.

| b2DynamicTree::~b2DynamicTree | ( | ) |

Destroy the tree, freeing the node pool.

Create a proxy. Provide a tight fitting AABB and a userData pointer.

Destroy a proxy. This asserts if the id is invalid.

Get the fat AABB for a proxy.

Get proxy user data.

Move a proxy with a swepted AABB. If the proxy has moved outside of its fattened AABB, then the proxy is removed from the tree and re-inserted. Otherwise the function returns immediately.

| void b2DynamicTree::Query | ( | T * | callback, |
|
| const
|

` [inline]`

Query an AABB for overlapping proxies. The callback class is called for each proxy that overlaps the supplied AABB.

| void b2DynamicTree::RayCast | ( | T * | callback, |
|
| const
|

` [inline]`

Ray-cast against the proxies in the tree. This relies on the callback to perform a exact ray-cast in the case were the proxy contains a shape. The callback also performs the any collision filtering. This has performance roughly equal to k * log(n), where k is the number of collisions and n is the number of proxies in the tree.

input | the ray-cast input data. The ray extends from p1 to p1 + maxFraction * (p2 - p1). | |
callback | a callback class that is called for each proxy that is hit by the ray. |