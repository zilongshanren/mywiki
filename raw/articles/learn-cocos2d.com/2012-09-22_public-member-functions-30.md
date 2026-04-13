---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_ray_cast_callback/
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

`#include <b2WorldCallbacks.h>`


| virtual float32 |
|

| virtual float32
|

` [pure virtual]`

Called for each fixture found in the query. You control how the ray cast proceeds by returning a float: return -1: ignore this fixture and continue return 0: terminate the ray cast return fraction: clip the ray to this point return 1: don't clip the ray and continue

| fixture | the fixture hit by the ray |
| point | the point of initial intersection |
| normal | the normal vector at the point of intersection |