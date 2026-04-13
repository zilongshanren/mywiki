---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/Box2D/html/structb2_fixture_def/
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

`#include <b2Fixture.h>`


|

A fixture definition is used to create a fixture. This class defines an abstract fixture definition. You can reuse fixture definitions safely.

A sensor shape collects contact information but never generates a collision response.

The shape, this must be set. The shape will be cloned, so you can create the shape on the stack.