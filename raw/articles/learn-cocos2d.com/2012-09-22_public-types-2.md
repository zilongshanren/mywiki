---
title: Public Types
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_draw/
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

`#include <b2Draw.h>`


| enum | {
} |
| void |
|

Implement and register this class with a [b2World](http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/classb2_world/) to provide debug drawing of physics entities in your game.

| anonymous enum |

| virtual void
|

` [pure virtual]`

Draw a circle.

| virtual void
|

` [pure virtual]`

Draw a closed polygon provided in CCW order.

| virtual void
|

` [pure virtual]`

Draw a line segment.

| virtual void
|

` [pure virtual]`

Draw a solid circle.

| virtual void
|

` [pure virtual]`

Draw a solid closed polygon provided in CCW order.

Draw a transform. Choose your own length scale.

| xf | a transform. |