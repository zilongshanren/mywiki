---
title: Public Types
url: http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/classb2_draw/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Draw.h>`


| enum | {
} |
| void |
|

Implement and register this class with a [b2World](http://www.learn-cocos2d.com/api-ref/latest/Box2D/html/classb2_world/) to provide debug drawing of physics entities in your game.

| anonymous enum |

| void b2Draw::AppendFlags | ( | uint32 | flags | ) |

Append flags to the current flags.

| void b2Draw::ClearFlags | ( | uint32 | flags | ) |

Clear flags from the current flags.

| virtual void b2Draw::DrawCircle | ( | const
|

` [pure virtual]`

Draw a circle.

| virtual void b2Draw::DrawPolygon | ( | const
|

` [pure virtual]`

Draw a closed polygon provided in CCW order.

| virtual void b2Draw::DrawSegment | ( | const
|

` [pure virtual]`

Draw a line segment.

| virtual void b2Draw::DrawSolidCircle | ( | const
|

` [pure virtual]`

Draw a solid circle.

| virtual void b2Draw::DrawSolidPolygon | ( | const
|

` [pure virtual]`

Draw a solid closed polygon provided in CCW order.

Draw a transform. Choose your own length scale.

| xf | a transform. |

| uint32 b2Draw::GetFlags | ( | ) | const |

Get the drawing flags.

| void b2Draw::SetFlags | ( | uint32 | flags | ) |

Set the drawing flags.