---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/Box2D/html/structb2_transform/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <b2Math.h>`


|

A transform contains translation and rotation. It is used to represent the position and orientation of rigid frames.

| b2Transform::b2Transform | ( | ) | ` [inline]` |

The default constructor does nothing.

Initialize using a position vector and a rotation.

Set this based on the position and angle.

| void b2Transform::SetIdentity | ( | ) | ` [inline]` |

Set this to the identity transform.