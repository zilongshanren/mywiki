---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_world_manifold/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This is used to compute the current state of a contact manifold.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_world_manifold/#details)

`#include <b2Collision.h>`


| void |
|

This is used to compute the current state of a contact manifold.

| void b2WorldManifold::Initialize | ( | const
|

Evaluate the manifold with supplied transforms. This assumes modest motion from the original state. This does not change the point count, impulses, etc. The radii must come from the shapes that generated the manifold.