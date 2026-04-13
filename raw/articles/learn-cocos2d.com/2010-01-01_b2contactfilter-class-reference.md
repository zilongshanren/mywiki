---
title: b2ContactFilter Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_contact_filter/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2WorldCallbacks.h](http://www.learn-cocos2d.com/box2d-api-reference/API/b2_world_callbacks_8h_source/)>

## Public Member Functions | |
| virtual |
|

Implement this class to provide collision filtering. In other words, you can implement this class if you want finer control over contact creation.

| virtual b2ContactFilter::~b2ContactFilter | ( | ) | ` [inline, virtual]` |

Return true if contact calculations should be performed between these two shapes.