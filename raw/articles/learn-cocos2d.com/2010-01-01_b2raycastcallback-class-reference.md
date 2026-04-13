---
title: b2RayCastCallback Class Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_ray_cast_callback/
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

Callback class for ray casts. See [b2World::RayCast](http://www.learn-cocos2d.com/box2d-api-reference/API/classb2_world/#ad902548be84df9cc36eced0f4c89ab0a)

| virtual b2RayCastCallback::~b2RayCastCallback | ( | ) | ` [inline, virtual]` |

| virtual
|

` [pure virtual]`

Called for each fixture found in the query. You control how the ray cast proceeds by returning a float: return -1: ignore this fixture and continue return 0: terminate the ray cast return fraction: clip the ray to this point return 1: don't clip the ray and continue

fixture | the fixture hit by the ray | |
point | the point of initial intersection | |
normal | the normal vector at the point of intersection |