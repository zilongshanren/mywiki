---
title: Public Types
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_broad_phase/
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

`#include <b2BroadPhase.h>`


| enum | { e_nullProxy = -1
} |
| int32 |
|

The broad-phase is used for computing pairs and performing volume queries and ray casts. This broad-phase does not persist pairs. Instead, this reports potentially new pairs. It is up to the client to consume the new pairs and to track subsequent overlap.

Create a proxy with an initial AABB. Pairs are not reported until UpdatePairs is called.

Destroy a proxy. It is up to the client to remove any pairs.

Get the fat AABB for a proxy.

Get the quality metric of the embedded tree.

Get user data from a proxy. Returns NULL if the id is invalid.

Call MoveProxy as many times as you like, then when you are done call UpdatePairs to finalized the proxy pairs (for your time step).

Query an AABB for overlapping proxies. The callback class is called for each proxy that overlaps the supplied AABB.

| void
|

` [inline]`

Ray-cast against the proxies in the tree. This relies on the callback to perform a exact ray-cast in the case were the proxy contains a shape. The callback also performs the any collision filtering. This has performance roughly equal to k * log(n), where k is the number of collisions and n is the number of proxies in the tree.

| input | the ray-cast input data. The ray extends from p1 to p1 + maxFraction * (p2 - p1). |
| callback | a callback class that is called for each proxy that is hit by the ray. |

Test overlap of fat AABBs.

Call to trigger a re-processing of it's pairs on the next call to UpdatePairs.

Update the pairs. This results in pair callbacks. This can only add pairs.