---
title: b2WorldManifold Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_world_manifold/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This is used to compute the current state of a contact manifold.
[More...](http://www.learn-cocos2d.com#_details)

`#include <`

[b2Collision.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
| void |
|

This is used to compute the current state of a contact manifold.

| void b2WorldManifold::Initialize | ( | const
|

Evaluate the manifold with supplied transforms. This assumes modest motion from the original state. This does not change the point count, impulses, etc. The radii must come from the shapes that generated the manifold.