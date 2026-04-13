---
title: b2Filter Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_filter/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This holds contact filtering data.
[More...](http://www.learn-cocos2d.com#_details)

`#include <`

[b2Fixture.h](http://www.learn-cocos2d.com/)>

## Public Attributes | |
|

This holds contact filtering data.

Collision groups allow a certain group of objects to never collide (negative) or always collide (positive). Zero means no collision group. Non-zero group filtering always wins against the mask bits.

The collision mask bits. This states the categories that this shape would accept for collision.