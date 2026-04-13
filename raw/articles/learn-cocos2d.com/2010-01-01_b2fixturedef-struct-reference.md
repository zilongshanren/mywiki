---
title: b2FixtureDef Struct Reference
url: http://www.learn-cocos2d.com/box2d-api-reference/API/structb2_fixture_def/
published: '2010-01-01'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <`

[b2Fixture.h](http://www.learn-cocos2d.com/)>

## Public Member Functions | |
|

A fixture definition is used to create a fixture. This class defines an abstract fixture definition. You can reuse fixture definitions safely.

| b2FixtureDef::b2FixtureDef | ( | ) | ` [inline]` |

The constructor sets the default fixture definition values.

| virtual b2FixtureDef::~b2FixtureDef | ( | ) | ` [inline, virtual]` |

A sensor shape collects contact information but never generates a collision response.

The shape, this must be set. The shape will be cloned, so you can create the shape on the stack.