---
title: b2BroadPhase Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_broad_phase/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2BroadPhase.h](http://www.learn-cocos2d.com/)>

## Public Types | |
| enum | {
|

The broad-phase is used for computing pairs and performing volume queries and ray casts. This broad-phase does not persist pairs. Instead, this reports potentially new pairs. It is up to the client to consume the new pairs and to track subsequent overlap.

| b2BroadPhase::b2BroadPhase | ( | ) |

| b2BroadPhase::~b2BroadPhase | ( | ) |

Create a proxy with an initial AABB. Pairs are not reported until UpdatePairs is called.

Destroy a proxy. It is up to the client to remove any pairs.

Get the fat AABB for a proxy.

Get user data from a proxy. Returns NULL if the id is invalid.

Call MoveProxy as many times as you like, then when you are done call UpdatePairs to finalized the proxy pairs (for your time step).

Query an AABB for overlapping proxies. The callback class is called for each proxy that overlaps the supplied AABB.

| void b2BroadPhase::RayCast | ( | T * | callback, |
|
| const
|

` [inline]`

Ray-cast against the proxies in the tree. This relies on the callback to perform a exact ray-cast in the case were the proxy contains a shape. The callback also performs the any collision filtering. This has performance roughly equal to k * log(n), where k is the number of collisions and n is the number of proxies in the tree.

input | the ray-cast input data. The ray extends from p1 to p1 + maxFraction * (p2 - p1). | |
callback | a callback class that is called for each proxy that is hit by the ray. |

Test overlap of fat AABBs.

| void b2BroadPhase::UpdatePairs | ( | T * | callback |
) | ` [inline]` |

Update the pairs. This results in pair callbacks. This can only add pairs.