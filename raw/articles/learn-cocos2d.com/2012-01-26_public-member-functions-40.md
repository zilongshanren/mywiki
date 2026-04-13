---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_fixture_def/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Fixture.h>`


|

A fixture definition is used to create a fixture. This class defines an abstract fixture definition. You can reuse fixture definitions safely.

| b2FixtureDef::b2FixtureDef | ( | ) | ` [inline]` |

The constructor sets the default fixture definition values.

A sensor shape collects contact information but never generates a collision response.

The shape, this must be set. The shape will be cloned, so you can create the shape on the stack.