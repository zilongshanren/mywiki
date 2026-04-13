---
title: b2ContactImpulse Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_contact_impulse/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2WorldCallbacks.h](http://www.learn-cocos2d.com/box2d-api-reference/API/b2_world_callbacks_8h_source/)>

## Public Attributes | |
|

Contact impulses for reporting. Impulses are used instead of forces because sub-step forces may approach infinity for rigid body collisions. These match up one-to-one with the contact points in [b2Manifold](http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_manifold/).