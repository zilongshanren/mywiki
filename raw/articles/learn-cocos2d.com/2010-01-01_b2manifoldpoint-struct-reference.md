---
title: b2ManifoldPoint Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_manifold_point/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Collision.h](http://www.learn-cocos2d.com/)>

## Public Attributes | |
|

A manifold point is a contact point belonging to a contact manifold. It holds details related to the geometry and dynamics of the contact points. The local point usage depends on the manifold type: -e_circles: the local center of circleB -e_faceA: the local center of cirlceB or the clip point of polygonB -e_faceB: the clip point of polygonA This structure is stored across time steps, so we keep it small. Note: the impulses are used for internal caching and may not provide reliable contact forces, especially for high speed collisions.