---
title: Public Attributes
url: http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/structb2_filter/
published: '2013-02-23'
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

This holds contact filtering data.
[More...](http://www.learn-cocos2d.com/api-ref/2.1/Box2D/html/structb2_filter/#details)

`#include <b2Fixture.h>`


| uint16 |
|

This holds contact filtering data.

Collision groups allow a certain group of objects to never collide (negative) or always collide (positive). Zero means no collision group. Non-zero group filtering always wins against the mask bits.

The collision mask bits. This states the categories that this shape would accept for collision.