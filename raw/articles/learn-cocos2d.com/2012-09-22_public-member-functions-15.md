---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_dynamic_tree/
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

`#include <b2DynamicTree.h>`


|

A dynamic AABB tree broad-phase, inspired by Nathanael Presson's btDbvt. A dynamic tree arranges data in a binary tree to accelerate queries such as volume queries and ray casts. Leafs are proxies with an AABB. In the tree we expand the proxy AABB by b2_fatAABBFactor so that the proxy AABB is bigger than the client object. This allows the client object to move by small amounts without triggering a tree update.

Nodes are pooled and relocatable, so we use node indices rather than pointers.

Create a proxy. Provide a tight fitting AABB and a userData pointer.

Destroy a proxy. This asserts if the id is invalid.

Get the ratio of the sum of the node areas to the root area.

Get the fat AABB for a proxy.

Compute the height of the binary tree in O(N) time. Should not be called often.

Get the maximum balance of an node in the tree. The balance is the difference in height of the two children of a node.

Get proxy user data.

Move a proxy with a swepted AABB. If the proxy has moved outside of its fattened AABB, then the proxy is removed from the tree and re-inserted. Otherwise the function returns immediately.

| void
|

` [inline]`

Query an AABB for overlapping proxies. The callback class is called for each proxy that overlaps the supplied AABB.

| void
|

` [inline]`

Ray-cast against the proxies in the tree. This relies on the callback to perform a exact ray-cast in the case were the proxy contains a shape. The callback also performs the any collision filtering. This has performance roughly equal to k * log(n), where k is the number of collisions and n is the number of proxies in the tree.

| input | the ray-cast input data. The ray extends from p1 to p1 + maxFraction * (p2 - p1). |
| callback | a callback class that is called for each proxy that is hit by the ray. |